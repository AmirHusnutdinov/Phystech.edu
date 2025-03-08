// Константы и настройки
const DAILY_GOALS = {
    protein: 120, // г
    fat: 50, // г
    carb: 250, // г
    calories: 2000, // ккал
    water: 2000 // мл
};

const GLASS_SIZE = 250; // мл

// Данные для демонстрации
const DEMO_DISHES = [
    { id: 1, name: 'Куриная грудка', protein: 23, fat: 1.5, carb: 0, calories: 110, per100g: true },
    { id: 2, name: 'Гречневая каша', protein: 4.5, fat: 1.1, carb: 21.3, calories: 110, per100g: true },
    { id: 3, name: 'Овсянка', protein: 3.2, fat: 1.8, carb: 12.3, calories: 68, per100g: true },
    { id: 4, name: 'Яблоко', protein: 0.4, fat: 0.4, carb: 9.8, calories: 47, per100g: true },
    { id: 5, name: 'Творог 5%', protein: 18, fat: 5, carb: 3, calories: 121, per100g: true },
    { id: 6, name: 'Яйцо куриное', protein: 12.7, fat: 10.9, carb: 0.7, calories: 157, per100g: true },
    { id: 7, name: 'Лосось', protein: 20, fat: 13, carb: 0, calories: 208, per100g: true },
    { id: 8, name: 'Брокколи', protein: 2.8, fat: 0.4, carb: 5.2, calories: 34, per100g: true },
    { id: 9, name: 'Рис отварной', protein: 2.6, fat: 0.5, carb: 24.9, calories: 116, per100g: true },
    { id: 10, name: 'Банан', protein: 1.5, fat: 0.2, carb: 21.8, calories: 96, per100g: true },
];

// Глобальные переменные
let meals = [];
let waterAmount = 0;
let planType = 'custom'; // 'custom' или 'diet'
let selectedDishId = null;
let currentMealIndex = null;

// DOM элементы
document.addEventListener('DOMContentLoaded', function() {
    // Инициализация даты
    updateCurrentDate();

    // Инициализация стаканов воды
    initWaterGlasses();

    // Обработчики событий
    setupEventListeners();

    // Обновление прогресс-баров
    updateNutritionSummary();
});

// Функция для обновления текущей даты
function updateCurrentDate() {
    const dateElement = document.getElementById('current-date');
    const now = new Date();

    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    dateElement.textContent = now.toLocaleDateString('ru-RU', options);
}

// Инициализация стаканов воды
function initWaterGlasses() {
    const waterGlassesContainer = document.getElementById('water-glasses');
    waterGlassesContainer.innerHTML = '';

    const glassCount = Math.ceil(DAILY_GOALS.water / GLASS_SIZE);

    for (let i = 0; i < glassCount; i++) {
        const glass = document.createElement('div');
        glass.className = 'water-glass';
        glass.dataset.index = i;

        glass.addEventListener('click', function() {
            toggleWaterGlass(i);
        });

        waterGlassesContainer.appendChild(glass);
    }
}

// Переключение стакана воды
function toggleWaterGlass(index) {
    const glasses = document.querySelectorAll('.water-glass');
    const clickedGlass = glasses[index];

    if (clickedGlass.classList.contains('filled')) {
        // Если стакан уже заполнен, опустошаем его и все последующие
        for (let i = index; i < glasses.length; i++) {
            glasses[i].classList.remove('filled');
        }
        waterAmount = GLASS_SIZE * index;
    } else {
        // Если стакан пуст, заполняем его и все предыдущие
        for (let i = 0; i <= index; i++) {
            glasses[i].classList.add('filled');
        }
        waterAmount = GLASS_SIZE * (index + 1);
    }

    updateWaterValue();
}

// Добавление стакана воды
function addWaterGlass() {
    const glasses = document.querySelectorAll('.water-glass');
    const filledGlasses = document.querySelectorAll('.water-glass.filled');

    if (filledGlasses.length < glasses.length) {
        const nextIndex = filledGlasses.length;
        toggleWaterGlass(nextIndex);
    }
}

// Обновление значения воды
function updateWaterValue() {
    const waterValueElement = document.getElementById('water-value');
    waterValueElement.textContent = `${waterAmount}/${DAILY_GOALS.water} мл`;
}

// Настройка обработчиков событий
function setupEventListeners() {
    // Переключение типа плана
    const planTypeButtons = document.querySelectorAll('.plan-type-btn');
    planTypeButtons.forEach(button => {
        button.addEventListener('click', function() {
            planTypeButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            planType = this.dataset.type;

            const mealTypeGroup = document.getElementById('meal-type-group');
            if (planType === 'diet') {
                mealTypeGroup.style.display = 'block';
            } else {
                mealTypeGroup.style.display = 'none';
            }
        });
    });

    // Добавление стакана воды
    document.getElementById('add-water').addEventListener('click', addWaterGlass);

    // Открытие модального окна для добавления приема пищи
    document.getElementById('add-meal-btn').addEventListener('click', openMealModal);

    // Закрытие модальных окон
    document.querySelectorAll('.close-modal').forEach(closeBtn => {
        closeBtn.addEventListener('click', function() {
            document.getElementById('meal-modal').style.display = 'none';
            document.getElementById('dish-modal').style.display = 'none';
        });
    });

    // Отмена добавления приема пищи
    document.getElementById('cancel-meal-btn').addEventListener('click', function() {
        document.getElementById('meal-modal').style.display = 'none';
    });

    // Сохранение приема пищи
    document.getElementById('save-meal-btn').addEventListener('click', saveMeal);

    // Открытие модального окна для добавления блюда
    document.getElementById('add-dish-btn').addEventListener('click', openDishModal);

    // Закрытие модального окна для добавления блюда
    document.getElementById('close-dish-modal').addEventListener('click', function() {
        document.getElementById('dish-modal').style.display = 'none';
    });

    // Отмена добавления блюда
    document.getElementById('cancel-dish-btn').addEventListener('click', function() {
        document.getElementById('dish-form').style.display = 'none';
        document.getElementById('search-results').style.display = 'block';
    });

    // Поиск блюд
    document.getElementById('search-btn').addEventListener('click', searchDishes);

    // Обработка нажатия Enter в поле поиска
    document.getElementById('dish-search').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchDishes();
        }
    });

    // Изменение веса блюда
    document.getElementById('dish-weight').addEventListener('input', updateDishNutrition);

    // Добавление блюда в прием пищи
    document.getElementById('add-dish-to-meal-btn').addEventListener('click', addDishToMeal);
}

// Открытие модального окна для добавления приема пищи
function openMealModal(event, mealIndex = null) {
    currentMealIndex = mealIndex;

    const modal = document.getElementById('meal-modal');
    const mealTimeInput = document.getElementById('meal-time');
    const mealTypeSelect = document.getElementById('meal-type');
    const dishesContainer = document.getElementById('dishes-container');

    // Очистка контейнера блюд
    dishesContainer.innerHTML = '';

    // Установка текущего времени, если это новый прием пищи
    if (mealIndex === null) {
        const now = new Date();
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        mealTimeInput.value = `${hours}:${minutes}`;

        // Сброс значений питательных веществ
        document.getElementById('meal-protein').textContent = '0 г';
        document.getElementById('meal-fat').textContent = '0 г';
        document.getElementById('meal-carb').textContent = '0 г';
        document.getElementById('meal-calories').textContent = '0 ккал';
    } else {
        // Заполнение данными существующего приема пищи
        const meal = meals[mealIndex];
        mealTimeInput.value = meal.time;

        if (planType === 'diet' && meal.type) {
            mealTypeSelect.value = meal.type;
        }

        // Отображение блюд
        meal.dishes.forEach((dish, index) => {
            addDishToContainer(dish, index);
        });

        // Обновление значений питательных веществ
        updateMealNutrition();
    }

    modal.style.display = 'block';
}

// Сохранение приема пищи
function saveMeal() {
    const mealTimeInput = document.getElementById('meal-time');
    const mealTypeSelect = document.getElementById('meal-type');
    const dishesContainer = document.getElementById('dishes-container');

    // Проверка наличия блюд
    if (dishesContainer.children.length === 0) {
        alert('Добавьте хотя бы одно блюдо');
        return;
    }

    // Создание объекта приема пищи
    const meal = {
        time: mealTimeInput.value,
        dishes: [],
        protein: 0,
        fat: 0,
        carb: 0,
        calories: 0
    };

    // Если это диета, добавляем тип приема пищи
    if (planType === 'diet') {
        meal.type = mealTypeSelect.value;
    }

    // Сбор данных о блюдах
    const dishItems = dishesContainer.querySelectorAll('.dish-item');
    dishItems.forEach(item => {
        const dishId = parseInt(item.dataset.id);
        const weight = parseInt(item.dataset.weight);
        const dish = DEMO_DISHES.find(d => d.id === dishId);

        if (dish) {
            const dishData = {
                id: dish.id,
                name: dish.name,
                weight: weight,
                protein: (dish.protein * weight / 100).toFixed(1),
                fat: (dish.fat * weight / 100).toFixed(1),
                carb: (dish.carb * weight / 100).toFixed(1),
                calories: Math.round(dish.calories * weight / 100),
                consumed: false
            };

            meal.dishes.push(dishData);
            meal.protein += parseFloat(dishData.protein);
            meal.fat += parseFloat(dishData.fat);
            meal.carb += parseFloat(dishData.carb);
            meal.calories += dishData.calories;
        }
    });

    // Округление значений
    meal.protein = meal.protein.toFixed(1);
    meal.fat = meal.fat.toFixed(1);
    meal.carb = meal.carb.toFixed(1);

    // Добавление или обновление приема пищи
    if (currentMealIndex !== null) {
        meals[currentMealIndex] = meal;
    } else {
        meals.push(meal);
    }

    // Закрытие модального окна
    document.getElementById('meal-modal').style.display = 'none';

    // Обновление отображения приемов пищи
    renderMeals();

    // Обновление сводки по питательным веществам
    updateNutritionSummary();
}

// Открытие модального окна для добавления блюда
function openDishModal() {
    document.getElementById('dish-modal').style.display = 'block';
    document.getElementById('dish-search').value = '';
    document.getElementById('dish-form').style.display = 'none';
    document.getElementById('search-results').style.display = 'block';
    document.getElementById('search-results').innerHTML = '';

    // Фокус на поле поиска
    setTimeout(() => {
        document.getElementById('dish-search').focus();
    }, 100);
}

// Поиск блюд
function searchDishes() {
    const searchInput = document.getElementById('dish-search');
    const searchResults = document.getElementById('search-results');
    const query = searchInput.value.trim().toLowerCase();

    // Очистка результатов поиска
    searchResults.innerHTML = '';

    if (query.length < 2) {
        searchResults.innerHTML = '<p>Введите минимум 2 символа для поиска</p>';
        return;
    }

    // Фильтрация блюд
    const filteredDishes = DEMO_DISHES.filter(dish =>
        dish.name.toLowerCase().includes(query)
    );

    if (filteredDishes.length === 0) {
        searchResults.innerHTML = '<p>Ничего не найдено</p>';
        return;
    }

    // Отображение результатов
    filteredDishes.forEach(dish => {
        const dishElement = document.createElement('div');
        dishElement.className = 'search-result-item';
        dishElement.innerHTML = `
            <div class="dish-name">${dish.name}</div>
            <div class="dish-nutrition">
                <span>Б: ${dish.protein}г</span>
                <span>Ж: ${dish.fat}г</span>
                <span>У: ${dish.carb}г</span>
                <span>${dish.calories} ккал</span>
            </div>
        `;

        dishElement.addEventListener('click', function() {
            selectDish(dish.id);
        });

        searchResults.appendChild(dishElement);
    });
}

// Выбор блюда
function selectDish(dishId) {
    selectedDishId = dishId;
    const dish = DEMO_DISHES.find(d => d.id === dishId);

    if (dish) {
        document.getElementById('search-results').style.display = 'none';
        document.getElementById('dish-form').style.display = 'block';
        document.getElementById('selected-dish-name').textContent = dish.name;
        document.getElementById('dish-weight').value = 100;

        updateDishNutrition();
    }
}

// Обновление питательных веществ блюда при изменении веса
function updateDishNutrition() {
    const weightInput = document.getElementById('dish-weight');
    const weight = parseInt(weightInput.value) || 0;

    if (weight <= 0) {
        weightInput.value = 1;
        return updateDishNutrition();
    }

    const dish = DEMO_DISHES.find(d => d.id === selectedDishId);

    if (dish) {
        document.getElementById('dish-protein').textContent = `${(dish.protein * weight / 100).toFixed(1)} г`;
        document.getElementById('dish-fat').textContent = `${(dish.fat * weight / 100).toFixed(1)} г`;
        document.getElementById('dish-carb').textContent = `${(dish.carb * weight / 100).toFixed(1)} г`;
        document.getElementById('dish-calories').textContent = `${Math.round(dish.calories * weight / 100)} ккал`;
    }
}

// Добавление блюда в прием пищи
function addDishToMeal() {
    const weight = parseInt(document.getElementById('dish-weight').value) || 0;

    if (weight <= 0) {
        alert('Вес должен быть больше 0');
        return;
    }

    const dish = DEMO_DISHES.find(d => d.id === selectedDishId);

    if (dish) {
        const dishData = {
            id: dish.id,
            name: dish.name,
            weight: weight,
            protein: (dish.protein * weight / 100).toFixed(1),
            fat: (dish.fat * weight / 100).toFixed(1),
            carb: (dish.carb * weight / 100).toFixed(1),
            calories: Math.round(dish.calories * weight / 100),
            consumed: false
        };

        // Добавление блюда в контейнер
        const dishesContainer = document.getElementById('dishes-container');
        const dishIndex = dishesContainer.children.length;
        addDishToContainer(dishData, dishIndex);

        // Обновление питательных веществ приема пищи
        updateMealNutrition();

        // Закрытие модального окна блюда
        document.getElementById('dish-modal').style.display = 'none';
    }
}

// Добавление блюда в контейнер
function addDishToContainer(dishData, index) {
    const dishesContainer = document.getElementById('dishes-container');

    const dishElement = document.createElement('div');
    dishElement.className = 'dish-item';
    dishElement.dataset.id = dishData.id;
    dishElement.dataset.weight = dishData.weight;
    dishElement.dataset.index = index;

    dishElement.innerHTML = `
        <div class="dish-info">
            <div class="dish-name">${dishData.name}</div>
            <div class="dish-weight">${dishData.weight} г</div>
        </div>
        <div class="dish-nutrition">
            <span>Б: ${dishData.protein}г</span>
            <span>Ж: ${dishData.fat}г</span>
            <span>У: ${dishData.carb}г</span>
            <span>${dishData.calories} ккал</span>
        </div>
        <div class="dish-actions">
            <button class="remove-dish-btn" data-index="${index}">✕</button>
        </div>
    `;

    // Обработчик удаления блюда
    dishElement.querySelector('.remove-dish-btn').addEventListener('click', function(e) {
        e.stopPropagation();
        removeDishFromContainer(index);
    });

    dishesContainer.appendChild(dishElement);
}

// Удаление блюда из контейнера
function removeDishFromContainer(index) {
    const dishesContainer = document.getElementById('dishes-container');
    const dishElements = dishesContainer.querySelectorAll('.dish-item');

    if (index < dishElements.length) {
        dishElements[index].remove();

        // Обновление индексов
        dishesContainer.querySelectorAll('.dish-item').forEach((item, i) => {
            item.dataset.index = i;
            item.querySelector('.remove-dish-btn').dataset.index = i;
        });

        // Обновление питательных веществ приема пищи
        updateMealNutrition();
    }
}

// Обновление питательных веществ приема пищи
function updateMealNutrition() {
    const dishesContainer = document.getElementById('dishes-container');
    const dishElements = dishesContainer.querySelectorAll('.dish-item');

    let protein = 0;
    let fat = 0;
    let carb = 0;
    let calories = 0;

    dishElements.forEach(item => {
        const dishId = parseInt(item.dataset.id);
        const weight = parseInt(item.dataset.weight);
        const dish = DEMO_DISHES.find(d => d.id === dishId);

        if (dish) {
            protein += dish.protein * weight / 100;
            fat += dish.fat * weight / 100;
            carb += dish.carb * weight / 100;
            calories += Math.round(dish.calories * weight / 100);
        }
    });

    document.getElementById('meal-protein').textContent = `${protein.toFixed(1)} г`;
    document.getElementById('meal-fat').textContent = `${fat.toFixed(1)} г`;
    document.getElementById('meal-carb').textContent = `${carb.toFixed(1)} г`;
    document.getElementById('meal-calories').textContent = `${calories} ккал`;
}

// Отображение приемов пищи
function renderMeals() {
    const mealsContainer = document.getElementById('meals-container');
    mealsContainer.innerHTML = '';

    // Сортировка приемов пищи по времени
    const sortedMeals = [...meals].sort((a, b) => {
        return a.time.localeCompare(b.time);
    });

    sortedMeals.forEach((meal, index) => {
        const mealElement = document.createElement('div');
        mealElement.className = 'meal-card';

        let headerContent = '';
        if (planType === 'diet' && meal.type) {
            headerContent = `<div class="meal-type">${getMealTypeName(meal.type)}</div>`;
        } else {
            headerContent = `<div class="meal-time">${meal.time}</div>`;
        }

        mealElement.innerHTML = `
            <div class="meal-header">
                ${headerContent}
                <div class="meal-actions">
                    <button class="edit-meal-btn" data-index="${index}">✎</button>
                    <button class="delete-meal-btn" data-index="${index}">✕</button>
                </div>
            </div>
            <div class="meal-nutrition">
                <div class="meal-nutrition-item">
                    <span>Белки</span>
                    <span>${meal.protein} г</span>
                </div>
                <div class="meal-nutrition-item">
                    <span>Жиры</span>
                    <span>${meal.fat} г</span>
                </div>
                <div class="meal-nutrition-item">
                    <span>Углеводы</span>
                    <span>${meal.carb} г</span>
                </div>
                <div class="meal-nutrition-item">
                    <span>Калории</span>
                    <span>${meal.calories} ккал</span>
                </div>
            </div>
            <div class="dishes-list">
                ${meal.dishes.map((dish, dishIndex) => `
                    <div class="dish-item ${dish.consumed ? 'consumed' : ''}" data-meal-index="${index}" data-dish-index="${dishIndex}">
                        <div class="dish-info">
                            <input type="checkbox" class="dish-checkbox" ${dish.consumed ? 'checked' : ''}>
                            <div>
                                <div class="dish-name">${dish.name}</div>
                                <div class="dish-weight">${dish.weight} г</div>
                            </div>
                        </div>
                        <div class="dish-nutrition">
                            <span>Б: ${dish.protein}г</span>
                            <span>Ж: ${dish.fat}г</span>
                            <span>У: ${dish.carb}г</span>
                            <span>${dish.calories} ккал</span>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;

        // Обработчики событий
        mealElement.querySelector('.edit-meal-btn').addEventListener('click', function() {
            openMealModal(null, index);
        });

        mealElement.querySelector('.delete-meal-btn').addEventListener('click', function() {
            if (confirm('Вы уверены, что хотите удалить этот прием пищи?')) {
                meals.splice(index, 1);
                renderMeals();
                updateNutritionSummary();
            }
        });

        // Обработчики для чекбоксов блюд
        const checkboxes = mealElement.querySelectorAll('.dish-checkbox');
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                const dishItem = this.closest('.dish-item');
                const mealIndex = parseInt(dishItem.dataset.mealIndex);
                const dishIndex = parseInt(dishItem.dataset.dishIndex);

                meals[mealIndex].dishes[dishIndex].consumed = this.checked;
                dishItem.classList.toggle('consumed', this.checked);

                updateNutritionSummary();
            });
        });

        mealsContainer.appendChild(mealElement);
    });
}

// Получение названия типа приема пищи
function getMealTypeName(type) {
    const types = {
        'breakfast': 'Завтрак',
        'lunch': 'Обед',
        'dinner': 'Ужин',
        'snack': 'Перекус'
    };

    return types[type] || type;
}

// Обновление сводки по питательным веществам
function updateNutritionSummary() {
    let consumedProtein = 0;
    let consumedFat = 0;
    let consumedCarb = 0;
    let consumedCalories = 0;

    meals.forEach(meal => {
        meal.dishes.forEach(dish => {
            if (dish.consumed) {
                consumedProtein += parseFloat(dish.protein);
                consumedFat += parseFloat(dish.fat);
                consumedCarb += parseFloat(dish.carb);
                consumedCalories += dish.calories;
            }
        });
    });

    // Округление значений
    consumedProtein = consumedProtein.toFixed(1);
    consumedFat = consumedFat.toFixed(1);
    consumedCarb = consumedCarb.toFixed(1);

    // Обновление значений
    document.getElementById('protein-value').textContent = `${consumedProtein}/${DAILY_GOALS.protein} г`;
    document.getElementById('fat-value').textContent = `${consumedFat}/${DAILY_GOALS.fat} г`;
    document.getElementById('carb-value').textContent = `${consumedCarb}/${DAILY_GOALS.carb} г`;
    document.getElementById('calorie-value').textContent = `${consumedCalories}/${DAILY_GOALS.calories} ккал`;

    // Обновление прогресс-баров
    document.getElementById('protein-fill').style.width = `${Math.min(100, (consumedProtein / DAILY_GOALS.protein) * 100)}%`;
    document.getElementById('fat-fill').style.width = `${Math.min(100, (consumedFat / DAILY_GOALS.fat) * 100)}%`;
    document.getElementById('carb-fill').style.width = `${Math.min(100, (consumedCarb / DAILY_GOALS.carb) * 100)}%`;
    document.getElementById('calorie-fill').style.width = `${Math.min(100, (consumedCalories / DAILY_GOALS.calories) * 100)}%`;
}

// Закрытие модальных окон при клике вне их содержимого
window.addEventListener('click', function(event) {
    const mealModal = document.getElementById('meal-modal');
    const dishModal = document.getElementById('dish-modal');

    if (event.target === mealModal) {
        mealModal.style.display = 'none';
    }

    if (event.target === dishModal) {
        dishModal.style.display = 'none';
    }
});

// Инициализация демо-данных (для тестирования)
function initDemoData() {
    // Добавление демо-приема пищи
    meals = [
        {
            time: '08:00',
            type: 'breakfast',
            dishes: [
                {
                    id: 3,
                    name: 'Овсянка',
                    weight: 200,
                    protein: '6.4',
                    fat: '3.6',
                    carb: '24.6',
                    calories: 136,
                    consumed: true
                },
                {
                    id: 10,
                    name: 'Банан',
                    weight: 150,
                    protein: '2.3',
                    fat: '0.3',
                    carb: '32.7',
                    calories: 144,
                    consumed: true
                }
            ],
            protein: '8.7',
            fat: '3.9',
            carb: '57.3',
            calories: 280
        }
    ];

    // Добавление воды
    waterAmount = 500;
    const glasses = document.querySelectorAll('.water-glass');
    for (let i = 0; i < waterAmount / GLASS_SIZE; i++) {
        glasses[i].classList.add('filled');
    }
    updateWaterValue();

    // Отображение приемов пищи
    renderMeals();

    // Обновление сводки по питательным веществам
    updateNutritionSummary();
}

// Раскомментируйте для демонстрации
// setTimeout(initDemoData, 500);

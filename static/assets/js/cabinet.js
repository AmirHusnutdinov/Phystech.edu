document.addEventListener("DOMContentLoaded", () => {
  // Profile form functionality
  const form = document.getElementById("profileForm")
  const editButton = document.getElementById("editButton")
  const saveButton = document.getElementById("saveButton")
  const cancelButton = document.getElementById("cancelButton")
  const fieldValues = form.querySelectorAll(".field-value")

  // Dropdowns for select fields
  const genderSelect = document.getElementById("gender-select")
  const activitySelect = document.getElementById("activity-select")

  // Store original values for cancel functionality
  const originalValues = {}

  // Edit profile button
  editButton.addEventListener("click", () => {
    // Make fields editable (except email and login)
    fieldValues.forEach((field) => {
      // Store original value
      originalValues[field.dataset.field] = field.textContent.trim()

      const fieldType = field.dataset.type
      const fieldName = field.dataset.field

      // Skip email and login fields - they should not be editable
      if (fieldName === "email" || fieldName === "login") {
        return
      }

      if (fieldType === "select") {
        // For select fields, show the dropdown
        if (field.dataset.field === "gender") {
          genderSelect.value = field.dataset.original
          genderSelect.style.display = "block"
          field.style.display = "none"
        } else if (field.dataset.field === "activity") {
          activitySelect.value = field.dataset.original
          activitySelect.style.display = "block"
          field.style.display = "none"
        }
      } else {
        // For text and number fields, make them editable
        field.contentEditable = true
        field.classList.add("editable")
      }
    })

    // Show save and cancel buttons, hide edit button
    editButton.style.display = "none"
    saveButton.style.display = "inline-block"
    cancelButton.style.display = "inline-block"

    // Show avatar change button
    changeAvatarBtn.style.display = "block"
  })

  // Save profile button
  saveButton.addEventListener("click", (e) => {
    e.preventDefault()

    // Update data attributes with new values
    fieldValues.forEach((field) => {
      const fieldType = field.dataset.type
      const fieldName = field.dataset.field

      // Skip email and login fields
      if (fieldName === "email" || fieldName === "login") {
        return
      }

      if (fieldType === "select") {
        if (field.dataset.field === "gender") {
          const selectedValue = genderSelect.value
          field.dataset.original = selectedValue
          field.textContent = selectedValue === "male" ? "Мужской" : "Женский"
          genderSelect.style.display = "none"
          field.style.display = "block"
        } else if (field.dataset.field === "activity") {
          const selectedValue = activitySelect.value
          field.dataset.original = selectedValue

          const activityLabels = {
            sedentary: "Сидячий образ жизни",
            light: "Легкая активность",
            moderate: "Умеренная активность",
            active: "Активный образ жизни",
            very_active: "Очень активный образ жизни",
          }

          field.textContent = activityLabels[selectedValue]
          activitySelect.style.display = "none"
          field.style.display = "block"
        }
      } else {
        // For text and number fields
        field.contentEditable = false
        field.classList.remove("editable")

        // Validate number fields
        if (fieldType === "number") {
          const value = field.textContent.trim()
          if (isNaN(value) || value === "") {
            field.textContent = field.dataset.original
          } else {
            field.dataset.original = value
          }
        } else {
          field.dataset.original = field.textContent.trim()
        }
      }
    })

    // Hide save and cancel buttons, show edit button
    editButton.style.display = "inline-block"
    saveButton.style.display = "none"
    cancelButton.style.display = "none"

    // Show success notification
    showNotification("Профиль успешно обновлен!", "success")

    // Hide avatar change button
    changeAvatarBtn.style.display = "none"
  })

  // Cancel button
  cancelButton.addEventListener("click", () => {
    // Restore original values
    fieldValues.forEach((field) => {
      const fieldType = field.dataset.type
      const fieldName = field.dataset.field

      // Skip email and login fields
      if (fieldName === "email" || fieldName === "login") {
        return
      }

      if (fieldType === "select") {
        if (field.dataset.field === "gender") {
          genderSelect.style.display = "none"
          field.style.display = "block"
        } else if (field.dataset.field === "activity") {
          activitySelect.style.display = "none"
          field.style.display = "block"
        }
      } else {
        // For text and number fields
        field.contentEditable = false
        field.classList.remove("editable")
        field.textContent = originalValues[field.dataset.field]
      }
    })

    // Hide save and cancel buttons, show edit button
    editButton.style.display = "inline-block"
    saveButton.style.display = "none"
    cancelButton.style.display = "none"

    // Hide avatar change button
    changeAvatarBtn.style.display = "none"
  })

  // KBGU edit button
  const editKBGUButton = document.getElementById("editKBGU")
  const saveKBGUButton = document.getElementById("saveKBGU")
  const cancelKBGUButton = document.getElementById("cancelKBGU")
  const kbguValues = document.querySelectorAll(".nutrition-value")

  // Store original KBGU values
  const originalKBGU = {}

  // Goal buttons event listeners
  const weightLossBtn = document.getElementById("weightLoss")
  const weightMaintenanceBtn = document.getElementById("weightMaintenance")
  const weightGainBtn = document.getElementById("weightGain")
  
    // Store the selected goal for later use
  let selectedGoal = null

  editKBGUButton.addEventListener("click", () => {
    // Make KBGU fields editable
    kbguValues.forEach((field) => {
      // Store original value
      originalKBGU[field.dataset.field] = field.textContent.trim()

      field.contentEditable = true
      field.classList.add("editable")
    })

    // Show save and cancel buttons, hide edit button
    editKBGUButton.style.display = "none"
    saveKBGUButton.style.display = "inline-block"
    cancelKBGUButton.style.display = "inline-block"
  })

  // Save KBGU button
  saveKBGUButton.addEventListener("click", () => {
    // Update data attributes with new values
    kbguValues.forEach((field) => {
      field.contentEditable = false
      field.classList.remove("editable")

      // Validate number fields
      const value = field.textContent.trim()
      if (isNaN(value) || value === "") {
        field.textContent = field.dataset.original
      } else {
        field.dataset.original = value
      }
    })

    // Hide save and cancel buttons, show edit button
    editKBGUButton.style.display = "inline-block"
    saveKBGUButton.style.display = "none"
    cancelKBGUButton.style.display = "none"

    // Show success notification
    if (selectedGoal) {
      const goalNames = {
        loss: "Похудение",
        maintenance: "Поддержание веса",
        gain: "Набор массы",
      }
      showNotification(`Цели питания обновлены! Выбранный план: ${goalNames[selectedGoal]}`, "success")
      // Reset selected goal
      selectedGoal = null
    } else {
      showNotification("Цели питания обновлены!", "success")
    }
  })

  // Cancel KBGU button
  cancelKBGUButton.addEventListener("click", () => {
    // Restore original values
    kbguValues.forEach((field) => {
      field.contentEditable = false
      field.classList.remove("editable")
      field.textContent = originalKBGU[field.dataset.field]
    })

    // Hide save and cancel buttons, show edit button
    editKBGUButton.style.display = "inline-block"
    saveKBGUButton.style.display = "none"
    // cancelKBGUButton.style.display = "none"[
    //   // Reset goal button highlighting
    //   (weightLossBtn, weightMaintenanceBtn, weightGainBtn)
    // ].forEach((btn) => {
    //   btn.classList.remove("active")
    // })
    weightGainBtn.classList.remove("active")
    weightMaintenanceBtn.classList.remove("active")
    weightLossBtn.classList.remove("active")
    // Reset selected goal
    selectedGoal = null

    // Show notification
    showNotification("Изменения отменены", "info")
  })


  // Modified goal button event listeners
  weightLossBtn.addEventListener("click", () => {
    // Enter edit mode first
    if (editKBGUButton.style.display !== "none") {
      // Only trigger edit mode if not already in edit mode
      editKBGUButton.click()
    }
    // Store the selected goal
    selectedGoal = "loss"
    // Apply the calculations
    applyGoalCalculations("loss")
    // Highlight the active goal button
    highlightGoalButton("loss")
  })

  weightMaintenanceBtn.addEventListener("click", () => {
    // Enter edit mode first
    if (editKBGUButton.style.display !== "none") {
      // Only trigger edit mode if not already in edit mode
      editKBGUButton.click()
    }
    // Store the selected goal
    selectedGoal = "maintenance"
    // Apply the calculations
    applyGoalCalculations("maintenance")
    // Highlight the active goal button
    highlightGoalButton("maintenance")
  })

  weightGainBtn.addEventListener("click", () => {
    // Enter edit mode first
    if (editKBGUButton.style.display !== "none") {
      // Only trigger edit mode if not already in edit mode
      editKBGUButton.click()
    }
    // Store the selected goal
    selectedGoal = "gain"
    // Apply the calculations
    applyGoalCalculations("gain")
    // Highlight the active goal button
    highlightGoalButton("gain")
  })

  // Function to highlight the active goal button
  function highlightGoalButton(goal) {
    ;[weightLossBtn, weightMaintenanceBtn, weightGainBtn].forEach((btn) => {
      btn.classList.remove("active")
    })

    if (goal === "loss") {
      weightLossBtn.classList.add("active")
    } else if (goal === "maintenance") {
      weightMaintenanceBtn.classList.add("active")
    } else if (goal === "gain") {
      weightGainBtn.classList.add("active")
    }
  }

  // Function to apply goal calculations without saving
  function applyGoalCalculations(goal) {
    const weightField = document.querySelector('.field-value[data-field="weight"]')
    const heightField = document.querySelector('.field-value[data-field="height"]')
    const ageField = document.querySelector('.field-value[data-field="age"]')
    const genderField = document.querySelector('.field-value[data-field="gender"]')
    const activityField = document.querySelector('.field-value[data-field="activity"]')

    const weight = Number.parseFloat(weightField.dataset.original)
    const height = Number.parseFloat(heightField.dataset.original)
    const age = Number.parseFloat(ageField.dataset.original)
    const gender = genderField.dataset.original
    const activityValue = activityField.dataset.original

    let bmr
    if (gender === "male") {
      bmr = 88.36 + 13.4 * weight + 4.8 * height - 5.7 * age
    } else {
      bmr = 447.6 + 9.2 * weight + 3.1 * height - 4.3 * age
    }

    const activityMultipliers = {
      sedentary: 1.2,
      light: 1.375,
      moderate: 1.55,
      active: 1.725,
      very_active: 1.9,
    }

    let calories = bmr * activityMultipliers[activityValue]

    if (goal === "loss") {
      calories *= 0.85
    } else if (goal === "gain") {
      calories *= 1.15
    }

    const protein = weight * 2
    const fats = (calories * 0.25) / 9
    const carbs = (calories - protein * 4 - fats * 9) / 4

    // Update nutrition values (only in the UI, not saving to data-original yet)
    const caloriesField = document.querySelector('.nutrition-value[data-field="calories"]')
    const proteinField = document.querySelector('.nutrition-value[data-field="protein"]')
    const fatsField = document.querySelector('.nutrition-value[data-field="fats"]')
    const carbsField = document.querySelector('.nutrition-value[data-field="carbs"]')

    caloriesField.textContent = Math.round(calories)
    proteinField.textContent = Math.round(protein)
    fatsField.textContent = Math.round(fats)
    carbsField.textContent = Math.round(carbs)

    // Show notification about the selected goal
    const goalMessages = {
      loss: "Выбрана цель: Похудение",
      maintenance: "Выбрана цель: Поддержание веса",
      gain: "Выбрана цель: Набор массы",
    }

    showNotification(goalMessages[goal], "info")
  }

  // Notification system
  function showNotification(message, type = "info") {
    const notification = document.createElement("div")
    notification.className = `notification ${type}`
    notification.textContent = message

    document.body.appendChild(notification)

    // Animate in
    setTimeout(() => {
      notification.classList.add("show")
    }, 10)

    // Animate out and remove
    setTimeout(() => {
      notification.classList.remove("show")
      setTimeout(() => {
        notification.remove()
      }, 300)
    }, 3000)
  }

  // Avatar functionality
  const avatarImage = document.getElementById("avatar-image")
  const changeAvatarBtn = document.getElementById("changeAvatarBtn")
  const avatarUpload = document.getElementById("avatar-upload")

  // Avatar change button click
  changeAvatarBtn.addEventListener("click", () => {
    avatarUpload.click()
  })

  // Handle file upload
  avatarUpload.addEventListener("change", (e) => {
    const file = e.target.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (event) => {
        avatarImage.src = event.target.result
        showNotification("Аватар обновлен! Сохраните изменения.", "info")
      }
      reader.readAsDataURL(file)
    }
  })
})


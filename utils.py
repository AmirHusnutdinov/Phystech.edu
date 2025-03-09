from flask import session

def is_login():
    return session["Login"]

def data():
    return {"Login": is_login, "Name": session["namme"]}
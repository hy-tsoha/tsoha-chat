from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT password, id FROM users WHERE username = %s"

    try:
        with db.session as transaction:
            transaction.execute(sql, (username,))
            user = transaction.fetchone()
    except Exception as e:
        print(e)
        return False

    if not (user and check_password_hash(user.password, password)):
        return False

    session.update(user_id=user.id)
    return True


def logout():
    return session.pop("user_id", None)


def register(username, password):
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username, password) VALUES (%s, %s)"

    try:
        with db.session as transaction:
            transaction.execute(sql, (username, hash_value,))
    except Exception as e:
        print(e)
        return False

    return login(username, password)


def user_id():
    return session.get("user_id", None)

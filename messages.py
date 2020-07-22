from db import db
import users

def get_list():
    sql = """
        SELECT
            M.content, U.username, M.sent_at
        FROM messages M, users U
        WHERE M.user_id = U.id
        ORDER BY M.id
    """

    try:
        with db.session as transaction:
            transaction.execute(sql)
            return transaction.fetchall()
    except Exception as e:
        print(e)


def send(content):
    user_id = users.user_id()

    if not user_id:
        return False

    sql = "INSERT INTO messages (content, user_id, sent_at) VALUES (%s, %s, NOW())"

    try:
        with db.session as transaction:
            transaction.execute(sql, (content, user_id,))
    except Exception as e:
        print(e)
        return False

    return True

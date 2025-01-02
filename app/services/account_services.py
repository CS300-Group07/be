from app.services.use_db import use_db
from hashlib import sha256

# def hashing_password(password: str):
    # return sha256(password.encode('utf-8')).hexdigest()

def check_user(username: str):
    try:
        query = """
        SELECT username
        FROM users
        WHERE username = %s;
        """
        result = use_db(query, (username,), fetch=True)
        if result and len(result) > 0:
            return True
        return False
    except Exception as e:
        print(f'Error in check_user: {str(e)}')
        return False

def check_user_password(username: str, password: str):
    query = """
    SELECT password_hash
    FROM users
    WHERE username = %s;
    """
    result = use_db(query, (username,), fetch=True)
    if result:
        return result[0][0] == password
    return False
def login(username: str, hashing_password: str):
    if check_user_password(username, hashing_password):
        return "cookies"
    return None

def sign_up(username: str, password: str, email: str):
    if len(username) == 0 or len(password) == 0:
        return "Username and password must not be empty"
    if len(email) == 0:
        return "Email must not be empty"
    # hash_password = hashing_password(password)
    if check_user(username):
        return "Username already exists"
    query = """
    INSERT INTO users (username, password_hash, email)
    VALUES (%s, %s, %s);
    """
    try:
        use_db(query, (username, password, email))
        return "Success"
    except Exception as e:
        return str(e)

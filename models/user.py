import hashlib
from database import connect


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_default_admin():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", ("admin",))
    existing_user = cursor.fetchone()

    if not existing_user:
        cursor.execute("""
        INSERT INTO users (username, password_hash, role)
        VALUES (?, ?, ?)
        """, ("admin", hash_password("admin123"), "admin"))

    conn.commit()
    conn.close()


def verify_login(username, password):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users
    WHERE username = ? AND password_hash = ?
    """, (username, hash_password(password)))

    user = cursor.fetchone()

    conn.close()
    return user
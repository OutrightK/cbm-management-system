from database import connect

def add_student(first_name, last_name, age, gender, email, payment_status, payment_method, notes):
    if not first_name.strip():
        raise ValueError("First name is required.")

    if not last_name.strip():
        raise ValueError("Last name is required.")

    if age is not None and (not isinstance(age, int) or age <= 0):
        raise ValueError("Age must be a positive number.")

    if email and "@" not in email:
        raise ValueError("Invalid email address.")

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM students WHERE email = ?", (email,))
    if email and cursor.fetchone():
        conn.close()
        raise ValueError("A student with this email already exists.")

    cursor.execute("""
    INSERT INTO students (
        first_name, last_name, age, gender, email,
        payment_status, payment_method, notes
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (first_name, last_name, age, gender, email, payment_status, payment_method, notes))

    conn.commit()
    conn.close()


def get_all_students():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()
    return students


def get_student_by_id(student_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()

    conn.close()
    return student


def update_student(student_id, first_name, last_name, age, gender, email, payment_status, payment_method, notes):
    if not first_name.strip():
        raise ValueError("First name is required.")

    if not last_name.strip():
        raise ValueError("Last name is required.")

    if age is not None and (not isinstance(age, int) or age <= 0):
        raise ValueError("Age must be a positive number.")

    if email and "@" not in email:
        raise ValueError("Invalid email address.")

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE students
    SET first_name = ?, last_name = ?, age = ?, gender = ?,
        email = ?, payment_status = ?, payment_method = ?, notes = ?
    WHERE id = ?
    """, (first_name, last_name, age, gender, email, payment_status, payment_method, notes, student_id))

    conn.commit()
    conn.close()


def delete_student(student_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM student_courses WHERE student_id = ?", (student_id,))
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))

    conn.commit()
    conn.close()


def search_students(keyword):
    conn = connect()
    cursor = conn.cursor()

    wildcard = f"%{keyword}%"

    cursor.execute("""
    SELECT * FROM students
    WHERE first_name LIKE ? OR last_name LIKE ? OR email LIKE ?
    """, (wildcard, wildcard, wildcard))

    results = cursor.fetchall()
    conn.close()
    return results


def filter_students_by_payment(status):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM students
    WHERE payment_status = ?
    """, (status,))

    results = cursor.fetchall()
    conn.close()
    return results

def get_student_by_email(email):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE email = ?", (email,))
    student = cursor.fetchone()

    conn.close()
    return student

def get_recent_students(limit=5):
        conn = connect()
        cursor = conn.cursor()
    
        cursor.execute("""
        SELECT id, first_name, last_name, email
        FROM students
        ORDER BY id DESC
        LIMIT ?
        """, (limit,))
    
        students = cursor.fetchall()
        conn.close()
        return students
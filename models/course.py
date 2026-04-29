from database import connect

def add_course(name, duration):
    if not name.strip():
        raise ValueError("Course name is required.")

    if not duration.strip():
        raise ValueError("Duration is required.")

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO courses (name, duration)
    VALUES (?, ?)
    """, (name, duration))

    conn.commit()
    conn.close()


def get_all_courses():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    conn.close()
    return courses


def get_course_by_id(course_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM courses WHERE id = ?", (course_id,))
    course = cursor.fetchone()

    conn.close()
    return course


def update_course(course_id, name, duration):
    if not name.strip():
        raise ValueError("Course name is required.")

    if not duration.strip():
        raise ValueError("Duration is required.")

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE courses
    SET name = ?, duration = ?
    WHERE id = ?
    """, (name, duration, course_id))

    conn.commit()
    conn.close()


def delete_course(course_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM student_courses WHERE course_id = ?", (course_id,))
    cursor.execute("DELETE FROM courses WHERE id = ?", (course_id,))

    conn.commit()
    conn.close()

def get_course_by_name(name):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM courses WHERE name = ?", (name,))
    course = cursor.fetchone()

    conn.close()
    return course

def get_recent_courses(limit=5):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, name, duration
    FROM courses
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    courses = cursor.fetchall()
    conn.close()
    return courses
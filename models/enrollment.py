from database import connect

def enroll_student(student_id, course_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM student_courses
    WHERE student_id = ? AND course_id = ?
    """, (student_id, course_id))

    if cursor.fetchone():
        conn.close()
        raise ValueError("Student is already enrolled in this course.")

    cursor.execute("""
    INSERT INTO student_courses (student_id, course_id)
    VALUES (?, ?)
    """, (student_id, course_id))

    conn.commit()
    conn.close()


def get_courses_for_student(student_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT courses.id, courses.name, courses.duration
    FROM courses
    JOIN student_courses ON courses.id = student_courses.course_id
    WHERE student_courses.student_id = ?
    """, (student_id,))

    courses = cursor.fetchall()
    conn.close()
    return courses


def get_students_in_course(course_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT students.id,
           students.first_name || ' ' || students.last_name AS full_name,
           students.email
    FROM students
    JOIN student_courses ON students.id = student_courses.student_id
    WHERE student_courses.course_id = ?
    """, (course_id,))

    students = cursor.fetchall()
    conn.close()
    return students


def get_students_with_courses():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT students.first_name || ' ' || students.last_name AS student_name,
           courses.name AS course_name
    FROM student_courses
    JOIN students ON students.id = student_courses.student_id
    JOIN courses ON courses.id = student_courses.course_id
    """)

    results = cursor.fetchall()
    conn.close()
    return results


def remove_enrollment(student_id, course_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM student_courses
    WHERE student_id = ? AND course_id = ?
    """, (student_id, course_id))

    conn.commit()
    conn.close()
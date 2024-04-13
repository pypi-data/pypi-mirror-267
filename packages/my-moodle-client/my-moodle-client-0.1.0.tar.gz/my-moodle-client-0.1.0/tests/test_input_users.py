"""
Copyright © 2024 Mark Crowe <https://github.com/marcocrowe>. All rights reserved.
Repository support
"""

from os.path import exists
from os import remove
from sqlite3 import Connection, connect

from my_moodle.json_utility import load_json_list_from_file
from my_moodle_client.data_base import MoodleSqLiteDatabase


def create_data_base():
    """Create the Moodle database."""

    db_path = "moodle.db"
    if exists(db_path):
        remove(db_path)

    connection = connect(db_path)

    # Execute SQL script
    execute_sql_script("my_moodle/data_base.sql", connection)

    print("SQL script executed successfully.")
    return connection


# Function to execute SQL script file
def execute_sql_script(script_file, connection: Connection):
    """Execute an SQL script file on the database connection."""
    with open(script_file, "r", encoding="utf-8") as script:
        sql_script = script.read()
        cursor = connection.cursor()
        cursor.executescript(sql_script)
        connection.commit()


def get_enrollments() -> list[dict]:
    """Get enrollments from json file

    Returns:
        list[dict]: List of enrollments
    """
    file_path = "C:/_data/students.json"
    return load_json_list_from_file(file_path)


def main() -> None:
    """Main function to insert data into the database"""
    connection = create_data_base()

    role_ids = []
    course_ids = []

    moodle_db = MoodleSqLiteDatabase(connection)

    enrollments: list[dict] = get_enrollments()

    for student in enrollments:
        moodle_db.student_repository.create_student(student)

        for role in student["roles"]:

            if role["roleid"] not in role_ids:
                role_ids.append(role["roleid"])
                moodle_db.role_repository.create_role(role)
            if (
                moodle_db.student_role_repository.get_by_id(
                    student["id"], role["roleid"]
                )
                is None
            ):
                moodle_db.student_role_repository.create_student_role(
                    role["roleid"], student["id"]
                )

        for course in student["enrolledcourses"]:
            if course["id"] not in course_ids:
                course_ids.append(course["id"])
                moodle_db.course_repository.create_course(course)
            moodle_db.student_course_repository.create_student_course(
                course["id"], student["id"]
            )


if __name__ == "__main__":
    main()

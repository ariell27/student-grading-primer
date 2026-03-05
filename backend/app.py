from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """

    try:
        students = db.get_all_students()
        return jsonify(students), 200
    except Exception:
        return jsonify({"error": "Failed to fetch students"}), 404



@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """

    try:
        data = request.json

        name = data.get("name")
        course = data.get("course")
        mark = data.get("mark", 0)  # mark optional, default 0

        if not name or not course:
            return jsonify({"error": "Missing name or course"}), 404

        if isinstance(name, str) and name.strip().isdigit():
            return jsonify({"error": "Name cannot be a number"}), 404

        student = db.insert_student(name, course, mark)
        return jsonify(student), 200

    except Exception:
        return jsonify({"error": "Failed to create student"}), 404



@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """

    try:
        data = request.json

        name = data.get("name")
        course = data.get("course")
        mark = data.get("mark")

        if name is not None and isinstance(name, str) and name.strip() and name.strip().isdigit():
            return jsonify({"error": "Name cannot be a number"}), 404

        updated = db.update_student(student_id, name, course, mark)

        if not updated:
            return jsonify({"error": "Student not found"}), 404

        return jsonify(updated), 200

    except Exception:
        return jsonify({"error": "Failed to update student"}), 404


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    try:
        deleted = db.delete_student(student_id)

        if not deleted:
            return jsonify({"error": "Student not found"}), 404

        return jsonify(deleted), 200

    except Exception:
        return jsonify({"error": "Failed to delete student"}), 404



@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """

    try:
        students = db.get_all_students()

        if not students:
            return jsonify({
                "count": 0,
                "average": 0,
                "min": 0,
                "max": 0
            }), 200

        marks = [s["mark"] for s in students]

        return jsonify({
            "count": len(marks),
            "average": sum(marks) / len(marks),
            "min": min(marks),
            "max": max(marks)
        }), 200

    except Exception:
        return jsonify({"error": "Failed to calculate stats"}), 404



@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

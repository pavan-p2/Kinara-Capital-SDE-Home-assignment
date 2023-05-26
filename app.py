from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

# Load student details from JSON file
with open('students.json') as f:
    students = json.load(f)


# Load Student Details API
@app.route('/api/students', methods=['GET'])
def load_students():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    paginated_students = students[start_index:end_index]

    return jsonify({
        'data': paginated_students,
        'totalItems': len(students),
        'totalPages': (len(students) + page_size - 1) // page_size
    })


# Server-side Filtering API
@app.route('/api/students/filter', methods=['POST'])
def filter_students_api():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Unsupported Media Type'}), 415

    filter_criteria = request.json.get('filterCriteria')
    filtered_students = []

    if filter_criteria:
        for student in students:
            # Filter based on the provided criteria
            if (
                str(filter_criteria).lower() in str(student['id']).lower()
                or str(filter_criteria).lower() in student['name'].lower()
                or str(filter_criteria).lower() in str(student['totalMarks']).lower()
            ):
                filtered_students.append(student)
    else:
        filtered_students = students

    return jsonify({
        'data': filtered_students,
        'totalItems': len(filtered_students),
        'totalPages': 1
    })


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        filter_criteria = request.form.get('filterCriteria')
        filtered_students = []

        if filter_criteria:
            for student in students:
                # Filter based on the provided criteria
                if (
                        str(filter_criteria).lower() in str(student['id']).lower()
                        or str(filter_criteria).lower() in student['name'].lower()
                        or str(filter_criteria).lower() in str(student['totalMarks']).lower()
                ):
                    filtered_students.append(student)
        else:
            filtered_students = students

        return render_template('index.html', students=filtered_students)

    return render_template('index.html', students=students)


# Start the server
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, redirect, url_for, render_template
from models import db, get_table_and_fields, initialize_database

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Create the table in the database
initialize_database(app)

# Home page - List all students
@app.route('/')
def list_students():
    table, fields = get_table_and_fields()
    students = db.session.query(table).all()
    return render_template('list.html', students=students, fields=fields)

# Create a new student
@app.route('/create', methods=['GET', 'POST'])
def create_student():
    table, fields = get_table_and_fields()
    if request.method == 'POST':
        data = {field: request.form[field] for field in fields}
        insert_query = table.insert().values(**data)
        db.session.execute(insert_query)
        db.session.commit()
        return redirect(url_for('list_students'))
    return render_template('create.html', fields=fields)

# Update a student
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    table, fields = get_table_and_fields()
    student = db.session.query(table).filter(table.c.id == id).first()
    if request.method == 'POST':
        data = {field: request.form[field] for field in fields}
        update_query = table.update().where(table.c.id == id).values(**data)
        db.session.execute(update_query)
        db.session.commit()
        return redirect(url_for('list_students'))
    return render_template('update.html', student=student, fields=fields)

# Delete a student
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_student(id):
    table, _ = get_table_and_fields()
    if request.method == 'POST':
        delete_query = table.delete().where(table.c.id == id)
        db.session.execute(delete_query)
        db.session.commit()
        return redirect(url_for('list_students'))
    student = db.session.query(table).filter(table.c.id == id).first()
    return render_template('delete.html', student=student)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define the table dynamically
def create_table():
    from sqlalchemy import Table, Column, Integer, String, MetaData
    metadata = MetaData()
    student_table = Table(
        'student', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(100), nullable=False),
        Column('age', Integer, nullable=False),
        Column('grade', String(10), nullable=False)
    )
    return student_table

# Get the table and field names
def get_table_and_fields():
    table = create_table()
    fields = [column.name for column in table.columns if column.name != 'id']
    return table, fields

# Create the table in the database
def initialize_database(app):
    with app.app_context():
        table, _ = get_table_and_fields()
        table.create(db.engine, checkfirst=True)

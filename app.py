from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
# Use the default SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)


class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256), nullable=False)
    table_name = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f"<UploadedFile {self.filename}>"


@app.route('/')
def home():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename

    df = pd.read_excel(file)

    # Generate a table name based on the filename (excluding extension)
    table_name = 'table_' + filename[:-5]

    # Create the table in the database
    df.to_sql(table_name, db.engine, if_exists='replace')

    uploaded_file = UploadedFile(filename=filename, table_name=table_name)
    db.session.add(uploaded_file)
    db.session.commit()

    return f'File "{filename}" uploaded and table "{table_name}" created successfully!'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

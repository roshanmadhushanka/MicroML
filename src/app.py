from flask import Flask, abort, render_template, request, jsonify, redirect, url_for, session, Session
from flask_cors import CORS
import os
import pandas as pd

# define
UPLOAD_FOLDER = '/home/wso2123/PycharmProjects/MicroML/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_upload_directory_contents():
    return os.listdir(app.config['UPLOAD_FOLDER'], )

def get_column_names(file_name):
    path = app.config['UPLOAD_FOLDER'] + '/' + file_name
    df = pd.read_csv(path, nrows=1)
    return list(df.columns)


@app.route('/')
def index():
    return render_template('index.html', content=get_upload_directory_contents())

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))

@app.route('/select', methods=['POST'])
def select():
    if request.method == 'POST':
        session['selected_file'] = request.form.get('selected_file')
        session['col_names'] = get_column_names(session['selected_file'])
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)



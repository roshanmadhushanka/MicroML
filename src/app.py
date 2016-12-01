from flask import Flask, abort, render_template, request, jsonify, redirect, url_for, session, Session, send_from_directory
from flask_cors import CORS
import os
import pandas as pd
from featureeng import Frame




app = Flask(__name__)
CORS(app)

# define
UPLOAD_FOLDER = '/home/wso2123/PycharmProjects/MicroML/src/uploads'
UPLOAD_FOLDER = app.root_path + '/uploads'
OUTPUT_FOLDER = app.root_path + '/output'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_upload_directory_contents():
    return os.listdir(app.config['UPLOAD_FOLDER'], )

def get_output_directory_contents():
    return os.listdir(app.config['OUTPUT_FOLDER'], )

def get_column_names(file_name):
    path = app.config['UPLOAD_FOLDER'] + '/' + file_name
    df = pd.read_csv(path, nrows=1)
    return list(df.columns)


@app.route('/')
def index():
    content = {'upload': get_upload_directory_contents(), 'output': get_output_directory_contents()}
    return render_template('index.html', content=content)

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

@app.route('/process', methods=['GET', 'POST'])
def process():
    # Call after select function
    if request.method == 'POST':
        file_name = session['selected_file']
        input_file_path = app.config['UPLOAD_FOLDER'] + '/' + file_name
        col_names = session['col_names']

        # Collecting meta data
        # Collecting moving average data
        ma = {}     # moving average
        for column in col_names:
            header = column + "_ma"
            ma[column] = int(request.form.get(header))

        # Collecting moving standard deviation data
        msd = {}    # moving standard deviation
        for column in col_names:
            header = column + "_ms"
            msd[column] = int(request.form.get(header))

        data = pd.read_csv(input_file_path)
        frame = Frame(data)

        # Applying moving average
        for key in ma.keys():
            if ma[key] == 0:
                continue
            frame.apply_moving_average(input_column=key, window=ma[key])

        # Applying moving standard deviation
        for key in msd.keys():
            if msd[key] == 0:
                continue
            frame.apply_moving_std(input_column=key, window=msd[key])

        output_file_name = 'result_' + file_name
        output_path = app.config['OUTPUT_FOLDER'] + '/' + output_file_name
        frame.save_file(file_name=output_path)
    return redirect(url_for('index'))

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    if request.method == 'GET':
        downloads = os.path.join(app.root_path, app.config['OUTPUT_FOLDER'])
        return send_from_directory(directory=downloads, filename=filename)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)



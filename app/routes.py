import os
from flask import render_template, request, redirect, url_for, abort
from werkzeug.utils import secure_filename
from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    uploaded_file = request.files['file']
    # Prueba de seguridad 
    # uploaded_file.filename = "../../.bashrc"
    # print("Viene por aqui")
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('index'))

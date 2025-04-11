import os, imghdr
from flask import render_template, request, redirect, url_for, abort, \
        send_from_directory
from werkzeug.utils import secure_filename
from app import app

def validate_image(stream):
    try:
        header = stream.read(1024)
        stream.seek(0)
        format = imghdr.what(None, header)
        if not format:
            return None
        return '.' + format
    except Exception as e:
        print(f"Error al validar la imagen: {e}")
        return None

@app.route('/')
def index():
    files = os.listdir("app/" + app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    uploaded_file = request.files['file']
    # Prueba de seguridad 
    # uploaded_file.filename = "../../.bashrc"
    # print("Viene por aqui")
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            abort(400)
        uploaded_file.save(os.path.join("app/"+ app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



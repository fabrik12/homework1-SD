import os, imghdr
from flask import render_template, request, redirect, url_for, abort, \
        send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
from app import app

def validate_image(stream, file_ext):
    try:
        img = Image.open(stream)
        img.verify()
        print(f"Este el formato detectado: {img.format.lower()}")
        if file_ext=='.jpg' and img.format.lower()=="jpeg":
            #Mantener la extension .jpg si el formato detectado es valido y retorna como jpeg
            return file_ext
        return '.' + img.format.lower() 
    except Exception as e:
        print(f"Error al validar la imagen: {e}")
        return None

@app.route('/')
def index():
    files = os.listdir("app/" + app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    # Prueba de seguridad 
    # uploaded_file.filename = "../../.bashrc"
    # print("Viene por aqui")
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        print(file_ext)
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream, file_ext):
            return "Invalid image", 400
        uploaded_file.save(os.path.join("app/"+ app.config['UPLOAD_FOLDER'], filename))
    return '', 204

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

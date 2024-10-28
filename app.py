from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os

app = Flask(__name__)

# Setze den Ordner, in dem die hochgeladenen Dateien gespeichert werden
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Stelle sicher, dass der Upload-Ordner existiert
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    # Hole die Liste der bereits hochgeladenen Dateien
    # files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('home.html') #files=files)

@app.route('/home.html')
def seite0():
    return render_template('home.html')


@app.route('/kontakt.html')
def seite1():
    return render_template('kontakt.html')

@app.route('/hausordnung.html')
def seite2():
    return render_template('hausordnung.html')

@app.route('/termine.html')
def seite3():
    return render_template('termine.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Überprüfen, ob die Datei im Anfrageobjekt vorhanden ist
    if 'file' not in request.files:
        return 'Keine Datei hochgeladen', 400
    
    file = request.files['file']

    # Überprüfen, ob eine Datei ausgewählt wurde
    if file.filename == '':
        return 'Keine Datei ausgewählt', 400
    
    # Speichere die Datei im Upload-Ordner
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    return f'Datei {file.filename} erfolgreich hochgeladen und gespeichert!'

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
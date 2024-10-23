from flask import Flask, request
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Konfiguration für den E-Mail-Versand
app.config['MAIL_SERVER'] = 'smtp.example.com'  # E-Mail-Server
app.config['MAIL_PORT'] = 587  # Port für TLS
app.config['MAIL_USERNAME'] = 'your-email@example.com'  # E-Mail-Adresse
app.config['MAIL_PASSWORD'] = 'your-email-password'  # Passwort
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# Ordner zum Speichern der hochgeladenen Dateien
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Keine Datei hochgeladen', 400
    
    file = request.files['file']
    
    if file.filename == '':
        return 'Keine Datei ausgewählt', 400
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)  # Speichern der Datei

    # E-Mail-Versand
    msg = Message('Neue Datei hochgeladen',
                  sender='your-email@example.com',
                  recipients=['recipient@example.com'])  # E-Mail-Adresse des Empfängers
    msg.body = f'Deine Datei wurde hochgeladen: {file.filename}'
    with app.open_resource(file_path) as fp:
        msg.attach(file.filename, 'application/octet-stream', fp.read())
    
    mail.send(msg)  # E-Mail senden
    
    return 'Datei erfolgreich hochgeladen und E-Mail gesendet', 200

if __name__ == '__main__':
    app.run(debug=True)



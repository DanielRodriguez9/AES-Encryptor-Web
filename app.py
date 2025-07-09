from flask import Flask, render_template, request, jsonify
from cryptography.fernet import Fernet
import base64

app = Flask(__name__)

def crear_cifrador(clave_texto):
    clave_bytes = clave_texto.encode().ljust(32, b'0')[:32]
    clave_segura = base64.urlsafe_b64encode(clave_bytes)
    return Fernet(clave_segura)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cifrar', methods=['POST'])
def cifrar():
    datos = request.json
    mensaje = datos.get('mensaje', '')
    clave = datos.get('clave', '')
    if not mensaje or not clave:
        return jsonify({'error': 'missing data'}), 400

    fernet = crear_cifrador(clave)
    cifrado = fernet.encrypt(mensaje.encode()).decode()
    return jsonify({'resultado': cifrado})

@app.route('/descifrar', methods=['POST'])
def descifrar():
    datos = request.json
    mensaje = datos.get('mensaje', '')
    clave = datos.get('clave', '')
    if not mensaje or not clave:
        return jsonify({'error': 'missing data'}), 400

    try:
        fernet = crear_cifrador(clave)
        descifrado = fernet.decrypt(mensaje.encode()).decode()
        return jsonify({'resultado': descifrado})
    except Exception:
        return jsonify({'error': 'Error decrypting, ¿is the key correct?'}), 400

if __name__ == '__main__':
    app.run(debug=True)

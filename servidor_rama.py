import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

# 1. Función para crear la base de datos y un usuario maestro
def init_db():
    conn = sqlite3.connect('rama_central.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')
    # Insertar el usuario admin por defecto si no existe
    cursor.execute('''
        INSERT OR IGNORE INTO usuarios (username, password, role) 
        VALUES ('admin', 'admin123', 'ADMINISTRADOR')
    ''')
    conn.commit()
    conn.close()

# Inicializamos la BD al arrancar
init_db()

@app.route('/', methods=['GET'])
def home():
    return jsonify({"mensaje": "Servidor RAMA ERP Activo con Base de Datos SQLite"})

# 2. Nueva ruta de Login conectada a SQLite
@app.route('/api/login', methods=['POST'])
def login():
    datos = request.get_json()
    
    if not datos or 'username' not in datos or 'password' not in datos:
        return jsonify({"status": "error", "mensaje": "Faltan datos"}), 400

    conn = sqlite3.connect('rama_central.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM usuarios WHERE username=? AND password=?", 
                   (datos['username'], datos['password']))
    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        return jsonify({
            "status": "success",
            "userId": usuario[0],
            "username": usuario[1],
            "role": usuario[2],
            "token": f"token_jwt_simulado_para_{usuario[1]}"
        }), 200
    else:
        return jsonify({"status": "error", "mensaje": "Credenciales inválidas"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


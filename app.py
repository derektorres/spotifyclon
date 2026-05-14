from flask import Flask, render_template, request, jsonify, redirect, url_for
from entities.user import User
from entities.artista import Artista
from entities.cancion import Cancion
app = Flask(__name__)

# --- AUTH ---
@app.route('/')
def signin():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

# --- ARTISTAS ---
@app.route('/artistas')
def listar_artistas():
    lista = Artista.get_all_ordered()
    return render_template('artistas.html', artistas=lista)
    
@app.route('/artistas/nuevo')
def crear_artista():
    return render_template('form_artista.html')

# --- CANCIONES ---
@app.route('/canciones')
def listar_canciones():
    todas_las_canciones = Cancion.get_all()
    return render_template('canciones.html', canciones=todas_las_canciones)

# --- PLAYLISTS ---
@app.route('/playlists')
def listar_playlists():
    return render_template('playlists.html')

@app.route('/playlist/<int:id>')
def detalle_playlist(id):
    return render_template('detalle_playlist.html', id=id)



@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/canciones/nuevo')
def formulario_cancion():
    artistas = Artista.get_all_ordered() 
    return render_template('form_cancion.html', artistas=artistas)

@app.route('/api/login', methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.check_login(email, password)

    if user:
        return jsonify({"success": True, "message": "Inicio de sesión exitoso."}), 200
    else:
        return jsonify({"success": False, "message": "Correo electrónico o contraseña incorrectos."}), 401

@app.route('/api/users', methods=["POST"])
def create_user():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    country = data.get("country") 

    if User.check_email_exists(email):
        return jsonify({"success": False, "message": "El correo electrónico ingresado ya se encuentra registrado."}), 409
    
    is_saved = User.save(name, email, password, country) 

    if is_saved:
        return jsonify({"success": True, "message": "Su cuenta fue creada correctamente."}), 201
    else:
        return jsonify({"success": False, "message": "Error al crear cuenta."}), 500



@app.route('/api/artistas', methods=["POST"])
def create_artista():
    data = request.get_json()

    nombre = data.get("nombre")
    nacionalidad = data.get("nacionalidad")
    fecha_nacimiento = data.get("fecha_nacimiento")
    oyentes_mensuales = data.get("oyentes_mensuales")

    if not nombre or not nacionalidad or not fecha_nacimiento:
        return jsonify({"success": False, "message": "Faltan datos obligatorios."}), 400

    is_saved = Artista.save(nombre, nacionalidad, fecha_nacimiento, oyentes_mensuales) 

    if is_saved:
        return jsonify({"success": True, "message": "Artista guardado exitosamente."}), 201
    else:
        return jsonify({"success": False, "message": "Error al guardar el artista en la base de datos."}), 500


@app.route('/api/canciones', methods=["POST"])
def create_cancion():
    data = request.get_json()

    nombre = data.get("nombre")
    artista_id = data.get("artista_id")
    duracion_segundos = data.get("duracion_segundos")
    genero = data.get("genero")

    if not nombre or not artista_id or not duracion_segundos:
        return jsonify({"success": False, "message": "Faltan datos obligatorios."}), 400

    is_saved = Cancion.save(nombre, duracion_segundos, genero, artista_id)

    if is_saved:
        return jsonify({"success": True, "message": "Canción guardada exitosamente."}), 201
    else:
        return jsonify({"success": False, "message": "Error al guardar la canción en la base de datos."}), 500


if __name__ == '__main__':
    app.run()
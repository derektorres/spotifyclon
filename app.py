from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from entities.user import User
from entities.artista import Artista
from entities.cancion import Cancion
from entities.playlist import Playlist 

app = Flask(__name__)
app.secret_key = 'llave_secreta_para_sesiones' 

@app.route('/')
def signin():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/artistas')
def listar_artistas():
    lista = Artista.get_all_ordered()
    return render_template('artistas.html', artistas=lista)
    
@app.route('/artistas/nuevo')
def crear_artista():
    return render_template('form_artista.html')

@app.route('/canciones')
def listar_canciones():
    todas_las_canciones = Cancion.get_all()
    return render_template('canciones.html', canciones=todas_las_canciones)

@app.route('/canciones/nuevo')
def formulario_cancion():
    artistas = Artista.get_all_ordered() 
    return render_template('form_cancion.html', artistas=artistas)

@app.route('/playlists')
def listar_playlists():
    user_id = session.get('user_id')
    
    if not user_id:
        return redirect(url_for('signin'))

    lista = Playlist.get_by_user(user_id)

    return render_template('playlists.html', playlists=lista)

@app.route('/playlist/<int:id>')
def detalle_playlist(id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('signin'))
    todas_las_canciones = Cancion.get_all() 
    return render_template('detalle_playlist.html', id=id, canciones=todas_las_canciones)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/api/login', methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.check_login(email, password)

    if user:
        session['user_id'] = user.id
        return jsonify({"success": True, "message": "Inicio de sesión exitoso."}), 200
    else:
        return jsonify({"success": False, "message": "Correo electrónico o contraseña incorrectos."}), 401

@app.route('/api/users', methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get("nombre") or data.get("name")
    email = data.get("email")
    password = data.get("password")
    country = data.get("pais") or data.get("country")

    if not name or not email:
        return jsonify({"success": False, "message": "Faltan datos en el JSON"}), 400

    if User.check_email_exists(email):
        return jsonify({"success": False, "message": "El correo ya existe."}), 409
    
    is_saved = User.save(name, email, password, country) 

    if is_saved:
        return jsonify({"success": True, "message": "¡Éxito! Usuario y Playlist creados."}), 201
    else:
        return jsonify({"success": False, "message": "Error en la transacción. Nada se guardó."}), 500

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
    
@app.route('/api/playlists', methods=["POST"])
def api_crear_playlist():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"success": False, "message": "Sesión no válida"}), 401

    data = request.get_json()
    nombre = data.get("nombre")

    if not nombre:
        return jsonify({"success": False, "message": "El nombre es obligatorio"}), 400

    if Playlist.save(nombre, user_id):
        return jsonify({"success": True, "message": "Playlist creada con éxito"}), 201
    else:
        return jsonify({"success": False, "message": "Error al guardar en la BD"}), 500
    
@app.route('/canciones/filtrar')
def filtrar_por_pais():
    pais = request.args.get('pais', '') 
    if pais:
        resultado = Cancion.get_by_artist_country(pais)
    else:
        resultado = Cancion.get_all()
        
    return render_template('canciones.html', canciones=resultado, filtro=pais)


@app.route('/api/playlist/agregar_cancion', methods=["POST"])
def api_agregar_cancion():
    data = request.get_json()
    playlist_id = data.get("playlist_id")
    cancion_id = data.get("cancion_id")

    if not playlist_id or not cancion_id:
        return jsonify({"success": False, "message": "Faltan datos."}), 400

    from entities.playlist import Playlist
    if Playlist.agregar_cancion(playlist_id, cancion_id):
        return jsonify({"success": True, "message": "¡Cancion agregada con éxito!"}), 201
    else:
        return jsonify({"success": False, "message": "Error al guardar en la base de datos."}), 500

@app.route('/logout')
def logout():
    session.clear() 
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)
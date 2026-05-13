from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# --- RUTA PRINCIPAL (REDIRIGE A LOGIN) ---
@app.route('/')
def index():
    return redirect(url_for('signin'))

# --- AUTH ---
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        # Tu lógica de validación aquí
        return "Procesando inicio de sesión..."
    return render_template('signin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Tu lógica de registro aquí
        return "Procesando registro..."
    return render_template('signup.html')

# --- ARTISTAS ---
@app.route('/artistas')
def listar_artistas():
    return render_template('artistas.html')

@app.route('/artistas/nuevo', methods=['GET', 'POST'])
def crear_artista():
    if request.method == 'POST':
        return redirect(url_for('listar_artistas'))
    return render_template('form_artista.html')

# --- CANCIONES ---
@app.route('/canciones')
def listar_canciones():
    return render_template('canciones.html')

# --- PLAYLISTS ---
@app.route('/playlists')
def listar_playlists():
    return render_template('playlists.html')

@app.route('/playlist/<int:id>')
def detalle_playlist(id):
    return render_template('detalle_playlist.html', id=id)

if __name__ == '__main__':
    app.run(debug=True)
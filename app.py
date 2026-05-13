from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/artistas')
def listar_artistas():
    return render_template('artistas.html')

@app.route('/artistas/nuevo', methods=['GET', 'POST'])
def crear_artista():
    if request.method == 'POST':
        return redirect(url_for('listar_artistas'))
    return render_template('form_artista.html')

@app.route('/canciones')
def listar_canciones():
    return render_template('canciones.html')

@app.route('/playlists')
def listar_playlists():
    return render_template('playlists.html')

@app.route('/playlist/<int:id>')
def detalle_playlist(id):
    return render_template('detalle_playlist.html', id=id)

if __name__ == '__main__':
    app.run()
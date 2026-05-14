document.addEventListener('DOMContentLoaded', function() {
    const btnAgregar = document.getElementById('btn-agregar-cancion');

    if (btnAgregar) {
        btnAgregar.addEventListener('click', async function() {
            const selectCancion = document.getElementById('select-cancion');
            const cancionId = selectCancion.value;
            const playlistId = this.getAttribute('data-playlist-id'); 

            if (!cancionId) {
                Swal.fire('Oye', 'Por favor selecciona una canción primero.', 'warning');
                return;
            }

            const response = await fetch('/api/playlist/agregar_cancion', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    playlist_id: parseInt(playlistId), 
                    cancion_id: parseInt(cancionId) 
                })
            });

            const result = await response.json();

            if (result.success) {
                Swal.fire('¡correcto!', result.message, 'success');
                selectCancion.value = ""; 
            } else {
                Swal.fire('Error', result.message, 'error');
            }
        });
    }
});
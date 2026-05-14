document.addEventListener('DOMContentLoaded', function() {
    const btnNueva = document.getElementById('btn-nueva-playlist');

    if (btnNueva) {
        btnNueva.addEventListener('click', async () => {
            const { value: nombre } = await Swal.fire({
                title: 'Nueva Playlist',
                input: 'text',
                inputLabel: 'Nombre de la lista:',
                showCancelButton: true,
                confirmButtonColor: '#1db954',
                cancelButtonText: 'Cancelar'
            });

            if (nombre) {
                const response = await fetch('/api/playlists', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ nombre: nombre })
                });

                const result = await response.json();

                if (result.success) {
                    Swal.fire('¡Listo!', result.message, 'success').then(() => {
                        location.reload(); // Recargamos para ver la nueva lista
                    });
                } else {
                    Swal.fire('Error', result.message, 'error');
                }
            }
        });
    }
});
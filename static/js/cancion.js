document.getElementById("btn-save-cancion").addEventListener("click", saveCancion);

function saveCancion() {
    const nombre = document.getElementById("can-nombre").value;
    const artista_id = document.getElementById("can-artista").value;
    const duracion = document.getElementById("can-duracion").value;
    const genero = document.getElementById("can-genero").value;

    // Validaciones
    if (nombre === "") {
        Swal.fire({ title: 'Falta información', text: 'Debes ingresar el título de la canción.', icon: 'warning', confirmButtonText: 'Aceptar' });
        return;
    }

    if (artista_id === "") {
        Swal.fire({ title: 'Falta información', text: 'Debes seleccionar un artista.', icon: 'warning', confirmButtonText: 'Aceptar' });
        return;
    }

    if (duracion === "" || parseInt(duracion) <= 0) {
        Swal.fire({ title: 'Falta información', text: 'Debes ingresar una duración válida en segundos.', icon: 'warning', confirmButtonText: 'Aceptar' });
        return;
    }

    
    const data = {
        nombre: nombre,
        artista_id: parseInt(artista_id),
        duracion_segundos: parseInt(duracion),
        genero: genero
    };

    
    fetch('/api/canciones', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            Swal.fire({
                title: '¡Guardado!',
                text: result.message,
                icon: 'success',
                confirmButtonText: 'Aceptar'
            }).then(() => {
                window.location.href = "/canciones"; 
            });
        } else {
            Swal.fire({
                title: 'Error',
                text: result.message,
                icon: 'error',
                confirmButtonText: 'Aceptar'
            });
        }
    })
    .catch(error => {
        console.error(error);
        Swal.fire({ title: 'Error', text: 'Problema de conexión con el servidor.', icon: 'error', confirmButtonText: 'Aceptar' });
    });
}
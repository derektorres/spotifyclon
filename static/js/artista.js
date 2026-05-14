document.getElementById("btn-save-artista").addEventListener("click", saveArtista);

function saveArtista() {
    const nombre = document.getElementById("art-nombre").value;
    const nacionalidad = document.getElementById("art-nacionalidad").value;
    const fecha = document.getElementById("art-fecha").value;
    const oyentes = document.getElementById("art-oyentes").value;

    
    if(nombre === "") {
        Swal.fire({ title: 'Falta información', text: 'Debe ingresar el nombre del artista.', icon: 'warning', confirmButtonText: 'Aceptar' });
        return;
    }

    if(nacionalidad === "") {
        Swal.fire({ title: 'Falta información', text: 'Debe ingresar la nacionalidad.', icon: 'warning', confirmButtonText: 'Aceptar' });
        return;
    }

    if(fecha === "") {
        Swal.fire({ title: 'Falta información', text: 'Debe seleccionar una fecha de nacimiento.', icon: 'warning', confirmButtonText: 'Aceptar' });
        return;
    }

    const oyentesMensuales = oyentes === "" ? 0 : parseInt(oyentes);

    const data = {
        nombre: nombre,
        nacionalidad: nacionalidad,
        fecha_nacimiento: fecha,
        oyentes_mensuales: oyentesMensuales
    };

   
    fetch('/api/artistas', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result =>  {
        if(result.success) {
            Swal.fire({
                title: '¡Guardado!',
                text: result.message,
                icon: 'success',
                confirmButtonText: 'Aceptar'
            }).then(() => {
                window.location.href = "/artistas"; 
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
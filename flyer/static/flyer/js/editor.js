// Simple Fabric.js based editor


// Save Project
document.getElementById('saveProject').addEventListener('click', () => {
    const name = prompt('Project name', 'My Flyer');
    if (!name) return;
    const json = JSON.stringify(canvas.toJSON());
    const dataURL = canvas.toDataURL({ format: 'png' });


    const form = new FormData();
    form.append('name', name);
    form.append('json_data', json);
    form.append('canvas_data', dataURL);


    fetch('/save_project/', {
        method: 'POST',
        body: form,
        headers: { 'X-CSRFToken': getCookie('csrftoken') }
    }).then(r => r.json()).then(js => {
        alert('Saved: ' + js.project_id);
    }).catch(e => { console.error(e); alert('Save failed') });
});


// small helper for CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
document.getElementById('toggleMode').addEventListener('click', () => {
    document.body.classList.toggle('dark');
    document.body.classList.toggle('light');
});

document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = e.target.file;
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const res = await fetch('/upload', {
        method: 'POST',
        body: formData
    });
    const data = await res.json();
    alert(data.message);
    location.reload();
});

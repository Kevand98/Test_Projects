const API = 'http://localhost:8000';

const searchBtn = document.getElementById('searchBtn');
const queryInput = document.getElementById('query');
const resultsDiv = document.getElementById('results');
const indexBtn = document.getElementById('indexBtn');


const dropZone = document.getElementById('dropZone');
const searchFile = document.getElementById('searchFile');
const uploadPrompt = document.getElementById('uploadPrompt');
const previewContainer = document.getElementById('previewContainer');
const imgPreview = document.getElementById('imgPreview');
const clearImgBtn = document.getElementById('clearImgBtn');


dropZone.onclick = () => searchFile.click();

searchFile.onchange = (e) => {
    if (e.target.files.length) handleFile(e.target.files[0]);
};

dropZone.ondragover = (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#38bdf8';
};
dropZone.ondragleave = () => {
    dropZone.style.borderColor = '#475569';
};
dropZone.ondrop = (e) => {
    e.preventDefault();
    dropZone.style.borderColor = '#475569';
    if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
};

function handleFile(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        imgPreview.src = e.target.result;
        uploadPrompt.classList.add('hidden');
        previewContainer.classList.remove('hidden');
    };
    reader.readAsDataURL(file);
}

clearImgBtn.onclick = (e) => {
    e.stopPropagation(); 
    searchFile.value = null;
    imgPreview.src = '';
    previewContainer.classList.add('hidden');
    uploadPrompt.classList.remove('hidden');
};


searchBtn.onclick = async () => {
    const text = queryInput.value;
    const file = searchFile.files[0];

    if (!text && !file) return alert("Please enter text or select an image.");

    resultsDiv.innerHTML = '<p style="text-align:center; color:#64748b;">Searching...</p>';

    const fd = new FormData();
    if (text) fd.append('text', text);
    if (file) fd.append('file', file);
    fd.append('top_k', 15);

    try {
        const res = await fetch(`${API}/search`, {
            method: 'POST',
            body: fd
        });
        const data = await res.json();
        showResults(data.results);
    } catch (err) {
        resultsDiv.innerHTML = '<p style="color:red; text-align:center">Search error.</p>';
        console.error(err);
    }
};

indexBtn.onclick = async () => {
    if(!confirm("Re-index images? This might take a moment.")) return;
    try {
        const res = await fetch(`${API}/index`, { method: 'POST' });
        const j = await res.json();
        alert(`Indexed ${j.count} images.`);
    } catch(e) {
        alert("Error indexing");
    }
};

function showResults(results) {
    resultsDiv.innerHTML = '';
    if (!results || results.length === 0) {
        resultsDiv.innerHTML = "<p style='text-align:center; color:#64748b;'>No matches found.</p>";
        return;
    }

    results.forEach(r => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <img src="${r.url}" loading="lazy">
            <div class="meta">
                <span>${r.path}</span>
                <span class="score">${(r.score * 100).toFixed(1)}%</span>
            </div>
        `;
        resultsDiv.appendChild(card);
    });
} 
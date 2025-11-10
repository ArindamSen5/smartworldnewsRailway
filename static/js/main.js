async function fetchNews() {
  const q = document.getElementById('topic').value || 'technology';
  const res = await fetch(`/api/news?q=${encodeURIComponent(q)}`);
  const data = await res.json();
  const results = document.getElementById('results');
  results.innerHTML = '';
  data.articles.forEach(a => {
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
        <h3><a href="${a.url}" target="_blank">${a.title}</a></h3>
        <p class="source">${a.source}</p>
        <p>${a.summary}</p>
    `;
    document.getElementById('results').appendChild(card);
});
}
document.getElementById('fetchBtn').addEventListener('click', fetchNews);

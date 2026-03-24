const DATA = window.BOOKS.reduce((acc, b) => {
  acc[b.genre] = acc[b.genre] || [];
  acc[b.genre].push(b);
  return acc;
}, {});

function fmt(n) {
  return parseInt(n).toLocaleString('en-GB');
}

// ── Table view ──────────────────────────────────────────
function applyFilters() {
  const genre  = document.getElementById('filter-genre').value;
  const year   = document.getElementById('filter-year').value;
  const sortBy = document.getElementById('sort-by').value;

  let books = [...window.BOOKS];
  if (genre) books = books.filter(b => b.genre === genre);
  if (year)  books = books.filter(b => String(b.year) === year);

  if (sortBy === 'votes')  books.sort((a, b) => parseInt(b.votes) - parseInt(a.votes));
  if (sortBy === 'title')  books.sort((a, b) => a.title.localeCompare(b.title));
  if (sortBy === 'author') books.sort((a, b) => a.author.localeCompare(b.author));

  document.getElementById('results-count').textContent = `Result # ${books.length}`;

  const tbody = document.getElementById('table-body');
  if (!books.length) {
    tbody.innerHTML = `<tr><td colspan="6" class="no-results">No results found.</td></tr>`;
    return;
  }

  tbody.innerHTML = books.map((b, i) => `
    <tr>
      <td class="rank-col">${i + 1}</td>
      <td class="title-col">
        <a href="${b.book_url}" target="_blank" rel="noopener noreferrer">${b.title}</a>
      </td>
      <td class="author-col">${b.author}</td>
      <td><span class="genre-pill">${b.genre}</span></td>
      <td class="year-col">${b.year}</td>
      <td class="votes-col">${fmt(b.votes)}</td>
    </tr>
  `).join('');
}

// ── Card / tab view ─────────────────────────────────────
let active = Object.keys(DATA)[0];

function renderTabs() {
  const el = document.getElementById('tabs');
  if (!el) return;
  el.innerHTML = Object.keys(DATA).map(g => `
    <button class="tab ${g === active ? 'active' : ''}"
            onclick="active='${g}';renderTabs();render()">${g}</button>
  `).join('');
}

function render() {
  const el = document.getElementById('list');
  if (!el) return;

  const books = [...(DATA[active] || [])];
  const sortEl = document.getElementById('sort');
  const sort   = sortEl ? sortEl.value : 'rank';

  if (!books.length) {
    el.innerHTML = `<p class="empty">No data for ${active} yet.</p>`;
    return;
  }

  if (sort === 'votes')  books.sort((a, b) => parseInt(b.votes) - parseInt(a.votes));
  if (sort === 'title')  books.sort((a, b) => a.title.localeCompare(b.title));
  if (sort === 'author') books.sort((a, b) => a.author.localeCompare(b.author));
  if (sort === 'rank')   books.sort((a, b) => a.rank - b.rank);

  const topVotes = Math.max(...books.map(b => parseInt(b.votes)));

  el.innerHTML = books.map(b => `
    <div class="book-card ${parseInt(b.votes) === topVotes ? 'winner' : ''}">
      <div class="rank">${b.rank}</div>
      <div class="book-info">
        <div class="book-title">${b.title}</div>
        <div class="book-author">${b.author}</div>
      </div>
      ${parseInt(b.votes) === topVotes ? '<span class="winner-badge">WINNER</span>' : ''}
      <div class="book-votes">
        <strong>${fmt(b.votes)}</strong> votes
      </div>
    </div>
  `).join('');
}

// ── Init ────────────────────────────────────────────────
applyFilters();
renderTabs();
render();
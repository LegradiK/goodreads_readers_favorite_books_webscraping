
const ALL_BOOKS = {{ data | tojson }};

function fmt(n) {
return parseInt(n).toLocaleString('en-GB');
}

function applyFilters() {
const genre  = document.getElementById('filter-genre').value;
const year   = document.getElementById('filter-year').value;
const sortBy = document.getElementById('sort-by').value;

let books = [...ALL_BOOKS];

if (genre) books = books.filter(b => b.genre === genre);
if (year)  books = books.filter(b => String(b.year) === year);

if (sortBy === 'votes')  books.sort((a, b) => parseInt(b.votes) - parseInt(a.votes));
if (sortBy === 'title')  books.sort((a, b) => a.title.localeCompare(b.title));
if (sortBy === 'author') books.sort((a, b) => a.author.localeCompare(b.author));
if (sortBy === 'year')   books.sort((a, b) => b.year - a.year);
if (sortBy === 'rank')   books.sort((a, b) => a.rank - b.rank);

const tbody = document.getElementById('table-body');
document.getElementById('results-count').textContent = `${books.length} books`;

if (!books.length) {
    tbody.innerHTML = `<tr><td colspan="6" class="no-results">No results found.</td></tr>`;
    return;
}

tbody.innerHTML = books.map(b => `
    <tr>
    <td class="rank-col">${b.rank}</td>
    <td class="title-col">${b.title}</td>
    <td class="author-col">${b.author}</td>
    <td><span class="genre-pill">${b.genre}</span></td>
    <td class="year-col">${b.year}</td>
    <td class="votes-col">${fmt(b.votes)}</td>
    </tr>
`).join('');
}

applyFilters();

let active = Object.keys(DATA)[0];
 
function fmt(n) { return n.toLocaleString('en-GB'); }
 
function renderTabs() {
  const el = document.getElementById('tabs');
  el.innerHTML = Object.keys(DATA).map(g => `
    <button class="tab ${g === active ? 'active' : ''}" onclick="active='${g}';renderTabs();render()">${g}</button>
  `).join('');
}
 
function render() {
  const books = [...(DATA[active] || [])];
  const sort  = document.getElementById('sort').value;
  const el    = document.getElementById('list');
 
  if (!books.length) {
    el.innerHTML = `<p class="empty">No data for ${active} yet.<br>Run your scraper to add books here.</p>`;
    return;
  }
 
  if (sort === 'votes')  books.sort((a, b) => b.votes - a.votes);
  if (sort === 'title')  books.sort((a, b) => a.title.localeCompare(b.title));
  if (sort === 'author') books.sort((a, b) => a.author.localeCompare(b.author));
  if (sort === 'rank')   books.sort((a, b) => a.rank - b.rank);
 
  const topVotes = Math.max(...books.map(b => b.votes));
 
  el.innerHTML = books.map(b => `
    <div class="book-card ${b.votes === topVotes ? 'winner' : ''}">
      <div class="rank">${b.rank}</div>
      <div class="book-info">
        <div class="book-title">${b.title}</div>
        <div class="book-author">${b.author}</div>
      </div>
      ${b.votes === topVotes ? '<span class="winner-badge">WINNER</span>' : ''}
      <div class="book-votes">
        <strong>${fmt(b.votes)}</strong>
        votes
      </div>
    </div>
  `).join('');
}
 
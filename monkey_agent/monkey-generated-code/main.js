// Simple Todo App logic with accessibility and states

const form = document.getElementById('todo-form');
const input = document.getElementById('todo-input');
const list = document.getElementById('todo-list');
const countEl = document.getElementById('todo-count');
const clearBtn = document.getElementById('clear-completed');
const filterAll = document.querySelector('[data-filter="all"]');
const filterActive = document.querySelector('[data-filter="active"]');
const filterCompleted = document.querySelector('[data-filter="completed"]');
const addBtn = document.querySelector('[data-id="add-todo"]');

let todos = [];
let filter = 'all';

function render() {
  // clear list
  list.innerHTML = '';
  const filtered = todos.filter(t => {
    if (filter === 'all') return true;
    if (filter === 'active') return !t.completed;
    if (filter === 'completed') return t.completed;
  });
  for (const t of filtered) {
    const li = document.createElement('li');
    li.className = 'todo-item' + (t.completed ? ' completed' : '') + (t.editing ? ' edit-mode' : '');
    // container with grid: checkbox, text or edit, actions
    li.innerHTML = `
      <input type="checkbox" class="todo-checkbox" ${t.completed ? 'checked' : ''} aria-label="Toggle completed" data-id="chk"/>
      <span class="todo-text">${escapeHtml(t.text)}</span>
      <span class="todo-edit" aria-label="Edit todo">
        <input type="text" value="${escapeHtml(t.text)}" data-id="edit-input" />
        <button data-id="edit-submit">Save</button>
      </span>
      <span class="todo-actions">
        <button class="edit-btn" data-id="edit">Edit</button>
        <button class="delete-btn" data-id="delete">Delete</button>
      </span>
    `;
    // events
    const checkbox = li.querySelector('.todo-checkbox');
    checkbox.addEventListener('change', () => {
      t.completed = checkbox.checked;
      updateCounts();
      render();
    });
    const editBtn = li.querySelector('[data-id="edit"]');
    const editInputWrap = li.querySelector('.todo-edit');
    const editInput = li.querySelector('[data-id="edit-input"]');
    const editSubmit = li.querySelector('[data-id="edit-submit"]');
    const textEl = li.querySelector('.todo-text');
    editBtn.addEventListener('click', () => {
      // enter edit mode for this item
      t.editing = true;
      render();
      // focus the edit input after re-render
      setTimeout(() => {
        const newInput = list.querySelector('[data-id="edit-input"]');
        if (newInput) { newInput.focus(); newInput.select(); }
      }, 0);
    });
    editSubmit.addEventListener('click', () => {
      const newText = editInput.value.trim();
      if (newText) {
        t.text = newText;
      }
      t.editing = false;
      render();
    });
    editInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        editSubmit.click();
      } else if (e.key === 'Escape') {
        t.editing = false;
        render();
      }
    });
    const deleteBtn = li.querySelector('[data-id="delete"]');
    deleteBtn.addEventListener('click', () => {
      todos = todos.filter(x => x !== t);
      updateCounts();
      render();
    });
    list.appendChild(li);
  }
  // Update counters and controls
  updateCounts();
  // Update filter button states
  [filterAll, filterActive, filterCompleted].forEach(btn => {
    const isActive = btn.getAttribute('data-filter') === filter;
    btn.setAttribute('aria-pressed', String(isActive));
    btn.classList.toggle('active', isActive);
  });
  // Clear button state
  clearBtn.disabled = todos.filter(t => t.completed).length === 0;
}

function updateCounts() {
  const remaining = todos.filter(t => !t.completed).length;
  countEl.textContent = `${remaining} item${remaining === 1 ? '' : 's'} left`;
}

function escapeHtml(text) {
  const map = { '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":"&#039;" };
  return String(text).replace(/[&<>"']/g, (c) => map[c]);
}

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const val = input.value.trim();
  if (!val) return;
  todos.push({ text: val, completed: false, editing: false });
  input.value = '';
  render();
  // reset add button state
  addBtn.disabled = true;
});

clearBtn.addEventListener('click', () => {
  const hadCompleted = todos.some(t => t.completed);
  if (!hadCompleted) return;
  todos = todos.filter(t => !t.completed);
  render();
});

function applyInitialSeed() {
  // seed with a few items for demonstration
  todos = [
    { text: 'Buy groceries', completed: false, editing: false },
    { text: 'Walk the dog', completed: true, editing: false },
    { text: 'Read a book', completed: false, editing: false }
  ];
  render();
}

// Initialize
applyInitialSeed();

// Keyboard: focus management for accessibility
document.addEventListener('keydown', (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
    input.focus();
  }
});

// Input state for add button (disabled when empty)
input.addEventListener('input', () => {
  addBtn.disabled = input.value.trim().length === 0;
});
addBtn.disabled = true;

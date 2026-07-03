document.addEventListener('DOMContentLoaded', () => {
    const newTodoInput = document.getElementById('new-todo');
    const todoList = document.getElementById('todo-list');
    const todoCount = document.getElementById('todo-count');

    let todos = [];

    function updateTodoCount() {
        todoCount.textContent = `${todos.length} items left`;
    }

    function addTodoItem(todo) {
        const li = document.createElement('li');
        li.textContent = todo;
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.addEventListener('click', () => {
            todos = todos.filter(t => t !== todo);
            todoList.removeChild(li);
            updateTodoCount();
        });
        li.appendChild(deleteButton);
        todoList.appendChild(li);
    }

    newTodoInput.addEventListener('keypress', event => {
        if (event.key === 'Enter') {
            const todoText = newTodoInput.value.trim();
            if (todoText !== '') {
                todos.push(todoText);
                addTodoItem(todoText);
                newTodoInput.value = '';
                updateTodoCount();
            }
        }
    });

    updateTodoCount();
});

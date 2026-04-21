window.onload = function() {
  document.querySelector('button').addEventListener('click', addTask);
  function addTask() {
    const taskInput = document.getElementById('taskInput');
    const taskText = taskInput.value.trim();
    if (taskText === '') return;
    const li = document.createElement('li');
    li.textContent = taskText;
    const removeBtn = document.createElement('button');   
    removeBtn.textContent = 'Remove';
    removeBtn.className = 'remove-btn';
    removeBtn.onclick = () => li.remove();
    li.appendChild(removeBtn);
    document.getElementById('taskList').appendChild(li);  
    taskInput.value = '';
  }
}
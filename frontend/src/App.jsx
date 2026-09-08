import { useEffect, useState } from 'react'
import { getTasks, createTask, updateTask, deleteTask } from './api'

function App() {
  const [tasks, setTasks] = useState([])
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Load tasks once when the component first mounts.
  useEffect(() => {
    loadTasks()
  }, [])

  async function loadTasks() {
    try {
      setLoading(true)
      const response = await getTasks()
      setTasks(response.data)
      setError(null)
    } catch (err) {
      setError('Could not load tasks. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  async function handleCreate(e) {
    e.preventDefault()
    if (!title.trim()) return
    try {
      await createTask({ title, description })
      setTitle('')
      setDescription('')
      loadTasks()
    } catch (err) {
      setError('Could not create task.')
    }
  }

  async function handleToggleComplete(task) {
    try {
      await updateTask(task.id, { completed: !task.completed })
      loadTasks()
    } catch (err) {
      setError('Could not update task.')
    }
  }

  async function handleDelete(id) {
    try {
      await deleteTask(id)
      loadTasks()
    } catch (err) {
      setError('Could not delete task.')
    }
  }

  return (
    <div className="container">
      <h1>Task Manager</h1>

      <form onSubmit={handleCreate} className="task-form">
        <input
          type="text"
          placeholder="Task title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <input
          type="text"
          placeholder="Description (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <button type="submit">Add Task</button>
      </form>

      {error && <p className="error">{error}</p>}
      {loading ? (
        <p>Loading tasks...</p>
      ) : (
        <ul className="task-list">
          {tasks.map((task) => (
            <li key={task.id} className={task.completed ? 'completed' : ''}>
              <div>
                <strong>{task.title}</strong>
                {task.description && <p>{task.description}</p>}
              </div>
              <div className="task-actions">
                <button onClick={() => handleToggleComplete(task)}>
                  {task.completed ? 'Undo' : 'Complete'}
                </button>
                <button onClick={() => handleDelete(task.id)}>Delete</button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default App

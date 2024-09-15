import { useState, useEffect } from 'react'
import { Dialog, DialogContent, DialogTrigger } from '@radix-ui/react-dialog'
import { Checkbox } from '@radix-ui/react-checkbox'
import { CheckIcon, PlusIcon, MagnifyingGlassIcon, TrashIcon } from '@radix-ui/react-icons'
import { openDB } from 'idb'

const dbPromise = openDB('TodoDB', 1, {
  upgrade(db) {
    db.createObjectStore('todos', { keyPath: 'id', autoIncrement: true })
  },
})

export default function App() {
  const [todos, setTodos] = useState([])
  const [newTodo, setNewTodo] = useState('')
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    loadTodos()
  }, [])

  async function loadTodos() {
    const db = await dbPromise
    const tx = db.transaction('todos', 'readonly')
    const store = tx.objectStore('todos')
    const items = await store.getAll()
    setTodos(items)
  }

  async function addTodo(e) {
    e.preventDefault()
    if (!newTodo.trim()) return
    const db = await dbPromise
    const tx = db.transaction('todos', 'readwrite')
    const store = tx.objectStore('todos')
    await store.add({ text: newTodo, completed: false })
    setNewTodo('')
    loadTodos()
  }

  async function toggleTodo(id) {
    const db = await dbPromise
    const tx = db.transaction('todos', 'readwrite')
    const store = tx.objectStore('todos')
    const todo = await store.get(id)
    await store.put({ ...todo, completed: !todo.completed })
    loadTodos()
  }

  async function deleteTodo(id) {
    const db = await dbPromise
    const tx = db.transaction('todos', 'readwrite')
    const store = tx.objectStore('todos')
    await store.delete(id)
    loadTodos()
  }

  const filteredTodos = todos.filter(todo =>
    todo.text.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-xl">
      <h1 className="text-3xl font-bold mb-6">TodoMaster</h1>
      <form onSubmit={addTodo} className="flex mb-4">
        <input
          type="text"
          value={newTodo}
          onChange={(e) => setNewTodo(e.target.value)}
          placeholder="Add new todo"
          className="flex-grow p-2 border rounded-l"
        />
        <button type="submit" className="bg-blue-500 text-white p-2 rounded-r">
          <PlusIcon />
        </button>
      </form>
      <div className="flex mb-4">
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search todos"
          className="flex-grow p-2 border rounded-l"
        />
        <button className="bg-gray-200 p-2 rounded-r">
          <MagnifyingGlassIcon />
        </button>
      </div>
      <ul>
        {filteredTodos.map((todo) => (
          <li key={todo.id} className="flex items-center mb-2">
            <Checkbox
              checked={todo.completed}
              onCheckedChange={() => toggleTodo(todo.id)}
              className="mr-2 w-5 h-5 border rounded"
            >
              {todo.completed && <CheckIcon />}
            </Checkbox>
            <span className={todo.completed ? 'line-through' : ''}>{todo.text}</span>
            <button onClick={() => deleteTodo(todo.id)} className="ml-auto text-red-500">
              <TrashIcon />
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}
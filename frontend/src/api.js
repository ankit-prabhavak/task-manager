/**
 * api.js
 * ------
 * Single place that knows the backend's base URL and exposes
 * functions for each API call. Every component imports from here
 * instead of hardcoding URLs, so the base URL only ever lives
 * in ONE place (this file, which reads it from an env variable).
 */

import axios from 'axios'

// Vite exposes env variables prefixed with VITE_ via import.meta.env.
// This comes from .env (local dev) or from build-time env vars (Docker).
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
})

export const getTasks = () => api.get('/api/tasks')
export const createTask = (task) => api.post('/api/tasks', task)
export const updateTask = (id, updates) => api.put(`/api/tasks/${id}`, updates)
export const deleteTask = (id) => api.delete(`/api/tasks/${id}`)

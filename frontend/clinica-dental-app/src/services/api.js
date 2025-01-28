import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:5000/api", // Cambia si usas otro puerto o dominio
  headers: {
    "Content-Type": "application/json",
  },
});

// Agregar el token JWT automáticamente si existe
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
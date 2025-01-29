// src/components/RegisterForm.js
"use client";
import React, { useState } from "react";
import { registrarUsuario, iniciarSesion } from "../data/database";

export default function RegisterForm({ onClose }) {
  const [formData, setFormData] = useState({
    nombre_usuario: "",
    password: "", // Campo de contraseña
    nombre: "",
    apellido: "",
    correo_electronico: "",
    telefono: "",
    fecha_nacimiento: "",
    direccion: "",
    rol: { id_rol: 3, nombre_rol: "paciente" }
  });

  const [mensaje, setMensaje] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRegister = () => {
    if (!formData.password) {
      setMensaje("Debe ingresar una contraseña.");
      return;
    }
    
    const nuevoUsuario = registrarUsuario(formData);
    if (nuevoUsuario) {
      iniciarSesion(nuevoUsuario.nombre_usuario, nuevoUsuario.password); // Simulación de autologin
      setMensaje("Registro exitoso. Redirigiendo...");
      setTimeout(() => {
        window.location.href = "/dashboard";
      }, 1000);
    }
  };

  return (
    <div className="modal">
      <div className="register-form">
        <h2>Registro</h2>
        <input type="text" name="nombre_usuario" placeholder="Usuario" onChange={handleChange} />
        <input type="password" name="password" placeholder="Contraseña" onChange={handleChange} />
        <input type="text" name="nombre" placeholder="Nombre" onChange={handleChange} />
        <input type="text" name="apellido" placeholder="Apellido" onChange={handleChange} />
        <input type="email" name="correo_electronico" placeholder="Correo" onChange={handleChange} />
        <input type="text" name="telefono" placeholder="Teléfono" onChange={handleChange} />
        <input type="date" name="fecha_nacimiento" onChange={handleChange} />
        <input type="text" name="direccion" placeholder="Dirección" onChange={handleChange} />
        <button onClick={handleRegister}>Registrar</button>
        <button onClick={onClose}>Cerrar</button>
        {mensaje && <p>{mensaje}</p>}
      </div>
    </div>
  );
}

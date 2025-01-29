
"use client";
import React, { useState } from "react";
import { iniciarSesion } from "../data/database";

export default function LoginForm({ onClose }) {
  const [nombreUsuario, setNombreUsuario] = useState("");
  const [password, setPassword] = useState("");
  const [mensaje, setMensaje] = useState("");

  const handleLogin = () => {
    const usuario = iniciarSesion(nombreUsuario, password);
    if (usuario) {
      setMensaje("Inicio de sesión exitoso");
      setTimeout(() => {
        window.location.href = "/dashboard";
      }, 1000);
    } else {
      setMensaje("Usuario o contraseña incorrectos");
    }
  };

  return (
    <div className="modal">
      <div className="login-form">
        <h2>Iniciar Sesión</h2>
        <input
          type="text"
          placeholder="Nombre de usuario"
          value={nombreUsuario}
          onChange={(e) => setNombreUsuario(e.target.value)}
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleLogin}>Iniciar Sesión</button>
        <button onClick={onClose}>Cerrar</button>
        {mensaje && <p>{mensaje}</p>}
      </div>
    </div>
  );
}
"use client";
import { useState } from "react";
import Navbar from "../components/Navbar";
import LoginForm from "../components/LoginForm";
import UserDashboard from "../components/UserDashboard";
import { loginUsuario } from "../data/database"; // Simulación de login
import Header from "../components/Header";
import Footer from "../components/Footer";

const Page = () => {
  const [usuarioActual, setUsuarioActual] = useState(null);
  const [mostrarLogin, setMostrarLogin] = useState(false);

  const handleLogin = (nombreUsuario, contrasena) => {
    const usuario = loginUsuario(nombreUsuario, contrasena);
    if (usuario) {
      setUsuarioActual(usuario);
      setMostrarLogin(false); // Cierra el formulario de login
    } else {
      alert("Credenciales incorrectas");
    }
  };

  const handleLogout = () => {
    setUsuarioActual(null);
  };

  return (
    <div>
      <Header />
      <Navbar usuario={usuarioActual} onLogout={handleLogout} onLoginClick={() => setMostrarLogin(true)} />

      {!usuarioActual ? (
        mostrarLogin ? (
          <LoginForm onLogin={handleLogin} />
        ) : (
          <p>Bienvenido a nuestra clínica dental. Inicia sesión para acceder a tu cuenta.</p>
        )
      ) : (
        <UserDashboard usuario={usuarioActual} />
      )}

      <Footer />
    </div>
  );
};

export default Page;

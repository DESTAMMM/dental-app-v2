"use client";
import { useState } from "react";
import PatientNavbar from "./navbars/PatientNavbar";
import AdminNavbar from "./navbars/AdminNavbar";
import AssistantNavbar from "./navbars/AssistantNavbar";

const UserDashboard = ({ usuario, onLogout }) => {
  const [contenido, setContenido] = useState(null);

  // Selección de navbar según el rol
  const renderNavbar = () => {
    switch (usuario.rol.nombre_rol) {
      case "paciente":
        return <PatientNavbar setContenido={setContenido} />;
      case "admin":
        return <AdminNavbar setContenido={setContenido} />;
      case "asistant":
        return <AssistantNavbar setContenido={setContenido} />;
      default:
        return null;
    }
  };

  return (
    <div>
      <header>
        <h1>Bienvenido, {usuario.nombre}</h1>
        <button onClick={onLogout}>Cerrar Sesión</button>
      </header>

      {renderNavbar()}

      <main>
        {contenido || <p>Selecciona una opción del menú.</p>}
      </main>
    </div>
  );
};

export default UserDashboard;

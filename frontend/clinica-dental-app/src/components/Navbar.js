"use client";
import { useState } from "react";

const Navbar = ({ usuario, onLogout, onLoginClick }) => {
  return (
    <nav style={{ display: "flex", justifyContent: "space-between", padding: "10px" }}>
      <span>🦷 Clínica Dental</span>

      {!usuario ? (
        <button onClick={onLoginClick}>Iniciar Sesión</button>
      ) : (
        <button onClick={onLogout}>Cerrar Sesión</button>
      )}
    </nav>
  );
};

export default Navbar;

import Image from "next/image";
import styles from "./page.module.css";
import Disponibilidad from "./disponibilidad/disponiblidad.js";

export default function Home() {
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", marginTop: "50px" }}>
      <h1>Bienvenido a la Clínica Dental</h1>
      <p>Por favor, inicia sesión para acceder al sistema.</p>
      <a href="/login" style={{ marginTop: "20px", color: "blue", textDecoration: "underline" }}>
        Ir al Login
      </a>

      <div style={{ marginTop: "50px", width: "100%", maxWidth: "800px" }}>
        <h2>Consulta la disponibilidad de horarios</h2>
        <Disponibilidad />
      </div>
    </div>
  );
}

import Image from "next/image";
import styles from "./page.module.css";

export default function Home() {
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", marginTop: "50px" }}>
      <h1>Bienvenido a la Clínica Dental</h1>
      <p>Por favor, inicia sesión para acceder al sistema.</p>
      <a href="/login" style={{ marginTop: "20px", color: "blue", textDecoration: "underline" }}>
        Ir al Login
      </a>
    </div>
  );
}

import { useState } from "react";
import { registrarPaciente } from "../data/database";

const RegisterForm = ({ onRegister }) => {
  const [form, setForm] = useState({
    nombre_usuario: "",
    contrasena: "",
    nombre: "",
    apellido: "",
    correo: "",
    telefono: "",
    fecha_nacimiento: "",
    direccion: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleRegister = () => {
    const nuevoPaciente = registrarPaciente(form);
    onRegister(nuevoPaciente); // Inicia sesión automáticamente
  };

  return (
    <div>
      <h2>Registro de Paciente</h2>
      <input type="text" name="nombre_usuario" placeholder="Usuario" onChange={handleChange} />
      <input type="password" name="contrasena" placeholder="Contraseña" onChange={handleChange} />
      <input type="text" name="nombre" placeholder="Nombre" onChange={handleChange} />
      <input type="text" name="apellido" placeholder="Apellido" onChange={handleChange} />
      <input type="email" name="correo" placeholder="Correo" onChange={handleChange} />
      <input type="tel" name="telefono" placeholder="Teléfono" onChange={handleChange} />
      <input type="date" name="fecha_nacimiento" onChange={handleChange} />
      <input type="text" name="direccion" placeholder="Dirección" onChange={handleChange} />
      <button onClick={handleRegister}>Registrar</button>
    </div>
  );
};

export default RegisterForm;

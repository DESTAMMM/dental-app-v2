// src/database.js
export const database = {
    usuarios: [
      {
        id_usuario: 1,
        nombre_usuario: "paciente1",
        contrasena: "1234",
        nombre: "Carlos",
        apellido: "López",
        correo_electronico: "carlos@example.com",
        telefono: "123456789",
        rol: { id_rol: 3, nombre_rol: "paciente" },
      },
      {
        id_usuario: 2,
        nombre_usuario: "admin1",
        contrasena: "admin123",
        nombre: "Dra. Ana",
        apellido: "Martínez",
        correo_electronico: "ana@example.com",
        telefono: "987654321",
        rol: { id_rol: 1, nombre_rol: "admin" },
      },
      {
        id_usuario: 3,
        nombre_usuario: "asistente1",
        contrasena: "asist123",
        nombre: "Luis",
        apellido: "Gómez",
        correo_electronico: "luis@example.com",
        telefono: "567891234",
        rol: { id_rol: 2, nombre_rol: "asistant" },
      },
    ],
  
    pacientes: [
      {
        id_paciente: 1,
        usuario: 1, // ID del usuario en la lista de usuarios
        fecha_nacimiento: "1990-05-20",
        direccion: "Av. Siempre Viva 123",
      },
    ],
  
    doctores: [
      {
        id_doctor: 2,
        usuario: 2,
        especialidad: "Ortodoncia",
      },
    ],
  
    asistentes: [
      {
        id_asistente: 3,
        usuario: 3,
        fecha_contratacion: "2023-01-10",
        turno: "Mañana",
        area_especialidad: "Atención al cliente",
      },
    ],
  };
  
  // 📌 Función para iniciar sesión
  export const loginUsuario = (nombre_usuario, contrasena) => {
    const usuario = database.usuarios.find(
      (user) =>
        user.nombre_usuario === nombre_usuario && user.contrasena === contrasena
    );
  
    if (!usuario) return null;
  
    // Verificar tipo de usuario
    let tipoUsuario = "desconocido";
    let datosExtra = {};
  
    if (database.pacientes.some((p) => p.usuario === usuario.id_usuario)) {
      tipoUsuario = "paciente";
      datosExtra = database.pacientes.find((p) => p.usuario === usuario.id_usuario);
    } else if (database.doctores.some((d) => d.usuario === usuario.id_usuario)) {
      tipoUsuario = "admin";
      datosExtra = database.doctores.find((d) => d.usuario === usuario.id_usuario);
    } else if (database.asistentes.some((a) => a.usuario === usuario.id_usuario)) {
      tipoUsuario = "asistant";
      datosExtra = database.asistentes.find((a) => a.usuario === usuario.id_usuario);
    }
  
    return { usuario, tipoUsuario, datosExtra };
  };
  
  // 📌 Función para registrar pacientes
  export const registrarPaciente = (nuevoPaciente) => {
    const id_usuario = database.usuarios.length + 1;
    const id_paciente = database.pacientes.length + 1;
  
    const usuario = {
      id_usuario,
      nombre_usuario: nuevoPaciente.nombre_usuario,
      contrasena: nuevoPaciente.contrasena,
      nombre: nuevoPaciente.nombre,
      apellido: nuevoPaciente.apellido,
      correo_electronico: nuevoPaciente.correo,
      telefono: nuevoPaciente.telefono,
      rol: { id_rol: 3, nombre_rol: "paciente" },
    };
  
    const paciente = {
      id_paciente,
      usuario: id_usuario,
      fecha_nacimiento: nuevoPaciente.fecha_nacimiento,
      direccion: nuevoPaciente.direccion,
    };
  
    database.usuarios.push(usuario);
    database.pacientes.push(paciente);
  
    return { usuario, tipoUsuario: "paciente", datosExtra: paciente };
  };
  
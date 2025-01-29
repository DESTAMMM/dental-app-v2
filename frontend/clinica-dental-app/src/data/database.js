export let database = {
    usuarios: [
      {
        id_usuario: 1,
        nombre_usuario: "paciente1",
        password: "123456", // Contraseña simulada
        nombre: "Juan",
        apellido: "Pérez",
        correo_electronico: "juanperez@example.com",
        telefono: "123456789",
        rol: {
          id_rol: 3,
          nombre_rol: "paciente"
        },
        fecha_nacimiento: "1990-05-15",
        direccion: "Calle Falsa 123"
      }
    ],
    sesiones: {
      usuarioActual: null // Aquí se guarda el usuario logueado
    }
  };
  
  // Función para registrar un nuevo usuario
  export function registrarUsuario(usuario) {
    usuario.id_usuario = database.usuarios.length + 1;
    database.usuarios.push(usuario);
    return usuario;
  }
  
  // Función para iniciar sesión (verifica usuario y contraseña)
  export function iniciarSesion(nombre_usuario, password) {
    const usuario = database.usuarios.find(user => 
      user.nombre_usuario === nombre_usuario && user.password === password
    );
    if (usuario) {
      database.sesiones.usuarioActual = usuario;
      return usuario;
    }
    return null;
  }
  
  // Función para cerrar sesión
  export function cerrarSesion() {
    database.sesiones.usuarioActual = null;
  }
  
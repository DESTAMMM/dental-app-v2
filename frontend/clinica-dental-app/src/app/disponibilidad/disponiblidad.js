"use client";
import { useEffect, useState } from "react";
import api from "../../services/api";
import { useRouter } from "next/navigation";

export default function Disponibilidad() {
  const [horarios, setHorarios] = useState([]);
  const [selectedHorario, setSelectedHorario] = useState(null);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const router = useRouter();

  // Fetch horarios disponibles al cargar el componente
  useEffect(() => {
    const fetchHorarios = async () => {
      try {
        const response = await api.get("/citas/disponibilidad");
        setHorarios(response.data);
      } catch (err) {
        setError("Error al cargar los horarios disponibles");
      }
    };

    fetchHorarios();
  }, []);

  const handleAgendar = async () => {
    if (!selectedHorario) {
      setError("Por favor selecciona un horario");
      return;
    }

    try {
      const response = await api.post("/citas", {
        id_paciente: localStorage.getItem("id_paciente"), // O el método adecuado para obtener el ID del paciente
        id_doctor: selectedHorario.id_doctor,
        fecha_cita: selectedHorario.fecha,
        hora_cita: selectedHorario.hora,
        motivo_cita: "Consulta general",
      });

      setSuccess("Cita agendada exitosamente");
      setError("");
      // Redireccionar o refrescar el estado
      router.push("/dashboard");
    } catch (err) {
      setError("Error al agendar la cita");
      setSuccess("");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Disponibilidad de horarios</h1>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {success && <p style={{ color: "green" }}>{success}</p>}

      <div>
        {horarios.length > 0 ? (
          <ul>
            {horarios.map((horario) => (
              <li key={horario.id}>
                <label>
                  <input
                    type="radio"
                    name="horario"
                    value={horario.id}
                    onChange={() => setSelectedHorario(horario)}
                  />
                  {horario.fecha} - {horario.hora} con el Dr. {horario.nombre_doctor}
                </label>
              </li>
            ))}
          </ul>
        ) : (
          <p>No hay horarios disponibles</p>
        )}
      </div>

      <button onClick={handleAgendar} style={{ marginTop: "20px" }}>
        Agendar cita
      </button>
    </div>
  );
}

"use client";
import MyHistory from "../../app/patient/MyHistory";
import MyInfo from "../../app/patient/MyInfo";
import MyAppointments from "../../app/patient/MyAppointments";
import MyInvoices from "../../app/patient/MyInvoices";

const PatientNavbar = ({ setContenido }) => {
  return (
    <nav>
      <button onClick={() => setContenido(<MyHistory />)}>Mi Historial</button>
      <button onClick={() => setContenido(<MyInfo />)}>Mi Info</button>
      <button onClick={() => setContenido(<MyAppointments />)}>Mis Citas</button>
      <button onClick={() => setContenido(<MyInvoices />)}>Mis Facturas</button>
    </nav>
  );
};

export default PatientNavbar;

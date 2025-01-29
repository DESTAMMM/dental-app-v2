"use client";
import ManageHistories from "../../app/assistant/ManageHistories";
import ManageCitas from "../../app/assistant/ManageCitas";
import ManageInventory from "../../app/assistant/ManageInventory";
import ManageUsers from "../../app/assistant/ManageUsers";
import ManageInvoices from "../../app/assistant/ManageInvoices";
import MyInfo from "../../app/assistant/MyInfo";

const AssistantNavbar = ({ setContenido }) => {
  return (
    <nav>
      <button onClick={() => setContenido(<ManageHistories />)}>Gestión de Historiales</button>
      <button onClick={() => setContenido(<ManageCitas />)}>Gestión de Citas</button>
      <button onClick={() => setContenido(<ManageInventory />)}>Gestión de Inventario</button>
      <button onClick={() => setContenido(<ManageUsers />)}>Gestión de Usuarios</button>
      <button onClick={() => setContenido(<ManageInvoices />)}>Gestión de Facturas</button>
      <button onClick={() => setContenido(<MyInfo />)}>Mi Info</button>
    </nav>
  );
};

export default AssistantNavbar;

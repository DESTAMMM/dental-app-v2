"use client";
import ManageHistories from "../../app/admin/ManageHistories";
import ManageCitas from "../../app/admin/ManageCitas";
import ManageInventory from "../../app/admin/ManageInventory";
import ManageUsers from "../../app/admin/ManageUsers";
import ManageInvoices from "../../app/admin/ManageInvoices";
import MyInfo from "../../app/admin/MyInfo";

const AdminNavbar = ({ setContenido }) => {
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

export default AdminNavbar;

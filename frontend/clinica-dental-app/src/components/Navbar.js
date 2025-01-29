"use client";
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { useRouter } from "next/navigation";

const Navbar = () => {
    const { user, logout } = useContext(AuthContext);
    const router = useRouter();

    const handleLogout = () => {
        logout();
        router.push("/");
    };

    return (
        <nav className="navbar">
            <h1>Clinical Dental</h1>
            <div>
                {user ? (
                    <>
                        {user.rol.nombre_rol === "patient" && (
                            <>
                                <a href="/dashboard/patient/MyHistory">Mi Historial</a>
                                <a href="/dashboard/patient/MyInfo">Mi Info</a>
                                <a href="/dashboard/patient/MyAppointments">Mis Citas</a>
                                <a href="/dashboard/patient/MyInvoices">Mis Facturas</a>
                            </>
                        )}
                        {user.rol.nombre_rol === "admin" && (
                            <>
                                <a href="/dashboard/admin/ManageHistories">Gestión de Historias</a>
                                <a href="/dashboard/admin/ManageAppointments">Gestión de Citas</a>
                                <a href="/dashboard/admin/ManageInventory">Gestión de Inventario</a>
                                <a href="/dashboard/admin/ManageUsers">Gestión de Usuarios</a>
                                <a href="/dashboard/admin/ManageInvoices">Gestión de Facturas</a>
                            </>
                        )}
                        {user.rol.nombre_rol === "assistant" && (
                            <>
                                <a href="/dashboard/assistant/ManageHistories">Gestión de Historias</a>
                                <a href="/dashboard/assistant/ManageAppointments">Gestión de Citas</a>
                                <a href="/dashboard/assistant/ManageInventory">Gestión de Inventario</a>
                            </>
                        )}
                        <button onClick={handleLogout}>Cerrar Sesión</button>
                    </>
                ) : (
                    <a href="/login">Iniciar Sesión</a>
                )}
            </div>
        </nav>
    );
};

export default Navbar;
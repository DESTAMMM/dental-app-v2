"use client"; // Habilita hooks

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Dashboard() {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login"); // Redirige al login si no hay token
    }
  }, []);

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Bienvenido al sistema de la clínica dental.</p>
    </div>
  );
}
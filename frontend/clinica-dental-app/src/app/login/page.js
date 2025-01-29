"use client";

import { useState } from "react";
import LoginForm from "../../components/LoginForm";
import RegisterForm from "../../components/RegisterForm";

export default function LoginPage() {
  const [isRegister, setIsRegister] = useState(false);

  return (
    <div className="auth-container">
      <div className="overlay"></div>
      <div className="auth-box">
        {isRegister ? <RegisterForm /> : <LoginForm />}
        <button onClick={() => setIsRegister(!isRegister)}>
          {isRegister ? "Ya tengo una cuenta" : "Crear cuenta"}
        </button>
      </div>
    </div>
  );
}
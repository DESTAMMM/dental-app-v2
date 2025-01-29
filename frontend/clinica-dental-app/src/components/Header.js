import Link from "next/link";

export default function Header() {
  return (
    <header className="header">
      <h1>Clinical Dental</h1>
      <nav>
        <Link href="/login">
          <button>Iniciar Sesión</button>
        </Link>
      </nav>
    </header>
  );
}
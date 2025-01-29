import Header from "../components/Header";
import Footer from "../components/Footer";

export default function HomePage() {
  return (
    <div className="home">
      <Header />
      <div className="content">
        <p>Bienvenido a Clinical Dental - Tu sonrisa, nuestra prioridad.</p>
      </div>
      <Footer />
    </div>
  );
}
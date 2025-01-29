export default function RootLayout({ children }) {
  return (
    <html lang="es">
      <body>
        <div className="container">
          {children}
        </div>
      </body>
    </html>
  );
}

import React from 'react';

function Footer() {
  return (
    <footer className="bg-brand-gray-light text-center py-5 mt-12 border-t border-gray-300">
      <p className="text-sm text-brand-gray-dark">
        © {new Date().getFullYear()} CondoMate. Todos los derechos reservados.
      </p>
    </footer>
  );
}

export default Footer;

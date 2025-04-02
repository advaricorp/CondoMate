import React from 'react';

function Documents() {
  // Placeholder data - replace with API call
  const docs = [
    { id: 1, filename: 'Acta Asamblea Julio 2024.pdf', url: '#' },
    { id: 2, filename: 'Reglamento Interno Actualizado.pdf', url: '#' },
  ];

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4 text-gray-700">Documentos</h1>
      <p className="mb-4 text-gray-600">Actas de asamblea, reglamentos y otros documentos importantes.</p>
      <ul className="bg-white shadow rounded p-4 space-y-3">
        {docs.map(doc => (
          <li key={doc.id} className="border-b pb-2 flex justify-between items-center">
            <span className="text-gray-800">{doc.filename}</span>
            <a 
              href={doc.url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-blue-600 hover:text-blue-800 hover:underline text-sm"
            >
              Descargar
            </a>
          </li>
        ))}
      </ul>
      {/* Add upload functionality for admins later */}
    </div>
  );
}

export default Documents;

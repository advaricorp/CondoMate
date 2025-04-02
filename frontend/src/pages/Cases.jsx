import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

const Cases = () => {
  const { user } = useAuth();
  const [newCase, setNewCase] = useState({
    title: '',
    description: '',
    category: 'mantenimiento',
    priority: 'media'
  });
  const [cases, setCases] = useState([
    {
      id: 1,
      title: 'Problema con el elevador',
      description: 'El elevador del piso 5 está haciendo ruidos extraños y se mueve de manera irregular.',
      category: 'mantenimiento',
      priority: 'alta',
      status: 'en_progreso',
      createdAt: '2024-03-15',
      updatedAt: '2024-03-15',
      responses: [
        {
          id: 1,
          user: 'Administración',
          message: 'Hemos programado una revisión técnica para mañana a las 10:00 AM.',
          createdAt: '2024-03-15'
        }
      ]
    },
    {
      id: 2,
      title: 'Solicitud de área social',
      description: 'Quisiera reservar el salón social para una reunión familiar el próximo sábado.',
      category: 'reservas',
      priority: 'baja',
      status: 'pendiente',
      createdAt: '2024-03-14',
      updatedAt: '2024-03-14'
    }
  ]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const newCaseObj = {
      ...newCase,
      id: cases.length + 1,
      status: 'pendiente',
      createdAt: new Date().toISOString().split('T')[0],
      updatedAt: new Date().toISOString().split('T')[0],
      responses: []
    };
    setCases([newCaseObj, ...cases]);
    setNewCase({
      title: '',
      description: '',
      category: 'mantenimiento',
      priority: 'media'
    });
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'pendiente':
        return 'bg-yellow-100 text-yellow-800';
      case 'en_progreso':
        return 'bg-blue-100 text-blue-800';
      case 'resuelto':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'alta':
        return 'bg-red-100 text-red-800';
      case 'media':
        return 'bg-yellow-100 text-yellow-800';
      case 'baja':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Mis Casos</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">Casos Activos</h2>
            <div className="space-y-4">
              {cases.map((caseItem) => (
                <div key={caseItem.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="text-lg font-medium text-gray-800">{caseItem.title}</h3>
                    <div className="flex space-x-2">
                      <span className={`px-2 py-1 rounded-full text-xs ${getStatusColor(caseItem.status)}`}>
                        {caseItem.status.replace('_', ' ')}
                      </span>
                      <span className={`px-2 py-1 rounded-full text-xs ${getPriorityColor(caseItem.priority)}`}>
                        {caseItem.priority}
                      </span>
                    </div>
                  </div>
                  <p className="text-gray-600 mb-2">{caseItem.description}</p>
                  <div className="text-sm text-gray-500 mb-2">
                    Creado: {caseItem.createdAt}
                  </div>
                  {caseItem.responses && caseItem.responses.length > 0 && (
                    <div className="mt-2">
                      <h4 className="font-medium text-gray-700 mb-1">Respuestas:</h4>
                      {caseItem.responses.map((response) => (
                        <div key={response.id} className="bg-gray-50 p-2 rounded mb-1">
                          <div className="flex justify-between text-sm">
                            <span className="font-medium">{response.user}</span>
                            <span className="text-gray-500">{response.createdAt}</span>
                          </div>
                          <p className="text-gray-600">{response.message}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">Nuevo Caso</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Título</label>
              <input
                type="text"
                value={newCase.title}
                onChange={(e) => setNewCase({ ...newCase, title: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Descripción</label>
              <textarea
                value={newCase.description}
                onChange={(e) => setNewCase({ ...newCase, description: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                rows="4"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Categoría</label>
              <select
                value={newCase.category}
                onChange={(e) => setNewCase({ ...newCase, category: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              >
                <option value="mantenimiento">Mantenimiento</option>
                <option value="reservas">Reservas</option>
                <option value="seguridad">Seguridad</option>
                <option value="otro">Otro</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Prioridad</label>
              <select
                value={newCase.priority}
                onChange={(e) => setNewCase({ ...newCase, priority: e.target.value })}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              >
                <option value="baja">Baja</option>
                <option value="media">Media</option>
                <option value="alta">Alta</option>
              </select>
            </div>
            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              Crear Caso
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Cases; 
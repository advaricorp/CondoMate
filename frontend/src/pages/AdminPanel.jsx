import React, { useState, useEffect } from 'react';
import apiClient from '../apiClient';
import { useAuth } from '../contexts/AuthContext';

const AdminPanel = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('casos');
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
      tenant: 'Juan Pérez',
      apartment: '501',
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
      updatedAt: '2024-03-14',
      tenant: 'María González',
      apartment: '302'
    }
  ]);

  const [newResponse, setNewResponse] = useState('');

  const handleStatusChange = (caseId, newStatus) => {
    setCases(cases.map(c => 
      c.id === caseId 
        ? { ...c, status: newStatus, updatedAt: new Date().toISOString().split('T')[0] }
        : c
    ));
  };

  const handleResponseSubmit = (caseId) => {
    if (!newResponse.trim()) return;
    
    const response = {
      id: Date.now(),
      user: 'Administración',
      message: newResponse,
      createdAt: new Date().toISOString().split('T')[0]
    };

    setCases(cases.map(c => 
      c.id === caseId 
        ? { 
            ...c, 
            responses: [...(c.responses || []), response],
            updatedAt: new Date().toISOString().split('T')[0]
          }
        : c
    ));
    setNewResponse('');
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
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Panel de Administración</h1>

      <div className="mb-6">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => setActiveTab('casos')}
              className={`${
                activeTab === 'casos'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
            >
              Gestión de Casos
            </button>
            <button
              onClick={() => setActiveTab('analisis')}
              className={`${
                activeTab === 'analisis'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
            >
              Análisis de Sentimiento
            </button>
          </nav>
        </div>
      </div>

      {activeTab === 'casos' && (
        <div className="space-y-6">
          {cases.map((caseItem) => (
            <div key={caseItem.id} className="bg-white rounded-lg shadow-md p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-medium text-gray-800">{caseItem.title}</h3>
                  <p className="text-sm text-gray-500">
                    Por: {caseItem.tenant} (Apto. {caseItem.apartment})
                  </p>
                </div>
                <div className="flex space-x-2">
                  <select
                    value={caseItem.status}
                    onChange={(e) => handleStatusChange(caseItem.id, e.target.value)}
                    className={`rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-sm ${
                      getStatusColor(caseItem.status)
                    }`}
                  >
                    <option value="pendiente">Pendiente</option>
                    <option value="en_progreso">En Progreso</option>
                    <option value="resuelto">Resuelto</option>
                  </select>
                  <span className={`px-2 py-1 rounded-full text-xs ${getPriorityColor(caseItem.priority)}`}>
                    {caseItem.priority}
                  </span>
                </div>
              </div>
              
              <p className="text-gray-600 mb-4">{caseItem.description}</p>
              
              <div className="text-sm text-gray-500 mb-4">
                Creado: {caseItem.createdAt} | Última actualización: {caseItem.updatedAt}
              </div>

              {caseItem.responses && caseItem.responses.length > 0 && (
                <div className="mb-4">
                  <h4 className="font-medium text-gray-700 mb-2">Respuestas:</h4>
                  {caseItem.responses.map((response) => (
                    <div key={response.id} className="bg-gray-50 p-3 rounded-lg mb-2">
                      <div className="flex justify-between text-sm mb-1">
                        <span className="font-medium">{response.user}</span>
                        <span className="text-gray-500">{response.createdAt}</span>
                      </div>
                      <p className="text-gray-600">{response.message}</p>
                    </div>
                  ))}
                </div>
              )}

              <div className="mt-4">
                <textarea
                  value={newResponse}
                  onChange={(e) => setNewResponse(e.target.value)}
                  placeholder="Escribe tu respuesta..."
                  className="w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  rows="3"
                />
                <button
                  onClick={() => handleResponseSubmit(caseItem.id)}
                  className="mt-2 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                >
                  Enviar Respuesta
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'analisis' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">Conversaciones Recientes</h2>
            {/* Add sentiment analysis content here */}
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminPanel;

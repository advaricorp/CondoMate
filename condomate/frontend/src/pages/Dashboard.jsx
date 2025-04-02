import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { FaMoneyBill, FaCalendar, FaFileAlt, FaBell } from 'react-icons/fa';

const Dashboard = () => {
  const { user } = useAuth();

  const summaryCards = [
    { title: 'Pagos Pendientes', value: '3', icon: <FaMoneyBill className="text-red-500" />, color: 'bg-red-100' },
    { title: 'Próximos Eventos', value: '2', icon: <FaCalendar className="text-blue-500" />, color: 'bg-blue-100' },
    { title: 'Documentos Nuevos', value: '5', icon: <FaFileAlt className="text-green-500" />, color: 'bg-green-100' },
    { title: 'Notificaciones', value: '4', icon: <FaBell className="text-yellow-500" />, color: 'bg-yellow-100' },
  ];

  const recentActivity = [
    { date: '2024-04-01', type: 'payment', description: 'Pago de mantenimiento recibido', amount: '$150.00' },
    { date: '2024-03-31', type: 'document', description: 'Nuevo reglamento publicado', amount: null },
    { date: '2024-03-30', type: 'event', description: 'Reunión de propietarios programada', amount: null },
    { date: '2024-03-29', type: 'payment', description: 'Pago de servicios pendiente', amount: '$75.00' },
  ];

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Bienvenido, {user?.full_name}</h1>
      
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {summaryCards.map((card, index) => (
          <div key={index} className={`${card.color} p-6 rounded-lg shadow-sm`}>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm">{card.title}</p>
                <p className="text-2xl font-bold mt-2">{card.value}</p>
              </div>
              <div className="text-2xl">{card.icon}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-xl font-semibold mb-4">Actividad Reciente</h2>
        <div className="divide-y">
          {recentActivity.map((activity, index) => (
            <div key={index} className="py-4 flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">{activity.date}</p>
                <p className="font-medium">{activity.description}</p>
              </div>
              {activity.amount && (
                <span className="text-green-600 font-medium">{activity.amount}</span>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

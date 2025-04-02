import React, { useState } from 'react';
import { FaCalendarPlus, FaUsers, FaTools, FaSwimmingPool } from 'react-icons/fa';

const Calendar = () => {
  const [selectedMonth] = useState('Abril 2024');

  const events = [
    {
      date: '2024-04-05',
      title: 'Asamblea General',
      type: 'meeting',
      description: 'Reunión anual de propietarios',
      time: '18:00',
      location: 'Salón Comunal',
      icon: <FaUsers className="text-blue-500" />
    },
    {
      date: '2024-04-10',
      title: 'Mantenimiento Piscina',
      type: 'maintenance',
      description: 'Limpieza y mantenimiento general',
      time: '09:00',
      location: 'Área de Piscina',
      icon: <FaSwimmingPool className="text-green-500" />
    },
    {
      date: '2024-04-15',
      title: 'Reparación Ascensores',
      type: 'maintenance',
      description: 'Mantenimiento preventivo',
      time: '10:00',
      location: 'Torre Principal',
      icon: <FaTools className="text-yellow-500" />
    }
  ];

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Calendario de Eventos</h1>
        <button className="bg-blue-500 text-white px-4 py-2 rounded-lg flex items-center gap-2">
          <FaCalendarPlus />
          Nuevo Evento
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">{selectedMonth}</h2>
        {/* Calendar grid would go here - simplified for mock */}
        <div className="grid grid-cols-7 gap-2 mb-4 text-center">
          {['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'].map(day => (
            <div key={day} className="font-medium text-gray-600 p-2">{day}</div>
          ))}
          {Array.from({ length: 35 }).map((_, i) => (
            <div key={i} className={`p-2 border rounded-lg ${i === 4 || i === 9 || i === 14 ? 'bg-blue-100 border-blue-300' : ''}`}>
              {i + 1}
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-xl font-semibold mb-4">Próximos Eventos</h2>
        <div className="space-y-4">
          {events.map((event, index) => (
            <div key={index} className="flex items-start gap-4 p-4 border rounded-lg hover:bg-gray-50">
              <div className="text-2xl">{event.icon}</div>
              <div className="flex-1">
                <h3 className="font-semibold">{event.title}</h3>
                <p className="text-sm text-gray-600">{event.description}</p>
                <div className="mt-2 flex gap-4 text-sm text-gray-600">
                  <span>📅 {event.date}</span>
                  <span>⏰ {event.time}</span>
                  <span>📍 {event.location}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Calendar;

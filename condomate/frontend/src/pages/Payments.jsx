import React, { useState } from 'react';
import { FaMoneyBill, FaFileInvoiceDollar, FaCreditCard, FaHistory } from 'react-icons/fa';

const Payments = () => {
  const [selectedTab, setSelectedTab] = useState('pending');

  const pendingPayments = [
    {
      id: 1,
      concept: 'Cuota de Mantenimiento',
      amount: 150.00,
      dueDate: '2024-04-15',
      status: 'pending'
    },
    {
      id: 2,
      concept: 'Fondo de Reserva',
      amount: 50.00,
      dueDate: '2024-04-15',
      status: 'pending'
    },
    {
      id: 3,
      concept: 'Servicios Especiales',
      amount: 75.00,
      dueDate: '2024-04-20',
      status: 'pending'
    }
  ];

  const paymentHistory = [
    {
      id: 101,
      concept: 'Cuota de Mantenimiento',
      amount: 150.00,
      date: '2024-03-15',
      status: 'completed',
      reference: 'REF-001-2024'
    },
    {
      id: 102,
      concept: 'Fondo de Reserva',
      amount: 50.00,
      date: '2024-03-15',
      status: 'completed',
      reference: 'REF-002-2024'
    },
    {
      id: 103,
      concept: 'Reparación Extraordinaria',
      amount: 100.00,
      date: '2024-03-01',
      status: 'completed',
      reference: 'REF-003-2024'
    }
  ];

  const summaryCards = [
    {
      title: 'Total Pendiente',
      value: '$275.00',
      icon: <FaMoneyBill className="text-red-500" />,
      color: 'bg-red-100'
    },
    {
      title: 'Último Pago',
      value: '$150.00',
      icon: <FaFileInvoiceDollar className="text-green-500" />,
      color: 'bg-green-100'
    },
    {
      title: 'Próximo Vencimiento',
      value: '15 Abril',
      icon: <FaCreditCard className="text-blue-500" />,
      color: 'bg-blue-100'
    }
  ];

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Pagos y Facturación</h1>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
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

      {/* Tabs */}
      <div className="flex gap-4 mb-6">
        <button
          className={`px-4 py-2 rounded-lg flex items-center gap-2 ${
            selectedTab === 'pending' ? 'bg-blue-500 text-white' : 'bg-gray-100'
          }`}
          onClick={() => setSelectedTab('pending')}
        >
          <FaMoneyBill />
          Pagos Pendientes
        </button>
        <button
          className={`px-4 py-2 rounded-lg flex items-center gap-2 ${
            selectedTab === 'history' ? 'bg-blue-500 text-white' : 'bg-gray-100'
          }`}
          onClick={() => setSelectedTab('history')}
        >
          <FaHistory />
          Historial
        </button>
      </div>

      {/* Content */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        {selectedTab === 'pending' ? (
          <>
            <h2 className="text-xl font-semibold mb-4">Pagos Pendientes</h2>
            <div className="space-y-4">
              {pendingPayments.map((payment) => (
                <div key={payment.id} className="border rounded-lg p-4 flex items-center justify-between hover:bg-gray-50">
                  <div>
                    <h3 className="font-semibold">{payment.concept}</h3>
                    <p className="text-sm text-gray-600">Vence: {payment.dueDate}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-lg font-bold">${payment.amount.toFixed(2)}</p>
                    <button className="mt-2 bg-blue-500 text-white px-4 py-1 rounded-lg text-sm">
                      Pagar
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </>
        ) : (
          <>
            <h2 className="text-xl font-semibold mb-4">Historial de Pagos</h2>
            <div className="space-y-4">
              {paymentHistory.map((payment) => (
                <div key={payment.id} className="border rounded-lg p-4 flex items-center justify-between hover:bg-gray-50">
                  <div>
                    <h3 className="font-semibold">{payment.concept}</h3>
                    <p className="text-sm text-gray-600">Fecha: {payment.date}</p>
                    <p className="text-sm text-gray-600">Ref: {payment.reference}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-lg font-bold">${payment.amount.toFixed(2)}</p>
                    <span className="inline-block mt-2 px-2 py-1 bg-green-100 text-green-800 rounded-lg text-sm">
                      Completado
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Payments;

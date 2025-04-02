import React from 'react';
import AIAssistant from '../components/AIAssistant';
import DocumentProcessor from '../components/DocumentProcessor';
import SentimentAnalyzer from '../components/SentimentAnalyzer';

const AIPage = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Características de IA</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">Asistente de IA</h2>
            <p className="text-gray-600 mb-4">Hazme cualquier pregunta sobre tu condominio</p>
            <AIAssistant />
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">Procesamiento de Documentos</h2>
          <DocumentProcessor />
        </div>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">Análisis de Sentimiento</h2>
          <SentimentAnalyzer />
        </div>
      </div>

      <div className="mt-8 bg-blue-50 rounded-lg p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Acerca de las Características de IA</h2>
        <div className="space-y-4">
          <p className="text-gray-600">
            Nuestras características impulsadas por IA te ayudan a gestionar tu condominio de manera más eficiente:
          </p>
          <ul className="list-disc list-inside space-y-2 text-gray-600">
            <li>
              <span className="font-medium">Asistente de IA:</span> Obtén respuestas instantáneas a tus preguntas sobre gestión de condominios, reglas y procedimientos.
            </li>
            <li>
              <span className="font-medium">Procesamiento de Documentos:</span> Extrae automáticamente información de recibos y facturas para un fácil seguimiento de gastos.
            </li>
            <li>
              <span className="font-medium">Análisis de Sentimiento:</span> Analiza comentarios y comunicaciones para entender la satisfacción de los residentes e identificar áreas de mejora.
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default AIPage; 
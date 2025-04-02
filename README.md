# CondoMate Project 🌟

A modern condominium management system with AI-powered features.

## Table of Contents / Tabla de Contenidos / Table des matières
- [Overview](#overview--descripción-general--aperçu)
- [Features](#features--características--fonctionnalités)
- [Setup](#setup--configuración--installation)
- [Development](#development--desarrollo--développement)
- [Deployment](#deployment--despliegue--déploiement)
- [Contributing](#contributing--contribución--contribution)

## Overview / Descripción General / Aperçu

CondoMate is a comprehensive condominium management platform that streamlines communication between residents and administration, manages payments, and provides AI-powered insights.

CondoMate es una plataforma integral de gestión de condominios que optimiza la comunicación entre residentes y administración, gestiona pagos y proporciona análisis potenciados por IA.

CondoMate est une plateforme complète de gestion de copropriété qui optimise la communication entre les résidents et l'administration, gère les paiements et fournit des analyses alimentées par l'IA.

## Features / Características / Fonctionnalités

### Core Features / Características Principales / Fonctionnalités Principales
- 🏠 Resident Management / Gestión de Residentes / Gestion des Résidents
- 💰 Payment Processing / Procesamiento de Pagos / Traitement des Paiements
- 📅 Event Calendar / Calendario de Eventos / Calendrier d'Événements
- 📄 Document Management / Gestión de Documentos / Gestion des Documents
- 🤖 AI-Powered Insights / Análisis con IA / Analyses avec IA

### AI Features / Características de IA / Fonctionnalités IA
- Sentiment Analysis / Análisis de Sentimiento / Analyse de Sentiment
- Smart Recommendations / Recomendaciones Inteligentes / Recommandations Intelligentes
- Automated Responses / Respuestas Automatizadas / Réponses Automatisées

## Setup / Configuración / Installation

### Prerequisites / Prerrequisitos / Prérequis
- Node.js 18+ / Python 3.8+
- MongoDB 6.0+
- Git

### Backend Setup / Configuración del Backend / Configuration du Backend

```bash
# English
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration

# Español
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edite .env con su configuración

# Français
cd backend
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Modifiez .env avec votre configuration
```

### Frontend Setup / Configuración del Frontend / Configuration du Frontend

```bash
# English
cd frontend
npm install
npm run dev

# Español
cd frontend
npm install
npm run dev

# Français
cd frontend
npm install
npm run dev
```

## Development / Desarrollo / Développement

### Running Locally / Ejecución Local / Exécution Locale

```bash
# English
# Backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 3000

# Frontend
npm run dev

# Español
# Backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 3000

# Frontend
npm run dev

# Français
# Backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 3000

# Frontend
npm run dev
```

### API Documentation / Documentación API / Documentation API
- Swagger UI: `http://localhost:3000/docs`
- OpenAPI Spec: `http://localhost:3000/openapi.json`

## Deployment / Despliegue / Déploiement

### Docker / Docker / Docker

```bash
# English
docker-compose up -d

# Español
docker-compose up -d

# Français
docker-compose up -d
```

### Environment Variables / Variables de Entorno / Variables d'Environnement

```env
# English
MONGODB_URL=your_mongodb_url
JWT_SECRET=your_jwt_secret
OPENAI_API_KEY=your_openai_key

# Español
MONGODB_URL=su_url_mongodb
JWT_SECRET=su_secreto_jwt
OPENAI_API_KEY=su_clave_openai

# Français
MONGODB_URL=votre_url_mongodb
JWT_SECRET=votre_secret_jwt
OPENAI_API_KEY=votre_cle_openai
```

## Contributing / Contribución / Contribution

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

¡Bienvenidas las contribuciones! Por favor, siga estos pasos:

1. Bifurque el repositorio
2. Cree su rama de características (`git checkout -b feature/amazing-feature`)
3. Confirme sus cambios (`git commit -m 'Add some amazing feature'`)
4. Empuje a la rama (`git push origin feature/amazing-feature`)
5. Abra una Solicitud de Extracción

Les contributions sont les bienvenues ! Veuillez suivre ces étapes :

1. Fork le dépôt
2. Créez votre branche de fonctionnalité (`git checkout -b feature/amazing-feature`)
3. Committez vos changements (`git commit -m 'Add some amazing feature'`)
4. Poussez vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrez une Pull Request

## License / Licencia / Licence

MIT License / Licencia MIT / Licence MIT

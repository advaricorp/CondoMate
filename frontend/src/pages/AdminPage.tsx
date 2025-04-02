import React, { useState } from 'react';
import { Container, Typography, Box } from '@mui/material';
import SentimentAnalysis from '../components/AdminPanel';

const AdminPage: React.FC = () => {
    const [selectedConversation, setSelectedConversation] = useState<string>('');

    return (
        <Container maxWidth="lg">
            <Box sx={{ my: 4 }}>
                <Typography variant="h4" component="h1" gutterBottom>
                    Panel de Administración
                </Typography>

                <Box sx={{ mt: 4 }}>
                    <Typography variant="h5" gutterBottom>
                        Análisis de Conversaciones
                    </Typography>
                    
                    <Box sx={{ mb: 3 }}>
                        <textarea
                            value={selectedConversation}
                            onChange={(e) => setSelectedConversation(e.target.value)}
                            placeholder="Pega una conversación para analizar..."
                            style={{ width: '100%', minHeight: '100px', padding: '10px' }}
                        />
                    </Box>

                    {selectedConversation && (
                        <SentimentAnalysis conversation={selectedConversation} />
                    )}
                </Box>
            </Box>
        </Container>
    );
};

export default AdminPage; 
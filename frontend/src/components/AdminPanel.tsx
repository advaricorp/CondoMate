import React, { useState } from 'react';
import { Box, Typography, Paper, List, ListItem, ListItemText, Divider } from '@mui/material';

interface SentimentAnalysisProps {
    conversation: string;
}

const SentimentAnalysis: React.FC<SentimentAnalysisProps> = ({ conversation }) => {
    const [analysis, setAnalysis] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    const analyzeConversation = async () => {
        try {
            setLoading(true);
            const response = await fetch('/api/v1/admin/sentiment-analysis', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ conversation })
            });

            if (!response.ok) {
                throw new Error('Error al analizar la conversación');
            }

            const data = await response.json();
            setAnalysis(data);
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
                Análisis de Sentimiento
            </Typography>
            
            <Box sx={{ mb: 2 }}>
                <Typography variant="body1" gutterBottom>
                    {conversation}
                </Typography>
            </Box>

            {loading ? (
                <Typography>Cargando análisis...</Typography>
            ) : analysis ? (
                <Box>
                    <Typography variant="subtitle1" gutterBottom>
                        Sentimiento: {analysis.sentiment} (Confianza: {analysis.confidence * 100}%)
                    </Typography>
                    
                    <Typography variant="subtitle2" gutterBottom>
                        Temas identificados:
                    </Typography>
                    <List dense>
                        {analysis.topics.map((topic: string, index: number) => (
                            <ListItem key={index}>
                                <ListItemText primary={topic} />
                            </ListItem>
                        ))}
                    </List>

                    <Typography variant="subtitle2" gutterBottom>
                        Recomendaciones:
                    </Typography>
                    <List dense>
                        {analysis.recommendations.map((rec: string, index: number) => (
                            <ListItem key={index}>
                                <ListItemText primary={rec} />
                            </ListItem>
                        ))}
                    </List>
                </Box>
            ) : (
                <button onClick={analyzeConversation}>
                    Analizar Conversación
                </button>
            )}
        </Paper>
    );
};

export default SentimentAnalysis; 
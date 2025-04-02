import React, { useState } from 'react';
import apiClient from '../apiClient';

const SentimentAnalyzer = () => {
  const [text, setText] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim()) {
      setError('Please enter some text to analyze');
      return;
    }

    setIsAnalyzing(true);
    setError(null);

    try {
      const response = await apiClient.post('/ai/analyze-sentiment', {
        text: text.trim()
      });

      setResult(response.data);
    } catch (error) {
      console.error('Error analyzing sentiment:', error);
      setError('Failed to analyze sentiment. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const getSentimentColor = (sentiment) => {
    switch (sentiment.toLowerCase()) {
      case 'positive':
        return 'text-green-600';
      case 'negative':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Sentiment Analysis</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Enter Text
          </label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Enter text to analyze sentiment..."
            rows={4}
            className="w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isAnalyzing}
          />
        </div>

        <button
          type="submit"
          disabled={isAnalyzing || !text.trim()}
          className="w-full px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
        >
          {isAnalyzing ? 'Analyzing...' : 'Analyze Sentiment'}
        </button>
      </form>

      {error && (
        <div className="mt-4 p-3 bg-red-100 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-6">
          <h3 className="text-lg font-medium text-gray-800 mb-2">Analysis Result</h3>
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-600">Sentiment</p>
                <p className={`font-medium ${getSentimentColor(result.sentiment)}`}>
                  {result.sentiment}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Positive Score</p>
                <p className="font-medium">
                  {(result.positive_score * 100).toFixed(1)}%
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Negative Score</p>
                <p className="font-medium">
                  {(result.negative_score * 100).toFixed(1)}%
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Timestamp</p>
                <p className="font-medium">
                  {new Date(result.timestamp).toLocaleString()}
                </p>
              </div>
            </div>
            {result.details && (
              <div className="mt-4">
                <p className="text-sm text-gray-600">Details</p>
                <pre className="mt-2 p-2 bg-white rounded border text-sm overflow-x-auto">
                  {JSON.stringify(result.details, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default SentimentAnalyzer; 
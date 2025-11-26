import React, { useState, useEffect } from 'react';
import axios from '../api/axiosClient';
import './AnalyzePage.css';

const AnalyzePage = () => {
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState('');
  const [question, setQuestion] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDatasets();
  }, []);

  const fetchDatasets = async () => {
    try {
      const response = await axios.get('/files/list');
      setDatasets(response.data.datasets || []);
    } catch (err) {
      console.error('Error fetching datasets:', err);
      setError('Failed to load datasets');
    }
  };

  const handleAnalyze = async () => {
    if (!selectedDataset || !question) {
      setError('Please select a dataset and enter a question');
      return;
    }

    setLoading(true);
    setError('');
    setAnalysisResult(null);

    try {
      const response = await axios.post(
        `/analyze?dataset_id=${selectedDataset}&question=${encodeURIComponent(question)}`
      );
      setAnalysisResult(response.data);
    } catch (err) {
      console.error('Error during analysis:', err);
      setError('Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="analyze-page">
      <h1>Analyze Your Data</h1>

      <div className="form-section">
        <div className="form-group">
          <label>Select Dataset:</label>
          <select
            value={selectedDataset}
            onChange={(e) => setSelectedDataset(e.target.value)}
            disabled={loading}
          >
            <option value="">-- Select a dataset --</option>
            {datasets.map((dataset) => (
              <option key={dataset._id} value={dataset._id}>
                {dataset.filename}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Ask a Question:</label>
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="e.g., What are the top 10 customers by sales?"
            disabled={loading}
          />
        </div>

        <button onClick={handleAnalyze} disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {analysisResult && (
        <div className="results-section">
          <h2>Analysis Results</h2>
          <div className="result-content">
            <p>{analysisResult.final_answer}</p>
          </div>

          <div className="debug-info" style={{ marginTop: '20px' }}>
            <details>
              <summary style={{ cursor: 'pointer', fontWeight: 'bold' }}>Debug Information</summary>
              <pre style={{ fontSize: '12px', backgroundColor: '#f9f9f9', padding: '10px', borderRadius: '4px', overflow: 'auto' }}>
                {JSON.stringify(analysisResult, null, 2)}
              </pre>
            </details>
          </div>
        </div>
      )}
    </div>
  );
};

export default AnalyzePage;

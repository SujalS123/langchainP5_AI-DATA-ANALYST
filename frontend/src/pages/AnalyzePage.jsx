import React, { useState, useEffect } from 'react';
import ChartRenderer from '../components/ChartRenderer';
import './AnalyzePage.css';

const AnalyzePage = () => {
  const [selectedDatasetId, setSelectedDatasetId] = useState('');
  const [question, setQuestion] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [datasets, setDatasets] = useState([]);
  const [fetchError, setFetchError] = useState(null);

  useEffect(() => {
    const fetchDatasets = async () => {
      try {
        const response = await fetch('/api/files/list', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const data = await response.json();
          setDatasets(data.datasets);
        } else {
          const errorData = await response.json();
          setFetchError(errorData.detail || 'Failed to fetch datasets.');
        }
      } catch (err) {
        setFetchError('Error fetching datasets: ' + err.message);
      }
    };

    fetchDatasets();
  }, []);

  const handleAnalyze = async () => {
    if (!selectedDatasetId || !question.trim()) {
      alert('Please select a dataset and enter a question.');
      return;
    }

    setLoading(true);
    setAnalysisResult(null);

    try {
      const response = await fetch(`/api/analyze/?dataset_id=${selectedDatasetId}&question=${encodeURIComponent(question.trim())}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setAnalysisResult(data);
      } else {
        const errorData = await response.json();
        alert(`Analysis failed: ${errorData.detail || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Error during analysis:', error);
      alert('Error during analysis.');
    } finally {
      setLoading(false);
    }
  };

  if (fetchError) {
    return <div className="analyze-page">Error: {fetchError}</div>;
  }

  return (
    <div className="analyze-page">
      <h1>Analyze Data</h1>
      <div className="analysis-controls">
        <div className="form-group">
          <label htmlFor="dataset-select">Select Dataset:</label>
          <select
            id="dataset-select"
            value={selectedDatasetId}
            onChange={(e) => setSelectedDatasetId(e.target.value)}
          >
            <option value="">--Please choose an option--</option>
            {datasets.map((dataset) => (
              <option key={dataset._id} value={dataset._id}>{dataset.filename}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="question-input">Ask a Question:</label>
          <textarea
            id="question-input"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="e.g., 'Show me total sales for each state in bar chart' or 'What are the top 10 customers by sales?'"
            rows={3}
            style={{ width: '100%', padding: '8px', marginTop: '4px' }}
          />
          <div style={{ marginTop: '10px', fontSize: '14px', color: '#666' }}>
            <strong>Sample questions:</strong>
            <ul style={{ margin: '5px 0', paddingLeft: '20px' }}>
              <li>"Show me total sales for each state in bar chart"</li>
              <li>"What are the top 10 customers by sales?"</li>
              <li>"Create a bar chart of profit by state"</li>
              <li>"Show me the most profitable states"</li>
              <li>"Visualize sales performance by region"</li>
              <li>"What are the columns in the dataset?"</li>
            </ul>
          </div>
        </div>

        <button onClick={handleAnalyze} disabled={loading || !selectedDatasetId || !question.trim()}>
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </div>

      {analysisResult && (
        <div className="analysis-results">
          <h2>Analysis Results</h2>
          
          {/* Display chart if available */}
          {analysisResult.chart_specification && (
            <div className="chart-container">
              <h3>Generated Chart</h3>
              <ChartRenderer 
                key={`chart-${Date.now()}-${JSON.stringify(analysisResult.chart_specification).substring(0, 50)}`}
                chartSpecification={analysisResult.chart_specification} 
              />
            </div>
          )}
          
          {/* Legacy support for old chart_image format */}
          {analysisResult.chart_image && !analysisResult.chart_specification && (
            <div className="chart-container">
              <h3>Generated Chart (Legacy Format)</h3>
              <img 
                src={analysisResult.chart_image} 
                alt="Analysis Chart" 
                style={{ maxWidth: '100%', height: 'auto', border: '1px solid #ddd', borderRadius: '4px' }}
              />
            </div>
          )}
          
          {/* Display text answer */}
          {analysisResult.final_answer && (
            <div className="text-result">
              <h3>Answer</h3>
              <pre style={{ whiteSpace: 'pre-wrap', backgroundColor: '#f4f4f4', padding: '10px', borderRadius: '4px', fontFamily: 'monospace' }}>
                {analysisResult.final_answer}
              </pre>
            </div>
          )}
          
          {/* Display error if any */}
          {analysisResult.error && (
            <div className="error-result" style={{ color: 'red', marginTop: '10px' }}>
              <h3>Error</h3>
              <p>{analysisResult.error}</p>
            </div>
          )}
          
          {/* Display raw response for debugging
          <div className="debug-info" style={{ marginTop: '20px' }}>
            <h3>Debug Information</h3>
            <pre>{JSON.stringify(analysisResult, null, 2)}</pre>
          </div> */}
        </div>
      )}
    </div>
  );
};

export default AnalyzePage;

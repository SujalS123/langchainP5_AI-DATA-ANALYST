          {/* Display raw response for debugging */}
          <div className="debug-info" style={{ marginTop: '20px' }}>
            <details>
              <summary style={{ cursor: 'pointer', fontWeight: 'bold' }}>Debug Information</summary>
              <pre style={{ fontSize: '12px', backgroundColor: '#f9f9f9', padding: '10px', borderRadius: '4px', overflow: 'auto' }}>
                {JSON.stringify(analysisResult, null, 2)}
              </pre>
            </details>
          </div>

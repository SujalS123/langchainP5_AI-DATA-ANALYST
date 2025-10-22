import React, { useState } from 'react';
import './UploadPage.css'; // Assuming a CSS file for UploadPage styling
import axiosClient from '../../api/axiosClient';

const UploadPage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setUploadStatus('');

    if (!file) {
      setSelectedFile(null);
      return;
    }

    // Validate file type - ensure it's a CSV file
    if (!file.name.toLowerCase().endsWith('.csv')) {
      setUploadStatus('Error: Please select a CSV file.');
      setSelectedFile(null);
      return;
    }

    // Validate file size (max 10MB)
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      setUploadStatus('Error: File size must be less than 10MB.');
      setSelectedFile(null);
      return;
    }

    setSelectedFile(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadStatus('Please select a CSV file first!');
      return;
    }

    setIsUploading(true);
    setUploadStatus('Uploading...');

    // Create FormData object
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      // Send POST request to the correct endpoint
      const response = await axiosClient.post('/files/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 30000, // 30 second timeout for large files
      });

      if (response.status === 200 || response.status === 201) {
        const { dataset_id, message } = response.data;
        setUploadStatus(`Upload successful! ${message || ''} Dataset ID: ${dataset_id}`);
        setSelectedFile(null);
        
        // Reset file input
        const fileInput = document.querySelector('input[type="file"]');
        if (fileInput) {
          fileInput.value = '';
        }
      } else {
        setUploadStatus('Upload failed. Please try again.');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      
      // Handle different types of errors
      if (error.response) {
        // Server responded with error status
        const errorMessage = error.response.data?.detail || 
                            error.response.data?.message || 
                            `Server error: ${error.response.status}`;
        setUploadStatus(`Error: ${errorMessage}`);
      } else if (error.request) {
        // Request was made but no response received
        setUploadStatus('Error: No response from server. Please check your connection.');
      } else if (error.code === 'ECONNABORTED') {
        // Request timeout
        setUploadStatus('Error: Upload timeout. Please try again with a smaller file.');
      } else {
        // Something else happened
        setUploadStatus('Error: Upload failed. Please try again.');
      }
    } finally {
      setIsUploading(false);
    }
  };

  const handleButtonClick = () => {
    const fileInput = document.querySelector('input[type="file"]');
    if (fileInput) {
      fileInput.click();
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="upload-page">
      <h1>Upload CSV Data</h1>
      <div className="upload-container">
        <input 
          type="file" 
          accept=".csv"
          onChange={handleFileChange}
          style={{ display: 'none' }}
          id="csv-file-input"
        />
        
        <div className="upload-section">
          <button 
            type="button"
            onClick={handleButtonClick}
            className="file-select-button"
            disabled={isUploading}
          >
            {selectedFile ? 'Change File' : 'Select CSV File'}
          </button>
          
          {selectedFile && (
            <div className="file-info">
              <p><strong>Selected file:</strong> {selectedFile.name}</p>
              <p><strong>Size:</strong> {formatFileSize(selectedFile.size)}</p>
              <p><strong>Type:</strong> {selectedFile.type || 'text/csv'}</p>
            </div>
          )}
        </div>

        <button 
          onClick={handleUpload} 
          disabled={!selectedFile || isUploading}
          className={`upload-button ${isUploading ? 'uploading' : ''}`}
        >
          {isUploading ? 'Uploading...' : 'Upload CSV'}
        </button>

        {uploadStatus && (
          <div className={`upload-status ${ 
            uploadStatus.startsWith('Error') ? 'error' : 
            uploadStatus.includes('successful') ? 'success' : 'info' 
          }`}>
            {uploadStatus}
          </div>
        )}

        <div className="upload-instructions">
          <h3>Instructions:</h3>
          <ul>
            <li>Select a CSV file from your computer</li>
            <li>File size must be less than 10MB</li>
            <li>Ensure your CSV has proper headers</li>
            <li>Click "Upload CSV" to process your data</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default UploadPage;

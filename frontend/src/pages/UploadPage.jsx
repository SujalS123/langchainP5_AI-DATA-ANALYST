import React, { useState, useRef } from 'react';
import axios from '../api/axiosClient';
import './UploadPage.css';

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
      if (!file) {
          alert('Please select a file to upload.');
          return;
      }
  
      setUploadStatus('Uploading...'); // Add loading message
  
      const formData = new FormData();
      formData.append('file', file);
  
      try {
          const response = await axios.post('/files/upload', formData, {
              headers: {
                  'Content-Type': 'multipart/form-data',
              },
          });
          setUploadStatus(`File uploaded successfully: ${response.data.filename}`);
          setSuccessMessage(`File "${response.data.filename}" uploaded successfully!`);
      } catch (error) {
          setUploadStatus(`Upload failed: ${error.message}`);
      } finally {
          setTimeout(() => {
              setUploadStatus(null); // Reset upload status after a delay
          }, 3000);
      }
  };

  const triggerFileInput = () => {
    fileInputRef.current.click();
  };

  return (
    <div className="upload-page">
      <h1>Upload CSV File</h1>
      <input
        type="file"
        accept=".csv"
        onChange={handleFileChange}
        style={{ display: 'none' }}
        ref={fileInputRef}
      />
      <button onClick={triggerFileInput}>Select File</button>
      {file && <p>Selected file: {file.name}</p>}
      <button onClick={handleUpload} disabled={!file}>Upload</button>
      {uploadStatus && <p>{uploadStatus}</p>}
      {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
    </div>
  );
};

export default UploadPage;
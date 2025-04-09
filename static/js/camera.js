// camera.js - Handle camera functionality for the scan page

let stream = null;
let capturedImage = null;

// Initialize the camera functionality
function initCamera() {
  const videoElement = document.getElementById('camera-feed');
  const captureButton = document.getElementById('capture-button');
  const retakeButton = document.getElementById('retake-button');
  const scanButton = document.getElementById('scan-button');
  const previewElement = document.getElementById('capture-preview');
  const statusElement = document.getElementById('camera-status');
  const errorContainer = document.getElementById('error-container');
  
  if (!videoElement || !captureButton || !retakeButton || !scanButton || !previewElement || !statusElement) {
    showError('Camera UI elements not found');
    return;
  }
  
  // Set initial UI state
  retakeButton.style.display = 'none';
  scanButton.style.display = 'none';
  previewElement.style.display = 'none';
  
  // Start camera
  startCamera(videoElement, statusElement);
  
  // Capture button click handler
  captureButton.addEventListener('click', () => {
    captureImage(videoElement, previewElement);
    
    // Update UI
    videoElement.style.display = 'none';
    previewElement.style.display = 'block';
    captureButton.style.display = 'none';
    retakeButton.style.display = 'block';
    scanButton.style.display = 'block';
  });
  
  // Retake button click handler
  retakeButton.addEventListener('click', () => {
    // Update UI
    videoElement.style.display = 'block';
    previewElement.style.display = 'none';
    captureButton.style.display = 'block';
    retakeButton.style.display = 'none';
    scanButton.style.display = 'none';
    capturedImage = null;
  });
  
  // Scan button click handler
  scanButton.addEventListener('click', () => {
    if (capturedImage) {
      // Set the captured image to the hidden input field
      const imageInput = document.getElementById('captured-image');
      if (imageInput) {
        imageInput.value = capturedImage;
        
        // Submit the form
        const form = document.getElementById('scan-form');
        if (form) {
          form.submit();
        } else {
          showError('Scan form not found');
        }
      } else {
        showError('Image input field not found');
      }
    } else {
      showError('No image captured');
    }
  });
}

// Start the camera stream
function startCamera(videoElement, statusElement) {
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Display loading status
    statusElement.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"></div><p>Requesting camera access...</p></div>';
    
    // Request camera access
    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
      .then(function(mediaStream) {
        stream = mediaStream;
        videoElement.srcObject = mediaStream;
        videoElement.play();
        
        // Update status
        statusElement.innerHTML = '';
      })
      .catch(function(error) {
        console.error('Error accessing the camera', error);
        statusElement.innerHTML = '<div class="alert alert-danger">Failed to access the camera: ' + error.message + '</div>';
      });
  } else {
    statusElement.innerHTML = '<div class="alert alert-danger">Your browser does not support camera access</div>';
  }
}

// Capture an image from the video feed
function captureImage(videoElement, previewElement) {
  const canvas = document.createElement('canvas');
  canvas.width = videoElement.videoWidth;
  canvas.height = videoElement.videoHeight;
  
  const ctx = canvas.getContext('2d');
  ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
  
  // Get the image as data URL
  capturedImage = canvas.toDataURL('image/jpeg');
  
  // Display the captured image
  previewElement.src = capturedImage;
}

// Stop the camera stream when leaving the page
function stopCamera() {
  if (stream) {
    const tracks = stream.getTracks();
    tracks.forEach(track => track.stop());
    stream = null;
  }
}

// Initialize when the document is loaded
document.addEventListener('DOMContentLoaded', function() {
  // Check if we're on the scan page
  if (document.getElementById('camera-feed')) {
    initCamera();
    
    // Stop camera when leaving page
    window.addEventListener('beforeunload', stopCamera);
  }
});

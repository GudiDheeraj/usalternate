// main.js - Handle general application functionality

document.addEventListener('DOMContentLoaded', function() {
  // Initialize tooltips
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Handle flash messages with auto-dismiss
  const flashMessages = document.querySelectorAll('.alert-dismissible');
  flashMessages.forEach(message => {
    // Auto-dismiss flash messages after 5 seconds
    setTimeout(() => {
      const closeButton = message.querySelector('.btn-close');
      if (closeButton) {
        closeButton.click();
      }
    }, 5000);
  });

  // Animation for page transitions
  document.body.classList.add('fade-in');
  
  // Add smooth scrolling to all links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: 'smooth'
        });
      }
    });
  });
  
  // Handle loading states for buttons when forms are submitted
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function() {
      const submitButton = this.querySelector('button[type="submit"]');
      if (submitButton) {
        // Save original button text
        const originalText = submitButton.innerHTML;
        
        // Update button to show loading state
        submitButton.disabled = true;
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
        
        // Reset button after timeout (in case form submission fails)
        setTimeout(() => {
          if (submitButton.disabled) {
            submitButton.disabled = false;
            submitButton.innerHTML = originalText;
          }
        }, 10000);
      }
    });
  });
});

// Function to show error messages
function showError(message) {
  const errorContainer = document.getElementById('error-container');
  if (errorContainer) {
    errorContainer.innerHTML = `
      <div class="alert alert-danger alert-dismissible fade show" role="alert">
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
    `;
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
      const alert = errorContainer.querySelector('.alert');
      if (alert) {
        const closeButton = alert.querySelector('.btn-close');
        if (closeButton) {
          closeButton.click();
        }
      }
    }, 5000);
  }
}

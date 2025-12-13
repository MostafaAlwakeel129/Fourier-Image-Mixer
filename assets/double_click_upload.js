// double_click_upload.js
// This script enables DOUBLE-CLICK ONLY to trigger file upload for image displays

document.addEventListener('DOMContentLoaded', function() {
    // Wait for the page to fully load and retry until elements are found
    let retryCount = 0;
    const maxRetries = 10;
    
    function setupDoubleClick() {
        let allFound = true;
        
        for (let i = 1; i <= 4; i++) {
            const uploadComponent = document.getElementById(`upload-image-${i}`);
            
            if (uploadComponent && !uploadComponent.dataset.doubleClickSetup) {
                // Mark as setup to avoid duplicate handlers
                uploadComponent.dataset.doubleClickSetup = 'true';
                
                // Find the hidden file input
                const fileInput = uploadComponent.querySelector('input[type="file"]');
                
                if (fileInput) {
                    // Hide the file input completely to prevent Dash's default click behavior
                    fileInput.style.pointerEvents = 'none';
                    
                    const imageDisplay = document.getElementById(`image-display-${i}`);
                    
                    if (imageDisplay) {
                        // Track clicks to distinguish single from double
                        let clickTimer = null;
                        let clickCount = 0;
                        
                        imageDisplay.addEventListener('click', function(e) {
                            e.preventDefault();
                            e.stopPropagation();
                            
                            clickCount++;
                            
                            if (clickCount === 1) {
                                // First click - wait to see if there's a second click
                                clickTimer = setTimeout(function() {
                                    // Single click - do nothing
                                    clickCount = 0;
                                }, 300); // 300ms window for double-click
                            } else if (clickCount === 2) {
                                // Double click detected
                                clearTimeout(clickTimer);
                                clickCount = 0;
                                
                                // Temporarily enable pointer events and trigger click
                                fileInput.style.pointerEvents = 'auto';
                                fileInput.click();
                                
                                // Disable again after a short delay
                                setTimeout(function() {
                                    fileInput.style.pointerEvents = 'none';
                                }, 100);
                            }
                        });
                        
                        // Visual feedback
                        imageDisplay.style.transition = 'background-color 0.2s';
                        imageDisplay.style.cursor = 'pointer';
                        
                        imageDisplay.addEventListener('mouseenter', function() {
                            this.style.backgroundColor = '#1a1a1a';
                        });
                        
                        imageDisplay.addEventListener('mouseleave', function() {
                            this.style.backgroundColor = '#0f0f0f';
                        });
                    }
                } else {
                    allFound = false;
                }
            } else if (!uploadComponent) {
                allFound = false;
            }
        }
        
        // Retry if not all elements found
        if (!allFound && retryCount < maxRetries) {
            retryCount++;
            setTimeout(setupDoubleClick, 300);
        }
    }
    
    setupDoubleClick();
});
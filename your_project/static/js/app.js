// static/js/app.js

/**
 * This JavaScript file adds interactive transitions and smooth scrolling effects
 * for the image captioning website. You can extend this file with more complex
 * interactive features such as modals, animations, or dynamic content updates.
 */

document.addEventListener("DOMContentLoaded", function() {
    // Smooth scrolling for all anchor links starting with "#"
    const anchors = document.querySelectorAll('a[href^="#"]');
    anchors.forEach(anchor => {
      anchor.addEventListener("click", function(e) {
        e.preventDefault();
        const targetId = this.getAttribute("href");
        document.querySelector(targetId).scrollIntoView({
          behavior: "smooth"
        });
      });
    });
  
    // Future interactive code can be added here.
    // For example, you can add event listeners for form submissions,
    // dynamically update the caption history, or animate elements on the page.
  });
  
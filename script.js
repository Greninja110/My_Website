// Wait for the DOM to load completely
document.addEventListener('DOMContentLoaded', function() {
    // Set your target launch date (adjust as needed)
    const launchDate = new Date("April 1, 2025 00:00:00").getTime();
    const countdownElement = document.getElementById("countdown");
  
    function updateCountdown() {
      const now = new Date().getTime();
      const timeLeft = launchDate - now;
  
      // If the countdown is finished, display a live message
      if (timeLeft < 0) {
        countdownElement.innerHTML = "We're live!";
        clearInterval(timer);
        return;
      }
  
      // Time calculations for days, hours, minutes, and seconds
      const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
      const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);
  
      // Display the countdown
      countdownElement.innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`;
    }
  
    // Update countdown immediately and then every second
    updateCountdown();
    const timer = setInterval(updateCountdown, 1000);
  });
  
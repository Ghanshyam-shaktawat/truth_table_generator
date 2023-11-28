document.addEventListener("DOMContentLoaded", function() {
    const queryInput = document.getElementById('queryInput');
    const propositionButtons = document.querySelectorAll('.proposition-btn');
  
    // Loop through each proposition button and add click event listener
    propositionButtons.forEach(button => {
      button.addEventListener("click", function() {
        // Append the clicked proposition symbol to the input field
        queryInput.value += button.textContent;
      });
    });
  });
  


  
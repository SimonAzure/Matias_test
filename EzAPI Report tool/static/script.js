// Index.html functionality
document.addEventListener('DOMContentLoaded', function () {
    const reportTypeSelect = document.getElementById('report_type');
    const columnsContainer = document.getElementById('columns-container');
  
    // Define the available columns for each report type
    const availableColumns = {
      network_analytics: ['day', 'imps', 'clicks', 'booked_revenue', 'line_item_id', 'buyer_member_id'],
      seller_fill_and_delivery: ['ad_requests', 'ad_responses', 'imps_resold'],
      // Add more report types and their respective columns as needed
    };
  
    // Update the columns checkboxes based on the selected report type
    function updateColumns() {
      const reportType = reportTypeSelect.value;
      const columns = availableColumns[reportType] || [];
  
      columnsContainer.innerHTML = ''; // Clear previous checkboxes
  
      columns.forEach(function (column) {
        const checkboxContainer = document.createElement('div');
        checkboxContainer.classList.add('checkbox-container');
  
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.name = 'columns';
        checkbox.value = column;
  
        const label = document.createElement('label');
        label.appendChild(checkbox);
        label.appendChild(document.createTextNode(column));
  
        checkboxContainer.appendChild(label);
        columnsContainer.appendChild(checkboxContainer);
      });
    }
  
    // Attach an event listener to the report type select
    reportTypeSelect.addEventListener('change', updateColumns);
  
    // Update the columns checkboxes on page load
    updateColumns();
  });
  
  // Results.html button functionality
  document.addEventListener('DOMContentLoaded', function() {
    // Select the copy button element
    let copyButton = document.getElementById('copyButton');
  
    // Select the JSON content and the JSON data textarea
    let jsonContent = document.getElementById('jsonContent');
    let jsonInput = document.getElementById('json-data');
  
    // Attach a click event listener to the copy button
    copyButton.addEventListener('click', function() {
      // Copy JSON content to clipboard
      jsonContent.select();
      document.execCommand('copy');
      window.getSelection().removeAllRanges();
  
      // Populate JSON data textarea
      jsonInput.value = jsonContent.value;
  
      // Update the button text
      copyButton.innerHTML = 'Copied!';
  
      // Reset the button text after a delay
      setTimeout(function() {
        copyButton.innerHTML = '<i class="fas fa-copy"></i> Copy JSON';
      }, 2000);
    });
  });
  
  
  
  document.addEventListener('DOMContentLoaded', function () {
    // ... Your existing code ...
  
    // Select the "Post the Report" button element
    const postReportButton = document.getElementById('post-report-button');
    
    // Attach a click event listener to the "Post the Report" button
    postReportButton.addEventListener('click', function () {
      // Get the Member ID and JSON Data from the input fields
      const memberId = document.getElementById('member-id').value;
      const jsonData = document.getElementById('json-data').value;
      
      // Create a data object to send as JSON in the request body
      const postData = {
        member_id: memberId,
        json_data: jsonData,
      };
  
      // Make the POST request
      fetch('/post-report', {
        method: 'POST',
        body: JSON.stringify(postData),
        headers: {
          'Content-Type': 'application/json', // Set the content type to JSON
        },
      })
        .then(response => response.json())
        .then(data => {
          // Handle the response from the server (e.g., report ID)
          alert(data); // You can display the response in an alert or update the page as needed
        })
        .catch(error => {
          console.error('Error:', error);
          // Handle any errors that occur during the POST request
        });
    });
  });
  
  
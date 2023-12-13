$(document).ready(function () {
        $('#leaveTable').DataTable();
      });


function editLeave(button) {
         var row = $(button).closest('tr');

         // Assuming you have data attributes in your HTML like data-leavetype, data-startdate, etc.
         var leavetype = row.find('td:eq(0)').text();  // Assuming leavetype is in the first column
         var startdate = row.find('td:eq(1)').text().trim();   // Assuming startdate is in the second column
         var enddate = row.find('td:eq(2)').text();     // Assuming enddate is in the third column
         var reason = $(button).data('reason');     // Assuming reason is in the fourth column
         var leaveId = row.find('button[data-leaveid]').data('leaveid');  // Assuming you have a data-leaveid attribute on the button

         // Populate modal fields with leave details
         $('#editLeaveType').val(leavetype);
         $('#editStartDate').val(startdate);
         $('#editEndDate').val(enddate);
         $('#reason').val(reason);

         // Set the leaveId in the modal
         $('#editLeaveId').val(leaveId);

         // Show the modal
         $('#editLeaveModal').modal('show');
        }


      function confirmDelete(leaveId) {
         if (confirm("Are you sure you want to delete this leave request?")) {
         // Create a form dynamically
         var form = document.createElement('form');
         form.method = 'POST';
         form.action = `/delete_leave/${leaveId}/`;  // Update the URL based on your project structure

         // Add a CSRF token to the form
         var csrfInput = document.createElement('input');
         csrfInput.type = 'hidden';
         csrfInput.name = 'csrfmiddlewaretoken';
         csrfInput.value =  csrfToken;  // Use Django template tag to get CSRF token
         form.appendChild(csrfInput);

         // Append the form to the body and submit it
         document.body.appendChild(form);
         form.submit();
          }
        }


function updateLeaveDetails(leaveId) {
    if (confirm("Are you sure you want to update this leave request?")) {
        // Get the form data
        var leavetype = $('#editLeaveType').val();
        var startdate = $('#editStartDate').val();
        var enddate = $('#editEndDate').val();
        var reason = $('#reason').val();

        // Validate the data if needed

        // Close the modal
        $('#editLeaveModal'+ leaveId).modal('hide');

        // Create a form dynamically (hidden)
        var form = document.createElement('form');
        form.method = 'POST';
        form.action = `/edit_leave/${leaveId}/`;  // Update the URL based on your project structure

        // Add a CSRF token to the form
        var csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrfToken;
        form.appendChild(csrfInput);

        // Added form fields for updating leave details
        var leaveTypeInput = document.createElement('input');
        leaveTypeInput.type = 'hidden';
        leaveTypeInput.name = 'leavetype';
        leaveTypeInput.value = getLeaveTypeId(leavetype);  // Call a function to get the leave type ID
        form.appendChild(leaveTypeInput);

        var startDateInput = document.createElement('input');
        startDateInput.type = 'hidden';
        startDateInput.name = 'startdate';
        startDateInput.value = startdate;
        form.appendChild(startDateInput);

        var endDateInput = document.createElement('input');
        endDateInput.type = 'hidden';
        endDateInput.name = 'enddate';
        endDateInput.value = enddate;
        form.appendChild(endDateInput);

        var reasonInput = document.createElement('input');
        reasonInput.type = 'hidden';
        reasonInput.name = 'reason';
        reasonInput.value = reason;
        form.appendChild(reasonInput);



        // Append the form to the body and submit it
        document.body.appendChild(form);
        form.submit();
    }
}
    function getLeaveTypeId(leaveTypeName) {

    if (leaveTypeName === 'Sick Leave') {
        return 2;
    } else if (leaveTypeName === 'Paid Leave') {
        return 1;
    } else if (leaveTypeName === 'Other') {
        return 3;
    } else {
        return 0;
    }
    }

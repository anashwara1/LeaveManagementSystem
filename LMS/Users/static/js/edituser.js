$(document).ready(function() {
            $('#details').DataTable();




        $('.btn-primary').on('click', function () {
            var row = $(this).closest('tr');
            var columns = row.find('td');
            var mail = row.data('mail')
            var fname = row.data('fname')
            var lname = row.data('lname')
            var dep = row.data('dep')

            var emp = $(columns[1]).text().trim();
            var employeeName = $(columns[2]).text().trim();
            var designation = $(columns[3]).text().trim();
            var dojText = $(columns[4]).text().trim();
            var doj = formatDate(dojText);


            // Set values in the modal input fields
            $('#employee-name').val(employeeName);
            $('#employee-id').val(emp);
            $('#empid').val(emp);
            $('#employee-designation').val(designation);
            $('#employee-doj').val(doj);
            $('#employee-mail').val(mail);
            $('#employee-firstname').val(fname);
            $('#employee-lastname').val(lname);
            $('#employee-department').val(dep);

            $('#Leavedetails').modal('show');
        });

         function formatDate(inputDate) {
        var date = new Date(inputDate);
        return date.toISOString().split('T')[0];
    }

        $('.btn-dark').on('click', function () {
            var row = $(this).closest('tr');
            var columns = row.find('td');

            var emppid = $(columns[1]).text().trim();
            var empName = $(columns[2]).text().trim();

            $('#emp-name').val(empName);
            $('#emp-id').val(emppid);

            $('#Lop').modal('show');

});
        function updateEndDateMin() {
            var startDate = document.getElementById('start_date').value;
            var endDateInput = document.getElementById('end_date');

            // Set the min attribute of the end date input
            endDateInput.min = startDate;

            // Ensure that the end date is always greater than or equal to the start date
            if (endDateInput.value < startDate) {
                endDateInput.value = startDate;
            }
            }


$('#start_date').on('change', updateEndDateMin);
});

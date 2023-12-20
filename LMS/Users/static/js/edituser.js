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

});

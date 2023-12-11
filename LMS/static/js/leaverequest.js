$(document).ready(function () {
        var table = $('#details').DataTable();

        $('.btn-primary').on('click', function () {
            var row = $(this).closest('tr');
            var columns = row.find('td');
            var reason = row.data('reason');
            var balance = row.data('balance');
            var emp = row.data('emp')

            // Assuming the order of columns in the DataTable matches this order
            var employeeName = $(columns[0]).text().trim();
            var leaveType = $(columns[1]).text().trim();
            var startDate = $(columns[2]).text().trim();
            var endDate = $(columns[3]).text().trim();
            var days = $(columns[4]).text().trim();
            var status = $(columns[5]).text().trim();


            // Populate modal form fields
            $('#employee-name').val(employeeName);
            $('#leave-type').val(leaveType);
            $('#start-date').val(startDate);
            $('#end-date').val(endDate);
            $('#Reason').val(reason);
            $('#days').val(days);
            $('#leave-balance').val(balance);
            $('#selected-employee').val(emp);
            $('#empid').val(emp);

            // Show the modal
            $('#Leavedetails').modal('show');
        });
    });

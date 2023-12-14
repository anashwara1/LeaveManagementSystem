$(document).ready(function() {
    var table = $('#details').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ]
        });


    // Trigger DataTables export when the "Download" button is clicked
//    $('#downloadButton').on('click', function() {
//        table.buttons.exportData();
//    });
//});

        $('.btn-primary').on('click', function () {
            var row = $(this).closest('tr');
            var columns = row.find('td');
            var reason = row.data('reason');
            var balance = row.data('balance');
            var emp = row.data('emp')
            var status = row.data('status')


            var employeeName = $(columns[0]).text().trim();
            var leaveType = $(columns[1]).text().trim();
            var startDate = $(columns[2]).text().trim();
            var endDate = $(columns[3]).text().trim();
            var days = $(columns[4]).text().trim();



            $('#employee-name').val(employeeName);
            $('#leave-type').val(leaveType);
            $('#start-date').val(startDate);
            $('#end-date').val(endDate);
            $('#Reason').val(reason);
            $('#days').val(days);
            $('#leave-balance').val(balance);
            $('#selected-employee').val(emp);
            $('#empid').val(emp);


            $('#Leavedetails').modal('show');

            if (status === 'Pending') {
            $('.pending-buttons').show();
        } else {
            $('.pending-buttons').hide();
        }

        });
});

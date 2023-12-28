$(document).ready(function() {
        $('#details').DataTable({
            scrollX: true,
            scrollCollapse: false,
            fixedColumns: {
                leftColumns: 8, // Set the number of columns that should be fixed (non-scrollable) on the left
            }
        });


    var hasUnreadLeaveRequests = document.getElementById('aaa').value;

    if (hasUnreadLeaveRequests === 'True') {
        toastr.success('You have new leave requests! Click to view.', 'New Leave Requests', {
            onclick: function () {
                window.location.href = "http://127.0.0.1:8000/leaveRequest";
            }
        });
    }
});



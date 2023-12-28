$(document).ready(function() {
        $('#details').DataTable({
            scrollX: true,
            scrollCollapse: false,
            fixedColumns: {
                leftColumns: 8, // Set the number of columns that should be fixed (non-scrollable) on the left
            }
        });
    });
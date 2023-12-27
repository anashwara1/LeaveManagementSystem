function updateEndDateMin() {
    var startDate = document.getElementById('start_date').value;
    document.getElementById('end_date').min = startDate;
}
document.addEventListener("DOMContentLoaded", function () {

            updateDefaultDates();
            document.getElementById("leave_type").addEventListener("change", updateDefaultDates);
        });

        function updateDefaultDates() {
            var leaveTypeSelect = document.getElementById("leave_type");
            var startDateInput = document.getElementById("start_date");
            var endDateInput = document.getElementById("end_date");

            console.log(leaveTypeSelect.value);

            if (leaveTypeSelect.value === "Sick Leave") {

                var today = new Date().toISOString().split('T')[0];
                startDateInput.value = today;
                endDateInput.value = today;


                startDateInput.max = today;
                endDateInput.max = today;
            } else {

                startDateInput.max = null;
                endDateInput.max = null;
            }
        }
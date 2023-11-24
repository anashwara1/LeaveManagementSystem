<script>
        function showInput() {
            var departmentSelect = document.getElementById("employee-department");
            var otherInput = document.getElementById("other-input");

            if (departmentSelect.value === "Other") {
                otherInput.style.display = "block";
            } else {
                otherInput.style.display = "none";
            }
        }
    </script>

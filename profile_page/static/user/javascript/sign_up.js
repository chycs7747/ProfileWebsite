<script>
    function validateForm() {
        var job = document.forms["signupForm"]["job"].value;
        var gender = document.forms["signupForm"]["gender"].value;
        if (job == "select..") {
            alert("Please select job before clicking submit button!");
            event.preventDefault(); // 기본 동작 취소
            return false;
        }
        if (gender == "select..") {
            alert("Please select gender before clicking submit button!");
            event.preventDefault(); // 기본 동작 취소
            return false;
        }
    }
</script>

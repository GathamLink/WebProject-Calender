/**
 * the AJAX usage is based on lectures.
 * Some structures have been changed
 */

$(document).ready(function () {
    console.log("Adding event handlers");
    $("#username").on("change", function () {
        var chosen_user = $("#username");
        $("#checkuser").removeClass();

        $.post('/checkuser', {
            'username': $('#username').val()
        }).done(function (response) {
            var server_response = response['text'];
            var server_code = response['returnvalue'];
            if (server_code == 0) {
                $("#email").focus();
                $("#checkuser").html('<span>' + server_response + '</span>');
                $('#checkuser').css("color", "green");
                $('#checkuser').css("font-weight", "normal");
                $('#checkuser').css("font-size", "15px");
                $("#checkuser").addClass("success");
            } else {
                chosen_user.focus();
                $("#checkuser").html('<span>' + server_response + '</span>');
                $('#checkuser').css("color", "red");
                $('#checkuser').css("font-weight", "normal");
                $('#checkuser').css("font-size", "15px");
                $("#checkuser").addClass("failure");
            }
        }).fail(function () {
            $("#checkuser").html('<span>Error contacting server</span>');
            $("#checkuser").addClass("failure");
        });
    });
});


$(document).ready(function () {
    $("#email").on("change", function () {
        var chosen_email = $("#email");
        $("#checkemail").removeClass();

        $.post('/checkemail', {
            'email': chosen_email.val()
        }).done(function (response) {
            var server_response = response['text']
            var server_code = response['code']
            if (server_code == 0) {
                $("#password").focus()
                $("#checkemail").html('<span>' + server_response + '</span>');
                $('#checkemail').css("color", "green");
                $('#checkemail').css("font-weight", "normal");
                $('#checkemail').css("font-size", "15px");
                $("#checkemail").addClass("success");
            } else {
                chosen_email.focus()
                $("#checkemail").html('<span>' + server_response + '</span>');
                $('#checkemail').css("color", "red");
                $('#checkemail').css("font-weight", "normal");
                $('#checkemail').css("font-size", "15px");
                $("#checkemail").addClass("failure");
            }
        }).fail(function () {
            $("#checkemail").html('<span>Error contacting server</span>');
            $("#checkemail").addClass("failure");
        });
    });
})

function check() {
    if (checkpassword()) {
        alert("Register Successfully");
        return true;
    } else {
        alert("Two passwords are not same, please enter again!");
        return false;
    }
}

function checkpassword() {
    let pass = document.getElementById("password");
    let pass2 = document.getElementById("password2");
    let password = pass.value;
    let password2 = pass2.value;

    if (password == password2) {
        return true;
    } else {
        return false;
    }

}
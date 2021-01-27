/**
 * the AJAX usage is based on lectures.
 * Some structures have been changed
 */

$(document).ready(function () {
    $("#username").on("change", function () {
        var chosen_user = $("#username");
        $("#checkuser").removeClass();

        $.post('/checkloginuser', {
            'username': $('#username').val()
        }).done(function (response) {
            var server_response = response['text'];
            var server_code = response['code'];
            if (server_code == 0) {
                chosen_user.focus()
                $("#checkuser").html('<span>' + server_response + '</span>');
                $('#checkuser').css("color", "red");
                $('#checkuser').css("font-weight", "normal");
                $('#checkuser').css("font-size", "15px");
                $("#checkuser").addClass("success");
            } else {
                $("#password").focus();
                $("#checkuser").html('<span>' + server_response + '</span>');
                $('#checkuser').css("color", "green");
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

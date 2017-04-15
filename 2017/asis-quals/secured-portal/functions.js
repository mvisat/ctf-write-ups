/**
 * Created by root on 3/24/17.
 * coded via PhpStorm :)
 */


function createCookie(name, value, days) {
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        var expires = "; expires=" + date.toGMTString();
    }
    else var expires = "";

    document.cookie = name + "=" + value + expires + "; path=/";
}

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function eraseCookie(name) {
    createCookie(name, "", -1);
}

function logout(){
    eraseCookie('loginString');
    window.location = '/';
}

$(document).ready(function() {

    $("#login").click(function(event){
        event.preventDefault();

        var username = $("#inputUsername").val();
        var password = $("#inputPassword").val();

        var loginString = btoa(username + ':' + password);

        $.get('/authentication/login/' + loginString, function(data){
            var loginString = readCookie('loginString');

            if(typeof loginString == 'undefined'){
                $("#showResult").remove();
                $("#result").append('<div id="showResult"></div>');
                $("#showResult").addClass('alert').addClass('alert-danger').html('Invalid credentials have been given.');
            }else{
                $("#showResult").remove();
                $("#result").append('<div id="showResult"></div>');
                $("#showResult").addClass('alert').addClass('alert-success').html('Login success, please wait until you are being redirected to the panel');

                setTimeout(function(){ window.location = '/panel/index?auth=' + decodeURI(loginString); }, 3000);
            }
        });
    });
})
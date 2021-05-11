$(document).ready(function () {

    $("#login").on("click", function () {
        $.ajax({
            url: '/valid/',
            type: 'post',
            dataType: 'json',
            data: $("#info").serialize(),
            success: function (data) {

                if (data.status == 'true') {
                    console.log('hello')
                    window.location.href = '/home'

                } else {

                }
            }


        });
    });


});





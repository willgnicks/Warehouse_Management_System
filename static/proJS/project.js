$(document).ready(function () {
    $('#plus').on('click',function () {

            console.log('hellow')

            $('#purchase').nextNode('<h1>hello world</h1>')


        })

    $("#project_add").on("click", function () {
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





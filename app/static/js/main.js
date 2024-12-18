$(document).ready(() => {

    $('#register-back').on('click', () => {
        window.history.back();
    })


    // 获取 CSRF 令牌
    var csrftoken = $('meta[name=csrf-token]').attr('content');

    // 为所有的 AJAX 请求设置默认的请求头
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
})



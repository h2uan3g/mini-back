const showModal = (message, onconfirm) => {
    let myModalEL = document.getElementById('myModal')
    myModalEL.addEventListener('show.bs.modal', function () {
        myModalEL.setAttribute('aria-hidden', 'false');
    });
    myModalEL.addEventListener('hidden.bs.modal', function () {
        myModalEL.setAttribute('aria-hidden', 'true');
    });
    let myModal = new bootstrap.Modal(myModalEL);
    $('#myModal .modal-body').html(message);
    $('#confirmButton').on('click', () => {
        myModal.hide()
        onconfirm()
    })
    myModal.show();
}

function deleteModel(el) {
    let title = el.dataset.title
    let name = el.dataset.name
    let data = name || title || ''
    let id = el.dataset.id
    let url = el.dataset.url
    showModal(`确定要删除「${data}」吗？`, function () {
        $.ajax({
            url: `${url}`,
            type: 'DELETE',
            contentType: false,
            processData: false,
            success: function (response) {
                if (response.data && response.data.redirect) {
                    window.location.href = response.data.redirect;
                }
            },
            error: function (xhr, status, error) {
                showModal(`提交失败!!! ${error}`)
            }
        });
    })
}

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



import { Uppy, Dashboard, } from '/static/js/file_upload/uppy.min.mjs'
import zh_CN from '/static/js/file_upload/zh_CN.min.js'

$(document).ready(function () {
    let newsInfo = $('#newsInfo').data('news-info');
    let status = $('#newsInfoIsView').data('status');

    const uppyNewsImage = new Uppy({
        debug: true,
        autoProceed: false,
        restrictions: {
            maxNumberOfFiles: 1,
            allowedFileTypes: ['image/*'],
        }
    }).use(Dashboard, {
        inline: true,
        target: '#news-image-area',
        locale: zh_CN.locales,
        hideUploadButton: true,
        hideCancelButton: true,
        showSelectedFiles: true,
        totalFileCount: 1,
        showPreview: true,
        height: 300,
        width: '100%',
        showRemoveButtonAfterComplete: false,
        proudlyDisplayPoweredByUppy: false,
        individualCancellation: true,
        disabled: status == 0
    })
    uppyNewsImage.on('file-removed', (result) => {
        console.log("result: ", result)
        if (status == 0) {
            uppynewsImage.addFile(result)
        }
    })

    if (newsInfo && newsInfo.image) {
        const addNetworkImage = async (url) => {
            const response = await fetch(url);
            const blob = await response.blob();
            const pathlist = url.split('/')
            uppyNewsImage.addFile({
                name: pathlist[pathlist.length - 1], // 自定义文件名
                type: blob.type,          // 动态获取文件类型
                data: blob,               // 文件数据
                source: 'remote',
                preview: url,
                isRemote: true,
            });


        };
        addNetworkImage(newsInfo.image)
    }

    $('#newsForm').on('submit', function (event) {
        event.preventDefault();  
        let formData = new FormData(this); 
        const files = uppyNewsImage.getFiles();
        if (files == undefined || files.length == 0) {
            alert('未选中图片!!!');
            return;
        }
        $.each(files, function (i, file) {
            formData.append('image', file.data, file.name);
        });
        const body = editor.getHtml()
        formData.append('body', body);

        let url = ''
        if (newsInfo.id) {
            url = `/workbench/news/${newsInfo.id}/detail?status=1`
        } else {
            url = '/workbench/news/detail'
        }

        $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                if (response && response.code == 0) {
                    let redirect = response.data.redirect
                    window.location.href = redirect;
                }
            },
            error: function (xhr, status, error) {
                console.error('Submission failed:', error);
            }
        });
    });

    const { createEditor, createToolbar } = window.wangEditor
    const csrftoken = $('meta[name=csrf-token]').attr('content');
    const editorConfig = {
        placeholder: '请输入...',
        MENU_CONF: {}
    }
    editorConfig.MENU_CONF['uploadImage'] = {
        server: '/workbench/upload',
        fieldName: 'upload',
        timeout: 5 * 1000,
        maxFileSize: 5 * 1024 * 1024,
        allowedFileTypes: ['image/*'],
        headers: {
            'X-CSRFToken': csrftoken
        },
        onSuccess(file, res) {
            console.log('onSuccess', file, res)
        },
        onFailed(file, res) {
            console.log('onFailed', file, res)
        },
    }

    const editor = createEditor({
        selector: '#editor-container',
        html: '<p><br></p>',
        config: editorConfig,
        mode: 'default', // or 'simple'
    })

    const toolbarConfig = {}

    const toolbar = createToolbar({
        editor,
        selector: '#toolbar-container',
        config: toolbarConfig,
        mode: 'simple', // or 'default'
    })

    if (status == 0) {
        editor.disable()
    } else {
        editor.enable()
    }
    if (newsInfo && newsInfo.body) {
        editor.setHtml(newsInfo.body)
    }
}
)




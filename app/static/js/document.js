import { Uppy, Dashboard, } from '/static/js/file_upload/uppy.min.mjs'
import zh_CN from '/static/js/file_upload/zh_CN.min.js'

$(document).ready(() => {
    let documentEl = $('#documentFormInfo').data('document');
    let status = $('#documentStatus').data('status');

    const uppySource = new Uppy({
        debug: true,
        autoProceed: false,
        restrictions: {
            maxNumberOfFiles: 5,
            allowedFileTypes: ['application/pdf',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
        }
    }).use(Dashboard, {
        inline: true,
        target: '#visual-source-area',
        locale: zh_CN.locales,
        hideUploadButton: true,
        hideCancelButton: true,
        showSelectedFiles: true,
        height: 300,
        width: '100%',
        showPreview: true,
        showRemoveButtonAfterComplete: false,
        proudlyDisplayPoweredByUppy: false,
        individualCancellation: true,
        disabled: status == 0
    })
    uppySource.on('file-removed', (result) => {
        console.log("result: ", result)
        if (isView == 0) {
            uppySource.addFile(result)
        }
    })

    const uppyWater = new Uppy({
        debug: true,
        autoProceed: false,
        restrictions: {
            maxNumberOfFiles: 5,
            allowedFileTypes: ['image/*'],
        }
    }).use(Dashboard, {
        inline: true,
        target: '#visual-watermark-area',
        locale: zh_CN.locales,
        hideUploadButton: true,
        hideCancelButton: true,
        showSelectedFiles: true,
        height: 300,
        width: '100%',
        showPreview: true,
        showRemoveButtonAfterComplete: false,
        proudlyDisplayPoweredByUppy: false,
        individualCancellation: true,
        disabled: status == 0
    })
    uppyWater.on('file-removed', (result) => {
        console.log("result: ", result)
        if (status == 0) {
            uppyWater.addFile(result)
        }
    })


    $('#documentForm').on('submit', function (event) {
        event.preventDefault(); // 阻止表单的默认提交行为

        // 获取表单数据
        let formData = new FormData(this); // 序列化表单数据
        // formData.append('type', topImage.type)

        const files1 = uppySource.getFiles();
        if (files1 == undefined || files1.length == 0) {
            alert('未选源文件!!!');
            return;
        }
        $.each(files1, function (i, file) {
            // 这里可以绑定 pre_image
            formData.append('source', file.data, file.name);
        });

        const files2 = uppyWater.getFiles();
        if (files2 == undefined || files2.length == 0) {
            alert('未选中水印图片!!!');
            return;
        }
        $.each(files2, function (i, file) {
            formData.append('watermark', file.data, file.name);
        });

        let url = ""
        if (documentEl && documentEl.id) {
            url = `/visual/${documentEl.id}/detail`
        } else {
            url = `/visual/detail`
        }

        $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                // 请求成功后的回调
                if (response.data && response.data.result && response.data.result) {
                    const rest = response.data.result;  
                    const a = document.createElement('a');
                    a.href = rest;   
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);   
                    window.URL.revokeObjectURL(url);  

                    const redirect = response.data.redirect; 
                    window.location.href = redirect;
                }
            },
            error: function (xhr, status, error) {
                // 请求失败后的回调
                console.error('Submission failed:', error);
                //alert('Submission failed!');
            }
        });
    });


})
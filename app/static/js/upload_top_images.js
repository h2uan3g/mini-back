import {Uppy, Dashboard,} from '/static/js/file_upload/uppy.min.mjs'
import zh_CN from '/static/js/file_upload/zh_CN.min.js'

$(document).ready(function () {
        let topImage = $('#topImageFormInfo').data('top-image');
        let isView = $('#topImageIsView').data('is-view');
        let csrfTokenTop = $('#topImageForm input[name="csrf_token"]').val();

        const uppyTopImage = new Uppy({
            debug: true,
            autoProceed: false,
            restrictions: {
                maxNumberOfFiles: 1,
                allowedFileTypes: ['image/*'],
            }
        }).use(Dashboard, {
            inline: true,
            target: '#image-top-area',
            locale: zh_CN.locales,
            hideUploadButton: true,
            hideCancelButton: true,
            showSelectedFiles: true,
            totalFileCount: 1,
            showPreview: true,
            showRemoveButtonAfterComplete: false,
            proudlyDisplayPoweredByUppy: false,
            individualCancellation: true,
            disabled: isView == 0
        }).on('file-removed', (result) => {
            console.log("result: ", result)
            if (isView == 0) {
                uppyTopImage.addFile(result)
            }
        })

        if (topImage && topImage.image) {
            const addNetworkImage = async (url) => {
                const response = await fetch(url);
                const blob = await response.blob();
                const pathlist = url.split('/')
                uppyTopImage.addFile({
                    name: pathlist[pathlist.length - 1], // 自定义文件名
                    type: blob.type,          // 动态获取文件类型
                    data: blob,               // 文件数据
                    source: 'remote',
                    preview: url,
                    isRemote: true,
                });


            };
            addNetworkImage(topImage.image)
        }

        $('#topImageForm').on('submit', function (event) {
            event.preventDefault(); // 阻止表单的默认提交行为

            // 获取表单数据
            let formData = new FormData(this); // 序列化表单数据

            // let files = $('#input-id')[0].files;
            const files = uppyTopImage.getFiles();
            if (files == undefined || files.length == 0) {
                alert('未选中图片!!!');
                return;
            }
            $.each(files, function (i, file) {
                formData.append('image', file.data);
            });

            $.ajax({
                url: `/workbench/${topImage.id}/edit`,  // 替换为你的服务器处理 URL
                type: 'POST',                   // 或 'GET'，根据需求选择
                data: formData,                 // 提交的表单数据
                contentType: false,
                processData: false,
                success: function (response) {
                    // 请求成功后的回调
                    //console.log('Form submitted successfully:', response);
                    alert('提交成功!');
                },
                error: function (xhr, status, error) {
                    // 请求失败后的回调
                    console.error('Submission failed:', error);
                    //alert('Submission failed!');
                }
            });
        });

    }
)




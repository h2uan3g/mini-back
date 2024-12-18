import {Uppy, Dashboard,} from '/static/js/file_upload/uppy.min.mjs'
import zh_CN from '/static/js/file_upload/zh_CN.min.js'

$(document).ready(function () {
        let healthInfo = $('#healthInfo').data('health-info');
        let status = $('#healthInfoIsView').data('status');

        const uppyHealthImage = new Uppy({
            debug: true,
            autoProceed: false,
            restrictions: {
                maxNumberOfFiles: 1,
                allowedFileTypes: ['image/*'],
            }
        }).use(Dashboard, {
            inline: true,
            target: '#health-image-area',
            locale: zh_CN.locales,
            hideUploadButton: true,
            hideCancelButton: true,
            showSelectedFiles: true,
            totalFileCount: 1,
            showPreview: true,
            width: '100%',
            showRemoveButtonAfterComplete: false,
            proudlyDisplayPoweredByUppy: false,
            individualCancellation: true,
            disabled: status == 0
        })
        uppyHealthImage.on('file-removed', (result) => {
            console.log("result: ", result)
            if (status == 0) {
                uppyHealthImage.addFile(result)
            }
        })

        if (healthInfo && healthInfo.image) {
            const addNetworkImage = async (url) => {
                const response = await fetch(url);
                const blob = await response.blob();
                const pathlist = url.split('/')
                uppyHealthImage.addFile({
                    name: pathlist[pathlist.length - 1], // 自定义文件名
                    type: blob.type,          // 动态获取文件类型
                    data: blob,               // 文件数据
                    source: 'remote',
                    preview: url,
                    isRemote: true,
                });


            };
            addNetworkImage(healthInfo.image)
        }

        $('#healthForm').on('submit', function (event) {
            event.preventDefault(); // 阻止表单的默认提交行为

            // 获取表单数据
            let formData = new FormData(this); // 序列化表单数据
            formData.append('type', healthInfo.type)

            // let files = $('#input-id')[0].files;
            const files = uppyHealthImage.getFiles();
            if (files == undefined || files.length == 0) {
                alert('未选中图片!!!');
                return;
            }
            $.each(files, function (i, file) {
                formData.append('image', file.data);
            });

            const body = editor.getHtml()
            formData.append('body', body);

            $.ajax({
                url: `/workbench/${healthInfo.id}/health_edit`,  // 替换为你的服务器处理 URL
                type: 'POST',                   // 或 'GET'，根据需求选择
                data: formData,                 // 提交的表单数据
                contentType: false,
                processData: false,
                success: function (response) {
                    // 请求成功后的回调
                    //console.log('Form submitted successfully:', response);
                    if (response.redirect) {
                        window.location.href = response.redirect; // 前端手动跳转
                    }
                },
                error: function (xhr, status, error) {
                    // 请求失败后的回调
                    console.error('Submission failed:', error);
                }
            });
        });

        const {createEditor, createToolbar} = window.wangEditor
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
        if (healthInfo && healthInfo.body) {
            editor.setHtml(healthInfo.body)
        }
    }
)




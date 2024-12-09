$(document).ready(function () {
        function initImageUpload(initialPreview, initialPreviewConfig, inputId, data, uploadUrl, deleteUrl, csrfToken) {
            $(inputId).fileinput({
                showPreview: true,
                language: "zh",
                uploadUrl: uploadUrl,
                dropZoneTitle: "拖拽文件到这里",
                uploadAsync: true,
                showUpload: false,
                showRemove: true,
                enableResumableUpload: true,
                dropZoneEnabled: true,
                initialPreview: initialPreview,
                initialPreviewAsData: true,
                initialPreviewConfig: initialPreviewConfig,
                previewFileType: 'image',  // 预览类型为图片
                allowedFileExtensions: ['jpg', 'png', 'gif', 'jpeg'], // 允许上传的文件类型
                theme: 'fas',
                overwriteInitial: false,
                deleteUrl: deleteUrl,
                deleteExtraData: {
                    "csrf_token": csrfToken,
                    "type": data.type,
                    "image": initialPreview
                },
                fileActionSettings: {
                    showRemove: true,
                    showRotate: false,
                    showDownload: false,
                    removeLabel: '删除', // 自定义移除按钮文本
                    showDrag: true,
                },
                'minFileCount': 0,
                'maxFileCount': 1,
            }).on('filedeleted', function (event, key, jqXHR, data) {
                location.reload(true);
            }).on('filebatchselected', function(event) {
                console.log('Files selected:', event.files);
            });
        }

        let topImage = $('#topImageFormInfo').data('top-image');
        let csrfTokenTop = $('#topImageForm input[name="csrf_token"]').val();
        let initialPreviewTopImage = []
        let initialPreviewConfigTopImage = []
        if (topImage && topImage.image) {
            initialPreviewTopImage = [topImage.image];
            initialPreviewConfigTopImage = [{
                caption: "图片", downloadUrl: topImage.image, key: 1,
            }]
        }
        console.log("topImage", topImage)
        if (topImage && topImage.id) {
            initImageUpload(
                initialPreviewTopImage,
                initialPreviewConfigTopImage,
                '#input-id',
                topImage,
                `/workbench/${topImage.id}/edit`,
                `/workbench/${topImage.id}/delete`,
                csrfTokenTop)
        }


        let healthInfo = $('#healthInfo').data('health-info');
        let csrfTokenHealth = $('#healthFormInfo input[name="csrf_token"]').val();
        let initialPreviewHealth = []
        let initialPreviewConfigHealth = []
        if (healthInfo && healthInfo.image) {
            initialPreviewHealth = [healthInfo.image];
            initialPreviewConfigHealth = [{
                caption: "图片", downloadUrl: healthInfo.image, key: 1,
            }]
        }

        if (healthInfo && healthInfo.id) {
            console.log("-----")
            initImageUpload(
                initialPreviewHealth,
                initialPreviewConfigHealth,
                '#cover-image-id',
                healthInfo,
                `/workbench/${healthInfo.id}/health_edit`,
                `/workbench/${healthInfo.id}/health_delete`,
                csrfTokenHealth)
        }

        $('#topImageForm').on('submit', function (event) {
            event.preventDefault(); // 阻止表单的默认提交行为
            // 获取表单数据
            let formData = new FormData(this); // 序列化表单数据

            let filesCount = $('#input-id').fileinput('getFilesCount', true);
            console.log("filesCount: ", filesCount)

            let fileStack = $('#input-id').fileinput('getPreview');
            if (fileStack.length === undefined || fileStack.length === 0) {
                alert('没有文件选中.');
                return;
            }
            $.each(fileStack, function(fileId, fileObj) {
                if (fileObj !== undefined) {
                    console.log("fileObj: ", fileObj)
                }
            });

            let files = $('#input-id')[0].files;
            $.each(files, function (i, file) {
                formData.append('image', file);
            });
            formData.append('type', topImage.type)
            debugger
            $.ajax({
                url: `/workbench/${topImage.id}/edit`,  // 替换为你的服务器处理 URL
                type: 'POST',                   // 或 'GET'，根据需求选择
                data: formData,                 // 提交的表单数据
                contentType: false,
                processData: false,
                success: function (response) {
                    // 请求成功后的回调
                    location.reload(true);
                    console.log('Form submitted successfully:', response);
                },
                error: function (xhr, status, error) {
                    // 请求失败后的回调
                    console.error('Submission failed:', error);
                    //alert('Submission failed!');
                }
            });
        });

        $('#healthForm').on('submit', function (event) {
            event.preventDefault(); // 阻止表单的默认提交行为
            // 获取表单数据
            let formData = $(this).serializeArray();
            console.log("formData: ", $(this))

            let files = $('#cover-image-id')[0].files;
            $.each(files, function (i, file) {
                // formData.append('image', file);
                formData.push({name: 'image', value: file});
            });
            // formData.append('type', healthInfo.type)
            formData.push({name: 'type', value: healthInfo.type});

            let csrfToken = $('meta[name="csrf-token"]').attr('content');
            console.log("csrfToken: ", csrfToken)
            console.log("formData: ", formData)
            debugger
            $.ajax({
                url: `/workbench/${healthInfo.id}/health_edit`,  // 替换为你的服务器处理 URL
                type: 'POST',                   // 或 'GET'，根据需求选择
                headers: {"X-CSRFToken": csrfToken},
                data: $.param(formData),                 // 提交的表单数据
                contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
                processData: false,
                success: function (response) {
                    // 请求成功后的回调
                    location.reload(true);
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




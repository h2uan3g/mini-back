import { Uppy, Dashboard, } from '/static/js/file_upload/uppy.min.mjs'
import zh_CN from '/static/js/file_upload/zh_CN.min.js'

$(document).ready(function () {
    let topImage = $('#topImageFormInfo').data('top-image');
    let status = $('#topImageStatus').data('status');

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
        height: 300,
        width: '100%',
        totalFileCount: 1,
        showPreview: true,
        showRemoveButtonAfterComplete: false,
        proudlyDisplayPoweredByUppy: false,
        individualCancellation: true,
        disabled: status == 0
    })
    uppyTopImage.on('file-removed', (result) => {
        console.log("result: ", result)
        if (status != 2) {
            uppyTopImage.addFile(result)
        }
    })

    if (topImage && topImage.image) {
        const addNetworkImage = async (url) => {
            const response = await fetch(url);
            const blob = await response.blob();
            const pathlist = url.split('/')
            uppyTopImage.addFile({
                name: pathlist[pathlist.length - 1], 
                type: blob.type,         
                data: blob,          
                source: 'remote',
                preview: url,
                isRemote: true,
            });
        };
        addNetworkImage(topImage.image)
    }

    $('#topImageForm').on('submit', function (event) {
        event.preventDefault();
        let formData = new FormData(this);
        const files = uppyTopImage.getFiles();
        if (files == undefined || files.length == 0) {
            alert('未选中图片!!!');
            return;
        }
        $.each(files, function (i, file) {
            formData.append('image', file.data, file.name);
        });

        let url = `/workbench/detail`
        if (topImage.id != undefined) {
            url = `/workbench/${topImage.id}/detail?status=1`
        }

        $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                if (response && response.code == 0) {
                    let redirect =  response.data.redirect
                    window.location.href = redirect;
                }
            },
            error: function (xhr, status, error) {
                console.error('Submission failed:', error);
            }
        });
    });

}
)




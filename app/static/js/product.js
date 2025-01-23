import {Uppy, Dashboard,} from '/static/js/file_upload/uppy.min.mjs'
import zh_CN from '/static/js/file_upload/zh_CN.min.js'

const addNetworkImage = async (url, uppy) => {
    const response = await fetch(url);
    const blob = await response.blob();
    const pathlist = url.split('/')
    uppy.addFile({
        name: pathlist[pathlist.length - 1], // 自定义文件名
        type: blob.type,          // 动态获取文件类型
        data: blob,               // 文件数据
        source: 'remote',
        preview: url,
        isRemote: true,
    });
};

$(document).ready(() => {
    let product = $('#productFormInfo').data('product');
    let isView = $('#productIsView').data('is-view');
    let type = $('#productType').data('type');

    const uppyTop = new Uppy({
        debug: true,
        autoProceed: false,
        restrictions: {
            maxNumberOfFiles: 5,
            allowedFileTypes: ['image/*'],
        }
    }).use(Dashboard, {
        inline: true,
        target: '#product-top-image-area',
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
        disabled: isView == 0
    })
    uppyTop.on('file-removed', (result) => {
        console.log("result: ", result)
        if (isView == 0) {
            uppyTopImage.addFile(result)
        }
    })

    if (product && product.image1) {
        addNetworkImage(product.image1, uppyTop)
    }

    const uppyInfo = new Uppy({
        debug: true,
        autoProceed: false,
        restrictions: {
            maxNumberOfFiles: 5,
            allowedFileTypes: ['image/*'],
        }
    }).use(Dashboard, {
        inline: true,
        target: '#product-info-image-area',
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
        disabled: isView == 0
    })
    uppyInfo.on('file-removed', (result) => {
        console.log("result: ", result)
        if (isView == 0) {
            uppyInfo.addFile(result)
        }
    })

    if (product && product.image2) {
        addNetworkImage(product.image2, uppyInfo)
    }

    $('#productForm').on('submit', function (event) {
        event.preventDefault(); // 阻止表单的默认提交行为
        let formData = new FormData(this); // 序列化表单数据
        if (type == '0') {
            formData.append('credits', formData.get('price'));
        }  

        const files1 = uppyTop.getFiles();
        if (files1 == undefined || files1.length == 0) {
            alert('未选中轮播图片!!!');
            return;
        }
        $.each(files1, function (i, file) {
            formData.append('image1', file.data, file.name);
        });

        const files2 = uppyInfo.getFiles();
        if (files2 == undefined || files2.length == 0) {
            alert('未选中轮播图片!!!');
            return;
        }
        $.each(files2, function (i, file) {
            formData.append('image2', file.data, file.name);
        });

        let url = ""
        if (product.id == null) {
            url = `/product/detail?type=${type}`
        } else {
            url = `/product/${product.id}/detail?type=${type}`
        }
        if (type == 0) {
            formData.append('price', 0);
            formData.append('discount', 1);
        } else {
            formData.append('credits', 0);
        }

        $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                // 请求成功后的回调
                if (response.data && response.data.redirect) {
                    window.location.href = response.data.redirect; // 前端手动跳转
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
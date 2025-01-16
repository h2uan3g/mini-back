import { Uppy, Dashboard, } from '/static/js/file_upload/uppy.min.mjs'
import zh_CN from '/static/js/file_upload/zh_CN.min.js'

async function renderPDF(url, container) {
    try {
        const loadingTask = pdfjsLib.getDocument(url);
        const pdf = await loadingTask.promise;
        for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
            const page = await pdf.getPage(pageNum);
            const scale = 1;
            const viewport = page.getViewport({ scale });
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            canvas.height = viewport.height;
            canvas.width = viewport.width;
            const renderContext = {
                canvasContext: context,
                viewport: viewport,
            };
            await page.render(renderContext).promise;
            container.appendChild(canvas);
        }
    } catch (error) {
        console.error('加载或渲染 PDF 失败:', error);
    }
}

$(document).ready(async () => {
    let documentEl = $('#documentFormInfo').data('document');
    let status = $('#documentStatus').data('status');
    pdfjsLib.GlobalWorkerOptions.workerSrc = '/static/js/pdf/pdf.worker.mjs';

    if (documentEl) {
        if (status == 1 || status == 2) {
            const uppySource = new Uppy({
                debug: true,
                autoProceed: false,
                restrictions: {
                    maxNumberOfFiles: 1,
                    allowedFileTypes: ['application/pdf',
                        'application/msword',
                        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
                }
            })
                .use(Dashboard, {
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
                    maxNumberOfFiles: 1,
                    allowedFileTypes: ['image/*'],
                }
            })
                .use(Dashboard, {
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
                    url = `/doc/${documentEl.id}/detail`
                } else {
                    url = `/doc/detail`
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
        } else if (status == 0) {
            if (documentEl.result_url) {
                const resultUrl = documentEl.result_url;
                const container = document.getElementById('preview-contain');
                if (resultUrl.endsWith("pdf")) {
                    renderPDF(resultUrl, container);

                    const a = document.createElement('a');
                    a.href = resultUrl;
                    a.textContent = "附件下载"
                    document.getElementById("preview-label").appendChild(a);
                } else {
                    let listPath = resultUrl.split("/")
                    let filename = listPath[listPath.length - 1]
                    const response = await fetch(`/visual/result/${filename}`)
                    const data = await response.json()
                    container.innerHTML = data.data

                    const a = document.createElement('a');
                    a.href = resultUrl;
                    a.textContent = "附件下载"
                    document.getElementById("preview-label").appendChild(a);
                }
            }
        }
    }
})
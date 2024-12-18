$(document).ready(() => {
    let data1 = $("#charOptProduct").data("char-opt")
    let chart1 = echarts.init(document.getElementById('echartProduct'));
    chart1.setOption(data1);

    let data2 = $("#charOptCustomer").data("char-opt")
    let chart2 = echarts.init(document.getElementById('echartCustomer'));
    chart2.setOption(data2);
})
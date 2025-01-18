function getColor(v) {
    const colors = ['#ffffe5', '#f7fcb9', '#d9f0a3', '#addd8e', '#78c679', '#41ab5d', '#238443', '#005a32'];
    return v > 50
        ? colors[7]
        : v > 40
            ? colors[6]
            : v > 30
                ? colors[5]
                : v > 20
                    ? colors[4]
                    : v > 10
                        ? colors[3]
                        : v > 5
                            ? colors[2]
                            : v > 0
                                ? colors[1]
                                : colors[0];
}

$(document).ready(() => {
    let data1 = $("#charOptProduct").data("char-opt")
    let chart1 = echarts.init(document.getElementById('echartProduct'));
    chart1.setOption(data1);

    let data2 = $("#charOptCustomer").data("char-opt")
    let chart2 = echarts.init(document.getElementById('echartCustomer'));
    chart2.setOption(data2);

    let data3 = $("#charOptNews").data("char-opt")
    let chart3 = echarts.init(document.getElementById('echartNews'));
    chart3.setOption(data3);


    const scene = new L7.Scene({
        id: 'map-container',
        logoVisible: false,
        map: new L7.GaodeMap({
            pitch: 0,
            mapStyle: 'amap://styles/darkblue',
            center: [116.368652, 39.93866],
            zoom: 10.07
        }),
    });

    scene.on("loaded", () => {
        fetch("https://gw.alipayobjects.com/os/bmw-prod/d6da7ac1-8b4f-4a55-93ea-e81aa08f0cf3.json")
            .then(res => res.json())
            .then(data => {
                const chinaPolygonLayer = new L7.PolygonLayer({
                    autoFit: true
                }).source(data);

                chinaPolygonLayer
                    .color("name", [
                        "rgb(239,243,255)",
                        "rgb(189,215,231)",
                        "rgb(107,174,214)",
                        "rgb(49,130,189)",
                        "rgb(8,81,156)"
                    ])
                    .shape("fill")
                    .style({
                        opacity: 1
                    });
                chinaPolygonLayer.active(true); //  开启默认高亮效果
                chinaPolygonLayer.active({ color: '#2F51E9' }); // 开启并设置高亮颜色为红色
                chinaPolygonLayer.on('mousemove', (e) => {
                    const popup = new L7.Popup({
                        offsets: [0, 0],
                        closeButton: false,
                    })
                        .setLnglat(e.lngLat)
                        .setHTML(
                            `<span>地区: ${e.feature.properties.name}</span><br><span>确诊数: ${e.feature.properties.case}</span>`,
                        );
                    scene.addPopup(popup);
                });


                //  图层边界
                const layer2 = new L7.LineLayer({
                    zIndex: 2
                })
                    .source(data)
                    .color("rgb(93,112,146)")
                    .size(0.6)
                    .style({
                        opacity: 1
                    });

                scene.addLayer(chinaPolygonLayer);
                scene.addLayer(layer2);

                // 加了这一段
                // document.addEventListener(
                //   "click",
                //   () => {
                //     scene.fitBounds([[112, 32], [114, 35]]);
                //   },
                //   false
                // );
            });
        fetch("https://gw.alipayobjects.com/os/bmw-prod/c4a6aa9d-8923-4193-a695-455fd8f6638c.json")
            .then(res => res.json())
            .then(data => {
                const labelLayer = new L7.PointLayer({
                    zIndex: 5
                })
                    .source(data, {
                        parser: {
                            type: "json",
                            coordinates: "center"
                        }
                    })
                    .color("#fff")
                    .shape("name", "text")
                    .size(12)
                    .style({
                        opacity: 1,
                        stroke: "#fff",
                        strokeWidth: 0,
                        padding: [5, 5],
                        textAllowOverlap: false
                    });

                scene.addLayer(labelLayer);
            });
        fetch('https://gw.alipayobjects.com/os/basement_prod/67f47049-8787-45fc-acfe-e19924afe032.json')
            .then(res => res.json())
            .then(nodes => {
                const markerLayer = new L7.MarkerLayer();
                for (let i = 0; i < nodes.length; i++) {
                    if (nodes[i].g !== '1' || nodes[i].v === '') {
                        continue;
                    }
                    const el = document.createElement('label');
                    el.className = 'labelclass';
                    el.textContent = nodes[i].v + '℃';
                    el.style.background = getColor(nodes[i].v);
                    el.style.borderColor = getColor(nodes[i].v);
                    const marker = new L7.Marker({
                        element: el
                    }).setLnglat({ lng: nodes[i].x * 1, lat: nodes[i].y });
                    markerLayer.addMarker(marker);
                }
                scene.addMarkerLayer(markerLayer);
            });
    });


    let mouseOverFlag = false;
    $('.scroll-carousel').on('mouseover', () => {
        mouseOverFlag = true;
    });
    $('.scroll-carousel').on('mouseleave', () => {
        mouseOverFlag = false;
    });
    function scrollList(scroll, height) {
        if (mouseOverFlag) {
            return;
        }
        if (scroll.scrollTop + scroll.offsetHeight >= scroll.scrollHeight) {
            scroll.scrollTop = 0;
          } else {
            scroll.scrollTo({
              top: scroll.scrollTop + height + 8,
              behavior: "smooth",
            });
        }
    }
    setInterval(() => {
        const scrollEl = $('.scroll-carousel')[0];
        const itemEl = $('.scroll-carousel .list-group-item')[0];
        scrollList(scrollEl, itemEl.offsetHeight)
    }, 1000);
})
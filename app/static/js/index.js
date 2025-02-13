async function setCusmer() {
    let customerData = await fetch('/visual/customer')
    let customerJson = await customerData.json()
    let data = customerJson.data

    let xData = data.map(it => `${it.year}-${it.month}`)
    let yData = data.map(it => it.count)
    let echartCustomer = echarts.init(document.getElementById('echartCustomer'));
    echartCustomer.setOption({
        tooltip: {
            trigger: 'item',
        },
        xAxis: {
            type: 'category',
            axisLine: {
                lineStyle: {
                    color: '#FFFFFF'
                }
            },
            data: xData
        },
        yAxis: {
            show: true,
            type: 'value',
            axisLabel: {
                color: '#FFFFFF'
            },
        },
        series: [
            {
                type: 'line',
                data: yData,
                smooth: true
            }
        ],
        grid: {
            top: '8%',
            bottom: '10%',
            left: '8%',
            right: '8%'
        }
    });
}

async function setNews() {
    let newsData = await fetch('/visual/news')
    let newsJson = await newsData.json()
    let data = newsJson.data
    let newsContain = $('#news-list')
    data.forEach(it => {
        newsContain.append(`<a href="#" class="list-group-item list-group-item-action active py-3 lh-sm"
                                aria-current="true">
                                <div class="d-flex w-100 align-items-center justify-content-between">
                                    <strong class="mb-1 title">${it.title}</strong>
                                    <small>${it.auth}</small>
                                </div>
                                <div class="col-10 mb-1 small body">${it.body}</div>
                            </a>`)
    })

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
    if (data.length > 4) {
        setInterval(() => {
            const scrollEl = $('.scroll-carousel')[0];
            const itemEl = $('.scroll-carousel .list-group-item')[0];
            scrollList(scrollEl, itemEl.offsetHeight)
        }, 1000);
    }
}

async function setClassify() {
    let classifyData = await fetch('/visual/classify')
    let classifyJson = await classifyData.json()
    let data = classifyJson.data

    let echartClassify = echarts.init(document.getElementById('echartClassify'))
    echartClassify.setOption({
        tooltip: {
            trigger: 'item'
        },
        legend: {
            top: '2%',
            left: 'center',
            textStyle: {
                color: '#fff',
                fontSize: 12
            },
        },
        series: [
            {
                type: 'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 10,
                    borderColor: '#0A1020',
                    borderWidth: 2
                },
                label: {
                    show: false,
                    position: 'center',
                    color: '#fff'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: 20,
                        fontWeight: 'bold'
                    },
                    itemStyle: {
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                },
                data: data,
            }
        ],
    })
}

async function setCusmerType() {
    let customerTypeData = await fetch('/visual/customer_type')
    let customerTypeJson = await customerTypeData.json()
    let data = customerTypeJson.data
    let xData = data.map(it => it.name)
    let yData = data.map(it => it.value)

    let echartCustomerType = echarts.init(document.getElementById('echartCustomerType'))
    echartCustomerType.setOption({
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        xAxis: {
            type: 'category',
            axisLine: {
                lineStyle: {
                    color: '#FFFFFF'
                }
            },
            data: xData
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                color: '#FFFFFF'
            },
        },
        series: [
            {
                data: yData,
                type: 'bar'
            }
        ],
        grid: {
            top: '8%',
            bottom: '10%',
            left: '8%',
            right: '8%'
        }
    })
}

function setMap() {
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

    scene.on("loaded", async () => {
        const mapData = await fetch("https://gw.alipayobjects.com/os/bmw-prod/d6da7ac1-8b4f-4a55-93ea-e81aa08f0cf3.json")
        const mapJson = await mapData.json()
        const chinaPolygonLayer = new L7.PolygonLayer({
            autoFit: true
        }).source(mapJson);
        chinaPolygonLayer.color("name", [
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
        chinaPolygonLayer.active(true);
        chinaPolygonLayer.active({ color: '#2F51E9' });
        chinaPolygonLayer.on('mousemove', (e) => {
            const popup = new L7.Popup({
                offsets: [0, 0],
                closeButton: false,
            })
                .setLnglat(e.lngLat)
                .setHTML(
                    `<span>地区: ${e.feature.properties.name}</span>`,
                );
            scene.addPopup(popup);
        });
        scene.addLayer(chinaPolygonLayer);

        const layer2 = new L7.LineLayer({
            zIndex: 2
        })
            .source(mapJson)
            .color("rgb(93,112,146)")
            .size(0.6)
            .style({
                opacity: 1
            });


        scene.addLayer(layer2);

        const cityData = await fetch("https://gw.alipayobjects.com/os/bmw-prod/c4a6aa9d-8923-4193-a695-455fd8f6638c.json")
        const cityJson = await cityData.json()
        const labelLayer = new L7.PointLayer({
            zIndex: 5
        })
            .source(cityJson, {
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

        const tempData = await fetch("https://gw.alipayobjects.com/os/basement_prod/67f47049-8787-45fc-acfe-e19924afe032.json")
        const nodes = await tempData.json()
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


        // fetch("https://gw.alipayobjects.com/os/bmw-prod/d6da7ac1-8b4f-4a55-93ea-e81aa08f0cf3.json")
        //     .then(res => res.json())
        //     .then(data => {
        // const chinaPolygonLayer = new L7.PolygonLayer({
        //     autoFit: true
        // }).source(data);

        // chinaPolygonLayer
        //     .color("name", [
        //         "rgb(239,243,255)",
        //         "rgb(189,215,231)",
        //         "rgb(107,174,214)",
        //         "rgb(49,130,189)",
        //         "rgb(8,81,156)"
        //     ])
        //     .shape("fill")
        //     .style({
        //         opacity: 1
        //     });
        // chinaPolygonLayer.active(true); //  开启默认高亮效果
        // chinaPolygonLayer.active({ color: '#2F51E9' }); // 开启并设置高亮颜色为红色
        // chinaPolygonLayer.on('mousemove', (e) => {
        //     const popup = new L7.Popup({
        //         offsets: [0, 0],
        //         closeButton: false,
        //     })
        //         .setLnglat(e.lngLat)
        //         .setHTML(
        //             `<span>地区: ${e.feature.properties.name}</span><br><span>确诊数: ${e.feature.properties.case}</span>`,
        //         );
        //     scene.addPopup(popup);
        // });


        //         //  图层边界
        //         const layer2 = new L7.LineLayer({
        //             zIndex: 2
        //         })
        //             .source(data)
        //             .color("rgb(93,112,146)")
        //             .size(0.6)
        //             .style({
        //                 opacity: 1
        //             });

        //         scene.addLayer(chinaPolygonLayer);
        //         scene.addLayer(layer2);

        //         // 加了这一段
        //         // document.addEventListener(
        //         //   "click",
        //         //   () => {
        //         //     scene.fitBounds([[112, 32], [114, 35]]);
        //         //   },
        //         //   false
        //         // );
        //     });
        // fetch("https://gw.alipayobjects.com/os/bmw-prod/c4a6aa9d-8923-4193-a695-455fd8f6638c.json")
        //     .then(res => res.json())
        //     .then(data => {
        //         const labelLayer = new L7.PointLayer({
        //             zIndex: 5
        //         })
        //             .source(data, {
        //                 parser: {
        //                     type: "json",
        //                     coordinates: "center"
        //                 }
        //             })
        //             .color("#fff")
        //             .shape("name", "text")
        //             .size(12)
        //             .style({
        //                 opacity: 1,
        //                 stroke: "#fff",
        //                 strokeWidth: 0,
        //                 padding: [5, 5],
        //                 textAllowOverlap: false
        //             });

        //         scene.addLayer(labelLayer);
        //     });
        // fetch('https://gw.alipayobjects.com/os/basement_prod/67f47049-8787-45fc-acfe-e19924afe032.json')
        //     .then(res => res.json())
        //     .then(nodes => {
        //         const markerLayer = new L7.MarkerLayer();
        //         for (let i = 0; i < nodes.length; i++) {
        //             if (nodes[i].g !== '1' || nodes[i].v === '') {
        //                 continue;
        //             }
        //             const el = document.createElement('label');
        //             el.className = 'labelclass';
        //             el.textContent = nodes[i].v + '℃';
        //             el.style.background = getColor(nodes[i].v);
        //             el.style.borderColor = getColor(nodes[i].v);
        //             const marker = new L7.Marker({
        //                 element: el
        //             }).setLnglat({ lng: nodes[i].x * 1, lat: nodes[i].y });
        //             markerLayer.addMarker(marker);
        //         }
        //         scene.addMarkerLayer(markerLayer);
        //     });
    });
}

$(document).ready(async () => {
    setCusmer()
    setNews()
    setMap()
    setClassify()
    setCusmerType()
})
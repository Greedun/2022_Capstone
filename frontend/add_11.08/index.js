
//main page
const height = 800;
const width = 1200;

/*const tooltip_info = [
    {ip:"20.168.75.125", peer_id : "DESKTOP-whitehouse", lat:38.89778, lon:-77.03667, region:"US", sent_pps:650, recv_pps:230, dst_lat : 36.7697899, dst_lon : 126.9317528},
    {ip: "192.168.45.55", peer_id : "DESKTOP-soonchunhyang", lat: 36.7697899, lon: 126.9317528, region:"KR", sent_pps: 120, recv_pps : 130, dst_lat : 30.6508899, dst_lon : 104.07572},
    {ip:"192.168.75.125", peer_id : "DESKTOP-lakepark", lat:39.7047104, lon: -105.0813532, region:"US", sent_pps:650, recv_pps:230, dst_lat : 43.8961599, dst_lon : 125.3268},
    {ip: "212.168.80.55", peer_id : "DESKTOP-Jilin", lat: 30.6508899, lon: 104.07572, region:"China", sent_pps: 120, recv_pps : 130, dst_lat : 39.7047104, dst_lon : -105.0813532},
    {ip:"34.168.30.80", peer_id : "DESKTOP-wayWang", lat:43.8961599, lon : 125.3268, region:"China", sent_pps:650, recv_pps:230, dst_lat : 38.89778, dst_lon : -77.03667},
    {ip:"192.168.75.121", peer_id : "DESKTOP-pr0v3rt", lat:36.7962041, lon: 127.1185261, region:"KR", sent_pps:650, recv_pps:230, dst_lat : 36.7697899, dst_lon : 126.9317528},
    {ip:"192.168.201.128", peer_id : "DESKTOP-unkown", lat:33.399111, lon : 126.7850112, region:"KR", sent_pps:650, recv_pps:230, dst_lat : 30.6508899, dst_lon : 126.9317528},
    {ip:"211.179.145.148", peer_id : "DESKTOP-KVS2023143", lat:47.62078950734489, lon : -122.34876836118201, region:"HK", sent_pps:650, recv_pps:230, dst_lat : 36.7697899, dst_lon : 126.9317528},
    {ip:"159.65.50.3", peer_id : "DESKTOP-russia", lat:47.48840015837247, lon : -121.95673075137742, region:"US", sent_pps:650, recv_pps:230, dst_lat : 36.7697899, dst_lon : 126.9317528},
    {ip:"159.65.50.3", peer_id : "DESKTOP-bibibic", lat:42.441439875495334, lon : -107.89482028215407, region:"US", sent_pps:650, recv_pps:230, dst_lat : 43.8961599, dst_lon : -105.0813532},
    {ip:"145.239.95.38", peer_id : "DESKTOP-russia", lat:47.900521374938315, lon : 67.54720270973282, region:"RU", sent_pps:650, recv_pps:230, dst_lat : 39.7047104, dst_lon : -105.0813532},
    {ip:"188.116.183.41", peer_id : "DESKTOP-unkown", lat:41.517946198837244, lon : 64.24871135601376, region:"RU", sent_pps:650, recv_pps:230, dst_lat : 42.441439875495334, dst_lon : -107.89482028215407},
    {ip:"188.215.183.41", peer_id : "DESKTOP-unkown", lat:41.517946198837244, lon : 64.24871135601376, region:"RU", sent_pps:650, recv_pps:230, dst_lat : 47.62078950734489, dst_lon : -121.95673075137742}
]*/

//데이터 파일 읽어오는 부분@@@
function get_traffic_data() {
    const path = "datas\\peers.json"
    d3.json(path).then((data) => {
        //데이터 쓰는 부분을 콜백 함수로 지정해서 data를 가져온 후 전달
        //콜백함수로 지정하지 않고 draw_main을 밖으로 빼면 함수 스코프를 벗어나서 data를 쓸 수 없음.
        //return 시 data는 promise객체로 리턴되기 때문에.. 값을 가져오려면 async await를 쓰거나. 이렇게 하위 스코프로 넣어줘야 함 
        draw_main(data);
    });
}

function draw_main(tooltip_info) {
    console.log(tooltip_info)

    //내 ip
    let my_ip = "192.168.75.121";
    
    //지도 그릴 메인 공간@@@
    const worldmap = d3.select("body").append("svg").classed("worldmap",true)
                       .attr('viewBox',[0,0,width,810]);
    
    //지도 투영법
    const projection = d3.geoMercator().scale(170).translate([width/2,height/1.4]);
    const geo_path = d3.geoPath(projection);
    
    const g = worldmap.append('g');
    //줌 함수@@@
    let zoom = d3.zoom()
                .scaleExtent([1,10])
                .on('zoom', mapzoom);

    init_zoom();

    //지도 json데이터 불러와서 geo-json 형식으로 변환.
    d3.json('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json')
        .then(data=>{
            const countries = topojson.feature(data, data.objects.countries);
            g.selectAll('path').data(countries.features).enter()
            .append('path').classed('country',true).attr('d',geo_path);
        });
    
    
    const loc = worldmap.append("g");
    
    loc
          .selectAll("loc_circle")
          .data(tooltip_info)
          .enter().append("circle").classed("loc_circle",true)
          .attr("cx", d=> projection([d.lon, d.lat])[0])
          .attr("cy", d=> projection([d.lon, d.lat])[1])
          .attr('stroke','none')
          .attr("fill",function(d){
              if(my_ip === d.ip){
                  return "red";
              }
              else
                return "white";
          })
          .attr("r", 5)
          .on("mouseover", tooltips)
          .on("mouseout", hide_tooltip);
    
    
          function tooltips(d){
              d3.select(this).style('fill','#FFD400');
              d3.select("#ip").text(d.srcElement.__data__.ip);
              d3.select("#peer").text(d.srcElement.__data__.peer_id);
              d3.select("#region").text(d.srcElement.__data__.region);
              d3.select("#sent_traffic").text(d.srcElement.__data__.sent_pps);
              d3.select("#recv_traffic").text(d.srcElement.__data__.recv_pps);
              d3.select(".tooltip")
                .style("left", (d.clientX + 20) + 'px')
                .style("top", d.clientY + 'px')
                .style('display','block');
          }
    
          function hide_tooltip(d){
            d3.select(this).style('fill', function(d)
            {
                if(my_ip === d.ip){return "red";}
                else return "white";
            })
            d3.select(".tooltip").style('display','none');
          }
    
    const plus_button = d3.select("#plus")
    
    plus_button
                .on("mouseover", show_menu)
                .on("mouseout", change_color)
    
                function show_menu(d){
                    d3.select(this).style('background-color','white')
                                   .style('color', 'black')
                                   .style('transform', 'rotate(1turn)')
                                   .style('transition', 'all 0.5s');
    
                    var menu = d3.select('.menu_bttns')
                                 .style('display', 'block');
                    menu.on("click", hide_menu);
                    
                }
                
                function change_color(d){
                    d3.select(this).style('background-color','transparent')
                                   .style('color', 'white')
                                   .style('border', '3px solid white')
                                   .style('transform', 'rotate(-1turn)')
                                   .style('transition', 'all 0.5s');
                }
    
                function hide_menu(d){
                    d3.select('.menu_bttns').style('display',' none');
                }

    
    d3.select('#zoom').on('click',()=>{
        zoom.scaleBy(worldmap.transition().duration(500), 1.3);
     });
    
    d3.select("#pan").on("clcik", ()=>{
        zoom.scaleBy(worldmap.transition().duration(500), 1 / 1.5);
    })
    
    //선에 그라데이션 추가 @@@
    const gradient = worldmap.append("defs").append("linearGradient").attr("id","gradcol")

    gradient.append("stop").attr("offset", "0%").attr("stop-color", 'rgb(200, 248, 255)')
    gradient.append("stop").attr("offset", "30%").attr("stop-color", 'rgb(211, 53, 255)')
    gradient.append("stop").attr("offset", "70%").attr("stop-color", 'rgb(93, 0, 255)')
    gradient.append("stop").attr("offset", "95%").attr("stop-color", 'rgb(71, 224, 255)');


    const lines = worldmap.append("g")
    // 패킷 송신지와 수신지를 이어주는 라인
    lines
         .selectAll(".line")
         .data(tooltip_info)
         .enter().append("path").classed('line', true)
         .attr('d', function(d){
            start_x = projection([d.lon, d.lat])[0];
            start_y = projection([d.lon, d.lat])[1];
            dest_x = projection([d.dst_lon, d.dst_lat])[0];
            dest_y = projection([d.dst_lon, d.dst_lat])[1];
            mid_x = (start_x + dest_x) / 2
            mid_y = (start_y + dest_y) / 2.5  
            
            return `M${start_x},${start_y} Q${mid_x},${mid_y} ${dest_x}, ${dest_y}`
    
            }  
         )
         .attr("fill", "transparent")
         .attr("stroke", "url(#gradcol)") //그라데이션 연결@@@
         .attr("stroke-width", 2)
         .attr("strokd-linecap", "round");

    //줌 함수@@@
    function mapzoom(){
       var transform = d3.event.transform;
       g.attr("transform", transform);
    }

    function init_zoom(){
       worldmap.call(zoom);
    }
}

//draw_main 실행하고 역할 끝남.
get_traffic_data();

//main page
const height = 800;
const width = 1600;

const tooltip_info = [
    {ip:"20.168.75.125", peer_id : "DESKTOP-whitehouse", lat:38.89778, lon:-77.03667, region:"US", sent_pps:650, recv_pps:230, dst_lat : 36.7697899, dst_lon : 126.9317528},
    {ip: "192.168.45.55", peer_id : "DESKTOP-soonchunhyang", lat: 36.7697899, lon: 126.9317528, region:"KR", sent_pps: 120, recv_pps : 130, dst_lat : 30.6508899, dst_lon : 104.07572},
    {ip:"192.168.75.125", peer_id : "DESKTOP-lakepark", lat:39.7047104, lon: -105.0813532, region:"US", sent_pps:650, recv_pps:230, dst_lat : 43.8961599, dst_lon : 125.3268},
    {ip: "212.168.80.55", peer_id : "DESKTOP-Jilin", lat: 30.6508899, lon: 104.07572, region:"China", sent_pps: 120, recv_pps : 130, dst_lat : 39.7047104, dst_lon : -105.0813532},
    {ip:"34.168.30.80", peer_id : "DESKTOP-wayWang", lat:43.8961599, lon : 125.3268, region:"China", sent_pps:650, recv_pps:230, dst_lat : 38.89778, dst_lon : -77.03667},
    {ip:"192.168.75.121", peer_id : "DESKTOP-pr0v3rt", lat:36.7962041, lon: 127.1185261, region:"KR", sent_pps:650, recv_pps:230, dst_lat : 36.7697899, dst_lon : 126.9317528}
    
]

//내 ip
let my_ip = "192.168.75.121";

//지도 그릴 메인 공간
const worldmap = 
d3.select(".worldmap").attr('viewBox',[0,0,width,height]);

//지도 투영법
const projection = d3.geoMercator().scale(170).translate([width/2,height/1.4]);
const geo_path = d3.geoPath(projection);

const g = worldmap.append('g');

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
tx = "0 0 7px #fff, 0 0 10px #fff, 0 0 21px #fff, 0 0 42px #b055ff, 0 0 82px #B055FF, 0 0 92px #B055FF, 0 0 102px #B055FF, 0 0 151px #B055FF"

plus_button
            .on("mouseover", show_menu)
            .on("mouseout", change_color)

            function show_menu(d){
                d3.select(this).style('background-color','rgb(192, 101, 238)')
                               .style('color', 'white')
                               .style('text-shadow', tx)
                               .style('transform', 'rotate(1turn)')
                               .style('transition', 'all 0.5s');

                var menu = d3.select('.menu_bttns')
                             .style('display', 'block');
                menu.on("click", hide_menu);
                
            }
            
            function change_color(d){
                d3.select(this).style('background-color','transparent')
                               .style('color', 'rgb(192, 101, 238)')
                               .style('transform', 'rotate(-1turn)')
                               .style('transition', 'all 0.5s');
            }

            function hide_menu(d){
                d3.select('.menu_bttns').style('display',' none');
            }

if(flag === 2){hide_menu};

const lines = worldmap.append("g");


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
     .attr("stroke", "white")
     .attr("stroke-width", 2)
     .attr("strokd-linecap", "round");
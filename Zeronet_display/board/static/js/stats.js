//path="datas/traffic.json"
//traffic = fetch("./datas/traffic.json").then(response => {return response.json()}).then(traffic =>{return traffic});
//import {x} from "../datas/test2.js"
const width=930;
const height=800;
const margin = {top:150, bottom:50, left:50, right:50};
const innerWidth = width-margin.left-margin.right;
const innerHeight = height-margin.top-margin.bottom;
//전달된 데이터 value에 따라 순서대로 scale 생성
const color = d3.scaleOrdinal(['#011FFD','#FF2281','#75D5FD','#B76CFD','#FFD300','#5CE5D5']);
const day = [
    {date: '04-04', amount: 200},
    {date: '04-05', amount: 120},
    {date: '04-06', amount: 520},
    {date: '04-07', amount: 70},
    {date: '04-08', amount: 200},
    {date: '04-09', amount: 120},
    {date: '04-10', amount: 520},
    {date: '04-11', amount: 70}
];


//그래프그릴 영역인 svg생성
const bar_day = d3.select(".day_traffic")
    .attr('height', innerHeight)
    .attr('width', innerWidth)
    .attr('viewBox', [0,0,width,height]);

//그래프 x축
const x = d3.scaleBand()
    .domain(d3.range(day.length)) //원래 데이터
    .range([margin.left, width-margin.right]) //출력 크기
    .paddingInner(0.2)
    .paddingOuter(0.2);

//y축
const y = d3.scaleLinear()
    .domain([0,d3.max(day, d=>d.amount+100)])
    .range([height-margin.bottom, margin.top]);

    //height-margin.bottom, margin.top

//생성해높은 svg영역에 rect생성해 표시
bar_day
    .append('g') //group 생성
    .selectAll('rect')
    .data(day)
    .join('rect')
        .attr('x', (d,i)=>x(i))
        .attr('y', (d)=>y(d.amount)) //svg는 그래프가 아래에서 자라므로 y시작점을 데이터 높이로 지정.
        .attr('height', d=>y(0)-y(d.amount)) // 지정한 높이에서 데이터 크기만큼 자람. 
        .attr('width', x.bandwidth())
        .attr('fill', d=>color(d.amount))
        .attr('class','bar');

//x축, y축 보이게 하기
function xAxis(g){
    g.call(d3.axisBottom(x).tickFormat(i=>day[i].date))
    .attr('font-size','1.2rem')
    .attr('font-family','Courier New')
    .attr('color','white')
    .attr('transform',`translate(0, ${height-margin.bottom})`);
    //svg에서 bottom은 (0,0)인 위쪽이므로 900-50 = 850으로 아래로 내려줌.
}

function yAxis(g){
    g.call(d3.axisLeft(y).ticks(null, day.format))
    .attr('font-size', '1.2rem')
    .attr('font-family','Courier New')
    .attr('color','white')
    .attr('transform',`translate(${margin.left},0)`);

}

bar_day.append('g').call(xAxis);
bar_day.append('g').call(yAxis);

bar_day.append('text')
.text('traffic amount')
.attr('transform','translate(300,80)')
.attr('fill','white')
.attr('font-size','3rem');

/*------------------------------------------------------------------------------------------------------------
pie 그래프 ----------------------------*/

const protos = [
        { name: 'TLS', value : 420},
        { name: 'ARP', value : 220},
        { name: 'TCP', value : 80},
        { name: 'UDP', value : 160},
        { name: 'ICMP', value : 74},
        { name: 'SSDP', value : 60}
];
const week_protos = [
    { name: 'TLS', value : 1250},
    { name: 'ARP', value : 640},
    { name: 'TCP', value : 980},
    { name: 'UDP', value : 1640},
    { name: 'ICMP', value : 450},
    { name: 'SSDP', value : 770}
];

let total = 0;
protos.forEach(d=>total+=d.value);

let w_total =0;
week_protos.forEach(d=>w_total+=d.value);

//그래프 영역에 svg 추가
const pie_g = d3.select('.proto_pie')
    //.attr("position","absolute")
    .attr('height', innerHeight)
    .attr('width', innerWidth)
    .attr('viewBox', [0,0,width,height]);

const radius = 200; //그릴 호의 반지름
const g= pie_g.append('g')
        .attr('transform', "translate(250,415)") //g가 svg의 가운데에 오게끔.

const pie = d3.pie().value(d=>d.value); //pie함수에 키 value의 값을 넘김
const arc = d3.arc().outerRadius(radius).innerRadius(0); //arc 설정
const label = d3.arc().outerRadius(radius+20).innerRadius(20); //데이터 라벨 표시할 호 
const view_pie =
    g.selectAll('.arc').data(pie(protos)).enter()   //arc클래스에 pie 넘김
     .append('g').attr('class','arc'); //arc들의 그룹 생성

//color설정
view_pie.append('path').attr('d',arc)
        .attr('fill',d=>color(d.data.name));
 
//text label append
view_pie.append('text').attr('transform', (d)=>`translate(${arc.centroid(d).map((e, i) => e - (i ? 0 : 15))})`)
//y축으로만 센터가 잡혀서 x축을 20만큼 옆으로 밂.
        .attr('class','label')
        .text(d=>Math.round(d.value/total*100)+"%");

//weekly pie
const week_g= pie_g.append('g')
        .attr('transform', "translate(700,415)") //g가 svg의 가운데에 오게끔.

const w_pie = d3.pie().value(d=>d.value); //pie함수에 키 value의 값을 넘김
const w_arc = d3.arc().outerRadius(radius).innerRadius(0); //arc 설정
const w_label = d3.arc().outerRadius(radius+20).innerRadius(20); //데이터 라벨 표시할 호 
const w_view_pie = week_g.selectAll('.arc').data(pie(week_protos)).enter()   //arc클래스에 pie 넘김
                    .append('g').attr('class','arc'); //arc들의 그룹 생성

//color설정
w_view_pie.append('path').attr('d',arc)
        .attr('fill',d=>color(d.data.name));
 
//text label append
w_view_pie.append('text').attr('transform',d=>`translate(${arc.centroid(d).map((e, i) => e - (i ? 0 : 15))})`)
        .attr('class','label')
        .text(d=>Math.round(d.value/w_total*100)+"%");
    

        /* //마우스 올리면 나타나게 하는거
        view_pie.append('text').attr("transform",d=>`translate(${label.centroid(d)})`)
        .attr("class","hovertext")
        .text(d => d.data.name + d.data.value);
        */

//범례 표시할 그룹
var legends = pie_g.append("g").attr("transform", "translate(0,40)")
                  .selectAll(".legend").data(pie(protos));

var legend = legends.enter().append("g").classed("legend", true)
                    .attr("transform", (d,i)=>`translate(0,${(i+1)*30})`);

legend.append("rect").attr("width",20).attr("height",20).attr("fill",d=>color(d.data.name))
    
legend.append("text").text(d=>d.data.name)
                     .attr("fill", "white")
                     .attr("x",30)
                     .attr("y",20);

pie_g.append('text')
.text('protocol distribution')
.attr('transform','translate(215,80)')
.attr('fill','white')
.attr('font-size','3rem');

//----------------------------------------------------------------------------------------------
//시간별 트래픽량
let t_time =
    { 
    sent_pps :[
        {time : '5:10', p_num : 220},
        {time : '5:20', p_num : 120},
        {time : '5:30', p_num : 98},
        {time : '5:40', p_num : 550},
        {time : '5:50', p_num : 230},
        {time : '6:00', p_num : 10},
        {time : '6:10', p_num : 20},
        {time : '6:20', p_num : 30},
        {time : '6:30', p_num : 70},
        {time : '6:40', p_num : 200},
        {time : '6:50', p_num : 10},
        ],
    sent_bps :[
        {time : '5:10',p_num : 500},
        {time : '5:20',p_num : 780},
        {time : '5:30',p_num : 1000},
        {time : '5:40',p_num : 640},
        {time : '5:50',p_num : 684},
        {time : '6:00',p_num : 700},
        {time : '6:10', p_num : 950},
        {time : '6:20', p_num : 950},
        {time : '6:30', p_num : 600},
        {time : '6:40', p_num : 500},
        {time : '6:50', p_num : 400}
        ],
    rcv_pps:[
        {time : '5:10', p_num : 132},
        {time : '5:20', p_num : 312},
        {time : '5:30', p_num : 142},
        {time : '5:40', p_num : 423},
        {time : '5:50', p_num : 80},
        {time : '6:00', p_num : 100},
        {time : '6:10', p_num : 700},
        {time : '6:20', p_num : 800},
        {time : '6:30', p_num : 600},
        {time : '6:40', p_num : 500},
        {time : '6:50', p_num : 230}
        ],
    rcv_bps:[
            {time : '5:10', p_num : 880},
            {time : '5:20', p_num : 945},
            {time : '5:30', p_num : 435},
            {time : '5:40', p_num : 1234},
            {time : '5:50', p_num : 4321},
            {time : '6:00', p_num : 765},
            {time : '6:10', p_num : 5000},
            {time : '6:20', p_num : 7000},
            {time : '6:30', p_num : 700},
            {time : '6:40', p_num : 550},
            {time : '6:50', p_num : 230}
        ]
    }

const flow = d3.select('.traffic_line')
                //.attr("position","absolute")
                .attr('height',innerHeight)
                .attr('width',innerWidth)
                .attr('viewBox', [0,0,width,height]);

const get_time = () => document.getElementById('input_time').value;

const button = d3.select("#time_bttn")
            .on('click',function(){
                if(get_time() <0 || get_time()>24){
                    alert("0부터 24까지만 입력해주세요.");
                    return false;}
                    
                else if(!get_time()){
                    alert("data required")
                    return false;    
                }
                    
                    draw();
            });


//const flow_g = flow.append("g").classed("timeline",true);

let t_time_key = Object.keys(t_time);
const n = t_time_key.length;


//draw();
function draw(){
    d3.select(".timeline").remove();
    const each_max = [];

    //matching된 time의 그래프만 그리기
    //selected_time = sp.filter(i => i.time.startsWith(get_time()));
    const selected_graph = [];
    //입력한 시간 저장하는 객체
    for(var i=0; i<n; i++){
        selected_graph.push(t_time[t_time_key[i]].filter(i=>i.time.startsWith(get_time())));
        each_max.push(d3.max(selected_graph[i], d=>d.p_num));
    }
    console.log(selected_graph[0]);

    console.log(each_max);

    if(selected_graph[0]==0){
        alert("no data");
    }
    let xScale = d3.scaleBand()
    .domain(d3.range(selected_graph[0].length))
    .range([margin.left,width-margin.right])
    .paddingInner(0.2)
    .paddingOuter(0.2);

    let yScale = d3.scaleLinear()
    .domain([0,d3.max(each_max,(d,i)=>d)])
    .range([height-margin.bottom,margin.top]);

    const flow_g = flow.append("g").classed("timeline",true);

    flow_g.append("g").attr("class",'x axis')
    .attr('transform',`translate(0,${height-margin.bottom})`)
    .call(d3.axisBottom(xScale).tickFormat(selected_graph[0][i].time))
    .attr('font-size','1.2rem')
    .attr('font-family','Courier New')
    .attr('color','white');

    flow_g.append("g").attr("class",'y axis')
    .call(d3.axisLeft(yScale))
    .attr('transform',`translate(${margin.left},0)`)
    .attr('font-size','1.2rem')
    .attr('font-family','Courier New')
    .attr('color','white');
    
    //line 생성
    const line = d3.line()
    .x((d,i)=>xScale(i))
    .y((d,i)=>yScale(d.p_num))
    .curve(d3.curveMonotoneX);

    for(var i=0; i<n; i++){
            flow_g.append('path')
            .datum(selected_graph[i])
            .attr('class','line')
            .attr('d',line)
            .attr('stroke',d=>color(i))
            .attr('transform','translate(0,0)');
    }    

    for(var e=0; e<4; e++){
        flow_g.selectAll("dot")
                    .data(selected_graph[e])
                    .enter().append("circle")
                    .attr("class","circle")
                    .attr("r",3)
                    .attr("cx", (d,e)=> xScale(e))
                    .attr("cy", d=> yScale(d.p_num))
                    .attr("fill",d=>color(e));
                }

    //범례 표시

    var line_legs = flow.append("g").attr("transform", "translate(900,80)")
                        .selectAll(".line_leg").data(selected_graph);

    var line_leg = line_legs.enter().append("g").classed("line_leg", true)
                            .attr("transform", (d,i)=>`translate(0,${i*30})`);

    line_leg.append("rect").attr("width",20).attr("height",20)
                            .attr("transform", "translate(0,65)")
                            .attr("fill",(d,i)=>color(i))

    line_leg.append("text").text((d,i)=>t_time_key[i])
            .attr("fill", "white")
            .attr("x",30)
            .attr("y",80);
}

flow.append('text')
.text('traffic flow')
.attr('transform','translate(300,80)')
.attr('fill','white')
.attr('font-size','3rem');


//---------------------------------------------------------------------------------------------------
//국가별 트래픽량
const country_traffic = [
    {name: 'US', amount: 600},
    {name: 'British', amount: 500},
    {name: 'Kor', amount: 46},
    {name: 'Japan', amount: 52}
];

const cntry = d3.select('.country_traffic')
//.attr("position","absolute")
.attr('height', innerHeight)
.attr('width', innerWidth)
.attr('viewBox', [0,0,width,height]);

const country_x = d3.scaleBand()
    .domain(d3.range(country_traffic.length)) //원래 데이터
    .range([margin.left, width-margin.right]) //출력 크기
    .paddingInner(0.2)
    .paddingOuter(0.2);

//y축
const country_y = d3.scaleLinear()
    .domain([0,d3.max(country_traffic, d=>d.amount+100)])
    .range([height-margin.bottom, margin.top]);


//생성해높은 svg영역에 rect생성해 표시
cntry
    .append('g') //group 생성
    .selectAll('rect')
    .data(country_traffic)
    .join('rect')
        .attr('x', (d,i)=>country_x(i))
        .attr('y', (d)=>country_y(d.amount)) //svg는 그래프가 아래에서 자라므로 y시작점을 데이터 높이로 지정.
        .attr('height', d=>y(0)-country_y(d.amount)) // 지정한 높이에서 데이터 크기만큼 자람. 
        .attr('width', country_x.bandwidth())
        .attr('class','country_bar')
        .attr('fill', (d,i)=>color(d.amount));

//x축, y축 보이게 하기
function c_xAxis(g){
    g.call(d3.axisBottom(country_x).tickFormat(i=>country_traffic[i].name))
    .attr('font-size','1.2rem')
    .attr('font-family','Courier New')
    .attr('color','white')
    .attr('transform',`translate(0, ${height-margin.bottom})`);
    //svg에서 bottom은 (0,0)인 위쪽이므로 900-50 = 850으로 아래로 내려줌.
}

function c_yAxis(g){
    g.call(d3.axisLeft(country_y).ticks(null, country_traffic.format))
    .attr('font-size', '1.2rem')
    .attr('font-family','Courier New')
    .attr('color','white')
    .attr('transform',`translate(${margin.left},0)`);

}

cntry.append('g').call(c_xAxis);
cntry.append('g').call(c_yAxis);
cntry.append('text')
.text('country traffic')
.attr('transform','translate(300,80)')
.attr('fill','white')
.attr('font-size','3rem');

/*-----------------------------------------------------------------------------------------------------------------------
ip별 sent/recv 패킷 수*/
const ip_traffic = [
    {ip:'192.168.75.128',sent:560, recv:20},
    {ip:'192.168.75.129',sent:125, recv:435},
    {ip:'53.168.55.125',sent:103, recv:732},
    {ip:'53.172.75.128',sent:10005, recv:8003},
    {ip:'117.175.20.0',sent:500, recv:640},
    {ip:'117.175.20.2',sent:130, recv:20},
    {ip:'0.0.0.0',sent:50, recv:0},
    {ip:'255.255.255.255',sent:0, recv:432},
    {ip:'117.200.0.0',sent:680, recv:185},
    {ip:'210.168.75.128',sent:54, recv:854},
    {ip:'210.200.75.128',sent:452, recv:159}
]
//svg 속성 설정
const ip_flow = d3.select(".ip_traffic")
                //.attr('position','absolute')
                .attr('width', innerWidth)
                .attr('height',innerHeight)
                .attr('viewBox',[0,0,width,height])

//sent와 recv의 max값 중 제일 큰 것 반환(x축 범위설정할 때 씀)
function max(){
    var sent_max = d3.max(ip_traffic, d=>d.sent);
    var recv_max = d3.max(ip_traffic, d=>d.recv);
    if(sent_max>recv_max){return sent_max;}
    else{return recv_max;}
}
//x축 생성
const ip_x = d3.scaleLinear()
                .domain([0,max()+5000])
                .range([margin.left, width-margin.right]);
//y축
const ip_y = d3.scaleBand()
                .domain(ip_traffic.map(d=>d.ip))
                .range([height-margin.bottom, margin.top])
                .paddingInner(0.2)
                .paddingOuter(0.2);
//그래프 그리는 그룹
//특정 ip에서 보낸 트래픽량
const ip_sent_g = ip_flow.append('g')
                    .selectAll('rect')
                    .data(ip_traffic)
                    .join('rect')
                    .attr('x', margin.left+50)
                    .attr('y',d=>ip_y(d.ip)) //d는 ip_traffic 자체
                    .attr('width',d=>ip_x(d.sent))
                    .attr('fill','#FF2281')
                    .attr('height', ip_y.bandwidth());

//특정 ip에서 받은 트래픽량
const ip_recv_g = ip_flow.append('g')
                    .selectAll('rect')
                    .data(ip_traffic)
                    .join('rect')
                    .attr('x', margin.left+50)
                    .attr('y',d=>ip_y(d.ip))
                    .attr('width',d=>ip_x(d.recv))
                    .attr('fill','#011FFD')
                    .attr('height', ip_y.bandwidth());

//x,y축 부르는 함수
function ip_xaxis(g){
    g.call(d3.axisTop(ip_x).tickFormat(d3.format('.2s')))
    .attr('transform',`translate(${margin.left},${margin.top})`)
    .attr('font-size','1.2rem')
    .attr('font-family','Courier New')
    .attr('color','white');
}

function ip_yaxis(g){
    g.call(d3.axisLeft(ip_y))
    .attr('transform', `translate(${margin.left+50},0)`)
    .attr('font-size','1.2rem')
    .attr('font-family','Courier New')
    .attr('color','white')
}

ip_flow.append('g').call(ip_xaxis);
ip_flow.append('g').call(ip_yaxis);

//범례
const ip_legend = ip_flow.append('g')

ip_legend.append('rect')
.attr('transform',`translate(${width-margin.right},${margin.top-60})`)
.attr('width',40).attr('height',5)
.attr('fill','#FF2281');

ip_legend.append("text").text('sent')
        .attr("fill", "white")
        .attr("x",width-margin.right+50)
        .attr("y",margin.top-55);

ip_legend.append('rect')
        .attr('transform',`translate(${width-margin.right},${margin.top-80})`)
        .attr('width',40).attr('height',5)
        .attr('fill','#011FFD');
        
ip_legend.append("text").text('recv')
                .attr("fill", "white")
                .attr("x",width-margin.right+50)
                .attr("y",margin.top-75);

//그래프이름
ip_flow.append('text')
        .attr('transform', `translate(200, ${margin.top-60})`)
        .text('ip vs traffic flow')
        .attr('font-size','3rem')
        .attr('fill','white');




//---------------------------------------------------------------------------------------------
//tor
const tor = [
    { name: 'tor', value : 72},
    { name: 'not_tor', value : 28}
];

let sum = tor[0].value+tor[1].value;

//그래프 영역에 svg 추가
const torp = d3.select('.tor')
//.attr("position","absolute")
.attr('height', innerHeight)
.attr('width', innerWidth)
.attr('viewBox', [0,0,width,height]);

const torg= torp.append('g')
    .attr('transform', "translate(450,415)") //g가 svg의 가운데에 오게끔.

const pie2 = d3.pie().value(d=>d.value); //pie함수에 키 value의 값을 넘김
const arc2 = d3.arc().innerRadius(100).outerRadius(radius); //arc 설정
const label2 = d3.arc().outerRadius(radius).innerRadius(50); //데이터 라벨 표시할 호 
const view_pie2 =
torg.selectAll('.arc').data(pie(tor)).enter()   //arc클래스에 pie 넘김
 .append('g').attr('class','arc'); //arc들의 그룹 생성

//color설정
view_pie2.append('path').attr('d',arc2)
    .attr('fill',d=>color(d.data.value));

//text label append
view_pie2.append('text').attr('transform',d=>`translate(${arc2.centroid(d)})`)
    .attr('class','label')
    .text(d=>Math.round(d.value/sum*100)+"%");


    /* //마우스 올리면 나타나게 하는거
    view_pie.append('text').attr("transform",d=>`translate(${label.centroid(d)})`)
    .attr("class","hovertext")
    .text(d => d.data.name + d.data.value);
    */

//범례 표시할 그룹
var legends2 = torp.append("g").attr("transform", "translate(650,40)")
              .selectAll(".legend2").data(pie(tor));

var legend2 = legends2.enter().append("g").classed("legend2", true)
                .attr("transform", (d,i)=>`translate(0,${(i+1)*30})`);

legend2.append("rect").attr("width",20).attr("height",20).attr("fill",d=>color(d.data.value))

legend2.append("text").text(d=>d.data.name)
                 .attr("fill", "white")
                 .attr("x",30)
                 .attr("y",20);

torp.append('text')
.text('Tor usage')
.attr('transform','translate(300,80)')
.attr('fill','white')
.attr('font-size','3rem');



    
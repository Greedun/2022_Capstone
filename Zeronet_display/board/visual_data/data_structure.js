//traffic amount 그래프 데이터 형식
//날짜와 해당 날짜에 해당하는 트래픽량
//ex. 05(월)-05(일) 4시 23분 트래픽량: 230byte, 05-05 4시 40분 트래픽량 : 500byte
//--> 05-05 amount : 730
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


//protocol 파이차트 데이터 형식
//하루와 주단위가 있으며, 각각 전체 패킷 중 프로토콜의 개수를 나타냄
//ex하루) 5월5일 3시- TCP :40개, ARP: 30개 -- 4시- TCP:20개, ARP:20개
//--> name:'TCP', value : 60
//    name:'ARP', value: 50개
//ex주단위) 5월5일 - TCP:130개, ARP: 70개
//          5월 6일 - TCP:200개, ARP: 90개
//          5월 10일 - TCP:230개, ARP: 203개
//------->name:'TCP', value: 560
//        name:'ARP', value: 363
//주단위는 7day를 말함. 월요일부터 시작

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


//시간별 트래픽량 데이터 타입
/* sent_ pps : 호스트가 보낸 패킷 개수
   sent_bps : 호스트가 보낸 트래픽량(byte합)
   recv_pps:받은 패킷 개수, recv_bps : 받은 트래픽량

   ex)5:10분 보낸패킷 4개,받은패킷 4개, 보낸패킷 총 길이 : 1200byte, 받은패킷 총 길이: 4000byte
   --> (sent_pps)time: '5:10', p_num:4
       (recv_pps)time: ""    , p_num:4
       (sent_bps)time: ""    , p_num:1200
       (recv_bps)time: "",   , p_num: 4000
*/

//그래프에 표시되는 시간은 5분간격으로 1시간 데이터를 표시
let t_time =
    { 
    sent_pps :[
        {time : '5:10', p_num : 220},
        {time : '5:20', p_num : 120},
        {time : '5:30', p_num : 98},
        {time : '5:40', p_num : 550},
        {time : '5:50', p_num : 230},
        {time : '6:00', p_num : 20}
        ],
    sent_bps :[
        {time : '5:10',p_num : 500},
        {time : '5:20',p_num : 780},
        {time : '5:30',p_num : 1000},
        {time : '5:40',p_num : 640},
        {time : '5:50',p_num : 684},
        {time : '6:00',p_num : 431},
        ],
    rcv_pps:[
        {time : '5:10', p_num : 132},
        {time : '5:20', p_num : 312},
        {time : '5:30', p_num : 142},
        {time : '5:40', p_num : 423},
        {time : '5:50', p_num : 80},
        {time : '6:00', p_num : 342}
        ],
    rcv_bps:[
            {time : '5:10', p_num : 880},
            {time : '5:20', p_num : 945},
            {time : '5:30', p_num : 435},
            {time : '5:40', p_num : 1234},
            {time : '5:50', p_num : 4321},
            {time : '6:00', p_num : 765}
        ]
    }

    

    //국가별 트래픽량 그래프 데이터 타입
    //나라 이름과 해당 나라에서 보낸 총 트래픽량, 총 패킷 개수(추가됨)
    //하루, 주단위 2개 그릴 예정(현재는 하루만 그려놓음)
    //ex)미국에서 보낸 패킷이 4개, 각 패킷의 길이가 60byte라 할 때
    // name:'US', amount:4, len:240
    // amount : 갯수 / len : 패킷의 길이(pkt_size) * amount
    const country_traffic = [
        {name: 'US', amount: 600, len:2560},
        {name: 'British', amount: 500, len:2560},
        {name: 'Kor', amount: 46, len:2560},
        {name: 'Japan', amount: 52, len:2560}
    ];

    const w_country_traffic = [
        {name: 'US', amount: 600, len:2560},
        {name: 'British', amount: 500, len:2560},
        {name: 'Kor', amount: 46, len:2560},
        {name: 'Japan', amount: 52, len:2560}
    ];

    //ip별 보내고 받은 패킷 수(하루 단위)
    //필요하면 주단위 추가 예정
    //ip와 보낸 패킷, 받은 패킷 개수
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

    //토르 사용유무
    //토르를 사용하는 사용자 수와 그렇지 않은 사용자 수
    const tor = [
        { name: 'tor', value : 72},
        { name: 'not_tor', value : 28}
    ];

    //메인페이지 지도 데이터
    //아직 미확정
    //확실한 것은 ip의 위도, 경도 데이터가 필요함

    //예정 타입(확정 ㄴㄴ)
    ip_loc = [
        {ip:'192.168.75.128', lon:53.242123, lat:23.123453, sent:1230, recv:230, ...},
        {ip:'192.168.75.128', lon:53.242123, lat:23.123453, sent:1230, recv:230, ...},
        {ip:'192.168.75.128', lon:53.242123, lat:23.123453, sent:1230, recv:230, ...}
    ]
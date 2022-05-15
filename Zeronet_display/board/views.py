from dataclasses import dataclass
from http.client import IM_USED
import os,re
from struct import pack

from django.shortcuts import render

from . import crawler_library
from scapy.all import*

test_json = {
        'sent_pps' :[
            {'time' : '5:10', 'p_num' : 220},
            {'time' : '5:20', 'p_num' : 120},
            {'time' : '5:30', 'p_num' : 98},
            {'time' : '5:40', 'p_num' : 550},
            {'time' : '5:50', 'p_num' : 230},
            {'time' : '6:00', 'p_num' : 20}    
            ],
        'sent_bps' :[
            {'time' : '5:10', 'p_num' : 500},
            {'time' : '5:20', 'p_num' : 780},
            {'time' : '5:30', 'p_num' : 1000},
            {'time' : '5:40', 'p_num' : 640},
            {'time' : '5:50', 'p_num' : 684},
            {'time' : '6:00', 'p_num' : 431}    
            ],
        'rcv_pps' :[
            {'time' : '5:10', 'p_num' : 132},
            {'time' : '5:20', 'p_num' : 312},
            {'time': '5:30', 'p_num': 142},
            {'time' : '5:40', 'p_num' : 640},
            {'time' : '5:50', 'p_num' : 684},
            {'time' : '6:00', 'p_num' : 431}    
            ],
        'rcv_bps' :[
            {'time' : '5:10', 'p_num' : 880},
            {'time' : '5:20', 'p_num' : 945},
            {'time' : '5:30', 'p_num' : 435},
            {'time' : '5:40', 'p_num' : 1234},
            {'time' : '5:50', 'p_num' : 4321},
            {'time' : '6:00', 'p_num' : 765}    
            ],
        
    }

# Create your views here.
def main(request):
    datas = []
    sent_pps, sent_bps, rcv_pps, rcv_bps = [], [], [], []
    im = []
    sent_pps = test_json['sent_pps']
    sent_bps = test_json['sent_bps']
    rcv_pps = test_json['rcv_pps']
    rcv_bps = test_json['rcv_bps']
    
    data = ''
    im = []
    v_data = []
    # 함수화 시키면 좋을듯
    for datas in sent_pps:
        keyList = datas.keys()
        data = ''
        for item in keyList:
            data = str(data) + str("_") +str(datas[item])
        im.append(data[1:])
    v_data.append(im)
    
    im = []
    for datas in sent_bps:
        keyList = datas.keys()
        data = ''
        for item in keyList:
            data = str(data) + str("_") +str(datas[item])
        im.append(data[1:])

    v_data.append(im)
    
    im = []
    for datas in rcv_pps:
        keyList = datas.keys()
        data = ''
        for item in keyList:
            data = str(data) + str("_") +str(datas[item])
        im.append(data[1:])
    v_data.append(im)
    
    im = []
    for datas in rcv_bps:
        keyList = datas.keys()
        data = ''
        for item in keyList:
            data = str(data) + str("_") +str(datas[item])
        im.append(data[1:])
    v_data.append(im)
    
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    
    # v_data : visual_data
    return render(request, 'main.html',{'v_data':v_data})

def crawler(request):
    res_data = {}
    path_base = os.getcwd()+"/board/crawler_data/"
    
    # 크롤링하는 과정(main)
    crawler_library.tracker_list()
    crawler_library.tor_node_list()
    directory = os.getcwd()+"/board/crawler_data/"
    input_files = os.listdir(directory)
    file_name = os.listdir(directory)
    site = '16FBB4'
    peer_check = 'Peer'
    peer_check2 = 'peer'
    ignore = ["127.0.0.1"]
    ipbox = list()
    site_address = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    
    for filename in input_files:
        if "debug" not in filename:
            continue
        f = open(directory + filename)
        while True:
            line = f.readline()
            site_true = None
            site_true = site in line
            peer_true = None
            peer_true = peer_check in line
            peer_true2 = None
            peer_true2 = peer_check2 in line
            
            if line == '':
                break
            if site_true == True:
                if peer_true == True:
                    address = site_address.findall(line)
                    for ip in address:
                        ipbox.append(ip)
                        
            if site_true == True:
                if peer_true2 == True:
                    address = site_address.findall(line)
                    for ip in address:
                        ipbox.append(ip)
                        
    a_ipbox = list(set(ipbox))
    a_ipbox.sort()
    
    g = open(path_base+"peer", 'w')
    for ip in a_ipbox:
        g.write(f"host {ip} or ")
    
    im_d = []
    boards = []
    
    p = open(path_base+"data", 'w')
    for ip in a_ipbox:
        im_d = []
        tor = crawler_library.check_tor(ip)
        tracker = crawler_library.check_tracker(ip)
        data = crawler_library.user_data(ip)
        country = data['country']
        city = data['city']
        loc = data['loc']

        im_d.append(ip)
        im_d.append(tor)
        im_d.append(tracker)
        im_d.append(country)
        im_d.append(city)
        im_d.append(loc)
        boards.append(im_d)
        p.write(f"{ip} {tor} {tracker} {country} {city} {loc} \n")
    
    p.close()
    g.close()
    del im_d
    
    return render(request,'crawler.html',{'boards':boards})

def packet(request):
    
    res_data = {'test'}
    packets = []
    path_base = os.getcwd()+"/board/packet_data/"
    host = ''
    
    with open(path_base+'traffic', 'r') as f:
        lines = f.readlines()
        # mywrite.write(f"{local_time} {proto_T} {layer_v} {src_ip} {dst_ip} {src_port} {dst_port} {pkt_size}\n")
        # 2022-04-04 04:08:46 TCP None 211.179.145.148 192.168.201.141 40
        for line in lines:
            tmp = list()
            tmp = line.split(' ')[0:6]
            tmp.append("None") #src_port
            tmp.append("None") #dst_port
            tmp.append(line.split(' ')[-1][:-1]) #pkt_size
            packets.append(tmp)
            #print(tmp)
            
    
    '''
    # contents
    with open(path_base+'peer', 'r') as ips:
        for line in ips:
            ip = line.rstrip('\n')
            host += "host" + " " + ip + " " + "or" + " "
    filter = host[:-4]
    load_layer('tls')
    p = sniff(filter = filter, prn=crawler_library.Traffic_Packet, store=0, timeout = 3600)
    print("finish")
    '''
    
    return render(request, 'packet.html',{'packets':packets})
# 패킷 리스팅 페이지를 만들었으니 페이지를 표시하는 것을 구현해야한다.
# json -> txt, csv변환
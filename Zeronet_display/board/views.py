from dataclasses import dataclass
from http.client import IM_USED
import os,re
from struct import pack

from django.shortcuts import render
import pandas as pd

from . import crawler_library
from scapy.all import*

# Create your views here.
def main(request):
    send_json = rawtojson() # 딕셔너리
    print(send_json['sent_pps'])
    
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    
    # v_data : visual_data
    return render(request, 'main.html',{'send_json':send_json})

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

def returnbase(time):
    # 5분단위로 범위 생성하는 로직
    test = int(time[3:6])
    if(test>=10):
        # 10이상
        if(test%10>5):
            # 10으로 나눈 나머지가 5이상
            base_line = time[:3]+str(test-test%5)
        else:
            # 10으로 나눈 나머지가 5미만
            base_line = time[:3]+str(test-test%5)
    else:
        # 10미만
        base_line = time[:3]+"0"+str(test-test%5)
    return base_line

def create_baseline(time):
    baseline_list = []
    hour = int(time[0][:2])
    mins = int(time[0][3:8])
    mins = (mins - mins%5)

    
    for i in range(13):
        if(hour>=10):
            s_hour = str(hour)
        else:
            s_hour = "0"+str(hour)
        
        if(mins>=10):
            s_mins = str(mins)
        else:
            s_mins = "0"+str(mins)
        baseline_list.append(s_hour+":"+s_mins)
        
        mins += 5
        if (mins == 60):
            # 분이 60이 되었을때
            hour += 1
            mins = 0
    return baseline_list

# baseline을 기반으로 json frame을 만들어 준다.
def create_json(baseline_list):
    send_json = {}
    
    l = []
    for b in baseline_list:
        tmp = {}
        tmp['time'] = b
        tmp['p_num'] = 0
        l.append(tmp)
        del tmp
    
    send_json['sent_pps'] = l
    send_json['sent_bps'] = l
    send_json['rcv_pps'] = l
    send_json['rcv_bps'] = l
    
    return send_json

# 원하는 컬럼값을 필터랑하여 카운팅 반환
def count_pps(df_list, cat, my_ip):
    count_packet = None
    count_packet = len(df_list[df_list[cat] == my_ip])
    
    return count_packet

# 원하는 행의 paket_size를 합산
def sum_bps(df_list, cat, my_ip):
    sum_size = pd.to_numeric((df_list[df_list[cat] == my_ip])['pkt_size']).sum()
    return sum_size

def rawtojson():
    res_data = {'test'}
    
    path_base = os.getcwd()+"/board/packet_data/"
    host = ''
    
    raw_data = [] # 이중 리스트
    time = []
    df_list = [] # 12개의 데이터프레임이 들어감. 5분단위의
    col_name = ['local_host_day', 'local_host_time', 'proto_T', 'layer_V', 'src_ip', 'dst_ip', 'src_port', 'dst_port', 'pkt_size']
    
    with open(path_base+'traffic', 'r') as f:
        lines = f.readlines()
        # ['2022-04-04', '05:07:42', 'TCP', 'None', '159.65.50.3', '192.168.201.141', 'None', 'None', '40']
        # mywrite.write(f"{local_time} {proto_T} {layer_v} {src_ip} {dst_ip} {src_port} {dst_port} {pkt_size}\n")
        for line in lines:
            tmp = list()
            tmp = line.split(' ')[0:6]
            tmp.append('None') #src_port
            tmp.append('None') #dst_port
            tmp.append(line.split(' ')[-1][:-1]) #pkt_size
            raw_data.append(tmp)
        
            # 서로 다른 시간의 모음
            if(not tmp[1][:5] in time):
                time.append(tmp[1][:5])
    a_df_list = pd.DataFrame(raw_data, columns=col_name)
        
    
    # 시간별로 데이터 프레임을 리스트에 저장
    for t in range(len(time)):
        #base_line = fiveminute(t,time) # 해당 시간에 포함되는 기준값
        #print(df_list.loc[df_list['local_host_time'].str.contains('04:08')])
        df_list.append(a_df_list.loc[a_df_list['local_host_time'].str.contains(time[t])])
    #print(df_list[0])
    #print(time)
    
    # 처음 시간에 대한 기준점부터 1시간(12개)의 기준 시간을 생성
    base_line = create_baseline(time)
    #print(base_line)
    send_json = create_json(base_line)
    #print(send_json)
    
    # send_pps, send_bps, rcv_pps, rcv_bps
    # df_list : 캡쳐된 시간별로 데이터 모음 -> base_line기준으로 합병
    my_ip = '211.179.145.148'
    for t in range(len(time)):
        base = returnbase(time[t])
        base_i = base_line.index(base)
        pps = count_pps(df_list[t],'src_ip', my_ip)
        send_json['sent_pps'][base_i]['p_num'] += pps
        
        bps = sum_bps(df_list[t],'src_ip', my_ip)
        send_json['sent_bps'][base_i]['p_num'] += bps
        
        pps = sum_bps(df_list[t],'dst_ip', my_ip)
        send_json['rcv_pps'][base_i]['p_num'] += pps
        
        bps = sum_bps(df_list[t],'dst_ip', my_ip)
        send_json['rcv_bps'][base_i]['p_num'] += bps
        
    #print(send_json['sent_pps'])
    #print(send_json['sent_bps'])
    #print(send_json['rcv_pps'])
    #print(send_json['rcv_bps'])      
    
    return send_json

# 현재까지 한것 : 시간별로 데이터 프레임 분할 저장 -> 기준시간(12개)생성 -> send_json의 프레임 완성 -> pps게산 완료 -> bps 계산 완료 -> send_json에 pps, bps반영

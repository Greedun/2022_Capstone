import pandas as pd
import os

my_ip = '211.179.145.148'
path_base = os.getcwd()+"/board/packet_data/"

# 데이터 가공의 main
def data_main():
    res_data = {'test'}

    host = ''
    
    raw_data = [] # 이중 리스트
    time = []
    df_list = [] # 12개의 데이터프레임이 들어감. 5분단위의
    
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
                
    # raw_data : 이중 리스트
    col_name = ['local_host_day', 'local_host_time', 'proto_T', 'layer_V', 'src_ip', 'dst_ip', 'src_port', 'dst_port', 'pkt_size']
    a_df_list = pd.DataFrame(raw_data, columns=col_name)

    # 시간별로 데이터 프레임을 리스트에 저장
    for t in range(len(time)):
        df_list.append(a_df_list.loc[a_df_list['local_host_time'].str.contains(time[t])])
    
    
    # (1) day - list
    day = data_day(df_list, time)
    # (2-1) protos - list
    # (2-2) weak_protos - list
    # (3) t_time - dic
    t_time = rawtojson(df_list, time)
    # (4-1) country_traffic - list
    # (4-2) w_country_traffic - list
    # (5) ip_traffic - list
    # (6) tor - list
    
    # (7) ip_sec - 아직 미완(개발X)
                
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
def create_json(baseline_list, my_ip, time,df_list):
    send_json = {}
    
    l1, l2, l3, l4 = [], [], [], []

    for b in baseline_list:
        tmp = {}
        tmp['time'] = b
        tmp['p_num'] = 0
        l1.append(tmp.copy())
        l2.append(tmp.copy())
        l3.append(tmp.copy())
        l4.append(tmp.copy())
        del tmp

    for t in range(len(time)):
        base = returnbase(time[t])
        base_i = baseline_list.index(base)
        l1[base_i]['p_num'] += count_pps(df_list[t],'src_ip', my_ip)
    send_json['sent_pps'] = l1

    for t in range(len(time)):
        base = returnbase(time[t])
        base_i = baseline_list.index(base)
        l2[base_i]['p_num'] += sum_bps(df_list[t],'src_ip', my_ip)
    send_json['sent_bps'] = l2
    
    for t in range(len(time)):
        base = returnbase(time[t])
        base_i = baseline_list.index(base)
        l3[base_i]['p_num'] += count_pps(df_list[t],'dst_ip', my_ip)
    send_json['rcv_pps'] = l3
    
    for t in range(len(time)):
        base = returnbase(time[t])
        base_i = baseline_list.index(base)
        l4[base_i]['p_num'] += sum_bps(df_list[t],'dst_ip', my_ip)
    send_json['rcv_bps'] = l4
    
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

# (1) t_time
def rawtojson(df_list, time):
    
    # 처음 시간에 대한 기준점부터 1시간(12개)의 기준 시간을 생성
    base_line = create_baseline(time)
    
    # 프론트가 원하는 데이터 형식으로 변환
    t_time = create_json(base_line, my_ip, time, df_list)
    #print(send_json['sent_pps'])

    # send_pps, send_bps, rcv_pps, rcv_bps
    # df_list : 캡쳐된 시간별로 데이터 모음 -> base_line기준으로 합병   
    return t_time

'''
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
'''

# (2) day : [] -> {}
def data_day(df_list, time):
    # basic
    # 처음 시간에 대한 기준점부터 1시간(12개)의 기준 시간을 생성
    base_line = create_baseline(time)
    
    send_list = []

    for b in base_line:
        tmp = {}
        tmp['date'] = b
        tmp['amount'] = 0
        send_list.append(tmp.copy())
        del tmp
    
    for t in range(len(time)):
        base = returnbase(time[t])
        base_i = base_line.index(base)
        amount = len(df_list[t].index)
        send_list[base_i]['amount'] += amount
    
    return send_list

data_main()
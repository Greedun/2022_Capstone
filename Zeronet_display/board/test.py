import pandas as pd
import os, time

from datetime import datetime, timedelta

my_ip = '211.179.145.148'
path_base = os.getcwd()+"/board/packet_data/"

# 데이터 가공의 main
def data_main():
    res_data = {'test'}

    host = ''
    
    raw_data = [] # 이중 리스트
    time = []
    days = []
    df_list = [] # 12개의 데이터프레임이 들어감. 5분단위의
    
    with open(path_base+'traffic3', 'r') as f:
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
                
            if(not tmp[0] in days):
                days.append(tmp[0])
                
    # raw_data : 이중 리스트
    col_name = ['local_host_day', 'local_host_time', 'proto_T', 'layer_V', 'src_ip', 'dst_ip', 'src_port', 'dst_port', 'pkt_size']
    a_df_list = pd.DataFrame(raw_data, columns=col_name)

    # 시간별로 데이터 프레임을 리스트에 저장
    for t in range(len(time)):
        df_list.append(a_df_list.loc[a_df_list['local_host_time'].str.contains(time[t])])
    
    # peer_df test
    p_df_list = peer_df()
    
    # (1) day - list
    day = data_day(df_list, time)
    
    # (2-1) protos - list - 보류
    protos = data_protos(a_df_list,days,1)
    # (2-2) week_protos - list - 추가수정필요
    w_protos = data_protos(a_df_list,days,7)
    
    # (3) t_time - dic
    t_time = rawtojson(df_list, time)
    
    # (4-1) country_traffic - list - 보류
    country = data_country(p_df_list, a_df_list)
    
    # (4-2) week_country_traffic - list
    w_count = data_country(p_df_list, a_df_list)
    
    # (5) ip_traffic - list
    ip_traffic = data_ip(a_df_list)
    # (peer)
    # (6) tor - list
    tor = data_tor(p_df_list)
    
    # => 남은것 country protos -> 일단 week만 구현
    
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
        if base in baseline_list:
            base_i = baseline_list.index(base)
        l1[base_i]['p_num'] += count_pps(df_list[t],'src_ip', my_ip)
    send_json['sent_pps'] = l1

    for t in range(len(time)):
        base = returnbase(time[t])
        if base in baseline_list:
            base_i = baseline_list.index(base)
        l2[base_i]['p_num'] += sum_bps(df_list[t],'src_ip', my_ip)
    send_json['sent_bps'] = l2
    
    for t in range(len(time)):
        base = returnbase(time[t])
        if base in baseline_list:
            base_i = baseline_list.index(base)
        l3[base_i]['p_num'] += count_pps(df_list[t],'dst_ip', my_ip)
    send_json['rcv_pps'] = l3
    
    for t in range(len(time)):
        base = returnbase(time[t])
        if base in baseline_list:
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

# (3) t_time
def rawtojson(df_list, time):
    
    # 처음 시간에 대한 기준점부터 1시간(12개)의 기준 시간을 생성
    base_line = create_baseline(time)
    
    # 프론트가 원하는 데이터 형식으로 변환
    t_time = create_json(base_line, my_ip, time, df_list)
    #print(send_json['sent_pps'])

    # send_pps, send_bps, rcv_pps, rcv_bps
    # df_list : 캡쳐된 시간별로 데이터 모음 -> base_line기준으로 합병   
    return t_time

# (1) day : [] -> {}
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
        if base in base_line:
            base_i = base_line.index(base)
        amount = len(df_list[t].index)
        send_list[base_i]['amount'] += amount
    
    return send_list

# 날짜 기준
def data_protos(a_df_list,days,per):
    
    date=datetime.strptime(days[0],'%Y-%m-%d')
    start = date
    end = start + timedelta(days=per-1)
    
    #end = time[0] + per # 날짜 + 숫자
    days_l = []
    df_list = []
    
    for d in days:
        com = datetime.strptime(d,'%Y-%m-%d')
        if(end >= com):
            days_l.append(com.strftime('%Y-%m-%d'))
    # 시간별로 데이터 프레임을 리스트에 저장
    for t in range(len(days_l)):
        df_list.append(a_df_list.loc[a_df_list['local_host_day'].str.contains(days_l[t])])
    # 프로토콜 타입 추출
    proto_list = []
    proto_list = a_df_list['proto_T'].unique()
    
    if(per == 1):
        send_list = []
        cur = df_list[0]
        
        # days
        for b in proto_list:
            tmp = {}
            tmp['name'] = b
            tmp['value'] = len(cur.loc[cur['proto_T'].str.contains(b)].index)
            send_list.append(tmp.copy())
            del tmp 
            
    elif(per == 7):
        send_list = []
        # frame
        for l in proto_list:
            tmp = {}
            tmp['name'] = l
            tmp['value'] = 0
            send_list.append(tmp.copy())
            del tmp
        
        # week
        for cur_df in df_list:
            for i in range(len(send_list)):
                proto = send_list[i]['name']
                add = len(cur_df.loc[cur_df['proto_T'].str.contains(proto)].index)
                send_list[i]['value'] += add       

    #print(send_list)
    return send_list

def data_ip(a_df_list):
    send_list = []
    
    # ip들 추출
    ip_list = []
    ip_list = list(a_df_list['src_ip'].unique())
    ip_list += list(a_df_list['dst_ip'].unique())
    ip_list = list(set(ip_list))
    
    for ip in ip_list:
        tmp = {}
        tmp['ip'] = ip
        tmp['sent'] = count_pps(a_df_list, 'src_ip', ip)
        tmp['recv'] = count_pps(a_df_list, 'dst_ip', ip)
        send_list.append(tmp.copy())
        del tmp
    
    return send_list

def peer_df():
    raw_data = []
    
    with open(path_base+'data', 'r') as f:
        lines = f.readlines()
        # {ip} {tor} {tracker} {country} {city} {loc} 
        # ['95.110.227.231', 'False', 'tracker', 'IT', 'Ponte San Pietro', '45.7060' ,'9.5905'] 
        for line in lines:
            tmp = list()
            tmp.append(line.split(' ')[0])
            tmp.append(line.split(' ')[1])
            tmp += line.split(' ')[2:4]
            tmp.append((' ').join(line.split(' ')[4:-2]))
            loc = (line.split(' ')[-2])
            tmp += loc.split(',')
            
            raw_data.append(tmp)
    
    col_name = ['ip', 'tor', 'peer&tracker', 'country', 'city', 'loc_lat', 'loc_lng']
    p_df_list = pd.DataFrame(raw_data, columns=col_name)
    
    return p_df_list

def data_tor(p_df_list):
    send_list = []
    t_l = ['tor','non_tor']
    t_b = ['True','False']
    
    for t in range(len(t_l)):
        tmp = {}
        tmp['name'] = t_l[t]
        tmp['value'] = len(p_df_list[p_df_list['tor']==t_b[t]].index)
        send_list.append(tmp.copy())
        del tmp
    
    return send_list

# 'data'파일에서 나라별 ip를 추출 -> 'traffic'에서 ip에 대한 패킷의 갯
def data_country(p_df_list, a_df_list):
    send_list = []
    coun_l = {}
    df_list = []
    c_l = p_df_list['country'].unique()
    #print(p_df_list)
    
    # 나라별로 ip추출 - dic + create frame
    for c in c_l:
        tmp = {}
        ip = p_df_list[p_df_list['country']==c]['ip'].values
        coun_l[c] = list(p_df_list[p_df_list['country']==c]['ip'].values)
        
        tmp['name'] = c
        tmp['amount'] = 0
        tmp['len'] = 0
        send_list.append(tmp.copy())
        del tmp 
        
    # 나라별로 라인 얻고 amount : 갯수 , len : 총 크기
    # 나라별 데이터 프레임 분할 -> coun_l과 함께 이용
    # 데이터 추출은 완료 => 날짜 제한 추가해야함 (day 가장 빠른 하루 / week 가장 빠른 하루 + 6일 범위)
    for c in range(len(c_l)):
        ips = coun_l[c_l[c]]
        amount = 0
        sum_len = 0

        for ip in ips:
            # pkt_size만 모음
            src_size = a_df_list[a_df_list['src_ip']==ip]['pkt_size']
            dst_size = a_df_list[a_df_list['dst_ip']==ip]['pkt_size']
            
            src_size = src_size.astype({'pkt_size':'int'})
            dst_size = dst_size.astype({'pkt_size':'int'})
            
            src_c = len(src_size.index)
            dst_c = len(dst_size.index)
            amount = amount + src_c + dst_c
    
            src_sum = src_size.sum()
            dst_sum = dst_size.sum()

            sum_len = sum_len + src_sum + dst_sum
        
        for l in send_list:
            if l['name'] == c_l[c]:
                l['amount'] = amount
                l['len']=sum_len
    print(send_list)
        
    
        
    return send_list

data_main()
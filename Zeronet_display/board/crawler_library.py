import re
import os
import requests

path_base = os.getcwd()+"/board/packet_data/"
def tracker_list():
    tracker_address = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    f = open(path_base+"trackers", "w")
    with open(path_base+"trackers.json", "r") as tracker:
        while True:
            line = tracker.readline()
            if line == '':
                break;
            address = tracker_address.findall(line)
            for ip in address:
                f.write(f"{ip}\n")
		
def tor_node_list():
	req = requests.get("https://check.torproject.org/exit-addresses")
	req_lines = req.text.split("\n")
	
	path = path_base+"tor"
	with open(path, "w") as node_file:
		for line in req_lines:
			if line.startswith("ExitAddress"):
				ip = line.split(" ")[1]
				node_file.write(f"{ip}\n")
		else:
			return True

def check_tor(ip):
    path = path_base+"tor"
    with open(path, 'r') as tor_ip:
        if ip in tor_ip.read():
            return "True"
        else:
            return "False"
			
def check_tracker(ip):
    path = path_base+"trackers"
    with open(path, 'r') as tracker_ip:
        if ip in tracker_ip.read():
            return "tracker"
        else:
            return "peer"

def user_data(ip):
	address = ip + "/"
	url = f"http://ipinfo.io/{address}json"
	response = requests.get(url)
	data =  response.json()
	return data

def Traffic_Packet(packet):
    if IP in packet:
                layer_v = "None"
                if packet.haslayer(Raw):
                    b = bytes(packet[Raw].load)
                    if b[0] == 0x17:
                        layer_v = "TLS1.3"
                    if b[0] == 0x16:
                        layer_v = "TLS1.2"
                if packet.haslayer(DNS):
                    layer_v = "DNS"

                proto = packet[IP].proto
                proto_T = "None"
                if proto == 1:
                    proto_T = "ICMP"
                if proto == 6:
                    proto_T = "TCP"
                if proto == 17:
                    proto_T = "UDP"

                pkt_size = packet[IP].len
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                src_port = packet[IP].sport
                dst_port = packet[IP].dport

                timestamp = packet.time
                local_time = time.localtime(timestamp)
                local_time = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
                print(f"{local_time} {proto_T} {layer_v} {src_ip} {dst_ip} {src_port} {dst_port} {pkt_size}")
                path = path_base+"traffic"
                with open(path, 'r') as myfile:
                    data = myfile.read()
                    with open('traffic', 'w') as mywrite:
                        mywrite.write(data)
                        mywrite.write(f"{local_time} {proto_T} {layer_v} {src_ip} {dst_ip} {src_port} {dst_port} {pkt_size}\n")
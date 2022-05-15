from scapy.all import*
import time

host = ""


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
                with open('traffic', 'r') as myfile:
                    data = myfile.read()
                    with open('traffic', 'w') as mywrite:
                        mywrite.write(data)
                        mywrite.write(f"{local_time} {proto_T} {layer_v} {src_ip} {dst_ip} {src_port} {dst_port} {pkt_size}\n")
with open('peer', 'r') as ips:
    for line in ips:
        ip = line.rstrip('\n')
        host += "host" + " " + ip + " " + "or" + " "
        
filter = host[:-4]    	
load_layer('tls')
p = sniff(filter = filter, prn=Traffic_Packet, store=0, timeout = 3600)

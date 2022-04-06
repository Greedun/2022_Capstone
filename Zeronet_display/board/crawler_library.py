import re
import os
import requests

path_base = os.getcwd()+"/board/crawler_data/"
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

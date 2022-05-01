def json_to_csv(l_j):
    # 구분자 : ","
    l_csv = []
    for json in l_j:
        line = ''
        l_key = list(l_j[0].keys())
        for key in l_key:
            line = line + str(json[key])+","
        line = line[:-1]+"\n"
        l_csv.append(line)
    print(l_csv)
        

def json_to_txt(l_j):
    # 구분자 : " "
    l_csv = []
    for json in l_j:
        line = ''
        l_key = list(l_j[0].keys())
        for key in l_key:
            line = line + str(json[key])+" "
        line = line[:-1]+"\n"
        l_csv.append(line)
    print(l_csv)

# 리스트
l_j = [
    {'date': '04-04', 'amount': 200},
    {'date': '04-05', 'amount': 120},
    {'date': '04-06', 'amount': 520},
    {'date': '04-07', 'amount': 70}
]
json_to_csv(l_j)
json_to_txt(l_j)
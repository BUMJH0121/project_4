
import csv
import json

region_name_gu = []
region_name_dong = []
service_name = []

with open('./region_name_gu.csv', newline='') as f:
    reader = csv.reader(f)
    region_name_gu = list(reader)

with open('./region_name_dong.csv', newline='') as f:
    reader = csv.reader(f)
    region_name_dong = list(reader)

with open('./service_name_big.csv', newline='') as f:
    reader = csv.reader(f)
    service_name_all = list(reader)
    for a in service_name_all:
        service_name.append(a[3])
    service_name.remove("업종중분류명")
    service_name = set(service_name)

convert_gu = json.dumps(region_name_gu[0], ensure_ascii=False).split(',')
for i in range(len(convert_gu)):
    convert_gu[i] = convert_gu[i].replace('"','').replace('[','').replace(']','').strip()

convert_dong = json.dumps(region_name_dong[0], ensure_ascii=False).split(',')
for i in range(len(convert_dong)):
    convert_dong[i] = convert_dong[i].replace('"','').replace('[','').replace(']','').strip()

region_dict = {}
for i in range(424):
    try:
        region_dict[convert_gu[i]].append(convert_dong[i])
    except:
        temp = [convert_dong[i]]
        region_dict[convert_gu[i]] = temp

convert_gu.sort()
convert_gu = set(convert_gu)


import csv
import json

region_name_gu = []
region_name_dong = []
with open('./region_name_gu.csv', 'rb') as f:
    reader = csv.reader(f)
    region_name_gu = list(reader)

with open('./region_name_dong.csv', 'rb') as f:
    reader = csv.reader(f)
    region_name_dong = list(reader)

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

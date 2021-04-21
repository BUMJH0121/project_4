
import csv
import json

region = []
region_name_gu = []
region_name_dong = []
service_name = []

with open('./dong_coords.json', 'r', encoding='utf-8') as f:
    region = json.load(f)
print(region, type(region))
len_region = len(region)
for d in region:
    region_name_gu.append(d["gu"])
    region_name_dong.append(d["dong"])

with open('./service_name_big.csv', newline='') as f:
    reader = csv.reader(f)
    service_name_all = list(reader)
    for a in service_name_all:
        service_name.append(a[3])
    service_name.remove("업종중분류명")
    service_name = set(service_name)

# convert_gu = json.dumps(region_name_gu[0], ensure_ascii=False).split(',')
# for i in range(len(convert_gu)):
#     convert_gu[i] = convert_gu[i].replace('"','').replace('[','').replace(']','').strip()

# convert_dong = json.dumps(region_name_dong[0], ensure_ascii=False).split(',')
# for i in range(len(convert_dong)):
#     convert_dong[i] = convert_dong[i].replace('"','').replace('[','').replace(']','').strip()

region_dict = {}
for i in range(len_region):
    try:
        region_dict[region_name_gu[i]].append(region_name_dong[i])
    except:
        temp = [region_name_dong[i]]
        region_dict[region_name_gu[i]] = temp

region_name_gu = set(region_name_gu)

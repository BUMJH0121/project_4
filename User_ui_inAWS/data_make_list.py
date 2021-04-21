
import csv
import json
import requests
import pandas as pd

region = []
region_name_gu = []
region_name_dong = []
service_name = []

with open('./dong_coords.json', 'r', encoding='utf-8') as f:
    region = json.load(f)
len_region = len(region)
for d in region:
    region_name_gu.append(d["gu"])
    region_name_dong.append(d["dong"])

with open('./service_name_small.csv', newline='') as f:
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

url = "http://18.206.167.14:20000/data/mysql"
bus_df = pd.read_json(url)
with open("./test.json", "r", encoding="utf-8") as f:
        ddata = json.load(f)
df = pd.DataFrame(ddata)

data = df[(df['gu'] == f'{x}') & (df['dong'] == f'{y}')][['xcode', 'ycode']]
output_df = pd.merge(bus_df, data, on=['xcode', 'ycode'])
stop_nm = np.array(output_df['stop_nm'].tolist())
xcode = np.array(output_df['xcode'].tolist())
ycode = np.array(output_df['ycode'].tolist())
output = {}
for i in range(len(stop_nm)):
    output[stop_nm[i]] = {"xcode": ycode[i], "ycode": xcode[i]}
bus_stop = output
print(bus_stop)


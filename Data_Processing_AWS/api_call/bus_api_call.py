import pandas as pd
import numpy as np

url = "http://18.206.167.14:20000/data/mysql"

## url으로 제공되는 json을 dataframe으로 저장
bus_df = pd.read_json(url)
print(bus_df.reset_index())
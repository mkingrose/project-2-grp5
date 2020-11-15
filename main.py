import os
import requests
import json
import pprint
import numpy as np
import pandas as pd
import flask

worldbank_url = "http://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL"

wb_data = []
wb_response = requests.get(worldbank_url).json()
wb_data.append(wb_response)

wb_df = pd.DataFrame(wb_data)
wb_df.head() 
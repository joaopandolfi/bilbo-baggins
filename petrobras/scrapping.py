# https://curl.trillworks.com/

import requests
from datetime import datetime

data = {}
window = "500"
interval = "60" # day, month
chart_type = "candlestick" # area
period = "1-years" # max

cookies = {
    'PHPSESSID': '3akrers8ivmss7be5bk00kvoi4',
    'geoC': 'BR',
    'adBlockerNewUserDomains': '1547765845',
    'gtmFired': 'OK',
    'StickySession': 'id.45732996909.434.br.investing.com',
    'r_p_s_n': '1',
    'G_ENABLED_IDPS': 'google',
    'SideBlockUser': 'a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A1%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%228849%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A22%3A%22%2Fcommodities%2Fcrude-oil%22%3B%7D%7D%7D%7D',
    'billboardCounter_30': '0',
    'nyxDorf': 'ZWE%2BZTZpMnBkNz42Yi84OzFkZDs%2FJjAwNTZhYg%3D%3D',
}

headers = {
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'https://br.investing.com/commodities/crude-oil',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

params = (
    ('pair_id', '8849'),
    ('pair_id_for_news', '8849'),
    ('chart_type', chart_type),
    ('pair_interval', interval),
    ('candle_count', window),
    ('events', 'yes'),
    ('volume_series', 'yes'),
    ('period', period),
)

response = requests.get('https://br.investing.com/common/modules/js_instrument_chart/api/data.php', headers=headers, params=params, cookies=cookies)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://br.investing.com/common/modules/js_instrument_chart/api/data.php?pair_id=8849&pair_id_for_news=8849&chart_type=area&pair_interval=week&candle_count=120&events=yes&volume_series=yes&period=', headers=headers, cookies=cookies)

json = response.json()
data["petrobras"] = json["candles"]

cookies = {
    'PHPSESSID': '3akrers8ivmss7be5bk00kvoi4',
    'geoC': 'BR',
    'adBlockerNewUserDomains': '1547765845',
    'gtmFired': 'OK',
    'StickySession': 'id.45732996909.434.br.investing.com',
    'r_p_s_n': '1',
    'G_ENABLED_IDPS': 'google',
    'SideBlockUser': 'a%3A2%3A%7Bs%3A10%3A%22stack_size%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Bi%3A8%3B%7Ds%3A6%3A%22stacks%22%3Ba%3A1%3A%7Bs%3A11%3A%22last_quotes%22%3Ba%3A1%3A%7Bi%3A0%3Ba%3A3%3A%7Bs%3A7%3A%22pair_ID%22%3Bs%3A4%3A%228849%22%3Bs%3A10%3A%22pair_title%22%3Bs%3A0%3A%22%22%3Bs%3A9%3A%22pair_link%22%3Bs%3A22%3A%22%2Fcommodities%2Fcrude-oil%22%3B%7D%7D%7D%7D',
    'billboardCounter_30': '0',
    'nyxDorf': 'ZWE%2BZTZpMnBkNz42Yi84OzFkZDs%2FJjAwNTZhYg%3D%3D',
}

headers = {
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'https://br.investing.com/commodities/crude-oil',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

params = (
    ('pair_id', '8849'),
    ('pair_id_for_news', '8849'),
    ('chart_type', chart_type),
    ('pair_interval', interval),
    ('candle_count', window),
    ('events', 'yes'),
    ('volume_series', 'yes'),
    ('period', period),
)

response = requests.get('https://br.investing.com/common/modules/js_instrument_chart/api/data.php', headers=headers, params=params, cookies=cookies)

json = response.json()
data["oil"] = json["candles"]

# Debug

print(data.keys())
print(len(data["oil"]),len(data["petrobras"]))

val = len(data["oil"])
last = data["oil"][val-1]
print(last)

print(datetime.fromtimestamp(last[0]/1000))

# Save data



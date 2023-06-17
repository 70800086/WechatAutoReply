import six
import sys
import requests
import pandas as pd


class Weather:
    def __init__(self):
        self.key = ''  # 高德开放平台key
        self.url = 'https://restapi.amap.com/v3/weather/weatherInfo'
        self.file = './AMap_adcode_citycode_20210406.xlsx'
        self.df = pd.read_excel(self.file)
        self.df.set_index('中文名', inplace=True)

    def get_adcode(self, location):
        try:
            adcode = int(self.df.loc[location, 'adcode'])
        except Exception as e:
            print(f'{sys._getframe().f_code.co_name} {e}')
            adcode = None
        return adcode

    def get_weather_info(self, location='北京市', extensions='base'):
        adcode = self.get_adcode(location)
        if adcode:
            params = {
                'key': self.key,
                'city': adcode,
                'extensions': extensions,
                'output': 'json'
            }
            response = requests.get(self.url, params=params)
            data = response.json()['lives'][0]
            res = {'省份': data['province'], '城市': data['city'], '天气': data['weather'],
                   '风向': data['winddirection'], '风力级别': data['windpower'], '温度': data['temperature_float'],
                   '湿度': data['humidity_float'], '发布数据时间': data['reporttime']}
        else:
            res = '查找的城市不存在'
        return res


if __name__ == '__main__':
    Weather().get_weather_info("\u5357\u5b81\u5e02")

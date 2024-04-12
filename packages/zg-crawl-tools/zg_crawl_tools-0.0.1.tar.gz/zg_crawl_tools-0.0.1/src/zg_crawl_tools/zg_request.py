# _*_ coding : utf-8 _*_
# @Time: 2024/4/12 09:20
# @Author : ZhiBoYuan
# @File : test
# @Project : zg_crawl_tools
import faker
import requests
from typing import Dict
from requests import Response


class ZgRequest():
    def __init__(self):
        pass

    def post(self, url, headers=None, data=None, params=None, **kwargs) -> Response:
        if headers is None:
            headers = self.get_fake_user_agent()
        response = requests.post(url, headers=headers, data=data, params=params, **kwargs)
        return response

    def get(self, url, headers=None, params=None, data=None, **kwargs) -> Response:
        if headers is None:
            headers = self.get_fake_user_agent()
        response = requests.get(url, headers=headers, params=params, data=data, **kwargs)
        return response

    @staticmethod
    def get_fake_user_agent() -> Dict[str, str]:
        fake = faker.Faker()
        return {'User-Agent': fake.user_agent()}

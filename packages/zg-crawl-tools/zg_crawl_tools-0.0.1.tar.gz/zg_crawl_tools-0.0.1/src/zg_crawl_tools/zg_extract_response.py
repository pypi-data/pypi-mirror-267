# _*_ coding : utf-8 _*_
# @Time: 2024/4/12 09:31
# @Author : ZhiBoYuan
# @File : zg_extract_response
# @Project : zg_crawl_tools
import json
from lxml import etree
from requests import Response
from typing import List, Dict, Any, Union


class ZgExtractResponse:

    def __init__(self):
        pass

    @classmethod
    def extarct_json(self, response: Response, extract_rule: str) -> Dict[str, Any]:
        """
        extract json from response
        :param response: 请求返回值
        :param extract_rule: 解析规则，temp [{"name": str}, {"age": int}]
        :return:
        """
        response_json: Dict[str, Any] = response.json()
        ruler = extract_rule.split('>')
        for rule in ruler:
            extract_result: Union[Any, None] = response_json.get(rule, None)
            if extract_result is None:
                return {}
            else:
                response_json = extract_result
        return {"result": response_json}

    @classmethod
    def extact_xpath(self, response: Response, extract_rule: str, format_list: Union[List[str], None] = None) -> str:
        """
        extract xpath from response
        :param response: 请求返回值
        :param extract_rule: 解析规则，temp //div[@class="name"]/text()
        :return:
        """
        response_text: str = response.text
        html = etree.HTML(response_text)
        result = html.xpath(extract_rule)
        result_str_unformat = ''.join(result)
        if not format_list:
            return result_str_unformat
        for format_str in format_list:
            result_str_unformat = result_str_unformat.replace(format_str, '')
        return result_str_unformat


if __name__ == '__main__':
    data = {"name": str}
    key = data.items()
    print(key)


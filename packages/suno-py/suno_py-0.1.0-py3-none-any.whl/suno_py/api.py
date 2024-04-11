import os
import json
import time
import hashlib
import random
from pathlib import Path
from pprint import pprint as pp

from exception import NeedAccessTokenException
from ._base_client import need_login, BaseClient

HEADERS = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    # "authorization": "Bearer ...",
    "dnt": "1",
    "origin": "https://suno.com",
    "referer": "https://suno.com/",
    "sec-ch-ua": "\"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}




class Suno(BaseClient):

    def __init__(self, base_url='https://open.douyin.com', headers=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = base_url
        self.set_headers(headers or HEADERS)
        self.data = {}
        self._access_token = None
        self._open_id = None

    def need_access_token(self):
        """
        检查是否已登录，我们还是只简单检查有没有 access_token
        """
        # self.get_count_message()
        if self._access_token is None:
            raise NeedAccessTokenException()

    def video_list(self, cursor=0, count=10):
        """
        该接口用于分页获取用户所有视频的数据，返回的数据是实时的。该接口适用于抖音

        cursor: 分页游标, 第一页请求cursor是0, response中会返回下一页请求用到的cursor, 同时response还会返回has_more来表明是否有更多的数据
        count: 每页数量

        注意：
        抖音的 OAuth API 以https://open.douyin.com/开头。
        目前暂不支持时间过滤，但相关功能正在评估开发中

        Scope: video.list.bind
        docs: https://developer.open-douyin.com/docs/resource/zh-CN/dop/develop/openapi/video-management/douyin/search-video/account-video-list/
        """
        self.need_access_token()
        url = f"{self.base_url}/api/douyin/v1/video/video_list/?open_id={self._open_id}&cursor={cursor}&count={count}"
        r = self._session.get(url, )
        return self.get_response_data(r)

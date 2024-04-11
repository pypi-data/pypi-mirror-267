import os
import json
import time
import hashlib
import random
from pathlib import Path
from pprint import pprint as pp

from .exception import NeedAccessTokenException
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

    def __init__(self, base_url='https://studio-api.suno.ai', headers=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = base_url
        self.set_headers(headers or HEADERS)
        self.data = {}
        self._access_token = None

    def need_access_token(self):
        """
        检查是否已登录，我们只简单检查有没有 access_token
        """
        if self._access_token is None:
            raise NeedAccessTokenException()

    def get_play_list(self, playlist_id, page=0):
        """
        获取公开的播放列表，不需要登录

        :param playlist_id: 播放列表id
        :param page: 播放列表页数，默认使用0，目前只有一页
        :return:
        """
        url = f'{self.base_url}/api/playlist/{playlist_id}/?page={page}'
        r = self._session.get(url, )
        return r.json()

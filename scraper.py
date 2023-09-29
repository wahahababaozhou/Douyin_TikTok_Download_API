#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author: https://github.com/Evil0ctal/
# @Time: 2021/11/06
# @Update: 2023/09/25
# @Version: 3.1.8
# @Note:
# Core code, valued at 1 bucks (๑•̀ㅂ•́)و✧
# For scraping Douyin/TikTok/Bilibili data and returning it in dictionary form.
# If this project is helpful to you, please give me a star, thank you!
# @备注:
# 核心代码，估值1块(๑•̀ㅂ•́)و✧
# 用于爬取Douyin/TikTok/Bilibili/xigua的数据并以字典形式返回。
# 如果本项目对您有帮助，请给我一个star，谢谢！
import random
import re
import os
import time
import execjs
import aiohttp
import httpx
import platform
import asyncio
import traceback
import configparser
import urllib.parse
import random
from aiosocksy.connector import ProxyConnector, ProxyClientRequest
from zlib import crc32
from typing import Union

from aiohttp_socks import ProxyConnector
from tenacity import *
import aiohttp_socks

class Scraper:
    """__________________________________________⬇️initialization(初始化)⬇️______________________________________"""

    # 初始化/initialization
    def __init__(self):
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }
        self.douyin_api_headers = {
            'accept-encoding': 'gzip, deflate, br',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'referer': 'https://www.douyin.com/',
            'cookie': 'ttwid=1%7C0YBAnAwiC5T3U5yJi8RVXEK3DOwF_2vpJ7kVJJZe8HU%7C1694528301%7Ca9d2d8a4164959a0d7a1f92fe29d37bb779753092ad24d4705a9543707327d49; __live_version__=%221.1.1.3713%22; odin_tt=7cc03fc9dcb682088842ab4494c2862765db476b30ae42ab083e10e8ceb34b88290d1360d16f7c499bac5925e6670a8df72a742a1ebee72ae6ba12fcea622efa; pwa2=%223%7C0%7C0%7C0%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCRXhuWUdqREVBa3ErdjRsT2l3anRIWi9HU2hRNXFseWdJMklLanIxM0orRHozYnA0M2pXc3M3N25CUzdnbE5tTXhHbWU3cldoSE9pdkJvVmNnT2JiWFU9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ==; n_mh=13KNPUKNEzoW3A4J-OLRxfal2zj1GbF-vJUFPs3WSIY; LOGIN_STATUS=0; store-region=us; store-region-src=uid; d_ticket=28acd5a9c6df4227b13582669694acded6ede; my_rd=1; MONITOR_WEB_ID=cf748a1e-9532-4d89-a1fc-13a5729f0942; publish_badge_show_info=%220%2C0%2C0%2C1695295934872%22; IsDouyinActive=true; home_can_add_dy_2_desktop=%220%22; strategyABtestKey=%221695695809.268%22; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1344%2C%5C%22screen_height%5C%22%3A756%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A16%2C%5C%22device_memory%5C%22%3A0%2C%5C%22downlink%5C%22%3A%5C%22%5C%22%2C%5C%22effective_type%5C%22%3A%5C%22%5C%22%2C%5C%22round_trip_time%5C%22%3A0%7D%22; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1695983681533%2C%22type%22%3A1%7D; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A1%7D; passport_csrf_token=56f6961b57a8d08feb7db46160908a87; passport_csrf_token_default=56f6961b57a8d08feb7db46160908a87; s_v_web_id=verify_lmt3fhsw_K7nE3bgs_zkNT_4N3S_BeK7_5x7F8Bgu5fVy; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; msToken=Z9-0y9elP0-Obz51QCWE2WH-JrZ-IHKgyHX6i0Fc7cNUBXQJFSIZjxemEKqgmm4EIxPVWfNPglnGQgzvANzOcW6OA3yzYv1W-plCkw-nP-OkNH00Ion2FohnZl4ySAc=; download_guide=%223%2F20230921%2F0%22; _bd_ticket_crypt_doamin=3; _bd_ticket_crypt_cookie=ddccf5fec8be44d560eb069c2f0bad6b; __security_server_data_status=1; SEARCH_RESULT_LIST_TYPE=%22single%22; xgplayer_user_id=362991673413; _tea_utm_cache_1243=undefined; douyin.com; device_web_cpu_core=16; device_web_memory_size=-1; architecture=amd64; webcast_local_quality=null; __ac_signature=_02B4Z6wo00f01OAvurgAAIDB.GwEB.TxAPDgH74AAF0f4YxOQt1lX7G.X.ym1.H9RXZ8GhgAMPpgMgVFfuGyJ0gwPNH6P21IVw3QQGVundxhs6atZTMMJQnum-pZ5gI-Y7bQVafwXlkIAKs699; tt_scid=WnohADMH48aNQjUPGqPJwRi3J2t3ShdUWylw0d7vHKM4J.wh4sR44Ccd5u5mIH7b7edc; msToken=tQwydd12h5Kq3jUn-FGOBneTMH8TjMOhkj5uQy1kcOogPeYFej3w8_sfGhxOLfRH_VJ1Tg8NDSCNfwch9EZNxHqIg5kgJhdAxtqNMtT8NRV1T_T76MmB3fcaOGNVz0g='
        }
        self.tiktok_api_headers = {
            'User-Agent': 'com.ss.android.ugc.trill/494+Mozilla/5.0+(Linux;+Android+12;+2112123G+Build/SKQ1.211006.001;+wv)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Version/4.0+Chrome/107.0.5304.105+Mobile+Safari/537.36'
        }
        self.bilibili_api_headers = {
            'User-Agent': 'com.ss.android.ugc.trill/494+Mozilla/5.0+(Linux;+Android+12;+2112123G+Build/SKQ1.211006.001;+wv)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Version/4.0+Chrome/107.0.5304.105+Mobile+Safari/537.36'
        }
        self.ixigua_api_headers = {
                    'authority': 'ib.365yg.com',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'zh-CN,zh;q=0.9',
                    'cache-control': 'no-cache',
                    'pragma': 'no-cache',
                    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"macOS"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'none',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }
        # 判断配置文件是否存在/Check if the configuration file exists
        if os.path.exists('config.ini'):
            self.config = configparser.ConfigParser()
            self.config.read('config.ini', encoding='utf-8')
            # 判断是否使用代理
            if self.config['Scraper']['Proxy_switch'] == 'True':
                # 判断是否区别协议选择代理
                if self.config['Scraper']['Use_different_protocols'] == 'False':
                    self.proxies = {
                        'all': self.config['Scraper']['All']
                    }
                else:
                    self.proxies = {
                        'http': self.config['Scraper']['Http_proxy'],
                        'https': self.config['Scraper']['Https_proxy'],
                    }
            else:
                self.proxies = None
        # 配置文件不存在则不使用代理/If the configuration file does not exist, do not use the proxy
        else:
            self.proxies = None
        # 针对Windows系统的异步事件规则/Asynchronous event rules for Windows systems
        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    """__________________________________________⬇️utils(实用程序)⬇️______________________________________"""

    # 检索字符串中的链接/Retrieve links from string
    @staticmethod
    def get_url(text: str) -> Union[str, None]:
        try:
            # 从输入文字中提取索引链接存入列表/Extract index links from input text and store in list
            url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
            # 判断是否有链接/Check if there is a link
            if len(url) > 0:
                return url[0]
        except Exception as e:
            print('Error in get_url:', e)
            return None

    @staticmethod
    def relpath(file):
        """ Always locate to the correct relative path. """
        from sys import _getframe
        from pathlib import Path
        frame = _getframe(1)
        curr_file = Path(frame.f_code.co_filename)
        return str(curr_file.parent.joinpath(file).resolve())

    # 生成X-Bogus签名/Generate X-Bogus signature
    @staticmethod
    def generate_x_bogus_url(url: str, headers: dict) -> str:
        query = urllib.parse.urlparse(url).query
        xbogus = execjs.compile(open('./X-Bogus.js').read()).call('sign', query, headers['User-Agent'])
        new_url = url + "&X-Bogus=" + xbogus
        return new_url

    # 转换链接/convert url
    @retry(stop=stop_after_attempt(4), wait=wait_fixed(7))
    async def convert_share_urls(self, url: str) -> Union[str, None]:
        """
        用于将分享链接(短链接)转换为原始链接/Convert share links (short links) to original links
        :return: 原始链接/Original link
        """
        # 检索字符串中的链接/Retrieve links from string
        url = self.get_url(url)
        # 判断是否有链接/Check if there is a link
        if url is None:
            print('无法检索到链接/Unable to retrieve link')
            return None
        # 判断是否为抖音分享链接/judge if it is a douyin share link
        if 'douyin' in url:
            """
            抖音视频链接类型(不全)：
            1. https://v.douyin.com/MuKhKn3/
            2. https://www.douyin.com/video/7157519152863890719
            3. https://www.iesdouyin.com/share/video/7157519152863890719/?region=CN&mid=7157519152863890719&u_code=ffe6jgjg&titleType=title&timestamp=1600000000&utm_source=copy_link&utm_campaign=client_share&utm_medium=android&app=aweme&iid=123456789&share_id=123456789
            抖音用户链接类型(不全)：
            1. https://www.douyin.com/user/MS4wLjABAAAAbLMPpOhVk441et7z7ECGcmGrK42KtoWOuR0_7pLZCcyFheA9__asY-kGfNAtYqXR?relation=0&vid=7157519152863890719
            2. https://v.douyin.com/MuKoFP4/
            抖音直播链接类型(不全)：
            1. https://live.douyin.com/88815422890
            """
            if 'v.douyin' in url:
                # 转换链接/convert url
                # 例子/Example: https://v.douyin.com/rLyAJgf/8.74
                url = re.compile(r'(https://v.douyin.com/)\w+', re.I).match(url).group()
                print('正在通过抖音分享链接获取原始链接...')
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url, headers=self.headers, proxy=self.proxies, allow_redirects=False,
                                               timeout=10) as response:
                            if response.status == 302:
                                url = response.headers['Location'].split('?')[0] if '?' in response.headers[
                                    'Location'] else \
                                    response.headers['Location']
                                print('获取原始链接成功, 原始链接为: {}'.format(url))
                                return url
                except Exception as e:
                    print('获取原始链接失败！')
                    print(e)
                    # return None
                    raise e
            else:
                print('该链接为原始链接,无需转换,原始链接为: {}'.format(url))
                return url
        # 判断是否为TikTok分享链接/judge if it is a TikTok share link
        elif 'tiktok' in url:
            """
            TikTok视频链接类型(不全)：
            1. https://www.tiktok.com/@tiktok/video/6950000000000000000
            2. https://www.tiktok.com/t/ZTRHcXS2C/
            TikTok用户链接类型(不全)：
            1. https://www.tiktok.com/@tiktok
            """
            if '@' in url:
                print('该链接为原始链接,无需转换,原始链接为: {}'.format(url))
                return url
            else:
                print('正在通过TikTok分享链接获取原始链接...')
                try:
                    proxies = "socks5://127.0.0.1:11080"
                    conn = aiohttp_socks.ProxyConnector.from_url(proxies)
                    async with aiohttp.ClientSession(connector=conn) as session:
                    # connector = ProxyConnector()
                    # socks = 'socks5://127.0.0.1:11080'
                    # async with aiohttp.ClientSession(connector=connector, request_class=ProxyClientRequest) as session:
                        async with session.get(url) as response:
                            print(await response.text())
                            if response.status == 301:
                                url = response.headers['Location'].split('?')[0] if '?' in response.headers[
                                    'Location'] else \
                                    response.headers['Location']
                                print('获取原始链接成功, 原始链接为: {}'.format(url))
                                return url
                            elif response.status == 200:
                                url = response.real_url.raw_host+response.real_url.raw_path
                                return url
                    # proxies = "socks5://127.0.0.1:11080"
                    # conn = aiohttp_socks.ProxyConnector.from_url(proxies)
                    # async with aiohttp.ClientSession(connector=conn) as session:
                    #     async with session.get(url, headers=self.headers, allow_redirects=False,
                    #                            timeout=10) as response:
                    #         if response.status == 301:
                    #             url = response.headers['Location'].split('?')[0] if '?' in response.headers[
                    #                 'Location'] else \
                    #                 response.headers['Location']
                    #             print('获取原始链接成功, 原始链接为: {}'.format(url))
                    #             return url
                except Exception as e:
                    print('获取原始链接失败！')
                    print(e)
                    return None
        elif 'b23.tv' in url or "bilibili" in url:
            """
            bilibili视频链接类型(不全)：
            1. https://b23.tv/Ya65brl
            2. https://www.bilibili.com/video/BV1MK4y1w7MV/
            bilibili用户链接类型(不全)：
            1. https://www.douyin.com/user/MS4wLjABAAAAbLMPpOhVk441et7z7ECGcmGrK42KtoWOuR0_7pLZCcyFheA9__asY-kGfNAtYqXR?relation=0&vid=7157519152863890719
            bilibili直播链接类型(不全)：
            """
            if 'b23.tv' in url:
                print('正在通过哔哩哔哩分享链接获取原始链接...')
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url, headers=self.headers, proxy=self.proxies, allow_redirects=False,
                                               timeout=10) as response:
                            if response.status == 302:
                                url = response.headers['Location'].split('?')[0] if '?' in response.headers[
                                    'Location'] else \
                                    response.headers['Location']
                                print('获取原始链接成功, 原始链接为: {}'.format(url))
                                return url
                except Exception as e:
                    print('获取原始链接失败！')
                    print(e)
                    # return None
                    raise e
            else:
                print('该链接为原始链接,无需转换,原始链接为: {}'.format(url))
                return url
        elif 'ixigua.com' in url:
            """
            西瓜视频链接类型(不全)：
            1. https://v.ixigua.com/ienrQ5bR/
            2. https://www.ixigua.com/7270448082586698281
            3. https://m.ixigua.com/video/7270448082586698281
            西瓜用户链接类型(不全)：
            1. https://www.ixigua.com/home/3189050062678823
            西瓜直播链接类型(不全)：
            """
            if 'v.ixigua.com' in url:
                print('正在通过西瓜分享链接获取原始链接...')
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url, headers=self.ixigua_api_headers, proxy=self.proxies, allow_redirects=False,
                                               timeout=10) as response:
                            print("asdfasdf",response.headers)
                            if response.status == 302:
                                url = response.headers['Location'].split('?')[0] if '?' in response.headers[
                                    'Location'] else \
                                    response.headers['Location']
                                print('获取原始链接成功, 原始链接为: {}'.format(url))
                                return url
                except Exception as e:
                    print('获取原始链接失败！')
                    print(e)
                    # return None
                    raise e
            else:
                print('该链接为原始链接,无需转换,原始链接为: {}'.format(url))
                return url

    """__________________________________________⬇️Douyin methods(抖音方法)⬇️______________________________________"""

    # 生成抖音X-Bogus签名/Generate Douyin X-Bogus signature
    # 下面的代码不能保证稳定性，随时可能失效/ The code below cannot guarantee stability and may fail at any time
    def generate_x_bogus_url(self, url: str) -> str:
        """
        生成抖音X-Bogus签名
        :param url: 视频链接
        :return: 包含X-Bogus签名的URL
        """
        # 调用JavaScript函数
        query = urllib.parse.urlparse(url).query
        xbogus = execjs.compile(open(self.relpath('./X-Bogus.js')).read()).call('sign', query,
                                                                                self.headers['User-Agent'])
        # print('生成的X-Bogus签名为: {}'.format(xbogus))
        new_url = url + "&X-Bogus=" + xbogus
        return new_url

    # 获取抖音视频ID/Get Douyin video ID
    async def get_douyin_video_id(self, original_url: str) -> Union[str, None]:
        """
        获取视频id
        :param original_url: 视频链接
        :return: 视频id
        """
        # 正则匹配出视频ID
        try:
            video_url = await self.convert_share_urls(original_url)
            # 链接类型:
            # 视频页 https://www.douyin.com/video/7086770907674348841
            if '/video/' in video_url:
                key = re.findall('/video/(\d+)?', video_url)[0]
                # print('获取到的抖音视频ID为: {}'.format(key))
                return key
            # 发现页 https://www.douyin.com/discover?modal_id=7086770907674348841
            elif 'discover?' in video_url:
                key = re.findall('modal_id=(\d+)', video_url)[0]
                # print('获取到的抖音视频ID为: {}'.format(key))
                return key
            # 直播页
            elif 'live.douyin' in video_url:
                # https://live.douyin.com/1000000000000000000
                video_url = video_url.split('?')[0] if '?' in video_url else video_url
                key = video_url.replace('https://live.douyin.com/', '')
                # print('获取到的抖音直播ID为: {}'.format(key))
                return key
            # note
            elif 'note' in video_url:
                # https://www.douyin.com/note/7086770907674348841
                key = re.findall('/note/(\d+)?', video_url)[0]
                # print('获取到的抖音笔记ID为: {}'.format(key))
                return key
        except Exception as e:
            print('获取抖音视频ID出错了:{}'.format(e))
            return None

    # 获取单个抖音视频数据/Get single Douyin video data
    @retry(stop=stop_after_attempt(4), wait=wait_fixed(7))
    async def get_douyin_video_data(self, video_id: str) -> Union[dict, None]:
        """
        :param video_id: str - 抖音视频id
        :return:dict - 包含信息的字典
        """
        try:
            # 构造访问链接/Construct the access link
            api_url = f"https://www.douyin.com/aweme/v1/web/aweme/detail/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id={video_id}&pc_client_type=1&version_code=190500&version_name=19.5.0&cookie_enabled=true&screen_width=1344&screen_height=756&browser_language=zh-CN&browser_platform=Win32&browser_name=Firefox&browser_version=110.0&browser_online=true&engine_name=Gecko&engine_version=109.0&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=&platform=PC&webid=7158288523463362079&msToken=abL8SeUTPa9-EToD8qfC7toScSADxpg6yLh2dbNcpWHzE0bT04txM_4UwquIcRvkRb9IU8sifwgM1Kwf1Lsld81o9Irt2_yNyUbbQPSUO8EfVlZJ_78FckDFnwVBVUVK"
            api_url = self.generate_x_bogus_url(api_url)
            # 访问API/Access API
            print("正在请求抖音视频API: {}".format(api_url))
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, headers=self.douyin_api_headers, proxy=self.proxies,
                                       timeout=10) as response:
                    response = await response.json()
                    # 获取视频数据/Get video data
                    video_data = response['aweme_detail']
                    # print('获取视频数据成功！')
                    # print("抖音API返回数据: {}".format(video_data))
                    return video_data
        except Exception as e:
            raise ValueError(f"获取抖音视频数据出错了: {e}")

    # 获取单个抖音直播视频数据/Get single Douyin Live video data
    @retry(stop=stop_after_attempt(4), wait=wait_fixed(7))
    async def get_douyin_live_video_data(self, web_rid: str) -> Union[dict, None]:
        try:
            # 构造访问链接/Construct the access link
            api_url = f"https://live.douyin.com/webcast/web/enter/?aid=6383&web_rid={web_rid}"
            # 访问API/Access API
            print("正在请求抖音直播API: {}".format(api_url))
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, headers=self.douyin_api_headers, proxy=self.proxies,
                                       timeout=10) as response:
                    response = await response.json()
                    # 获取视频数据/Get video data
                    video_data = response['data']
                    print(video_data)
                    print('获取视频数据成功！')
                    # print("抖音API返回数据: {}".format(video_data))
                    return video_data
        except Exception as e:
            print('获取抖音视频数据失败！原因:{}'.format(e))
            # return None
            raise e

    """__________________________________________⬇️TikTok methods(TikTok方法)⬇️______________________________________"""

    # 获取TikTok视频ID/Get TikTok video ID
    async def get_tiktok_video_id(self, original_url: str) -> Union[str, None]:
        """
        获取视频id
        :param original_url: 视频链接
        :return: 视频id
        """
        try:
            # 转换链接/Convert link
            original_url = await self.convert_share_urls(original_url)
            # 获取视频ID/Get video ID
            if '/video/' in original_url:
                video_id = re.findall('/video/(\d+)', original_url)[0]
            elif '/v/' in original_url:
                video_id = re.findall('/v/(\d+)', original_url)[0]
            # print('获取到的TikTok视频ID是{}'.format(video_id))
            # 返回视频ID/Return video ID
            return video_id
        except Exception as e:
            print('获取TikTok视频ID出错了:{}'.format(e))
            return None

    @retry(stop=stop_after_attempt(4), wait=wait_fixed(7))
    async def get_tiktok_video_data(self, video_id: str) -> Union[dict, None]:
        """
        获取单个视频信息
        :param video_id: 视频id
        :return: 视频信息
        """
        # print('正在获取TikTok视频数据...')
        try:
            # 构造访问链接/Construct the access link
            api_url = f'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={video_id}'
            print("正在获取视频数据API: {}".format(api_url))
            proxies = "socks5://127.0.0.1:11080"
            conn = aiohttp_socks.ProxyConnector.from_url(proxies)
            async with aiohttp.ClientSession(connector=conn) as session:
                async with session.get(api_url, headers=self.tiktok_api_headers,
                                       timeout=10) as response:
                    response = await response.json()
                    video_data = response['aweme_list'][0]
                    # print('获取视频信息成功！')
                    return video_data
        except Exception as e:
            print('获取视频信息失败！原因:{}'.format(e))
            # return None
            raise e

    """__________________________________________⬇️bilibili methods(Bilibili方法)⬇️______________________________________"""

    # 获取bilibili视频ID/Get BiliBili video ID
    async def get_bilibili_video_id(self, original_url: str) -> Union[str, None]:
        """
        获取视频id
        :param original_url: 视频链接
        :return: 视频id
        """
        try:
            # 转换链接/Convert link
            original_url = await self.convert_share_urls(original_url)
            if "video/BV" in original_url:
                match = re.search(r"video/BV(?P<id>[0-9a-zA-Z]+)", original_url)
                if match:
                    return f"video/BV{match.group('id')}"
            elif "video/av" in original_url:
                match = re.search(r"video/av(?P<id>[0-9a-zA-Z]+)", original_url)
                if match:
                    return f"video/av{match.group('id')}"
            # 如果未找到匹配项，可以选择抛出异常或返回 None，这里我选择返回 None
            return None
        except Exception as e:
            raise ValueError(f'获取BiliBili视频ID出错了:{e}')

    @retry(stop=stop_after_attempt(4), wait=wait_fixed(7))
    async def get_bilibili_video_data(self, video_id: str) -> Union[dict, None]:
        """
        获取单个视频信息
        :param video_id: 视频id
        :return: 视频信息
        """
        print('正在获取BiliBili视频数据...')
        try:
            # 构造访问链接/Construct the access link
            api_url = f'https://api.bilibili.com/x/web-interface/view?bvid={video_id.replace("video/BV", "")}'
            if "video/av" in video_id:
                api_url = f'https://api.bilibili.com/x/web-interface/view?aid={video_id.replace("video/av", "")}'
            print(f"正在获取视频数据API: {api_url}")
            # 这里获取的是m端端播放地址，清晰度不高，需要请求两次 第一次拿需要端参数第二次才能拿到最终的播放地址
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, headers=self.bilibili_api_headers, proxy=self.proxies,
                                       timeout=10) as response:
                    response = await response.json()
                    avid = response.get("data", {}).get("aid", "")
                    cid = response.get("data", {}).get("cid", "")
                    print('获取视频信息成功！')
            play_url_api = f"https://api.bilibili.com/x/player/playurl?avid={avid}&cid={cid}&platform=html5"  # platform 参数得加上不加上获取的播放地址403 待解决
            async with aiohttp.ClientSession() as session:
                async with session.get(play_url_api, headers=self.bilibili_api_headers, proxy=self.proxies,
                                       timeout=10) as response:
                    response = await response.json()
                    video_data = response.get("data", {}).get("durl", [])[0]["url"]
                    video_data = {
                        'status': 'success',
                        'message': "更多接口请查看(More API see): https://api.tikhub.io/",
                        'type': 'video',
                        'platform': 'bilibili',
                        'video_url': video_data,
                    }
            return video_data
        except Exception as e:
            raise ValueError(f'获取BiliBili视频数据出错了:{e}')


    """__________________________________________⬇️xigua methods(xigua方法)⬇️______________________________________"""
    # 获取西瓜拿播放地址的接口
    def get_xigua_json_url(self,video_id):
        # 获取json文件的地址
        r = str(random.random())[2:]
        url_part = "/video/urls/v/1/toutiao/mp4/{}?r={}".format(video_id, r)
        s = crc32(url_part.encode())
        json_url = "https://ib.365yg.com{}&s={}&nobase64=true".format(url_part, s)
        return json_url
    # 获取西瓜视频ID/Get xigua video ID
    async def get_ixigua_video_id(self, original_url: str) -> Union[str, None]:
        """
        获取视频id
        :param original_url: 视频链接
        :return: 视频id
        """
        try:
            # 转换链接/Convert link
            original_url = await self.convert_share_urls(original_url)
            # 获取视频ID/Get video ID
            if 'www.ixigua.com/' in original_url:
                video_id = re.findall('ixigua\.com/(\d+)', original_url)[0]
            elif 'm.ixigua.com/video' in original_url:
                video_id = re.findall('/video/(\d+)', original_url)[0]
            # 返回视频ID/Return video ID
            return video_id
        except Exception as e:
            raise ValueError(f'获取西瓜视频ID出错了:{e}')

    @retry(stop=stop_after_attempt(4), wait=wait_fixed(7))
    async def get_ixigua_video_data(self, video_id: str) -> Union[dict, None]:
        """
        获取单个视频信息
        :param video_id: 视频id
        :return: 视频信息
        """
        print('正在获取西瓜视频数据...')
        try:
            # 构造访问链接/Construct the access link
            video_url = f'https://m.ixigua.com/video/{video_id}?wid_try=1'
            print("video_url",video_url)
            async with aiohttp.ClientSession() as session:
                async with session.get(video_url, headers=self.ixigua_api_headers, proxy=self.proxies,
                                       timeout=10) as response:
                    response = await response.text()
                    search = re.search("\"vid\":\"([^\"]+)\",", response)
                    vid = search.group(1)
                    print('获取视频vid信息成功！')
                    play_url_api = self.get_xigua_json_url(vid)
            print(f"正在获取视频数据API: {play_url_api}")
            async with aiohttp.ClientSession() as session:
                async with session.get(play_url_api, headers=self.ixigua_api_headers, proxy=self.proxies,
                                       timeout=10) as response:
                    response = await response.json()
                    video_data = response.get("data",{}).get("video_list",{}).get("video_3",{}).get("main_url","")
                    video_data = {
                        'status': 'success',
                        'message': "更多接口请查看(More API see): https://api.tikhub.io/",
                        'type': 'video',
                        'platform': '西瓜',
                        'video_url': video_data,
                    }
            return video_data
        except Exception as e:
            raise ValueError(f'获取西瓜视频数据出错了:{e}')

    """__________________________________________⬇️Hybrid methods(混合方法)⬇️______________________________________"""

    # 判断链接平台/Judge link platform
    async def judge_url_platform(self, video_url: str) -> str:
        if 'douyin' in video_url:
            url_platform = 'douyin'
        elif 'bilibili' in video_url:
            url_platform = 'bilibili'
        elif 'xigua' in video_url:
            url_platform = 'xigua'
        elif 'tiktok' in video_url:
            url_platform = 'tiktok'
        else:
            url_platform = None
        return url_platform

    # 自定义获取数据/Custom data acquisition
    async def hybrid_parsing(self, video_url: str) -> dict:
        # URL平台判断/Judge URL platform
        url_platform = await self.judge_url_platform(video_url)

        # 如果不是指定平台抛出异常/If it is not the specified platform, an exception is thrown
        if not url_platform:
            raise ValueError(f"链接**{video_url}**不是抖音、Bilibili、TikTok链接！")

        print(f"正在解析**{url_platform}**视频链接...")

        # 获取视频ID/Get video ID
        video_id = await self.get_douyin_video_id(video_url) if url_platform == 'douyin' \
            else await self.get_tiktok_video_id(video_url) if url_platform == 'tiktok' \
            else await self.get_bilibili_video_id(video_url) if url_platform == 'bilibili' \
            else await self.get_ixigua_video_id(video_url) if url_platform == 'xigua' \
            else None

        # 如果获取不到视频ID抛出异常/If the video ID cannot be obtained, an exception is thrown
        if not video_id:
            raise ValueError(f"获取**{url_platform}**视频ID失败！")

        print(f"获取到的**{url_platform}**视频ID是{video_id}")
        # 获取视频数据/Get video data
        data = await self.get_douyin_video_data(video_id) if url_platform == 'douyin' \
            else await self.get_tiktok_video_data(video_id) if url_platform == 'tiktok' \
            else await self.get_bilibili_video_data(video_id) if url_platform == 'bilibili' \
            else await self.get_ixigua_video_data(video_id) if url_platform == 'xigua' \
            else None

        if data:

            # 如果是Bilibili平台则返回视频数据/If it is a Bilibili platform, return video data
            if url_platform == 'bilibili':
                print("获取Bilibili视频数据成功！")
                return data
            # 如果是西瓜平台则返回视频数据/If it is a ixigua platform, return video data
            if url_platform == 'xigua':
                print("获取西瓜视频数据成功！")
                return data

            # 如果是抖音/TikTok平台则继续进行数据解析/If it is a Douyin/TikTok platform, continue to parse the data
            print(f"获取**{url_platform}**视频数据成功，正在判断数据类型...")
            url_type_code = data['aweme_type']
            # 以下为抖音或TikTok类型代码/Type code for Douyin or TikTok
            url_type_code_dict = {
                # 抖音/Douyin
                2: 'image',
                4: 'video',
                68: 'image',
                # TikTok
                0: 'video',
                51: 'video',
                55: 'video',
                58: 'video',
                61: 'video',
                150: 'image'
            }
            # 判断链接类型/Judge link type
            url_type = url_type_code_dict.get(url_type_code, 'video')
            print(f"获取到的**{url_platform}**的链接类型是{url_type}")
            print("准备开始判断并处理数据...")

            """
            以下为(视频||图片)数据处理的四个方法,如果你需要自定义数据处理请在这里修改.
            The following are four methods of (video || image) data processing. 
            If you need to customize data processing, please modify it here.
            """

            """
            创建已知数据字典(索引相同)，稍后使用.update()方法更新数据
            Create a known data dictionary (index the same), 
            and then use the .update() method to update the data
            """

            result_data = {
                'status': 'success',
                'message': "更多接口请查看(More API see): https://api.tikhub.io/",
                'type': url_type,
                'platform': url_platform,
                'aweme_id': video_id,
                'official_api_url':
                    {
                        "User-Agent": self.headers["User-Agent"],
                        "api_url": f"https://www.iesdouyin.com/aweme/v1/web/aweme/detail/?aweme_id={video_id}&aid=1128&version_name=23.5.0&device_platform=android&os_version=2333&Github=Evil0ctal&words=FXXK_U_ByteDance"
                    } if url_platform == 'douyin'
                    else
                    {
                        "User-Agent": self.tiktok_api_headers["User-Agent"],
                        "api_url": f'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={video_id}'
                    },
                'desc': data.get("desc"),
                'create_time': data.get("create_time"),
                'author': data.get("author"),
                'music': data.get("music"),
                'statistics': data.get("statistics"),
                'cover_data': {
                    'cover': data.get("video").get("cover"),
                    'origin_cover': data.get("video").get("origin_cover"),
                    'dynamic_cover': data.get("video").get("dynamic_cover")
                },
                'hashtags': data.get('text_extra'),
            }
            # 创建一个空变量，稍后使用.update()方法更新数据/Create an empty variable and use the .update() method to update the data
            api_data = None
            # 判断链接类型并处理数据/Judge link type and process data
            try:
                # 抖音数据处理/Douyin data processing
                if url_platform == 'douyin':
                    # 抖音视频数据处理/Douyin video data processing
                    if url_type == 'video':
                        print("正在处理抖音视频数据...")
                        # 将信息储存在字典中/Store information in a dictionary
                        uri = data['video']['play_addr']['uri']
                        wm_video_url = data['video']['play_addr']['url_list'][0]
                        wm_video_url_HQ = f"https://aweme.snssdk.com/aweme/v1/playwm/?video_id={uri}&radio=1080p&line=0"
                        nwm_video_url = wm_video_url.replace('playwm', 'play')
                        nwm_video_url_HQ = f"https://aweme.snssdk.com/aweme/v1/play/?video_id={uri}&ratio=1080p&line=0"
                        api_data = {
                            'video_data':
                                {
                                    'wm_video_url': wm_video_url,
                                    'wm_video_url_HQ': wm_video_url_HQ,
                                    'nwm_video_url': nwm_video_url,
                                    'nwm_video_url_HQ': nwm_video_url_HQ
                                }
                        }
                    # 抖音图片数据处理/Douyin image data processing
                    elif url_type == 'image':
                        print("正在处理抖音图片数据...")
                        # 无水印图片列表/No watermark image list
                        no_watermark_image_list = []
                        # 有水印图片列表/With watermark image list
                        watermark_image_list = []
                        # 遍历图片列表/Traverse image list
                        for i in data['images']:
                            no_watermark_image_list.append(i['url_list'][0])
                            watermark_image_list.append(i['download_url_list'][0])
                        api_data = {
                            'image_data':
                                {
                                    'no_watermark_image_list': no_watermark_image_list,
                                    'watermark_image_list': watermark_image_list
                                }
                        }
                # TikTok数据处理/TikTok data processing
                elif url_platform == 'tiktok':
                    # TikTok视频数据处理/TikTok video data processing
                    if url_type == 'video':
                        print("正在处理TikTok视频数据...")
                        # 将信息储存在字典中/Store information in a dictionary
                        wm_video = data['video']['download_addr']['url_list'][0]
                        api_data = {
                            'video_data':
                                {
                                    'wm_video_url': wm_video,
                                    'wm_video_url_HQ': wm_video,
                                    'nwm_video_url': data['video']['play_addr']['url_list'][0],
                                    'nwm_video_url_HQ': data['video']['bit_rate'][0]['play_addr']['url_list'][0]
                                }
                        }
                    # TikTok图片数据处理/TikTok image data processing
                    elif url_type == 'image':
                        print("正在处理TikTok图片数据...")
                        # 无水印图片列表/No watermark image list
                        no_watermark_image_list = []
                        # 有水印图片列表/With watermark image list
                        watermark_image_list = []
                        for i in data['image_post_info']['images']:
                            no_watermark_image_list.append(i['display_image']['url_list'][0])
                            watermark_image_list.append(i['owner_watermark_image']['url_list'][0])
                        api_data = {
                            'image_data':
                                {
                                    'no_watermark_image_list': no_watermark_image_list,
                                    'watermark_image_list': watermark_image_list
                                }
                        }
                # 更新数据/Update data
                result_data.update(api_data)
                # print("数据处理完成，最终数据: \n{}".format(result_data))
                # 返回数据/Return data
                return result_data
            except Exception as e:
                traceback.print_exc()
                print("数据处理失败！")
                return {'status': 'failed', 'message': '数据处理失败！/Data processing failed!'}
        else:
            print("[抖音|TikTok方法]返回数据为空，无法处理！")
            return {'status': 'failed',
                    'message': '返回数据为空，无法处理！/Return data is empty and cannot be processed!'}

    # 处理数据方便快捷指令使用/Process data for easy-to-use shortcuts
    @staticmethod
    def hybrid_parsing_minimal(data: dict) -> dict:
        # 如果数据获取成功/If the data is successfully obtained
        if data['status'] == 'success':
            result = {
                'status': 'success',
                'message': data.get('message'),
                'platform': data.get('platform'),
                'type': data.get('type'),
                'desc': data.get('desc'),
                'wm_video_url': data['video_data']['wm_video_url'] if data['type'] == 'video' else None,
                'wm_video_url_HQ': data['video_data']['wm_video_url_HQ'] if data['type'] == 'video' else None,
                'nwm_video_url': data['video_data']['nwm_video_url'] if data['type'] == 'video' else None,
                'nwm_video_url_HQ': data['video_data']['nwm_video_url_HQ'] if data['type'] == 'video' else None,
                'no_watermark_image_list': data['image_data']['no_watermark_image_list'] if data[
                                                                                                'type'] == 'image' else None,
                'watermark_image_list': data['image_data']['watermark_image_list'] if data['type'] == 'image' else None
            }
            return result
        else:
            return data


"""__________________________________________⬇️Test methods(测试方法)⬇️______________________________________"""


async def async_test(_douyin_url: str = None, _tiktok_url: str = None, _bilibili_url: str = None, _ixigua_url: str = None) -> None:
    # 异步测试/Async test
    start_time = time.time()
    print("<异步测试/Async test>")

    print('\n--------------------------------------------------')
    print("正在测试异步获取西瓜视频ID方法...")
    ixigua_id = await api.get_ixigua_video_id(_ixigua_url)
    print(f"西瓜视频ID: {ixigua_id}")
    print("正在测试异步获取西瓜视频数据方法...")
    ixigua_data = await api.get_ixigua_video_data(ixigua_id)
    print(f"西瓜视频数据: {str(ixigua_data)[:100]}")

    print('\n--------------------------------------------------')
    print("正在测试异步获取哔哩哔哩视频ID方法...")
    bilibili_id = await api.get_bilibili_video_id(_bilibili_url)
    print(f"哔哩哔哩视频ID: {bilibili_id}")
    print("正在测试异步获取哔哩哔哩视频数据方法...")
    bilibili_data = await api.get_bilibili_video_data(bilibili_id)
    print(f"哔哩哔哩视频数据: {str(bilibili_data)[:100]}")

    print('\n--------------------------------------------------')
    print("正在测试异步获取抖音视频ID方法...")
    douyin_id = await api.get_douyin_video_id(_douyin_url)
    print(f"抖音视频ID: {douyin_id}")
    print("正在测试异步获取抖音视频数据方法...")
    douyin_data = await api.get_douyin_video_data(douyin_id)
    print(f"抖音视频数据: {str(douyin_data)[:100]}")

    print('\n--------------------------------------------------')
    print("正在测试异步获取TikTok视频ID方法...")
    tiktok_id = await api.get_tiktok_video_id(_tiktok_url)
    print(f"TikTok视频ID: {tiktok_id}")
    print("正在测试异步获取TikTok视频数据方法...")
    tiktok_data = await api.get_tiktok_video_data(tiktok_id)
    print(f"TikTok视频数据: {str(tiktok_data)[:100]}")

    print('\n--------------------------------------------------')
    print("正在测试异步混合解析方法...")
    douyin_hybrid_data = await api.hybrid_parsing(_douyin_url)
    tiktok_hybrid_data = await api.hybrid_parsing(_tiktok_url)
    bilibili_hybrid_data = await api.hybrid_parsing(_bilibili_url)
    xigua_hybrid_data = await api.hybrid_parsing(_ixigua_url)
    print(f"抖音、TikTok、哔哩哔哩、西瓜混合解析全部成功！")

    print('\n--------------------------------------------------')
    # 总耗时/Total time
    total_time = round(time.time() - start_time, 2)
    print("异步测试完成，总耗时: {}s".format(total_time))


if __name__ == '__main__':
    api = Scraper()
    # 运行测试
    # params = "device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=7153585499477757192&pc_client_type=1&version_code=190500&version_name=19.5.0&cookie_enabled=true&screen_width=1344&screen_height=756&browser_language=zh-CN&browser_platform=Win32&browser_name=Firefox&browser_version=110.0&browser_online=true&engine_name=Gecko&engine_version=109.0&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=&platform=PC&webid=7158288523463362079"
    # api.generate_x_bogus(params)
    douyin_url = 'https://v.douyin.com/rLyrQxA/6.66'
    tiktok_url = 'https://www.tiktok.com/@evil0ctal/video/7217027383390555438'
    bilibili_url = "https://www.bilibili.com/video/BV1Th411x7ii/"
    ixigua_url = "https://www.ixigua.com/7270448082586698281"
    # ixigua_url = "ttps://v.ixigua.com/ienrQ5bR/"  # convert_share_urls 这里有bug 如果抖音的口令解析的出来其他的都是none
    asyncio.run(async_test(_douyin_url=douyin_url, _tiktok_url=tiktok_url, _bilibili_url=bilibili_url, _ixigua_url=ixigua_url))


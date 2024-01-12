from datetime import datetime

import pandas as pd
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Content-Type': 'application/json'
}


class VideoInfo:
    def __init__(self, title, desc, owner_name, pubdate, tname, view, danmaku, reply, favorite, coin, like, share):
        # 标题
        self.title = title
        # 描述
        self.desc = desc
        # up主名称
        self.owner_name = owner_name
        # 投稿时间
        self.pubdate = pubdate
        # 分区
        self.tname = tname
        # 观看人数
        self.view = view
        # 弹幕数
        self.danmaku = danmaku
        # 评论数
        self.reply = reply
        # 收藏数
        self.favorite = favorite
        # 投币数
        self.coin = coin
        # 点赞数
        self.like = like
        # 分享数
        self.share = share


# 获取指定pages的热门视频bvid,用于后续视频信息获取
# 默认 20条/页
def get_bvids(pages):
    bvids = []
    # 定义 URL 参数
    params = {
        'ps': 20
    }
    for i in range(pages):
        params['pn'] = i + 1
        response = requests.get('https://api.bilibili.com/x/web-interface/popular', params=params, headers=headers)
        bvids.extend([item['bvid'] for item in response.json()['data']['list']])
    return bvids


def get_video_infos(bvids):
    video_infos = []
    for bvid in bvids:
        params = {
            'bvid': bvid
        }
        response = requests.get('https://api.bilibili.com/x/web-interface/view', params=params, headers=headers)
        data = response.json()['data']
        stat = data['stat']
        video_info = VideoInfo(title=data['title'], desc=data['desc'], owner_name=data['owner']['name'],
                               pubdate=datetime.fromtimestamp(data['pubdate']), tname=data['tname'], view=stat['view'],
                               danmaku=stat['danmaku'], reply=stat['reply'], favorite=stat['favorite'],
                               coin=stat['coin'], like=stat['like'], share=stat['share'])
        video_infos.append(video_info)
    return video_infos


def to_excel(video_infos):
    data = {
        '标题': [video_info.title for video_info in video_infos],
        '描述': [video_info.desc for video_info in video_infos],
        'UP主': [video_info.owner_name for video_info in video_infos],
        '投稿时间': [video_info.pubdate for video_info in video_infos],
        '分区': [video_info.tname for video_info in video_infos],
        '观看人数': [video_info.view for video_info in video_infos],
        '弹幕': [video_info.danmaku for video_info in video_infos],
        '评论': [video_info.reply for video_info in video_infos],
        '收藏': [video_info.favorite for video_info in video_infos],
        '投币': [video_info.coin for video_info in video_infos],
        '点赞': [video_info.like for video_info in video_infos],
        '分享': [video_info.share for video_info in video_infos]
    }
    pd.DataFrame(data).to_excel('video_info.xlsx', index=False)


if __name__ == '__main__':
    # 设置爬取页数,默认10页,200条数据
    bvids = get_bvids(10)
    to_excel(get_video_infos(bvids))
    print('执行完毕!')

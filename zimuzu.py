# -*- coding:utf-8 -*-  

import json
import time
from datetime import date
from hashlib import md5

import requests


APIURL = 'http://api.foo.bar/'

class Zimuzu(object):
    def __init__(self, cid=None, accesskey=None):
        self.cid = cid
        self.accesskey = accesskey


    def _request(self, url, **kwargs):
        # if not isinstance(url, str) and url is not None:
        #     raise TypeError("first parameter must be a URL")

        _url = APIURL + url
        timestamp = str(int(time.time()))

        secretkey = '{}$${}&&{}'.format(self.cid, self.accesskey, timestamp)
        encryptkey = md5(secretkey).hexdigest()

        if kwargs.has_key('debug'):
            return '?cid={}&accesskey={}&timestamp={}'.format(self.cid, encryptkey, timestamp)
        if not kwargs:
            data = {
                'cid': self.cid,
                'accesskey': encryptkey,
                'timestamp': timestamp
            }
        else:
            data = {}
            for key, value in kwargs.iteritems():
                data[key] = value

            data['cid'] = self.cid
            data['accesskey'] = encryptkey
            data['timestamp'] = timestamp


        return requests.get(_url, data)



    def search(self, key, type_=None, order=None, limit=None, page=None):
        """
        接口功能: 全站搜索
        接口地址: search
        传递参数:
           *k       搜索关键词
            st      搜索类型,resource-影视资源,subtitle-字幕资源,article-资讯以及影评和剧评.如果为空,则在以上三种资源中搜索
            order   排序 pubtime发布时间 uptime更新时间    默认为更新时间
            limit   每页数量(默认输出20个)
            page    页码
        返回数据:
            status  请求状态
            info    状态描述信息
            data    记录列表
                count   [未知意义字段]
                list    字幕列表
                    itemid      对应的资源ID
                    title       资源标题
                    type        resource-影视资源 subtitle-字幕 article-资讯
                    channel     当type为resource的时候有效,tv-电视剧,movie-电影,openclass-公开课
                    pubtime     发布时间
                    uptime      更新时间
        """
        url = 'search'

        response = self._request(url, k=key, st=type_, order=order, limit=limit, page=page)

        return response.json()


    def resource_list(self, channel=None, area=None,
                      sort=None, year=None, category=None,
                      limit=None, page=None):
        """
        接口功能: 影视资源列表
        接口地址: resource/fetchlist
        传递参数:
            channel     频道 电影:movie,电视剧:tv,公开课:openclass
            area        国家,例如:”美国”,”日本”,”英国”
            sort        排序 更新时间update,发布时间pubdate,上映时间premiere,名称name,排名rank,评分score,点击率views
            year        年代 最小值为1990
            category    影视类型 具体值请参看网站
            limit       默认为10个,不能大于20
            page        列表页码
        返回数据:
            status  请求状态
            info    信息
            data    记录列表
                id          资源ID
                cnname      中文名
                enname      英文名
                remark      说明
                area        国家
                format      格式
                category    类型
                poster      海报
                channel     频道
                lang        语言
                play_status 播放状态
                rank        排名
                score       评分
                views       浏览数
        """

        url = 'resource/fetchlist'

        response = self._request(url, channel=channel, area=area,
                                 sort=sort, year=year, category=category,
                                 limit=limit, page=page)

        return response.json()

    def resource_info(self, rid, prevue=None, share=None):
        """
        接口功能: 影视资源详情
        接口地址: resource/getinfo
        传递参数:
           *id          影视ID
            prevue      是否获取播放档期(只有电视剧才有效) 1-获取
            share       是否获取分享信息 1-获取
        返回数据:
            status  请求状态
            info    信息
            data    记录列表
                id          资源ID
                cnname      中文名
                enname      英文名
                remark      说明
                poster      海报
                play_status 播放状态
                area        地区
                category    类型
                views       浏览数
                score       评分
                content     简介
                prevue      播放档期
                        season      季度
                        episode     集数
                        play_time   播放时间
                        week        星期
                shareTitle  分享标题
                shareContent分享内容
                shareImage  分享图片
                shareUrl    分享地址
                item_permission 为0表示当前用户没有权限下载资源(必须传递uid和token给当前接口),仅限IOS客户端
        """
        url = 'resource/getinfo'

        response = self._request(url, id=rid, prevue=prevue, share=share)

        return response.json()

    def resource_seasonepisode(self, rid):
        """
        接口功能: 影视资源季度信息
        接口地址: resource/season_episode
        传递参数:
           *id          影视ID
        返回数据:
            status      请求状态
            info        信息
            data        记录列表
                season      季度
                episode     集数

            该接口会把电视剧的所有季度信息列出来(包括了单剧等),如果影视是电影则返回错误信息
            例如:{‘season’:7,’episode’:10} 表示第7季总共有10集
        """

        url = 'resource/season_episode'

        response = self. _request(url, id=rid)

        return response.json()

    def resource_itemlist(self, rid, file_=None, season=None, episode=None):
        """
        接口功能: 影视下载资源列表
        接口地址: resource/itemlist_web
        传递参数:
           *id      影视ID
            file    是否同时获取下载链接 1-获取,0-不获取
            season  季度
            episode 集数
        返回数据:
            status  请求状态
            info    状态描述信息
            data    记录列表
                id          资源ID
                name        资源名
                format      资源格式
                season      资源季度
                episode     资源集数
                size        文件大小
                dateline    资源添加时间
                link        当需要同时获取下载链接时该参数有数据,仅限返回电驴和磁力链接
                info        如果当前用户没有足够权限获取电视剧的资源列表,该参数会输出提示用户最多只能查看资源条数的信息,默认为空

        """
        url = 'resource/itemlist_web'

        response = self._request(url, id=rid, file=file_, season=season, episode=episode)

        return response.json()


    def resource_itemlink(self, lid):
        """
        接口功能: 影视资源下载地址
        接口地址: resource/itemlink
        传递参数:
           *id          资源ID
        返回参数:
            status      请求状态
            info        信息
            data        记录列表
                address     下载地址
                way         下载方式  1-电驴  2-磁力  9-网盘  12-城通盘
        """
        url = 'resource/itemlink'

        response = self._request(url, id=lid)

        return response.json()


    def subtitle_list(self, limit=None, page=None):
        """
        接口功能: 字幕列表
        接口地址: subtitle/fetchlist
        传递参数:
            limit   数量
            page    页码
        返回数据:
            status  请求状态
            info    信息
            data    记录列表
                id              字幕ID
                cnname          字幕中文名
                enname          字幕英文名
                resourceid      对应的资源ID
                segment         对应片源
                source          字幕发布者 zimuzu(字幕组)
                category        类型
                file            字幕文件下载地址(如果用户没权限浏览则为空)
                filename        字幕文件名
                lang            语言
                format          格式
                remark          备注
                views           浏览数
                dateline        发布时间
                downloads       下载次数
                comments        评论数
                updatetime      更新时间
                updater         更新人员
                protect_expire  字幕下载保护期到期时间(unix时间戳),表示当前字幕处于保护期内,用户不能查看,同时file的值为空,如为0则表示没有保护期或者已过期
                resource_info   对应的资源信息
                        id          影视ID
                        cnname      中文名
                        enname      英文名
                        poster      海报 原始图
                        poster_a    海报 超大尺寸
                        poster_b    海报 大尺寸
                        poster_m    海报 中尺寸
                        poster_s    海报 小尺寸

        """
        url = 'subtitle/fetchlist'

        response = self._request(url, limit=limit, page=page)

        return response.json()


    def subtitle_info(self, sid):
        """
        接口功能: 字幕详情
        接口地址: subtitle/getinfo_web
        传递参数:
           *id     字幕ID
        返回数据:
            status  请求状态
            info    信息
            data    记录列表
                id              字幕ID
                cnname          字幕中文名
                enname          字幕英文名
                resourceid      对应的资源ID
                segment         对应片源
                source          字幕发布者 zimuzu(字幕组)
                category        类型
                file            字幕文件下载地址(如果在保护期就不显示)
                filename        字幕文件名
                lang            语言
                format          格式
                remark          备注
                views           浏览数
                dateline        发布时间
                segment_num     [未知字段]
                operator        上传人员
                comments        评论
                ddd             ISO格式日期
                downloads       下载次数
                updatetime      更新日期
                protect_expire  字幕下载保护期到期时间(unix时间戳),表示当前字幕处于保护期内,用户不能查看,同时file的值为空,如为0则表示没有保护期或者已过期
                resource_info   对应的资源信息
                        id          影视ID
                        cnname      中文名
                        enname      英文名
                        poster      海报 原始图
                        poster_a    海报 超大尺寸
                        poster_b    海报 大尺寸
                        poster_m    海报 中尺寸
                        poster_s    海报 小尺寸
        """

        url = 'subtitle/getinfo_web'

        response = self._request(url, id=sid)

        return response.json()

    def tv_schedule(self, start=None, end=None, limit=None):
        """
        接口功能: 美剧时间表
        接口地址: tv/schedule
        传递参数:
            start   开始时间,标准的时间格式,如:2015-02-03或2015-2-3或20150203
            end     结束时间,开始时间和结束时间不能超过31天,不传参数则默认为本月时间表.
            limit   返回数量
        返回数据:
            status  请求状态
            info    信息
            data    记录列表
                "20xx-xx-xx":    日期
                        id          电视剧ID
                        cnname      电视剧中文名
                        enname      电视剧英文名
                        season      季度
                        episode     集数
                        poster      海报

        """

        url = 'tv/schedule'

        current_month = date.today().isoformat()[0:8]
        firstday = current_month + '01'
        lastday = current_month + '31'

        if start and end:
            response = self._request(url, start=start, end=end, limit=limit)
        else:
            response = self._request(url, start=firstday, end=lastday, limit=limit)

        return response.json()

    def resource_top(self, channel=None, limit=None):
        """
        接口功能: 今日热门排行
        接口地址: resource/top
        传递参数:
            channel     频道 默认为电影和电视剧的排行榜  tv电视剧 movie 电影
            limit       获取数量,默认为5个
        返回数据:
            status  请求状态
            info    状态描述信息
            data    记录列表
                id              影视ID
                cnname          中文名
                channel           频道
                area            国家
                category        类型
                publish_year    发布年份
                play_status     播放状态
                poster          海报 原始图
                poster_a        海报 超大尺寸
                poster_b        海报 大尺寸
                poster_m        海报 中尺寸
                poster_s        海报 小尺寸
        """
        url = 'resource/top'

        response = self._request(url, channel=channel, limit=limit)

        return response.json()


    def resource_today(self):
        """
        接口功能: 今日更新
        接口地址: resource/today
        传递参数:
            无
        返回数据:
            status  请求状态
            info    状态描述信息
            data    记录列表
                resourceid      影视ID
                cnname          中文名
                season          季度
                channel         资源类型
                name            下载资源名
                format          格式
                season          季度
                episode         集数
                size            文件大小
                ways            下载方式集合   1-电驴 2-磁力
        """
        url = 'resource/today'

        response = self._request(url)

        return response.json()


def json_print(data):
    """
    此函数用于打印带有中文内容的json
    """
    return json.dumps(data, indent=4, ensure_ascii=False, encoding="utf-8")


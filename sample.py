# -*- coding:utf-8 -*-

from zimuzu import Zimuzu, json_print
import sys

CID = 'xx'
ACCESSKEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

api = Zimuzu(cid=CID, accesskey=ACCESSKEY)


# 全部函数中分别有三种 ID , 分别为 rid, lid, sid 
# 对应为 影视ID, 影视资源ID, 字幕ID
# 影视资源ID 只在 resource_itemlink 存在.


"""
全站搜索
"""
# result = api.search("绿箭", type='subtitle') # 搜索电视剧字幕
# print result


"""
影视资源列表
"""
# result = api.resource_list() 
# print json_print(result)


"""
影视资源详情
"""
# result = api.resource_info('26779', prevue=1) # 获取「绿箭」详情,并获得播放档期
# print json_print(result)


"""
影视资源季度信息
"""
# result = api.resource_seasonepisode('26779') # 如果是电影则返回错误
# print result


"""
影视资源下载列表
"""
# result = api.resource_itemlist('26779', file_=1) # 获取「绿箭」资源列表,并获得下载链接
# print json_print(result)


"""
影视资源下载地址

此ID为「影视资源下载列表」所获得的ID,与影视ID不同.
函数参数名为 lid
"""
# result = api.resource_itemlink('147732')
# print json_print(result)


"""
字幕列表
"""
# result = api.subtitle_list(limit=30) # 获取30条最新发布字幕
# print json_print(result)

"""
字幕详细
"""
# result = api.subtitle_info('50768')
# print json_print(result)


"""
美剧时间表

不传递参数则为本月时间表
start 与 end 参数可以传递 2016-01-01 2016-1-1 20160101 三种格式字符串日期
两者间隔不得超过31填
"""
# result = api.tv_schedule()
# print json_print(result)


"""
今日热门排行
"""
# result = api.resource_top(channel='tv') # 获取电视剧热门排行, 获取电影则传递 'movie'
# print json_print(result)


"""
今日更新
"""
# result = api.resource_today()
# print json_print(result)
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-05-07 14:39:40
# Project: MTime

from pyspider.libs.base_handler import *
import re


class Handler(BaseHandler):
    
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
    }
    
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):  #从首页进入
        self.crawl('http://theater.mtime.com/China_Fujian_Province_Xiamen/',callback=self.index_page,headers=self.headers,fetch_type='js')

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match("http://movie.mtime.com/\d+/$",each.attr.href):  #选择符合格式的URL
                self.crawl(each.attr.href,callback=self.detail_page,headers=self.headers,fetch_type='js')

    @config(priority=2)
    def detail_page(self, response):
        title = response.doc('.clearfix > h1').text()  #电影名称
        publish_time = response.doc('.db_year > a').text()  #上映时间
        marketed = response.doc('.__r_c_ > b').text()    #评分
        ticket_num = response.doc('.only').text()   #票房
        markered_people = response.doc('#ratingCountRegion').text()   #参与评分人数
        wanted_people = response.doc('#attitudeCountRegion').text()   #想要看人数
        message_details = response.doc('.info_l > dd > a').text()    #电影的信息
        message = response.doc('.lh18').text()                   #电影简介
        main_actor = response.doc('.main_actor p > a').text()       #主演人员
        
        return {
            
            "title": title,
            "publish_time": publish_time,
            "marketed":marketed,
            "ticket_num":ticket_num,
            "markered_people":markered_people,
            "wanted_people":wanted_people,
            "message_details":message_details,
            "message":message,
            "main_actor":main_actor,
            }
# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json
from zhihu.items import ZhihuItem


class ZhihuUserSpider(scrapy.Spider):
    name = 'zhihu_user'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    #定义查找账号
    start_user = "excited-vczh"

    #接口拆分，user_url存储用户url地址，user_query存储接口参数
    user_url = "https://www.zhihu.com/api/v4/members/{user}?include={include}"
    user_query = "locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_bind_phone,is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics"

    # follows_url存储的为关注列表的url地址,fllows_query存储的为查询参数。这里涉及到offset和limit是关于翻页的参数，0，20表示第一页
    """ request请求
    https://www.zhihu.com/api/v4/members/excited-vczh/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=20&limit=20
    """
    follows_url = "https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}"
    follows_query = "data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics"

    # followers_url是获取粉丝列表信息的url地址，followers_query存储的为查询参数。
    followers_url = "https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}"
    followers_query = "data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics"

    def start_requests(self):
        #重写了scrapy中的start_requests方法，分别请求了用户查询的url和关注列表的查询以及粉丝列表信息查询

        yield Request(self.user_url.format(user=self.start_user, include=self.user_query), callback=self.parse_user)
        yield Request(self.follows_url.format(user=self.start_user, include=self.follows_query, offset=0, limit=20),
                      callback=self.parse_follows)
        yield Request(self.followers_url.format(user=self.start_user, include=self.followers_query, offset=0, limit=20),
                      callback=self.parse_followers)

    def parse_user(self, response):
        '''
        因为返回的是json格式的数据，所以这里直接通过json.loads获取结果
        :param response:
        :return:
        '''
        result = json.loads(response.text)
        item = ZhihuItem()
        # 这里循环判断获取的字段是否在自己定义的字段中，然后进行赋值
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)

        # 这里在返回item的同时返回Request请求，继续递归拿关注用户信息的用户获取他们的关注列表
        yield item
        yield Request(
            self.follows_url.format(user=result.get("url_token"), include=self.follows_query, offset=0, limit=20),
            callback=self.parse_follows)
        yield Request(
            self.followers_url.format(user=result.get("url_token"), include=self.followers_query, offset=0, limit=20),
            callback=self.parse_followers)

    def parse_follows(self, response):
        '''
        用户关注列表的解析，这里返回的也是json数据 这里有两个字段data和paging，其中paging是分页信息
        :param response:
        :return:
        '''
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get("url_token"), include=self.user_query),
                              callback=self.parse_user)

        # 这里判断paging是否存在并且判断paging里的参数is_end判断是否为False，如果为False表示不是最后一页，否则则是最后一页
        """ 返回json数据
        paging:{is_end: false, totals: 2837,…}
            is_end:false
            is_start:false
            next:"http://www.zhihu.com/api/v4/members/excited-vczh/followees?include=data%5B%2A%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=40"
            previous:"http://www.zhihu.com/api/v4/members/excited-vczh/followees?include=data%5B%2A%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=0"
            totals:2837
        """

        if 'page' in results.keys() and results.get('is_end') == False:
            next_page = results.get('paging').get("next")
            # 获取下一页的地址然后通过yield继续返回Request请求，继续请求自己再次获取下页中的信息
            yield Request(next_page, self.parse_follows)

    def parse_followers(self, response):
        #粉丝的与关注的一样
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get("url_token"), include=self.user_query),
                              callback=self.parse_user)

        if 'page' in results.keys() and results.get('is_end') == False:
            next_page = results.get('paging').get("next")
            yield Request(next_page, self.parse_followers)
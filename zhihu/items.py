# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.field()
    name = scrapy.field()
    account_status = scrapy.field()
    allow_message = scrapy.field()
    answer_count = scrapy.field()
    articles_count = scrapy.field()
    avatar_hue = scrapy.field()
    avatar_url = scrapy.field()
    avatar_url_template = scrapy.field()
    badge = scrapy.field()
    business = scrapy.field()
    employments = scrapy.field()
    columns_count = scrapy.field()
    commercial_question_count = scrapy.field()
    cover_url = scrapy.field()
    description = scrapy.field()
    educations = scrapy.field()
    favorite_count = scrapy.field()
    favorited_count = scrapy.field()
    follower_count = scrapy.field()
    following_columns_count = scrapy.field()
    following_favlists_count = scrapy.field()
    following_question_count = scrapy.field()
    following_topic_count = scrapy.field()
    gender = scrapy.field()
    headline = scrapy.field()
    hosted_live_count = scrapy.field()
    is_active = scrapy.field()
    is_bind_sina = scrapy.field()
    is_blocked = scrapy.field()
    is_advertiser = scrapy.field()
    is_blocking = scrapy.field()
    is_followed = scrapy.field()
    is_following = scrapy.field()
    is_force_renamed = scrapy.field()
    is_privacy_protected = scrapy.field()
    locations = scrapy.field()
    is_org = scrapy.field()
    type = scrapy.field()
    url = scrapy.field()
    url_token = scrapy.field()
    user_type = scrapy.field()
    logs_count = scrapy.field()
    marked_answers_count = scrapy.field()
    marked_answers_text = scrapy.field()
    message_thread_token = scrapy.field()
    mutual_followees_count = scrapy.field()
    participated_live_count = scrapy.field()
    pins_count = scrapy.field()
    question_count = scrapy.field()
    show_sina_weibo = scrapy.field()
    thank_from_count = scrapy.field()
    thank_to_count = scrapy.field()
    thanked_count = scrapy.field()
    type = scrapy.field()
    vote_from_count = scrapy.field()
    vote_to_count = scrapy.field()
    voteup_count = scrapy.field()

    pass

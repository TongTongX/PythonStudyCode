# FBSpider - A facebook crwalling software
#
#  Copyright (c) 2016 Michael(Zichun) Lin, Yu Zhu, Xutong Zhao. All rights reserved.
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
# 	along with this program.  If not, see <http://www.gnu.org/licenses/>.


import scrapy
from fb_login import FBLogin

# create user
user = FBLogin()

class FBSpider(scrapy.Spider):
    name = "facebook"
    allowed_domains = ["facebook.com"]
    start_urls = ["https://www.facebook.com"]
    user.login()

    #user.likeFriend()
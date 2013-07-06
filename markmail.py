#!/usr/bin/env python
# -*- coding: utf8 -*-
import datetime

# LinkedMarkMail, an RDFizer for Mark Mail 
#
# Copyright (C) 2011 Sergio Fernández
#
# This file is part of SWAML <http://swaml.berlios.de/>
# 
# LinkedMarkMail is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# LinkedMarkMail is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with LinkedMarkMail. If not, see <http://www.gnu.org/licenses/>.


"""
A simple python client for MarkMail hacky API

Futher details at: http://pastebin.com/M5NnyEZ8
"""

import urllib2
import simplejson as json
from StringIO import StringIO
from datetime import datetime, timedelta
import re
#import warnings

class MarkMail:

    def __init__(self, base="http://markmail.org"):
        self.base = base
        self.p_yesterday = re.compile('^yesterday.*', re.IGNORECASE)
        
    def search(self, query, page=1, mode="json"):
        uri = "%s/results.xqy?q=%s&page=%d&mode=%s" % (self.base, query, page, mode)
        response = self.__request(uri).read()
        obj = json.load(StringIO(response))
        #warnings.warn("This method is still fully unimplemented")
        return obj #FIXME

    def get_message(self, key, mode="json"):
        uri = "%s/message.xqy?id=%s&mode=%s" % (self.base, key, mode)
        response = self.__request(uri).read()
        obj = json.load(StringIO(response))
        message = obj["message"]
        if (message["subject"]==None or message["subject"]==None):            
            return None
        else:
            return message

    def get_thread(self, key, mode="json"):
        uri = "%s/thread.xqy?id=%s&mode=%s" % (self.base, key, mode)
        response = self.__request(uri).read()
        obj = json.load(StringIO(response))
        thread = obj["thread"]
        if (thread["subject"]==None or thread["list"]==None):
            return None
        return thread
        
    def parse_date(self, date):
        if (date is None):
            return None
        
        # yesterday
        regex = re.compile("^yesterday\s*(\d*):(\d*)\spm",re.IGNORECASE)
        r = regex.search(date)
        if (r):
            hour = r.group(1)
            minute = r.group(2)
            d = datetime.today()
            d = d - timedelta(days = 1)
            d.replace(hour = hour, minute = minute)
            return d
            
        # today
        regex = re.compile("^today\s*(\d*):(\d*)\spm",re.IGNORECASE)
        r = regex.search(date)
        if (r):
            hour = r.group(1)
            minute = r.group(2)
            d = datetime.today()
            #d = d - timedelta(days = 1)
            d.replace(hour = hour, minute = minute)
            return d
        
        # n days ago
        regex = re.compile("^(\d*)\sdays\sago",re.IGNORECASE)
        r = regex.search(date)
        if (r):
            days = r.group(1)
            d = datetime.now()
            d = d - timedelta(days = int(days))
            return d
         
        return datetime.strptime(date, '%b %d, %Y')
        
    def __request(self, uri, accept="application/json"):
        """
        Generic HTTP request
       
        @param uri: uri to request
        @return: response
        @rtype: file-like object
        """
       
        headers = {
                    "User-Agent" : "swaml (http://swaml.berlios.de/; sergio@wikier.org)",
                    "Accept"     : accept
                  }
        request = urllib2.Request(uri, headers=headers)
        return urllib2.urlopen(request)
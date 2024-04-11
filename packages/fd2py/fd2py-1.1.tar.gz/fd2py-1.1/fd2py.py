#!/usr/bin/python
# -*- coding: UTF-8 -*-
 

import json
from urllib.parse import urlparse, parse_qs
 



def extract_params_from_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    params = {key: value[0] for key, value in query_params.items()}
    # open('./format_url.json','w',encoding='utf-8').write(json.dumps(params,ensure_ascii=False))
    return params


class FidderToPy():
    def __init__(self, file_name, sa_name):
        '''
        str_name : fidder session txt
        sa_name : ?.py is output name
        '''
        self.str_filename = file_name
        self.save_name = sa_name
        self.text = ""
        self.url_list = []
        self.headers = {}
        self.cookies = {}
        self.data = {}
        self.start()
 
    def get_url(self):
        infos = self.text.split("\n")[0]
        self.url_list = [infos.split(" ")[0], infos.split(" ")[1]]
 
    def get_headers(self):
        infos = self.text.split("\n")[1:]
        info = ""
        for i in infos:
            if "Cookie: " in i:
                break
            info += i + "\n"
        headers = info.split("\n")
        while "" in headers:
            headers.remove("")
        for i in headers:
            if ": " not in i:
                break
            self.headers[i.split(": ")[0]] = i.split(": ")[1]
        self.get_cookies()
        self.headers['cookie'] =  self.cookies
    def get_cookies(self):
        infos = self.text.split("\n")[1:]
        cookies_flag = 0
        for i in infos:
            if "Cookie: " in i:
                self.cookies = i.replace("Cookie: ", "")
                cookies_flag = 1
                break
            if cookies_flag==1:
                # print("===>",i.split("=")[0])
                self.cookies = {i.split("=")[0]: i.split("=")[1] for i in self.cookies.split("; ")}
    
    def get_data(self):
        try:
            infos = self.text.split("\n")
            for i in range(2, len(infos)):
                if infos[i - 1] == "" and "HTTP" in infos[i + 1]:
                    self.data = infos[i]
                    break
            self.data = {i.split("=")[0]: i.split("=")[1] for i in self.data.split("&")}
        except:
            pass
 
    def get_req(self):
        info_beg = r'''
#-*- coding: UTF-8 -*
import json
import requests
import urllib3
from urllib.parse import urlparse, parse_qs
urllib3.disable_warnings()

def extract_params_from_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    params = {key: value[0] for key, value in query_params.items()}
    open('./format_url.json','w',encoding='utf-8').write(json.dumps(params,ensure_ascii=False))
    return params



px = {
    'http':'http://127.0.0.1:7890',
    'https':'http://127.0.0.1:7890'
}
'''
        info_url = "url = \'{}\'\n".format(self.url_list[1].strip())
        url = info_url.split('/?')[0] +"/'" +'\n'
        qs_params = 'params='+ json.dumps(extract_params_from_url(info_url),ensure_ascii=False) +'\n'
        info_headers = "headers = {}\n".format(self.headers)
        
        info_data = "data = {}\n\n".format(self.data)
        if "GET" in self.url_list[0]:
            info_req = "html = requests.get(url, headers=headers, params=params,  verify=False,proxies=px)\n"
        else:
            info_req = "html = requests.post(url, headers=headers, params=params,  verify=False, data=data,proxies=px)\n"
        info_end = "print(len(html.text))\nprint(html.text)\n"
        text = info_beg + url + qs_params + info_headers  + info_data + info_req + info_end
        with open(self.save_name, "w+", encoding="utf8") as p:
            p.write(text)
        # print("转化成功！！")
        print(self.save_name, "success")
 
    def read_infos(self):
        with open(self.str_filename, "r+", encoding="utf-8") as p:
            old_line = ""
            for line in p:
                if old_line == b"\n" and line.encode() == b"\n":
                    break
                old_line = line.encode()
                self.text += old_line.decode()
        # print("self.text:", self.text)
 
    def start(self):
        self.read_infos()
        self.get_url()
        self.get_headers()
        # self.get_cookies()
        self.get_data()
        # print("self.url_list:", self.url_list)
        # print("self.headers:", self.headers)
        # print("self.cookies:", self.cookies)
        # print("self.data:", self.data)
        self.get_req()




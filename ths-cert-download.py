#!/usr/bin/python
# Download ths cert files
# Ver 2.0
# Edit By hanlin @Beijing

import os
import json
import urllib
from urllib.request import urlopen
from urllib.request import Request
from urllib.parse import urlencode
from urllib.parse import quote

'''
http://services.myhexin.com/produser/downloadcert?libver=20030506
&authcode=M11-ics3-JqUK-0Lab-%2FwIY-HTRL&Submit=%CF%C2%D4%D8%D6%A4%CA%E9
'''

class ThsCertSave:
    path = ''
    ip = ''
    codelist = []
    url_base = ''
    url_data = ''
    def __init__(self,path,ip,codelist,url_base,url_data):
        self.path = path
        self.ip = ip
        self.codelist = codelist
        self.url_base = url_base
        self.url_data = url_data
    def __createPathName(self,code):
        file_name = code.split('-')[0] + '.dat'
        if not os.path.exists(self.path + self.ip):
            os.makedirs(self.path + self.ip)
        path_file = self.path + self.ip + '/' + file_name
        return path_file
    def __iUrlEncode(self,code):
        # special process for Chinese Char
        data_cn = self.url_data["Submit"].encode('gb2312')
        data_cn = quote(data_cn)
        self.url_data["Submit"] = '123'
        req_data = urlencode(self.url_data)
        req_data = req_data.replace('123', data_cn)
        iurl = self.url_base + '?' + req_data
        return iurl

    def save(self):
        for code in self.codelist:
            path_file = self.__createPathName(code)
            iurl = self.__iUrlEncode(code)
            res = urlopen(iurl)
            with open(path_file,"wb") as mydat:
                mydat.write(res.read())
                print('Saving: '+path_file)

def main():
    path = './download/'
    url_base = 'http://services.myhexin.com/produser/downloadcert'
    url_data = {"libver": '20030506',
                "authcode": 'M11-ics3-JqUK-0Lab-/wIY-HTRL',
                "Submit": '下载证书'}
    #is_json = is_json.is_json('ths.json')
    with open('ths.json', 'r') as f:
        ths_data = json.load(f)

    ip_list = ths_data.keys()
    for ip in ip_list:
        codelist = ths_data[ip]
        isave = ThsCertSave(path,ip,ths_data[ip],url_base,url_data)
        isave.save()

if __name__ == "__main__":
    main()
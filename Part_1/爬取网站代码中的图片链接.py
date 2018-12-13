#!/usr/bin/python
# coding: utf-8

"""
@version: Python3
@author: Ann
@contact: 494792590@qq.com
@software: Pycharm
@file: 正则表达式解析.py
@time: 2018/12/5 0005 下午 8:44
"""

"""
目的：爬取'www.qiushibaike.com'中图片链接并下载保存 

"""
import urllib.request
import urllib.parse
import re
import os


def handle_request(url, page):
    url = url + str(page) + '/'
    # print(url) # 测试page的url是否正确
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
     Chrome/70.0.3538.110 Safari/537.36',
    }
    request = urllib.request.Request(url=url, headers=headers)

    return request


def download_image(response):
    # 下载图片就要分析网页代码，图片链接是包含在一层又一层的标签里(通常是div中)
    # 查看网页代码后发现，图片链接是在<img src=''>中,<img src=''>又在<a>中,<a>又在<div class='thumb'>中
    # 因为<a>标签中有一大堆，所有直接用 .*? 匹配
    pattern = re.compile(r'<div class="thumb">.*?<img src="(.*?)".*?>.*?</div>', re.S)  # 因为标签之间有换行
    it = pattern.findall(response)
    print(it)  # 这就拿到了图片链接
    # 遍历列名，依次下载图片
    for image_src in it:
        # 处理拼接image_src链接
        image_src = 'https:' + image_src
        # 发送请求,下载图片,创建文件夹存放图片
        dir_name = 'qiutu'
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        # 图片名字，按照图片链接进行分割，取最后一个/
        file_name = image_src.split('/')[-1]
        file_path = dir_name + '/' + file_name
        print('%s图片正在下载...' % file_name)
        urllib.request.urlretrieve(image_src, file_path)
        print('%s图片下载结束...' % file_name)


def main():
    url = 'https://www.qiushibaike.com/pic/page/'
    start_page = int(input('请输入起始页码：'))
    end_page = int(input('请输入结束页码：'))
    for page in range(start_page, end_page + 1):
        print('第%s页开始下载...' % page)
        # 生成请求对象
        request = handle_request(url, page)
        # 发送请求对象，获取响应内容
        response = urllib.request.urlopen(request).read().decode()
        # 解析内容，提取所有图片链接，并下载
        download_image(response)
        print('第%s页开始下载结束...' % page)
        print()
        print()


if __name__ == '__main__':
    main()

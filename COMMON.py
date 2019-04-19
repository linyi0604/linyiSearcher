"""
一些公共配置
"""

# 爬取根网页地址存放文件目录
BASE_URL_LIST_FILE = "./data/base_url_list.txt"


# 发送请求的报文头列表
HEADERS = [
    {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"},
    {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13"},
    {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13 "},
    {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3"},
    {"User-Agent":"Opera/9.80 (Windows NT 5.1; U; zh-cn) Presto/2.9.168 Version/11.50"},
]
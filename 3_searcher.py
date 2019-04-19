# coding=utf-8
import jieba
import sqlite3
from bottle import route, run, template, request, static_file, redirect


@route('/static/<filename>')
def server_static(filename):
    if filename == "jquery.min.js":
        return static_file("jquery.min.js", root='./data/front/js/')
    elif filename == "bootstrap.min.js":
        return static_file("bootstrap.js", root='./data/front/js/')
    elif filename == "bootstrap.min.css":
        return static_file("bootstrap.css", root='./data/front/css/')


@route('/')
def index():
    return redirect("/hello/")


@route('/hello/')
def index():
    form = request.GET.decode("utf-8")
    keyword = form.get("keyword", "")
    cut = list(jieba.cut(keyword))
    # 根据索引查询包含关键词的网页编号
    page_id_list = get_page_id_list_from_key_word_cut(cut)
    # 根据网页编号 查询网页具体内容
    page_list = get_page_list_from_page_id_list(page_id_list)
    # 根据查询关键字和网页包含的关键字，进行相关度排序 余弦相似度
    page_list = sort_page_list(page_list, cut)
    context = {
        "page_list": page_list[:20],
        "keyword": keyword
    }
    return template("./data/front/searcher.html", context)


# 计算page_list中每个page 和 cut的余弦相似度
def sort_page_list(page_list, cut):
    con_list = []
    for page in page_list:
        url = page[2]
        words = page[1]
        title = page[3]
        vector = words.split(" ")
        same = 0
        for i in vector:
            if i in cut:
                same += 1
        cos = same / (len(vector)*len(cut))
        con_list.append([cos, url, words, title])
    con_list = sorted(con_list, key=lambda i: i[0], reverse=True)
    return con_list



# 根据网页id列表获取网页详细内容列表
def get_page_list_from_page_id_list(page_id_list):
    id_list = "("
    for k in page_id_list:
        id_list += "%s,"%k
    id_list = id_list.strip(",") + ")"
    conn = sqlite3.connect("./data/database.db")
    c = conn.cursor()
    sql = "select * " \
          + "from page_info  " \
          + "where id in " + id_list + ";"
    res = c.execute(sql)
    res = [r for r in res]
    return res


# 根据关键词在索引中获取网页编号
def get_page_id_list_from_key_word_cut(cut):
    keyword = "("
    for k in cut:
        if k == " ":
            continue
        keyword += "'%s',"%k
    keyword = keyword.strip(",") + ")"
    conn = sqlite3.connect("./data/database.db")
    c = conn.cursor()
    sql = "select page_id " \
            + "from page_index  " \
            + "where keyword in " + keyword + ";"
    res = c.execute(sql)
    res = [r[0] for r in res]
    return res



if __name__ == '__main__':
    run(host='localhost', port=8080)
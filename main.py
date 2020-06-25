# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import json
from epub import Epub
from os import path

def get_config():
    with open("config.json", 'r') as f:
        dict = json.load(fp = f)
        return dict

def login_with_cookie(cookies):
    print("正在登录…")
    session = requests.session()
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72"
    }
    cookie = {}
    for i in cookies.split(";"):
        value = i.split("=")
        cookie[value[0]] = value[1]
    session.cookies.update(cookie)
    r = session.get("https://m.jjwxc.net//my", headers=headers)
    r.encoding = 'GBK'
    soup = BeautifulSoup(r.text,'html.parser')
    #print(r.text[3000:-1000])
    if soup.select("h2")[0].get_text() == "首页>我的晋江":
        print("登陆成功")
    else:
        print("cookie失效")
    return session

def login_with_password(username, password):
    print("正在登录…")
    session = requests.session()
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72"
    }
    data = {
        "loginname":username,
        "loginpass":password
    }
    r = session.post("https://m.jjwxc.net/login/wapLogin", data=data, headers = headers)

    r.encoding = 'GBK'
    soup = BeautifulSoup(r.text,'html.parser')
    #print(r.text[3000:-1000])
    if soup.select("h2")[0].get_text() == "首页>我的晋江":
        print("登陆成功")
    else:
        print("登陆失败")
    return session

def get_summary(novelid, session):
    print("获取简介…")
    r = session.get("http://www.jjwxc.net/onebook.php?novelid=" + str(novelid))
    r.encoding = 'GBK'
    soup = BeautifulSoup(r.text,'html.parser')
    novelintro = soup.select("#novelintro")[0].get_text("<br/>",strip=True)
    novelintro_list = novelintro.split("<br/>")
    novelintro = "\n".join(novelintro_list)
    smallreadbody = soup.select(".smallreadbody")[1].get_text()
    summary = novelintro + '\n' + smallreadbody
    #print(summary)
    return summary

def get_intro(novelid, session):
    r = session.get("http://www.jjwxc.net/onebook.php?novelid=" + str(novelid))
    r.encoding = 'GBK'
    soup = BeautifulSoup(r.text,'html.parser')
    rightuls = soup.select("ul.rightul")[0]
    intro = ""
    for rightul in rightuls.select("li"):
        intro = intro + rightul.get_text(strip=True) + '\n'
    #print(intro)
    return intro

def get_link(novelid, n ,session):
    r = session.get("https://m.jjwxc.net/book2/" + str(novelid) + "?more=0&whole=1")
    r.encoding = 'GBK'
    soup = BeautifulSoup(r.text,'html.parser')
    all_links = soup.select("body > div.grid-c > div:nth-child(9) > div:nth-child(4) a")
    link = all_links[n].get("href")
    return link

def get_contents(novelid, VIP, session):
    print("获取目录…")
    r = session.get("http://www.jjwxc.net/onebook.php?novelid=" + str(novelid))
    r.encoding = 'GBK'
    soup = BeautifulSoup(r.text,'html.parser')
    tbody = soup.select("tbody")[0]
    author = tbody.select("h2")[0].get_text(strip=True)
    name = tbody.select("h1")[0].get_text(strip=True)
    contents_html = tbody.select("tr")[3:-1]
    contents = []
    i = 0
    for content_html in contents_html:
        #print(i)
        try:
            contents.append([0,content_html.select('td > b')[0].get_text()])
        except:
            chapter = content_html.select("td")[0].get_text(strip=True)
            title = content_html.select("td")[1].get_text(strip=True)
            summary = content_html.select("td")[2].get_text(strip=True)
            link = "https://m.jjwxc.net" + get_link(novelid, i, session)
            contents.append([1,[chapter, title, summary], link])
            i += 1
            if not VIP:
                try:
                    if content_html.select('a > font[color=red]')[0].get_text() == "[VIP]":
                        del contents[-1]
                        break
                except:
                    continue
    return author, name, contents

def get_all_text(url, session):
    r = session.get(url)
    r.encoding = 'GBK'
    #print(r.text[3000:-1000])
    
    soup = BeautifulSoup(r.text,'html.parser')
    all_text = soup.select("ul")[0].select("li")
    text_list = []
    for li in all_text:
        sort_text_1 = "\n".join(li.get_text("<br/>").split("<br/>"))
        sort_text_2 = "  ".join(sort_text_1.split("\u3000"))
        text_list.append(sort_text_2)
        #text = text + "\n————————————\n" + sort_text_2
    text = "\n————————————\n".join(text_list) + "\n"
    return text

def write_to_txt(novelids, login, session):
    for novelid in novelids:
        #session = requests.session()
        summary = get_summary(novelid, session)
        intro = get_intro(novelid, session)
        author, name, contents = get_contents(novelid, login, session)
        
        
        file_name = name + "_" + author + ".txt"
        '''
        while path.exists(file_name):
            file_name = file_name + "_1"
        '''
        print(file_name)
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(name + "_" + author + "\n\n" + intro + "\n" + summary + "\n\n\n")
            for chapter in contents:
                if chapter[0]:
                    text = get_all_text(chapter[2], session)
                    title = chapter[1][0] + "   " + chapter[1][1] + "\n" + chapter[1][2]
                    f.write(title + "\n" + text + "\n\n")
                    print(title)
                else:
                    f.write("\n\n————" + chapter[1] + "————\n\n")
                    print(chapter[1])
        print("done")

def get_pic(novelid, file_name, session):
    print("获取图片…")
    r = session.get("http://www.jjwxc.net/onebook.php?novelid=" + str(novelid))
    r.encoding = 'GBK'
    soup = BeautifulSoup(r.text,'html.parser')
    pic_url = soup.select("img.noveldefaultimage")[0].get("src")
    p = session.get(pic_url)
    return p.content

def write_to_epub(novelids, login, session):
    for novelid in novelids:
        e = Epub()
        e.summary = get_summary(novelid, session)
        e.intro = get_intro(novelid, session)
        e.author, e.name, contents = get_contents(novelid, login, session)
        e.init()
        pic_con = get_pic(novelid, e.filename, session)
        e.write_pic(pic_con)
        e.write_coverandintro()
        e.write_chapters(contents)
        for chapter in contents:
            if chapter[0]:
                text = get_all_text(chapter[2], session)
                print(chapter[1][0], " ", chapter[1][1])
                e.write_text(chapter[1], text)
        e.packet()

if __name__ == "__main__":
    config = get_config()
    if config["login"]:
        if config["cookie_login"]:
            session = login_with_cookie(config["cookies"])
        else:
            session = login_with_password(config["loginname"], config["loginpass"])
    else:
        session = requests.session()
    if not config["epub"]:
    	write_to_txt(config["novelids"],config["login"], session)
    else:
    	write_to_epub(config["novelids"],config["login"], session)

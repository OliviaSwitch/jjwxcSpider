# jjwxcSpider


## 关于使用
#### clone
```
$ git clone https://github.com/gaoliujiadi/jjwxcSpider.git
$ cd watchlist
```

#### 创建环境
```
$ python -m venv env  # use `virtualenv env` for Python2, use `python3 ...` for Python3 on Linux & macOS
$ source env/bin/activate  # use `env\Scripts\activate` on Windows
$ pip install -r requirements.txt
```

#### 设置“comfig.json”
- "login"填"true"or"false"选择是否需要登录，如果需要登录则继续选填以下几项。
- "epub"填"true"or"false"选择是否需要epub格式书籍。
- "cookie_login"填"true"or"false"选择是否需要使用cookie登录，如果使用cookie登录，则将cookie填入引号内；如果使用密码登录，则将晋江邮箱或笔名或手机号填入"loginname"中，将密码填入"loginpass"中。
  - cookie的获取：使用chrome或其它浏览器，打开网址："https://m.jjwxc.net/"，
  登陆后打开开发者工具，在控制台中输入：`document.cookie`
- 将你需要下载的晋江小说书号填入"novelids"中。
  - 小说书号的获取：
    - app端可以点开作者专栏，每本小说的左下角，显示`ID:XXXXXX`，点击即可复制。
    - 网页端这在地址栏中，跟在“novelid”后。
- 最后执行`python main.py`

#### 运行
```
$ python main.py
```

## `get_authors_.py`
用于获取某个作者全部作品的id号。
材料：
- 作者专栏号
- `$ python get_authors_.py`
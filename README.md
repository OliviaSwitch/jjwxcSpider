# jjwxcSpide
## 关于使用
先设置“comfig.json”。
- "login"填"true"or"false"选择是否需要登录，如果需要登录则继续选填以下几项。
- "cookie_login"填"true"or"false"选择是否需要使用cookie登录，如果使用cookie登录，则将cookie填入引号内。如果使用密码登录，则将晋江邮箱或笔名或手机号填入"loginname"中，将密码填入"loginpass"中。
  - cookie的获取：使用chrome或其它浏览器，打开开发者工具，在控制台中输入：document.cookie
- 将你需要下载的晋江小说书号填入"novelids"中。
  - 小说书号的获取：
    - app端可以点开作者专栏，每本小说的右上角就有。
    - 网页端这在地址栏中，跟在“novelid”后

再使用python直接运行“2txt.py”

## 所需库
- requests
- beautifulsoup

## 测试环境
- win10 x64
- 手机app：termux 0.94

# -*- coding: UTF-8 -*-
import zipfile
import os
from shutil import rmtree

class Epub():
    def __init__(self):
        self.name = ""
        self.author = ""
        self.summary = ""
        self.intro = ""

    def init(self):
        name, author = self.name, self.author
        self.filename = name + "_" + author
        while os.path.exists(self.filename):
            self.filename = self.filename + "_1"
        os.mkdir(self.filename)
        os.mkdir(os.path.join(self.filename, "META-INF"))
        os.mkdir(os.path.join(self.filename, "OEBPS"))
        os.mkdir(os.path.join(self.filename, "OEBPS", "Text"))
        os.mkdir(os.path.join(self.filename, "OEBPS", "Images"))
        #os.mkdir(self.filename + "\\OEBPS\\Styles")
        with open(os.path.join(self.filename, "mimetype"), "a", encoding="utf-8") as f:
            f.write("application/epub+zip")
        with open(os.path.join(self.filename, "META-INF", "container.xml"), "a", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n')
            f.write('<rootfiles>\n  <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>\n</rootfiles>\n</container>')
        with open(os.path.join(self.filename,"OEBPS", "content.opf"), "a", encoding="utf-8") as f:
            f.write('''<?xml version="1.0" encoding="utf-8"?>
<package version="2.0" unique-identifier="uid" xmlns="http://www.idpf.org/2007/opf">
            ''')
            f.write('\n  <metadata xmlns:opf="http://www.idpf.org/2007/opf" xmlns:dc="http://purl.org/dc/elements/1.1/">')
            f.write("\n    <dc:title>%s</dc:title>" %self.name)
            f.write("\n    <dc:creator>%s</dc:creator>" %self.author)
            f.write("\n    <dc:language>zh-CN</dc:language>")
            f.write("\n    <dc:description>%s</dc:description>" %self.summary)
            f.write('\n    <meta content="cover.jpg" name="cover" />')
            f.write('\n    <meta content="utf-8" name="output encoding" />\n  </metadata>\n')
        with open(os.path.join(self.filename, "OEBPS", "toc.ncx"), "a", encoding="utf-8") as f:
            f.write('''<?xml version='1.0' encoding='utf-8'?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="zh">

<head>
    <meta content="" name="dtb:uid"/>
    <meta content="2" name="dtb:depth"/>
    <meta content="0" name="dtb:totalPageCount"/>
    <meta content="0" name="dtb:maxPageNumber"/>
</head>
            ''')
            f.write("\n<docTitle>\n<text>%s</text>\n</docTitle>" %self.name)

    def write_pic(self, content):
        filename = os.path.join(self.filename, "OEBPS", "Images", "cover.jpg")
        with open(filename, "wb") as f:
            f.write(content)

    def re_sort_cons(self,contents):#[[0, "roll_1"], [1, [chap_1, tit_1, sum_1], link]]
        i = 0
        cons = []
        try:# [["roll_1", ["chap_1", "tit_1", "sum_1"]]]
            for chap in contents:
                if not chap[0]:
                    roll = [chap[1]]
                    cons.append(roll)
                    i += 1
                else:
                    cons[i - 1].append(chap[1])
            flag = True
        except:
            for chap in contents:
                cons.append(chap[1])
            flag = False
        return cons, flag

    def write_chapters(self, contents):
        with open(os.path.join(self.filename, "OEBPS", "content.opf"), "a", encoding="utf-8") as f:
            f.write("\n  <manifest>")
            f.write('\n    <item id="cover.xhtml" href="Text/cover.xhtml" media-type="application/xhtml+xml"/>')
            f.write('\n    <item id="intro.xhtml" href="Text/intro.xhtml" media-type="application/xhtml+xml"/>')
            for chap in contents:
                if chap[0]:
                    f.write('\n    <item id="{0}.xhtml" href="Text/{0}.xhtml" media-type="application/xhtml+xml"/>'.format("chap_" + chap[1][0]))
            f.write('\n    <item id="cover.jpg" href="Images/cover.jpg" media-type="image/jpeg"/>')
            f.write('\n    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>')
            f.write("\n  </manifest>")
            f.write('\n  <spine toc="ncx">')
            f.write('\n    <itemref idref="cover.xhtml"/>')
            f.write('\n    <itemref idref="intro.xhtml"/>')
            for chap in contents:
                if chap[0]:
                    f.write('\n    <itemref idref="{}.xhtml"/>'.format("chap_" + chap[1][0]))
            f.write('\n  </spine>')
        with open(os.path.join(self.filename, "OEBPS", "toc.ncx"), "a", encoding="utf-8") as f:
            f.write("\n<navMap>\n")
            f.write('''  <navPoint id="np_1" playOrder="1">
    <navLabel>
      <text>Cover</text>
    </navLabel>
    <content src="Text/cover.xhtml"/>
  </navPoint>
    <navPoint id="np_2" playOrder="2">
    <navLabel>
      <text>简介</text>
    </navLabel>
    <content src="Text/intro.xhtml"/>
  </navPoint>''')
            contents, flag = self.re_sort_cons(contents)
            #i = 0
            j = 2
            for rolls in contents:
                j += 1
                #;i += 1
                f.write('\n  <navPoint id="np_{0}" playOrder="{0}">'.format(str(j)))
                f.write('\n    <navLabel>')
                if flag:
                    f.write('\n      <text>%s</text>' %rolls[0])
                else:
                    f.write('\n      <text>{0} {1}        {2}</text>'.format(rolls[0], rolls[1], rolls[2]))
                f.write('\n    </navLabel>')
                if flag:
                    f.write('\n    <content src="Text/{}.xhtml"/>'.format("chap_"+rolls[1][0]))
                    #i += 1
                else:
                    f.write('\n    <content src="Text/{}.xhtml"/>'.format("chap_"+rolls[0]))
                if flag:
                	for chap in rolls[1:]:
                		j += 1
                		f.write('\n    <navPoint id="np_{0}" playOrder="{0}">'.format(str(j)))
                		f.write('\n      <navLabel>')
                		f.write('\n        <text>{0} {1}        {2}</text>'.format(chap[0], chap[1], chap[2]))
                		f.write('\n      </navLabel>')
                		f.write('\n      <content src="Text/{}.xhtml"/>'.format("chap_"+chap[0]))
                		f.write('\n    </navPoint>')
                f.write('\n  </navPoint>')
            f.write("\n</navMap>")
        
    def write_text(self, title, text):# title输入列表
        filename = os.path.join(self.filename, "OEBPS", "Text", "chap_{}.xhtml".format(title[0]))
        with open(filename, "w", encoding="utf-8") as f:
            #我吐了因为垃圾晋江用转义以及一系列问题，有锁章的小说软件会读不了，回头再搞
            f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\n"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n')
            f.write('\n<head>')
            f.write('\n  <meta charset="utf-8"/>')
            f.write('\n  <title>{0} {1}</title>'.format(title[0], title[1]))
            f.write('\n</head>\n')
            f.write('\n<body>')
            f.write('\n  <h2>{0} {1}</h2>'.format(title[0], title[1]))
            f.write('\n  <h3>{0}</h3>'.format(title[2]))
            for para in text.split("\n"):
                f.write('\n  <p>%s</p>'%para)
            f.write('\n</body>')
            f.write('\n</html>')

    def write_coverandintro(self):
        filename = os.path.join(self.filename, "OEBPS", "Text", "cover.xhtml")
        with open(filename, "w", encoding="utf-8") as f:
            f.write('''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
 
<html xmlns="http://www.w3.org/1999/xhtml">
 
<head>
  <meta charset="utf-8"/>
  <title>Cover</title>
</head>
 
<body>
    <img src="../Images/cover.jpg"/>
</body>
 
</html>''')
        filename = os.path.join(self.filename, "OEBPS", "Text", "intro.xhtml")
        with open(filename, "w", encoding="utf-8") as f:
            f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\n"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">')
            f.write('\n<head>\n  <meta charset="utf-8"/>\n  <title>intro</title>\n</head>')
            f.write('\n<body>\n  <h1>简介</h1>')
            #f.write('\n  <p>Intro</p>')
            for para in self.intro.split("\n"):
                f.write('\n  <p>%s</p>'%para)
            f.write('\n  <h1>文案</h1>')
            for para in self.summary.split("\n"):
                f.write('\n  <p>%s</p>'%para)
            f.write('\n</body>\n</html>')

    def packet(self):
        print("打包为epub文件…")
        with open(os.path.join(self.filename, "OEBPS", "content.opf"), "a", encoding="utf-8") as f:
            f.write("\n</package>")
        with open(os.path.join(self.filename, "OEBPS","toc.ncx"), "a", encoding="utf-8") as f:
            f.write("\n</ncx>")

        file_list = []
        for maindir, subdir, file_name_list in os.walk(self.filename):
            for file_name in file_name_list:
                apath = os.path.join(maindir, file_name)
                file_list.append(apath)
        z = zipfile.ZipFile(self.filename + ".epub", "w", zipfile.ZIP_STORED)
        sep = os.sep
        for file in file_list:
        	new_file = sep.join(file.split(sep)[1:])
        	z.write(file, new_file)
        	#print(file)
        rmtree(self.filename)
        z.close()

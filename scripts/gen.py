#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SongGems · 经典歌曲年榜 — 数据生成器
数据唯一来源：本文件 SONGS 数组。改动后 `python3 scripts/gen.py` 重建 index.html 标记区。
年份以歌曲/专辑发行年为准（部分经典存在多个版本，允许 ±1 年出入，页面已有说明）。
"""
import re, urllib.parse

# r: cn=华语 w=世界 | y: 发行年(参考) | n: 歌名 | a: 歌手 | tag: 可选备注
SONGS = [
    # ---------- 华语 · 70-80年代 ----------
    {"r":"cn","y":1977,"n":"月亮代表我的心","a":"邓丽君","tag":"传唱度最高的华语情歌"},
    {"r":"cn","y":1979,"n":"橄榄树","a":"齐豫","tag":"台湾民歌运动巅峰"},
    {"r":"cn","y":1980,"n":"龙的传人","a":"李建复"},
    {"r":"cn","y":1982,"n":"光阴的故事","a":"罗大佑","tag":"华语流行教父出道"},
    {"r":"cn","y":1983,"n":"风继续吹","a":"张国荣"},
    {"r":"cn","y":1984,"n":"我的中国心","a":"张明敏","tag":"春晚国民金曲"},
    {"r":"cn","y":1984,"n":"雾之恋","a":"谭咏麟"},
    {"r":"cn","y":1984,"n":"似水流年","a":"梅艳芳"},
    {"r":"cn","y":1985,"n":"Monica","a":"张国荣","tag":"粤语快歌里程碑"},
    {"r":"cn","y":1985,"n":"狼","a":"齐秦"},
    {"r":"cn","y":1986,"n":"一无所有","a":"崔健","tag":"中国摇滚开山之作"},
    {"r":"cn","y":1987,"n":"一场游戏一场梦","a":"王杰"},
    {"r":"cn","y":1987,"n":"大约在冬季","a":"齐秦"},
    {"r":"cn","y":1988,"n":"恋曲1990","a":"罗大佑"},
    {"r":"cn","y":1989,"n":"梦醒时分","a":"陈淑桦"},
    # ---------- 华语 · 90年代 ----------
    {"r":"cn","y":1989,"n":"真的爱你","a":"Beyond","tag":"献给母亲的赞歌"},
    {"r":"cn","y":1990,"n":"光辉岁月","a":"Beyond","tag":"致敬曼德拉"},
    {"r":"cn","y":1990,"n":"爱上一个不回家的人","a":"林忆莲"},
    {"r":"cn","y":1990,"n":"失恋阵线联盟","a":"草蜢"},
    {"r":"cn","y":1991,"n":"潇洒走一回","a":"叶倩文"},
    {"r":"cn","y":1991,"n":"爱","a":"小虎队"},
    {"r":"cn","y":1992,"n":"吻别","a":"张学友","tag":"华语唱片销量神话"},
    {"r":"cn","y":1993,"n":"海阔天空","a":"Beyond","tag":"Beyond 精神图腾"},
    {"r":"cn","y":1993,"n":"凡人歌","a":"李宗盛"},
    {"r":"cn","y":1993,"n":"爱如潮水","a":"张信哲"},
    {"r":"cn","y":1994,"n":"我愿意","a":"王菲"},
    {"r":"cn","y":1994,"n":"同桌的你","a":"老狼","tag":"校园民谣代表"},
    {"r":"cn","y":1995,"n":"一千个伤心的理由","a":"张学友"},
    {"r":"cn","y":1996,"n":"心太软","a":"任贤齐"},
    # ---------- 华语 · 00-10年代 ----------
    {"r":"cn","y":1997,"n":"朋友","a":"周华健"},
    {"r":"cn","y":1998,"n":"红豆","a":"王菲"},
    {"r":"cn","y":1998,"n":"对面的女孩看过来","a":"任贤齐"},
    {"r":"cn","y":1999,"n":"爱你一万年","a":"刘德华"},
    {"r":"cn","y":2000,"n":"可爱女人","a":"周杰伦","tag":"周杰伦时代开启"},
    {"r":"cn","y":2000,"n":"天黑黑","a":"孙燕姿"},
    {"r":"cn","y":2001,"n":"简单爱","a":"周杰伦"},
    {"r":"cn","y":2002,"n":"他一定很爱你","a":"阿杜"},
    {"r":"cn","y":2003,"n":"十年","a":"陈奕迅","tag":"KTV 国民金曲"},
    {"r":"cn","y":2003,"n":"遇见","a":"孙燕姿"},
    {"r":"cn","y":2003,"n":"江南","a":"林俊杰"},
    {"r":"cn","y":2004,"n":"2002年的第一场雪","a":"刀郎"},
    {"r":"cn","y":2004,"n":"七里香","a":"周杰伦"},
    {"r":"cn","y":2004,"n":"倔强","a":"五月天"},
    {"r":"cn","y":2005,"n":"发如雪","a":"周杰伦","tag":"中国风代表作"},
    {"r":"cn","y":2006,"n":"隐形的翅膀","a":"张韶涵"},
    {"r":"cn","y":2006,"n":"舞娘","a":"蔡依林"},
    {"r":"cn","y":2007,"n":"青花瓷","a":"周杰伦","tag":"中国风巅峰"},
    {"r":"cn","y":2007,"n":"好久不见","a":"陈奕迅"},
    {"r":"cn","y":2008,"n":"稻香","a":"周杰伦"},
    {"r":"cn","y":2008,"n":"突然好想你","a":"五月天"},
    {"r":"cn","y":2010,"n":"老男孩","a":"筷子兄弟","tag":"微电影时代国民泪点"},
    {"r":"cn","y":2013,"n":"董小姐","a":"宋冬野"},
    {"r":"cn","y":2014,"n":"平凡之路","a":"朴树","tag":"复出封神之作"},
    # ---------- 世界 · 50-70年代 ----------
    {"r":"w","y":1958,"n":"Johnny B. Goode","a":"Chuck Berry","tag":"摇滚吉他的原点"},
    {"r":"w","y":1961,"n":"Stand by Me","a":"Ben E. King"},
    {"r":"w","y":1962,"n":"Love Me Do","a":"The Beatles","tag":"披头士首支单曲"},
    {"r":"w","y":1963,"n":"Blowin' in the Wind","a":"Bob Dylan","tag":"民谣抗议圣歌"},
    {"r":"w","y":1965,"n":"(I Can't Get No) Satisfaction","a":"The Rolling Stones"},
    {"r":"w","y":1965,"n":"Yesterday","a":"The Beatles","tag":"被翻唱最多的歌"},
    {"r":"w","y":1965,"n":"California Dreamin'","a":"The Mamas & the Papas"},
    {"r":"w","y":1966,"n":"God Only Knows","a":"The Beach Boys"},
    {"r":"w","y":1967,"n":"Respect","a":"Aretha Franklin","tag":"灵魂乐女皇宣言"},
    {"r":"w","y":1968,"n":"Hey Jude","a":"The Beatles"},
    {"r":"w","y":1969,"n":"Suspicious Minds","a":"Elvis Presley","tag":"猫王复出之作"},
    # ---------- 世界 · 70年代 ----------
    {"r":"w","y":1970,"n":"Bridge over Troubled Water","a":"Simon & Garfunkel"},
    {"r":"w","y":1970,"n":"Let It Be","a":"The Beatles"},
    {"r":"w","y":1971,"n":"Stairway to Heaven","a":"Led Zeppelin","tag":"摇滚圣经"},
    {"r":"w","y":1971,"n":"Imagine","a":"John Lennon","tag":"和平圣歌"},
    {"r":"w","y":1972,"n":"Smoke on the Water","a":"Deep Purple","tag":"最著名的吉他 Riff"},
    {"r":"w","y":1973,"n":"Money","a":"Pink Floyd"},
    {"r":"w","y":1974,"n":"Waterloo","a":"ABBA","tag":"欧洲歌唱大赛夺冠曲"},
    {"r":"w","y":1974,"n":"Sweet Home Alabama","a":"Lynyrd Skynyrd"},
    {"r":"w","y":1975,"n":"Bohemian Rhapsody","a":"Queen","tag":"摇滚歌剧神作"},
    {"r":"w","y":1975,"n":"Born to Run","a":"Bruce Springsteen"},
    {"r":"w","y":1976,"n":"Dancing Queen","a":"ABBA"},
    {"r":"w","y":1977,"n":"Hotel California","a":"Eagles","tag":"必听结尾吉他solo"},
    {"r":"w","y":1978,"n":"Stayin' Alive","a":"Bee Gees","tag":"迪斯科时代象征"},
    {"r":"w","y":1979,"n":"Another Brick in the Wall (Part II)","a":"Pink Floyd"},
    # ---------- 世界 · 80年代 ----------
    {"r":"w","y":1980,"n":"(Just Like) Starting Over","a":"John Lennon"},
    {"r":"w","y":1981,"n":"Under Pressure","a":"Queen & David Bowie"},
    {"r":"w","y":1983,"n":"Billie Jean","a":"Michael Jackson","tag":"流行之王的月球漫步"},
    {"r":"w","y":1983,"n":"Every Breath You Take","a":"The Police"},
    {"r":"w","y":1984,"n":"Purple Rain","a":"Prince"},
    {"r":"w","y":1984,"n":"Careless Whisper","a":"Wham!"},
    {"r":"w","y":1985,"n":"Take On Me","a":"a-ha","tag":"经典 MV 手绘动画"},
    {"r":"w","y":1986,"n":"Livin' on a Prayer","a":"Bon Jovi"},
    {"r":"w","y":1987,"n":"Sweet Child O' Mine","a":"Guns N' Roses"},
    {"r":"w","y":1987,"n":"I Wanna Dance with Somebody","a":"Whitney Houston"},
    {"r":"w","y":1988,"n":"Don't Worry Be Happy","a":"Bobby McFerrin"},
    {"r":"w","y":1989,"n":"Like a Prayer","a":"Madonna"},
    # ---------- 世界 · 90年代 ----------
    {"r":"w","y":1991,"n":"Smells Like Teen Spirit","a":"Nirvana","tag":"垃圾摇滚引爆点"},
    {"r":"w","y":1991,"n":"Losing My Religion","a":"R.E.M."},
    {"r":"w","y":1992,"n":"I Will Always Love You","a":"Whitney Houston","tag":"电影《保镖》主题曲"},
    {"r":"w","y":1993,"n":"Creep","a":"Radiohead"},
    {"r":"w","y":1995,"n":"Wonderwall","a":"Oasis","tag":"英伦摇滚国民曲"},
    {"r":"w","y":1996,"n":"Wannabe","a":"Spice Girls"},
    {"r":"w","y":1997,"n":"Candle in the Wind 1997","a":"Elton John","tag":"致敬戴安娜王妃"},
    {"r":"w","y":1998,"n":"I Don't Want to Miss a Thing","a":"Aerosmith"},
    {"r":"w","y":1999,"n":"Livin' la Vida Loca","a":"Ricky Martin"},
    {"r":"w","y":1999,"n":"Smooth","a":"Santana feat. Rob Thomas"},
    # ---------- 世界 · 00-10年代 ----------
    {"r":"w","y":2000,"n":"Oops!… I Did It Again","a":"Britney Spears"},
    {"r":"w","y":2001,"n":"In the End","a":"Linkin Park","tag":"新金属时代地标"},
    {"r":"w","y":2002,"n":"Lose Yourself","a":"Eminem","tag":"奥斯卡最佳原创歌曲"},
    {"r":"w","y":2002,"n":"The Scientist","a":"Coldplay"},
    {"r":"w","y":2003,"n":"Bring Me to Life","a":"Evanescence"},
    {"r":"w","y":2004,"n":"Boulevard of Broken Dreams","a":"Green Day"},
    {"r":"w","y":2004,"n":"This Love","a":"Maroon 5"},
    {"r":"w","y":2004,"n":"Vertigo","a":"U2"},
    {"r":"w","y":2005,"n":"You're Beautiful","a":"James Blunt"},
    {"r":"w","y":2006,"n":"SexyBack","a":"Justin Timberlake"},
    {"r":"w","y":2007,"n":"Umbrella","a":"Rihanna"},
    {"r":"w","y":2008,"n":"Single Ladies (Put a Ring on It)","a":"Beyoncé"},
    {"r":"w","y":2008,"n":"Viva la Vida","a":"Coldplay"},
    {"r":"w","y":2009,"n":"Poker Face","a":"Lady Gaga"},
    {"r":"w","y":2011,"n":"Rolling in the Deep","a":"Adele","tag":"格莱美横扫之年"},
    {"r":"w","y":2012,"n":"Somebody That I Used to Know","a":"Gotye feat. Kimbra"},
    {"r":"w","y":2013,"n":"Happy","a":"Pharrell Williams"},
    {"r":"w","y":2014,"n":"Blank Space","a":"Taylor Swift"},
    {"r":"w","y":2014,"n":"Thinking Out Loud","a":"Ed Sheeran"},
    {"r":"w","y":2015,"n":"Hello","a":"Adele"},
]

MARK_L = "<!--SONGS:START-->"
MARK_R = "<!--SONGS:END-->"
DATA_L = "/*SONGSDATA:START*/"
DATA_R = "/*SONGSDATA:END*/"

def qq_url(n, a):
    return "https://y.qq.com/n/ryqq/search?w=" + urllib.parse.quote(f"{n} {a}")

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def build():
    html = open("index.html", encoding="utf-8").read()
    # 按 (region, year) 分组，年内保持精选顺序
    blocks = {"cn": [], "w": []}
    seen = {}
    for r in ("cn", "w"):
        years = sorted({s["y"] for s in SONGS if s["r"] == r})
        for y in years:
            items = [s for s in SONGS if s["r"] == r and s["y"] == y]
            lis = []
            for i, s in enumerate(items, 1):
                q = qq_url(s["n"], s["a"])
                tag = f'<span class="tag">{esc(s["tag"])}</span>' if s.get("tag") else ""
                lis.append(
                    f'<li data-y="{y}" data-search="{esc((s["n"]+" "+s["a"]).lower())}">'
                    f'<span class="rk">{i}</span>'
                    f'<span class="tx"><span class="tn">{esc(s["n"])}</span>'
                    f'<span class="ta">{esc(s["a"])}{tag}</span></span>'
                    f'<a class="qq" href="{q}" target="_blank" rel="noopener" data-en="Play on QQ Music ↗">QQ 音乐播放 ↗</a></li>'
                )
            blocks[r].append(f'<section class="yr" data-year="{y}"><h3>{y}</h3><ol class="sc">{"".join(lis)}</ol></section>')
    new_cards = (MARK_L + '<div class="yrset" id="setCN">' + "".join(blocks["cn"]) + "</div>"
                 + '<div class="yrset" id="setW" hidden>' + "".join(blocks["w"]) + "</div>" + MARK_R)
    html = re.sub(re.escape(MARK_L) + ".*?" + re.escape(MARK_R), lambda m: new_cards, html, flags=re.S)
    data = [{"r":s["r"],"y":s["y"],"n":s["n"],"a":s["a"],**( {"tag":s["tag"]} if s.get("tag") else {} )} for s in SONGS]
    import json as J
    new_data = DATA_L + J.dumps(data, ensure_ascii=False) + DATA_R
    html = re.sub(re.escape(DATA_L) + ".*?" + re.escape(DATA_R), lambda m: new_data, html, flags=re.S)
    open("index.html", "w", encoding="utf-8").write(html)
    cn = sum(1 for s in SONGS if s["r"]=="cn"); w = len(SONGS)-cn
    print(f"rebuilt: {len(SONGS)} songs (华语 {cn} / 世界 {w}), {len(blocks['cn'])}+{len(blocks['w'])} year sections")

if __name__ == "__main__":
    build()

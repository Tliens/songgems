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
    {"r":"cn","y":1994,"n":"十七岁的雨季","a":"林志颖"},
    {"r":"cn","y":1998,"n":"记事本","a":"陈慧琳"},
    {"r":"cn","y":2007,"n":"彩虹","a":"周杰伦"},
    {"r":"w","y":1971,"n":"Maggie May","a":"Rod Stewart"},
    {"r":"w","y":1973,"n":"Goodbye Yellow Brick Road","a":"Elton John"},
    {"r":"w","y":1980,"n":"Woman in Love","a":"Barbra Streisand"},
    {"r":"w","y":1990,"n":"To Be with You","a":"Mr. Big"},
    {"r":"w","y":1996,"n":"Killing Me Softly","a":"Fugees"},
    # ---------- 华语扩容 · 70-80年代 ----------
    {"r":"cn","y":1973,"n":"千言万语","a":"邓丽君"},
    {"r":"cn","y":1977,"n":"我是一片云","a":"凤飞飞"},
    {"r":"cn","y":1979,"n":"小城故事","a":"邓丽君"},
    {"r":"cn","y":1979,"n":"甜蜜蜜","a":"邓丽君"},
    {"r":"cn","y":1980,"n":"恋曲1980","a":"罗大佑"},
    {"r":"cn","y":1980,"n":"上海滩","a":"叶丽仪","tag":"电视剧主题曲天花板"},
    {"r":"cn","y":1980,"n":"恰似你的温柔","a":"蔡琴"},
    {"r":"cn","y":1981,"n":"三月里的小雨","a":"刘文正"},
    {"r":"cn","y":1982,"n":"童年","a":"罗大佑"},
    {"r":"cn","y":1982,"n":"万水千山总是情","a":"汪明荃"},
    {"r":"cn","y":1982,"n":"野百合也有春天","a":"潘越云"},
    {"r":"cn","y":1983,"n":"一剪梅","a":"费玉清"},
    {"r":"cn","y":1983,"n":"铁血丹心","a":"罗文&甄妮","tag":"射雕英雄传"},
    {"r":"cn","y":1983,"n":"万里长城永不倒","a":"叶振棠","tag":"霍元甲主题曲"},
    {"r":"cn","y":1983,"n":"偏偏喜欢你","a":"陈百强"},
    {"r":"cn","y":1983,"n":"漫步人生路","a":"邓丽君","tag":"粤语代表作"},
    {"r":"cn","y":1983,"n":"但愿人长久","a":"邓丽君"},
    {"r":"cn","y":1983,"n":"酒干倘卖无","a":"苏芮"},
    {"r":"cn","y":1983,"n":"跟着感觉走","a":"苏芮"},
    {"r":"cn","y":1984,"n":"难忘今宵","a":"李谷一","tag":"春晚守门歌"},
    {"r":"cn","y":1985,"n":"明天会更好","a":"群星"},
    {"r":"cn","y":1985,"n":"朋友","a":"谭咏麟"},
    {"r":"cn","y":1985,"n":"爱在深秋","a":"谭咏麟"},
    {"r":"cn","y":1985,"n":"顺流逆流","a":"徐小凤"},
    {"r":"cn","y":1985,"n":"爱情陷阱","a":"谭咏麟"},
    {"r":"cn","y":1986,"n":"掌声响起","a":"凤飞飞"},
    {"r":"cn","y":1986,"n":"几许风雨","a":"罗文"},
    {"r":"cn","y":1987,"n":"粉红色的回忆","a":"韩宝仪"},
    {"r":"cn","y":1987,"n":"冬天里的一把火","a":"费翔"},
    {"r":"cn","y":1987,"n":"故乡的云","a":"费翔"},
    {"r":"cn","y":1987,"n":"外面的世界","a":"齐秦"},
    {"r":"cn","y":1987,"n":"月半小夜曲","a":"李克勤"},
    {"r":"cn","y":1987,"n":"倩女幽魂","a":"张国荣"},
    {"r":"cn","y":1988,"n":"爱拼才会赢","a":"叶启田","tag":"闽南语国民曲"},
    {"r":"cn","y":1988,"n":"沉默是金","a":"张国荣"},
    {"r":"cn","y":1988,"n":"喜欢你","a":"Beyond"},
    {"r":"cn","y":1988,"n":"你的样子","a":"罗大佑"},
    {"r":"cn","y":1988,"n":"天天想你","a":"张雨生"},
    {"r":"cn","y":1988,"n":"水中花","a":"谭咏麟"},
    # ---------- 华语扩容 · 90年代 ----------
    {"r":"cn","y":1989,"n":"一生何求","a":"陈百强"},
    {"r":"cn","y":1989,"n":"再回首","a":"姜育恒"},
    {"r":"cn","y":1989,"n":"其实你不懂我的心","a":"童安格"},
    {"r":"cn","y":1989,"n":"千千阙歌","a":"陈慧娴"},
    {"r":"cn","y":1989,"n":"我想有个家","a":"潘美辰"},
    {"r":"cn","y":1989,"n":"让我一次爱个够","a":"庾澄庆"},
    {"r":"cn","y":1989,"n":"花房姑娘","a":"崔健"},
    {"r":"cn","y":1990,"n":"我是一只小小鸟","a":"赵传"},
    {"r":"cn","y":1990,"n":"对你爱不完","a":"郭富城"},
    {"r":"cn","y":1990,"n":"你知道我在等你吗","a":"张洪量"},
    {"r":"cn","y":1991,"n":"无地自容","a":"黑豹","tag":"中国摇滚代表作"},
    {"r":"cn","y":1991,"n":"梦回唐朝","a":"唐朝乐队"},
    {"r":"cn","y":1991,"n":"一起走过的日子","a":"刘德华"},
    {"r":"cn","y":1991,"n":"今夜你会不会来","a":"黎明"},
    {"r":"cn","y":1991,"n":"男儿当自强","a":"林子祥","tag":"黄飞鸿主题曲"},
    {"r":"cn","y":1991,"n":"飘洋过海来看你","a":"娃娃","tag":"李宗盛词曲"},
    {"r":"cn","y":1992,"n":"每天爱你多一些","a":"张学友"},
    {"r":"cn","y":1992,"n":"大海","a":"张雨生"},
    {"r":"cn","y":1992,"n":"星星点灯","a":"郑智化"},
    {"r":"cn","y":1992,"n":"红日","a":"李克勤"},
    {"r":"cn","y":1992,"n":"花心","a":"周华健"},
    {"r":"cn","y":1992,"n":"我不想说","a":"杨钰莹"},
    {"r":"cn","y":1992,"n":"千万次的问","a":"刘欢","tag":"北京人在纽约"},
    {"r":"cn","y":1992,"n":"容易受伤的女人","a":"王菲","tag":"天后成名曲"},
    {"r":"cn","y":1993,"n":"涛声依旧","a":"毛宁"},
    {"r":"cn","y":1993,"n":"用心良苦","a":"张宇"},
    {"r":"cn","y":1993,"n":"九百九十九朵玫瑰","a":"邰正宵"},
    {"r":"cn","y":1993,"n":"新不了情","a":"万芳","tag":"电影同名主题曲"},
    {"r":"cn","y":1993,"n":"小芳","a":"李春波"},
    {"r":"cn","y":1993,"n":"味道","a":"辛晓琪"},
    {"r":"cn","y":1994,"n":"忘情水","a":"刘德华"},
    {"r":"cn","y":1994,"n":"棋子","a":"王菲"},
    {"r":"cn","y":1994,"n":"执着","a":"田震"},
    {"r":"cn","y":1994,"n":"回到拉萨","a":"郑钧"},
    {"r":"cn","y":1994,"n":"祝你平安","a":"孙悦"},
    {"r":"cn","y":1994,"n":"懂你","a":"满文军"},
    {"r":"cn","y":1994,"n":"刀剑如梦","a":"周华健","tag":"倚天屠龙记"},
    {"r":"cn","y":1994,"n":"领悟","a":"辛晓琪"},
    {"r":"cn","y":1995,"n":"离开以后","a":"张学友"},
    {"r":"cn","y":1995,"n":"大中国","a":"高枫"},
    {"r":"cn","y":1995,"n":"春天的故事","a":"董文华"},
    {"r":"cn","y":1996,"n":"姐妹","a":"张惠妹"},
    {"r":"cn","y":1996,"n":"剪爱","a":"张惠妹"},
    {"r":"cn","y":1996,"n":"城里的月光","a":"许美静"},
    {"r":"cn","y":1996,"n":"值得","a":"郑秀文"},
    {"r":"cn","y":1996,"n":"精忠报国","a":"屠洪刚"},
    {"r":"cn","y":1997,"n":"青藏高原","a":"李娜"},
    {"r":"cn","y":1997,"n":"听海","a":"张惠妹"},
    {"r":"cn","y":1997,"n":"相约一九九八","a":"那英&王菲"},
    {"r":"cn","y":1997,"n":"爱很简单","a":"陶喆"},
    {"r":"cn","y":1997,"n":"冰雨","a":"刘德华"},
    {"r":"cn","y":1998,"n":"伤心太平洋","a":"任贤齐"},
    {"r":"cn","y":1998,"n":"中国人","a":"刘德华"},
    {"r":"cn","y":1998,"n":"爱我别走","a":"张震岳"},
    {"r":"cn","y":1998,"n":"当","a":"动力火车","tag":"还珠格格主题曲"},
    {"r":"cn","y":1998,"n":"雨蝶","a":"李翊君","tag":"还珠格格片尾曲"},
    {"r":"cn","y":1998,"n":"有多少爱可以重来","a":"迪克牛仔"},
    {"r":"cn","y":1998,"n":"广岛之恋","a":"莫文蔚&张洪量"},
    {"r":"cn","y":1999,"n":"志明与春娇","a":"五月天"},
    {"r":"cn","y":1999,"n":"那些花儿","a":"朴树"},
    {"r":"cn","y":1999,"n":"单身情歌","a":"林志炫"},
    {"r":"cn","y":1999,"n":"约定","a":"周蕙"},
    # ---------- 华语扩容 · 00年代 ----------
    {"r":"cn","y":2000,"n":"至少还有你","a":"林忆莲"},
    {"r":"cn","y":2000,"n":"拯救","a":"孙楠"},
    {"r":"cn","y":2000,"n":"最熟悉的陌生人","a":"萧亚轩"},
    {"r":"cn","y":2000,"n":"勇气","a":"梁静茹"},
    {"r":"cn","y":2000,"n":"温柔","a":"五月天"},
    {"r":"cn","y":2000,"n":"最美","a":"羽泉"},
    {"r":"cn","y":2000,"n":"下沙","a":"游鸿明"},
    {"r":"cn","y":2001,"n":"安静","a":"周杰伦"},
    {"r":"cn","y":2001,"n":"开不了口","a":"周杰伦"},
    {"r":"cn","y":2001,"n":"唯一","a":"王力宏"},
    {"r":"cn","y":2001,"n":"流星雨","a":"F4","tag":"流星花园现象"},
    {"r":"cn","y":2001,"n":"K歌之王","a":"陈奕迅"},
    {"r":"cn","y":2001,"n":"一生有你","a":"水木年华","tag":"校园民谣收山之作"},
    {"r":"cn","y":2001,"n":"开始懂了","a":"孙燕姿"},
    {"r":"cn","y":2001,"n":"屋顶","a":"温岚&周杰伦"},
    {"r":"cn","y":2003,"n":"Super Star","a":"S.H.E"},
    {"r":"cn","y":2003,"n":"说爱你","a":"蔡依林"},
    {"r":"cn","y":2003,"n":"Lydia","a":"F.I.R."},
    {"r":"cn","y":2003,"n":"晴天","a":"周杰伦","tag":"青春回忆杀"},
    {"r":"cn","y":2003,"n":"叶子","a":"阿桑"},
    {"r":"cn","y":2003,"n":"痴心绝对","a":"李圣杰"},
    {"r":"cn","y":2003,"n":"下一站天后","a":"Twins"},
    {"r":"cn","y":2004,"n":"不得不爱","a":"潘玮柏&弦子"},
    {"r":"cn","y":2004,"n":"欧若拉","a":"张韶涵"},
    {"r":"cn","y":2004,"n":"宁夏","a":"梁静茹"},
    {"r":"cn","y":2004,"n":"死了都要爱","a":"信乐团"},
    {"r":"cn","y":2004,"n":"一直很安静","a":"阿桑","tag":"仙剑奇侠传"},
    {"r":"cn","y":2004,"n":"断点","a":"张敬轩"},
    {"r":"cn","y":2004,"n":"两只蝴蝶","a":"庞龙","tag":"网络歌曲时代标志"},
    {"r":"cn","y":2004,"n":"老鼠爱大米","a":"杨臣刚","tag":"网络歌曲元年"},
    {"r":"cn","y":2004,"n":"爱你","a":"王心凌"},
    {"r":"cn","y":2004,"n":"冲动的惩罚","a":"刀郎"},
    {"r":"cn","y":2004,"n":"旅行的意义","a":"陈绮贞"},
    {"r":"cn","y":2004,"n":"大城小爱","a":"王力宏"},
    {"r":"cn","y":2005,"n":"夜曲","a":"周杰伦","tag":"十一月的萧邦"},
    {"r":"cn","y":2005,"n":"童话","a":"光良"},
    {"r":"cn","y":2005,"n":"知足","a":"五月天"},
    {"r":"cn","y":2005,"n":"天路","a":"韩红"},
    {"r":"cn","y":2005,"n":"月亮之上","a":"凤凰传奇"},
    {"r":"cn","y":2005,"n":"认真的雪","a":"薛之谦"},
    {"r":"cn","y":2005,"n":"怒放的生命","a":"汪峰"},
    {"r":"cn","y":2005,"n":"一千年以后","a":"林俊杰"},
    {"r":"cn","y":2005,"n":"恋爱ing","a":"五月天"},
    {"r":"cn","y":2005,"n":"暧昧","a":"杨丞琳"},
    {"r":"cn","y":2005,"n":"浮夸","a":"陈奕迅","tag":"粤语现场封神"},
    {"r":"cn","y":2006,"n":"秋天不回来","a":"王强"},
    {"r":"cn","y":2006,"n":"小情歌","a":"苏打绿"},
    {"r":"cn","y":2006,"n":"独家记忆","a":"陈小春"},
    {"r":"cn","y":2006,"n":"日不落","a":"蔡依林"},
    {"r":"cn","y":2006,"n":"嘻唰唰","a":"花儿乐队"},
    {"r":"cn","y":2006,"n":"爱得太迟","a":"古巨基"},
    {"r":"cn","y":2007,"n":"最炫民族风","a":"凤凰传奇"},
    {"r":"cn","y":2007,"n":"思念是一种病","a":"张震岳"},
    {"r":"cn","y":2007,"n":"爱情转移","a":"陈奕迅","tag":"爱情呼叫转移"},
    {"r":"cn","y":2007,"n":"日不落","a":"蔡依林"},
    {"r":"cn","y":2007,"n":"一个像夏天一个像秋天","a":"范玮琪"},
    # ---------- 华语扩容 · 10年代 ----------
    {"r":"cn","y":2009,"n":"身骑白马","a":"徐佳莹"},
    {"r":"cn","y":2009,"n":"说谎","a":"林宥嘉"},
    {"r":"cn","y":2010,"n":"雨爱","a":"杨丞琳","tag":"海派甜心"},
    {"r":"cn","y":2010,"n":"荷塘月色","a":"凤凰传奇"},
    {"r":"cn","y":2010,"n":"给我一个理由忘记","a":"A-Lin"},
    {"r":"cn","y":2011,"n":"夜空中最亮的星","a":"逃跑计划"},
    {"r":"cn","y":2011,"n":"泡沫","a":"邓紫棋"},
    {"r":"cn","y":2011,"n":"我的歌声里","a":"曲婉婷"},
    {"r":"cn","y":2011,"n":"那些年","a":"胡夏","tag":"那些年我们一起追的女孩"},
    {"r":"cn","y":2011,"n":"煎熬","a":"李佳薇"},
    {"r":"cn","y":2011,"n":"北京北京","a":"汪峰"},
    {"r":"cn","y":2013,"n":"模特","a":"李荣浩"},
    {"r":"cn","y":2013,"n":"丑八怪","a":"薛之谦"},
    {"r":"cn","y":2013,"n":"南山南","a":"马頔"},
    {"r":"cn","y":2014,"n":"匆匆那年","a":"王菲"},
    {"r":"cn","y":2015,"n":"凉凉","a":"张碧晨&杨宗纬","tag":"三生三世十里桃花"},
    {"r":"cn","y":2015,"n":"大鱼","a":"周深","tag":"大鱼海棠印象曲"},
    {"r":"cn","y":2015,"n":"小幸运","a":"田馥甄","tag":"我的少女时代"},
    {"r":"cn","y":2015,"n":"演员","a":"薛之谦"},
    {"r":"cn","y":2015,"n":"默","a":"那英&周杰伦","tag":"何以笙箫默"},
    {"r":"cn","y":2016,"n":"告白气球","a":"周杰伦"},
    {"r":"cn","y":2016,"n":"成都","a":"赵雷","tag":"民谣出圈之作"},
    {"r":"cn","y":2016,"n":"光年之外","a":"邓紫棋","tag":"太空旅客中文主题曲"},
    {"r":"cn","y":2016,"n":"水星记","a":"郭顶"},
    {"r":"cn","y":2016,"n":"奇妙能力歌","a":"陈粒"},
    {"r":"cn","y":2017,"n":"消愁","a":"毛不易","tag":"明日之子出道季"},
    {"r":"cn","y":2017,"n":"年少有为","a":"李荣浩"},
    {"r":"cn","y":2017,"n":"凉凉","a":"张碧晨&杨宗纬","tag":"三生三世十里桃花"},
    {"r":"cn","y":2017,"n":"体面","a":"于文文","tag":"前任3"},
    {"r":"cn","y":2017,"n":"我们不一样","a":"大壮"},
    # ---------- 世界扩容 · 50-60年代 ----------
    {"r":"w","y":1939,"n":"Over the Rainbow","a":"Judy Garland","tag":"绿野仙踪"},
    {"r":"w","y":1956,"n":"Heartbreak Hotel","a":"Elvis Presley"},
    {"r":"w","y":1959,"n":"Take Five","a":"The Dave Brubeck Quartet"},
    {"r":"w","y":1961,"n":"Can't Help Falling in Love","a":"Elvis Presley"},
    {"r":"w","y":1963,"n":"Ring of Fire","a":"Johnny Cash"},
    {"r":"w","y":1964,"n":"The House of the Rising Sun","a":"The Animals"},
    {"r":"w","y":1964,"n":"Oh, Pretty Woman","a":"Roy Orbison"},
    {"r":"w","y":1964,"n":"My Girl","a":"The Temptations"},
    {"r":"w","y":1965,"n":"Unchained Melody","a":"The Righteous Brothers","tag":"人鬼情未了"},
    {"r":"w","y":1965,"n":"The Sound of Silence","a":"Simon & Garfunkel"},
    {"r":"w","y":1965,"n":"I Got You (I Feel Good)","a":"James Brown"},
    {"r":"w","y":1966,"n":"Good Vibrations","a":"The Beach Boys"},
    {"r":"w","y":1966,"n":"Paint It, Black","a":"The Rolling Stones"},
    {"r":"w","y":1967,"n":"A Whiter Shade of Pale","a":"Procol Harum"},
    {"r":"w","y":1967,"n":"Happy Together","a":"The Turtles"},
    {"r":"w","y":1967,"n":"What a Wonderful World","a":"Louis Armstrong"},
    {"r":"w","y":1968,"n":"(Sittin' On) The Dock of the Bay","a":"Otis Redding"},
    {"r":"w","y":1968,"n":"I Heard It Through the Grapevine","a":"Marvin Gaye"},
    {"r":"w","y":1969,"n":"Come Together","a":"The Beatles"},
    {"r":"w","y":1969,"n":"Here Comes the Sun","a":"The Beatles"},
    {"r":"w","y":1969,"n":"My Way","a":"Frank Sinatra"},
    {"r":"w","y":1969,"n":"Whole Lotta Love","a":"Led Zeppelin"},
    {"r":"w","y":1969,"n":"Space Oddity","a":"David Bowie"},
    # ---------- 世界扩容 · 70年代 ----------
    {"r":"w","y":1970,"n":"Your Song","a":"Elton John"},
    {"r":"w","y":1971,"n":"American Pie","a":"Don McLean","tag":"8分半的国民史诗"},
    {"r":"w","y":1971,"n":"It's Too Late","a":"Carole King"},
    {"r":"w","y":1971,"n":"What's Going On","a":"Marvin Gaye"},
    {"r":"w","y":1971,"n":"Ain't No Sunshine","a":"Bill Withers"},
    {"r":"w","y":1972,"n":"Heart of Gold","a":"Neil Young"},
    {"r":"w","y":1972,"n":"Rocket Man","a":"Elton John"},
    {"r":"w","y":1972,"n":"Lean on Me","a":"Bill Withers"},
    {"r":"w","y":1972,"n":"Let's Stay Together","a":"Al Green"},
    {"r":"w","y":1972,"n":"Walk on the Wild Side","a":"Lou Reed"},
    {"r":"w","y":1972,"n":"A Horse with No Name","a":"America"},
    {"r":"w","y":1973,"n":"Piano Man","a":"Billy Joel"},
    {"r":"w","y":1973,"n":"Time in a Bottle","a":"Jim Croce"},
    {"r":"w","y":1973,"n":"Dream On","a":"Aerosmith"},
    {"r":"w","y":1973,"n":"Band on the Run","a":"Wings"},
    {"r":"w","y":1974,"n":"No Woman, No Cry","a":"Bob Marley & The Wailers"},
    {"r":"w","y":1975,"n":"Wish You Were Here","a":"Pink Floyd"},
    {"r":"w","y":1975,"n":"Sailing","a":"Rod Stewart"},
    {"r":"w","y":1975,"n":"I'm Not in Love","a":"10cc"},
    {"r":"w","y":1976,"n":"Blitzkrieg Bop","a":"Ramones"},
    {"r":"w","y":1976,"n":"More Than a Feeling","a":"Boston"},
    {"r":"w","y":1977,"n":"God Save the Queen","a":"Sex Pistols"},
    {"r":"w","y":1977,"n":"Heroes","a":"David Bowie"},
    {"r":"w","y":1977,"n":"Mr. Blue Sky","a":"Electric Light Orchestra"},
    {"r":"w","y":1977,"n":"How Deep Is Your Love","a":"Bee Gees"},
    {"r":"w","y":1978,"n":"Y.M.C.A.","a":"Village People"},
    {"r":"w","y":1978,"n":"Le Freak","a":"Chic"},
    {"r":"w","y":1978,"n":"I Will Survive","a":"Gloria Gaynor"},
    {"r":"w","y":1978,"n":"September","a":"Earth, Wind & Fire"},
    {"r":"w","y":1979,"n":"Heart of Glass","a":"Blondie"},
    {"r":"w","y":1979,"n":"Roxanne","a":"The Police"},
    {"r":"w","y":1979,"n":"Message in a Bottle","a":"The Police"},
    # ---------- 世界扩容 · 80年代 ----------
    {"r":"w","y":1980,"n":"Love Will Tear Us Apart","a":"Joy Division"},
    {"r":"w","y":1981,"n":"Don't You Want Me","a":"The Human League"},
    {"r":"w","y":1981,"n":"In the Air Tonight","a":"Phil Collins"},
    {"r":"w","y":1981,"n":"Don't Stop Believin'","a":"Journey"},
    {"r":"w","y":1982,"n":"Africa","a":"Toto"},
    {"r":"w","y":1982,"n":"Hungry Like the Wolf","a":"Duran Duran"},
    {"r":"w","y":1982,"n":"Eye of the Tiger","a":"Survivor","tag":"洛奇3"},
    {"r":"w","y":1983,"n":"Beat It","a":"Michael Jackson"},
    {"r":"w","y":1983,"n":"Sweet Dreams (Are Made of This)","a":"Eurythmics"},
    {"r":"w","y":1983,"n":"Total Eclipse of the Heart","a":"Bonnie Tyler"},
    {"r":"w","y":1983,"n":"Girls Just Want to Have Fun","a":"Cyndi Lauper"},
    {"r":"w","y":1983,"n":"Karma Chameleon","a":"Culture Club"},
    {"r":"w","y":1984,"n":"What's Love Got to Do with It","a":"Tina Turner"},
    {"r":"w","y":1984,"n":"Like a Virgin","a":"Madonna"},
    {"r":"w","y":1984,"n":"Wake Me Up Before You Go-Go","a":"Wham!"},
    {"r":"w","y":1984,"n":"Footloose","a":"Kenny Loggins"},
    {"r":"w","y":1984,"n":"Ghostbusters","a":"Ray Parker Jr."},
    {"r":"w","y":1984,"n":"Hello","a":"Lionel Richie"},
    {"r":"w","y":1985,"n":"West End Girls","a":"Pet Shop Boys"},
    {"r":"w","y":1985,"n":"Everybody Wants to Rule the World","a":"Tears for Fears"},
    {"r":"w","y":1985,"n":"Don't You (Forget About Me)","a":"Simple Minds","tag":"早餐俱乐部"},
    {"r":"w","y":1985,"n":"Money for Nothing","a":"Dire Straits"},
    {"r":"w","y":1985,"n":"The Power of Love","a":"Huey Lewis and the News","tag":"回到未来"},
    {"r":"w","y":1986,"n":"Walk This Way","a":"Run-DMC & Aerosmith","tag":"说唱摇滚联姻"},
    {"r":"w","y":1987,"n":"With or Without You","a":"U2"},
    {"r":"w","y":1987,"n":"I Still Haven't Found What I'm Looking For","a":"U2"},
    {"r":"w","y":1987,"n":"Never Gonna Give You Up","a":"Rick Astley","tag":"Rickroll 本尊"},
    {"r":"w","y":1987,"n":"Faith","a":"George Michael"},
    {"r":"w","y":1987,"n":"Pour Some Sugar on Me","a":"Def Leppard"},
    {"r":"w","y":1987,"n":"Alone","a":"Heart"},
    # ---------- 世界扩容 · 90年代 ----------
    {"r":"w","y":1990,"n":"Enjoy the Silence","a":"Depeche Mode"},
    {"r":"w","y":1990,"n":"(Everything I Do) I Do It for You","a":"Bryan Adams","tag":"罗宾汉主题曲"},
    {"r":"w","y":1991,"n":"Enter Sandman","a":"Metallica"},
    {"r":"w","y":1991,"n":"Nothing Else Matters","a":"Metallica"},
    {"r":"w","y":1991,"n":"Alive","a":"Pearl Jam"},
    {"r":"w","y":1991,"n":"Everlong","a":"Foo Fighters"},
    {"r":"w","y":1992,"n":"November Rain","a":"Guns N' Roses"},
    {"r":"w","y":1992,"n":"Under the Bridge","a":"Red Hot Chili Peppers"},
    {"r":"w","y":1992,"n":"End of the Road","a":"Boyz II Men"},
    {"r":"w","y":1993,"n":"All That She Wants","a":"Ace of Base"},
    {"r":"w","y":1993,"n":"Mr. Jones","a":"Counting Crows"},
    {"r":"w","y":1994,"n":"Zombie","a":"The Cranberries"},
    {"r":"w","y":1994,"n":"Kiss from a Rose","a":"Seal","tag":"永远的蝙蝠侠"},
    {"r":"w","y":1994,"n":"Hero","a":"Mariah Carey"},
    {"r":"w","y":1995,"n":"Gangsta's Paradise","a":"Coolio"},
    {"r":"w","y":1995,"n":"Fantasy","a":"Mariah Carey"},
    {"r":"w","y":1995,"n":"Bitter Sweet Symphony","a":"The Verve"},
    {"r":"w","y":1996,"n":"Ironic","a":"Alanis Morissette"},
    {"r":"w","y":1996,"n":"Don't Look Back in Anger","a":"Oasis"},
    {"r":"w","y":1996,"n":"I Believe I Can Fly","a":"R. Kelly","tag":"空中大灌篮"},
    {"r":"w","y":1997,"n":"My Heart Will Go On","a":"Celine Dion","tag":"泰坦尼克号"},
    {"r":"w","y":1997,"n":"Song 2","a":"Blur"},
    {"r":"w","y":1998,"n":"Iris","a":"The Goo Goo Dolls","tag":"城市英雄"},
    {"r":"w","y":1998,"n":"Believe","a":"Cher","tag":"Auto-Tune 开山"},
    {"r":"w","y":1998,"n":"Changes","a":"2Pac"},
    {"r":"w","y":1999,"n":"I Want It That Way","a":"Backstreet Boys"},
    {"r":"w","y":1999,"n":"…Baby One More Time","a":"Britney Spears"},
    {"r":"w","y":1999,"n":"Blue (Da Ba Dee)","a":"Eiffel 65"},
    {"r":"w","y":1999,"n":"All Star","a":"Smash Mouth","tag":"怪物史莱克"},
    {"r":"w","y":1999,"n":"Californication","a":"Red Hot Chili Peppers"},
    # ---------- 世界扩容 · 00年代 ----------
    {"r":"w","y":2000,"n":"Yellow","a":"Coldplay"},
    {"r":"w","y":2000,"n":"Oops!… I Did It Again","a":"Britney Spears"},
    {"r":"w","y":2002,"n":"Complicated","a":"Avril Lavigne"},
    {"r":"w","y":2002,"n":"Cry Me a River","a":"Justin Timberlake"},
    {"r":"w","y":2002,"n":"The Scientist","a":"Coldplay"},
    {"r":"w","y":2002,"n":"A Thousand Miles","a":"Vanessa Carlton"},
    {"r":"w","y":2002,"n":"Beautiful","a":"Christina Aguilera"},
    {"r":"w","y":2002,"n":"Clocks","a":"Coldplay"},
    {"r":"w","y":2003,"n":"Hey Ya!","a":"OutKast"},
    {"r":"w","y":2003,"n":"In Da Club","a":"50 Cent"},
    {"r":"w","y":2003,"n":"Seven Nation Army","a":"The White Stripes"},
    {"r":"w","y":2003,"n":"Crazy in Love","a":"Beyoncé feat. Jay-Z"},
    {"r":"w","y":2003,"n":"Where Is the Love?","a":"Black Eyed Peas"},
    {"r":"w","y":2004,"n":"Yeah!","a":"Usher feat. Lil Jon & Ludacris"},
    {"r":"w","y":2004,"n":"Mr. Brightside","a":"The Killers"},
    {"r":"w","y":2004,"n":"Since U Been Gone","a":"Kelly Clarkson"},
    {"r":"w","y":2004,"n":"Somewhere Only We Know","a":"Keane"},
    {"r":"w","y":2004,"n":"Dragostea Din Tei","a":"O-Zone","tag":"麦阿喜全球热梗"},
    {"r":"w","y":2005,"n":"Crazy","a":"Gnarls Barkley"},
    {"r":"w","y":2005,"n":"Home","a":"Michael Bublé"},
    {"r":"w","y":2005,"n":"Bad Day","a":"Daniel Powter"},
    {"r":"w","y":2005,"n":"Feel Good Inc.","a":"Gorillaz"},
    {"r":"w","y":2005,"n":"Starlight","a":"Muse"},
    {"r":"w","y":2005,"n":"Fix You","a":"Coldplay"},
    {"r":"w","y":2006,"n":"Chasing Cars","a":"Snow Patrol"},
    {"r":"w","y":2006,"n":"Hips Don't Lie","a":"Shakira feat. Wyclef Jean"},
    {"r":"w","y":2006,"n":"How to Save a Life","a":"The Fray"},
    {"r":"w","y":2006,"n":"Rehab","a":"Amy Winehouse"},
    {"r":"w","y":2007,"n":"Hey There Delilah","a":"Plain White T's"},
    {"r":"w","y":2007,"n":"Apologize","a":"Timbaland feat. OneRepublic"},
    {"r":"w","y":2007,"n":"Bleeding Love","a":"Leona Lewis"},
    {"r":"w","y":2008,"n":"I'm Yours","a":"Jason Mraz"},
    {"r":"w","y":2008,"n":"Use Somebody","a":"Kings of Leon"},
    {"r":"w","y":2008,"n":"Single Ladies (Put a Ring on It)","a":"Beyoncé"},
    {"r":"w","y":2008,"n":"Sex on Fire","a":"Kings of Leon"},
    {"r":"w","y":2008,"n":"Halo","a":"Beyoncé"},
    {"r":"w","y":2009,"n":"I Gotta Feeling","a":"Black Eyed Peas"},
    {"r":"w","y":2009,"n":"Fireflies","a":"Owl City"},
    {"r":"w","y":2009,"n":"Bad Romance","a":"Lady Gaga"},
    # ---------- 世界扩容 · 10年代 ----------
    {"r":"w","y":2010,"n":"Just the Way You Are","a":"Bruno Mars"},
    {"r":"w","y":2010,"n":"Firework","a":"Katy Perry"},
    {"r":"w","y":2011,"n":"Someone Like You","a":"Adele"},
    {"r":"w","y":2011,"n":"Titanium","a":"David Guetta feat. Sia"},
    {"r":"w","y":2011,"n":"What Makes You Beautiful","a":"One Direction"},
    {"r":"w","y":2011,"n":"Radioactive","a":"Imagine Dragons"},
    {"r":"w","y":2011,"n":"Pumped Up Kicks","a":"Foster the People"},
    {"r":"w","y":2012,"n":"Call Me Maybe","a":"Carly Rae Jepsen"},
    {"r":"w","y":2012,"n":"Let Her Go","a":"Passenger"},
    {"r":"w","y":2013,"n":"Get Lucky","a":"Daft Punk feat. Pharrell Williams"},
    {"r":"w","y":2013,"n":"All of Me","a":"John Legend"},
    {"r":"w","y":2013,"n":"Take Me to Church","a":"Hozier"},
    {"r":"w","y":2013,"n":"Royals","a":"Lorde"},
    {"r":"w","y":2013,"n":"Say Something","a":"A Great Big World & Christina Aguilera"},
    {"r":"w","y":2013,"n":"Counting Stars","a":"OneRepublic"},
    {"r":"w","y":2014,"n":"Stay with Me","a":"Sam Smith"},
    {"r":"w","y":2015,"n":"Uptown Funk","a":"Mark Ronson feat. Bruno Mars"},
    {"r":"w","y":2015,"n":"See You Again","a":"Wiz Khalifa feat. Charlie Puth","tag":"速度与激情7"},
    {"r":"w","y":2015,"n":"Faded","a":"Alan Walker"},
    {"r":"w","y":2015,"n":"Love Yourself","a":"Justin Bieber"},
    {"r":"w","y":2016,"n":"Closer","a":"The Chainsmokers feat. Halsey"},
    {"r":"w","y":2017,"n":"Shape of You","a":"Ed Sheeran"},
    {"r":"w","y":2017,"n":"Perfect","a":"Ed Sheeran"},
    {"r":"w","y":2017,"n":"Despacito","a":"Luis Fonsi & Daddy Yankee"},
    {"r":"w","y":2017,"n":"Believer","a":"Imagine Dragons"},
    {"r":"w","y":2017,"n":"Havana","a":"Camila Cabello"},
    {"r":"w","y":2018,"n":"Shallow","a":"Lady Gaga & Bradley Cooper","tag":"一个明星的诞生"},
    {"r":"w","y":2019,"n":"Old Town Road","a":"Lil Nas X"},
    {"r":"w","y":2019,"n":"bad guy","a":"Billie Eilish"},
    {"r":"w","y":2019,"n":"Don't Start Now","a":"Dua Lipa"},
    {"r":"w","y":2019,"n":"Someone You Loved","a":"Lewis Capaldi"},
    # ========== 扩容批次 A1 · 华语 ==========
    ("cn",1976,"诺言","刘文正"),
    ("cn",1978,"何日君再来","邓丽君"),
    ("cn",1979,"外婆的澎湖湾","潘安邦"),
    ("cn",1980,"旧梦不须记","雷安娜"),
    ("cn",1980,"热情的沙漠","欧阳菲菲"),
    ("cn",1983,"一生有意义","罗文&甄妮"),
    ("cn",1983,"今宵多珍重","陈百强"),
    ("cn",1983,"天蚕变","关正杰"),
    ("cn",1984,"我的未来不是梦","张雨生"),
    ("cn",1985,"情已逝","张学友"),
    ("cn",1986,"当年情","张国荣","英雄本色"),
    ("cn",1986,"有谁共鸣","张国荣"),
    ("cn",1986,"无言的结局","林淑容&罗时丰"),
    ("cn",1987,"无心睡眠","张国荣"),
    ("cn",1987,"安妮","王杰"),
    ("cn",1988,"傻女","陈慧娴"),
    ("cn",1988,"我很丑可是我很温柔","赵传"),
    ("cn",1988,"红蜻蜓","小虎队"),
    ("cn",1989,"谁明浪子心","王杰"),
    ("cn",1989,"青苹果乐园","小虎队"),
    ("cn",1989,"可不可以","刘德华"),
    ("cn",1989,"爱的代价","张艾嘉"),
    ("cn",1989,"明天你是否依然爱我","童安格"),
    ("cn",1989,"跟往事干杯","姜育恒"),
    ("cn",1989,"我是不是你最疼爱的人","潘越云"),
    ("cn",1990,"李香兰","张学友"),
    ("cn",1990,"特别的爱给特别的你","伍思凯"),
    ("cn",1991,"不再犹豫","Beyond"),
    ("cn",1991,"让我欢喜让我忧","周华健"),
    ("cn",1991,"追梦人","凤飞飞","滚石经典"),
    ("cn",1992,"暗里着迷","刘德华"),
    ("cn",1992,"难念的经","周华健","天龙八部"),
    ("cn",1992,"冬季到台北来看雨","孟庭苇"),
    ("cn",1992,"选择","叶蒨文&林子祥"),
    ("cn",1992,"谢谢你的爱","刘德华"),
    ("cn",1992,"鬼迷心窍","李宗盛"),
    ("cn",1993,"情人","Beyond"),
    ("cn",1993,"新鸳鸯蝴蝶梦","黄安","包青天"),
    ("cn",1993,"执迷不悔","王菲"),
    ("cn",1993,"只想一生跟你走","张学友"),
    ("cn",1993,"不必在乎我是谁","林忆莲"),
    ("cn",1993,"灰姑娘","郑钧"),
    ("cn",1993,"走四方","韩磊"),
    ("cn",1993,"纤夫的爱","尹相杰&于文华"),
    ("cn",1994,"天空","王菲"),
    ("cn",1994,"祝你一路顺风","吴奇隆"),
    ("cn",1994,"别怕我伤心","张信哲"),
    ("cn",1994,"灰姑娘","郑钧"),
    ("cn",1994,"走四方","韩磊"),
    ("cn",1994,"轻轻地告诉你","杨钰莹"),
    ("cn",1995,"情书","张学友"),
    ("cn",1995,"囚鸟","彭羚"),
    ("cn",1995,"爱情鸟","林依轮"),
    ("cn",1995,"太傻","巫启贤"),
    ("cn",1995,"白天不懂夜的黑","那英"),
    ("cn",1995,"过火","张信哲"),
    ("cn",1996,"你的名字我的姓氏","张学友"),
    ("cn",1996,"情深说话未曾讲","黎明"),
    ("cn",1996,"独角戏","许茹芸"),
    ("cn",1996,"野花","田震"),
    ("cn",1996,"Lemon Tree","苏慧伦"),
    ("cn",1996,"泪海","许茹芸"),
    ("cn",1997,"心雨","杨钰莹&毛宁"),
    ("cn",1997,"阳光总在风雨后","许美静"),
    ("cn",1997,"短发","梁咏琪"),
    ("cn",1997,"无情的情书","动力火车"),
    ("cn",1997,"愚人码头","熊天平"),
    ("cn",1997,"他不爱我","莫文蔚"),
    ("cn",1998,"当你孤单你会想起谁","张栋梁"),
    ("cn",1999,"阴天","莫文蔚"),
    ("cn",1999,"爱一个人好难","苏永康"),
    ("cn",1999,"后来","刘若英"),
    ("cn",1999,"为爱痴狂","刘若英"),
    ("cn",1999,"最浪漫的事","赵咏华"),
    ("cn",1999,"你快回来","孙楠"),
    ("cn",1986,"女儿情","吴静","西游记"),
    ("cn",1990,"滚滚红尘","陈淑桦"),
    ("cn",1991,"追梦人","凤飞飞"),
    ("cn",1994,"当爱已成往事","李宗盛&林忆莲","霸王别姬"),
    ("cn",1994,"爱江山更爱美人","李丽芬","倚天屠龙记"),
    ("cn",1992,"鬼迷心窍","李宗盛"),
    # ========== 扩容批次 A2 · 华语 ==========
    ("cn",1994,"浪人情歌","伍佰"),
    ("cn",1993,"把根留住","童安格"),
    ("cn",1991,"我是不是该安静的走开","郭富城"),
    ("cn",1993,"爱如潮水","张信哲"),
    ("cn",1995,"白天不懂夜的黑","那英"),
    ("cn",1994,"哭砂","黄莺莺"),
    ("cn",1994,"谁的眼泪在飞","孟庭苇"),
    ("cn",1995,"真的吗","莫文蔚"),
    ("cn",1994,"我是不是你最疼爱的人","潘越云"),
    ("cn",2000,"笑忘书","王菲"),
    ("cn",2000,"盛夏的果实","莫文蔚"),
    ("cn",2000,"黄昏","周传雄"),
    ("cn",2000,"你快回来","孙楠"),
    ("cn",2001,"记得","张惠妹"),
    ("cn",2001,"绿光","孙燕姿"),
    ("cn",2001,"东北人都是活雷锋","雪村"),
    ("cn",2002,"半岛铁盒","周杰伦"),
    ("cn",2002,"无所谓","杨坤"),
    ("cn",2002,"好心分手","卢巧音"),
    ("cn",2003,"以父之名","周杰伦"),
    ("cn",2003,"看我72变","蔡依林"),
    ("cn",2003,"暗香","沙宝亮","金粉世家"),
    ("cn",2003,"旋木","王菲"),
    ("cn",2003,"挥着翅膀的女孩","容祖儿"),
    ("cn",2004,"倒带","蔡依林"),
    ("cn",2004,"栀子花开","何炅"),
    ("cn",2004,"孤单北半球","欧得洋"),
    ("cn",2004,"那女孩对我说","黄义达"),
    ("cn",2004,"我不难过","孙燕姿"),
    ("cn",2005,"一万个理由","郑源"),
    ("cn",2005,"可惜不是你","梁静茹"),
    ("cn",2005,"珊瑚海","周杰伦&Lara"),
    ("cn",2005,"睫毛弯弯","王心凌"),
    ("cn",2006,"求佛","誓言"),
    ("cn",2006,"牡丹江","南拳妈妈"),
    ("cn",2006,"最佳损友","陈奕迅"),
    ("cn",2007,"有没有人告诉你","陈楚生"),
    ("cn",2007,"暖暖","梁静茹"),
    ("cn",2007,"无与伦比的美丽","苏打绿"),
    ("cn",2008,"小酒窝","林俊杰&蔡卓妍"),
    ("cn",2008,"洋葱","杨宗纬"),
    ("cn",2008,"Love Song","方大同"),
    ("cn",2008,"北京欢迎你","群星"),
    ("cn",2008,"说好的幸福呢","周杰伦"),
    ("cn",2009,"春天里","汪峰"),
    ("cn",2009,"没那么简单","黄小琥"),
    ("cn",2009,"有何不可","许嵩"),
    ("cn",1990,"把悲伤留给自己","陈升"),
    ("cn",1986,"一无所有","崔健","中国摇滚开山之作"),
    # ========== 扩容批次 A3 · 华语 ==========
    ("cn",2012,"明明就","周杰伦"),
    ("cn",2013,"山丘","李宗盛"),
    ("cn",2014,"青春修炼手册","TFBOYS"),
    ("cn",2016,"后来的我们","五月天"),
    ("cn",2017,"追光者","岑宁儿"),
    ("cn",2017,"起风了","买辣椒也用券"),
    ("cn",2018,"云烟成雨","房东的猫"),
    ("cn",2018,"我曾","隔壁老樊"),
    ("cn",2018,"绿色","陈雪凝"),
    ("cn",2019,"世间美好与你环环相扣","柏松"),
    ("cn",2019,"你的答案","阿冗"),
    ("cn",2021,"孤勇者","陈奕迅"),
    ("cn",2023,"乌梅子酱","李荣浩"),
    ("cn",2003,"普通朋友","陶喆"),
    ("cn",2004,"最初的梦想","范玮琪"),
    ("cn",2005,"不想长大","S.H.E"),
    ("cn",2007,"亲爱的那不是爱情","张韶涵"),
    ("cn",2008,"画心","张靓颖","画皮"),
    ("cn",2008,"左边","杨丞琳"),
    ("cn",2008,"心跳","王力宏"),
    ("cn",2009,"背对背拥抱","林俊杰"),
    ("cn",2010,"她说","林俊杰"),
    ("cn",2010,"新贵妃醉酒","李玉刚"),
    ("cn",2006,"玫瑰花的葬礼","许嵩"),
    ("cn",2002,"坚持到底","阿杜"),
    ("cn",2002,"撕夜","阿杜"),
]

# 扩容批次 B/C/D（世界深挖 + 华语补充）
SONGS += [{"r": "w", "y": 1955, "n": "The Great Pretender", "a": "The Platters"}, {"r": "w", "y": 1958, "n": "La Bamba", "a": "Ritchie Valens"}, {"r": "w", "y": 1958, "n": "Smoke Gets in Your Eyes", "a": "The Platters"}, {"r": "w", "y": 1959, "n": "Mack the Knife", "a": "Bobby Darin"}, {"r": "w", "y": 1959, "n": "What'd I Say", "a": "Ray Charles"}, {"r": "w", "y": 1960, "n": "At Last", "a": "Etta James"}, {"r": "w", "y": 1960, "n": "Will You Love Me Tomorrow", "a": "The Shirelles"}, {"r": "w", "y": 1960, "n": "Save the Last Dance for Me", "a": "The Drifters"}, {"r": "w", "y": 1960, "n": "The Twist", "a": "Chubby Checker"}, {"r": "w", "y": 1961, "n": "Runaway", "a": "Del Shannon"}, {"r": "w", "y": 1961, "n": "Crazy", "a": "Patsy Cline"}, {"r": "w", "y": 1963, "n": "Be My Baby", "a": "The Ronettes"}, {"r": "w", "y": 1963, "n": "I Want to Hold Your Hand", "a": "The Beatles"}, {"r": "w", "y": 1963, "n": "Twist and Shout", "a": "The Beatles"}, {"r": "w", "y": 1964, "n": "You Really Got Me", "a": "The Kinks"}, {"r": "w", "y": 1964, "n": "Under the Boardwalk", "a": "The Drifters"}, {"r": "w", "y": 1965, "n": "Help!", "a": "The Beatles"}, {"r": "w", "y": 1965, "n": "In My Life", "a": "The Beatles"}, {"r": "w", "y": 1965, "n": "Turn! Turn! Turn!", "a": "The Byrds"}, {"r": "w", "y": 1966, "n": "Eleanor Rigby", "a": "The Beatles"}, {"r": "w", "y": 1966, "n": "Reach Out I'll Be There", "a": "Four Tops"}, {"r": "w", "y": 1966, "n": "When a Man Loves a Woman", "a": "Percy Sledge"}, {"r": "w", "y": 1967, "n": "Light My Fire", "a": "The Doors"}, {"r": "w", "y": 1967, "n": "Nights in White Satin", "a": "The Moody Blues"}, {"r": "w", "y": 1967, "n": "Brown Eyed Girl", "a": "Van Morrison"}, {"r": "w", "y": 1968, "n": "Born to Be Wild", "a": "Steppenwolf"}, {"r": "w", "y": 1968, "n": "The Weight", "a": "The Band"}, {"r": "w", "y": 1968, "n": "Build Me Up Buttercup", "a": "The Foundations"}, {"r": "w", "y": 1969, "n": "Sweet Caroline", "a": "Neil Diamond"}, {"r": "w", "y": 1969, "n": "Proud Mary", "a": "Creedence Clearwater Revival"}, {"r": "w", "y": 1969, "n": "Fortunate Son", "a": "Creedence Clearwater Revival"}, {"r": "w", "y": 1969, "n": "I Want You Back", "a": "The Jackson 5"}, {"r": "w", "y": 1970, "n": "My Sweet Lord", "a": "George Harrison"}, {"r": "w", "y": 1970, "n": "The Long and Winding Road", "a": "The Beatles"}, {"r": "w", "y": 1971, "n": "Baba O'Riley", "a": "The Who"}, {"r": "w", "y": 1971, "n": "Behind Blue Eyes", "a": "The Who"}, {"r": "w", "y": 1971, "n": "Jealous Guy", "a": "John Lennon"}, {"r": "w", "y": 1972, "n": "Take It Easy", "a": "Eagles"}, {"r": "w", "y": 1972, "n": "Listen to the Music", "a": "The Doobie Brothers"}, {"r": "w", "y": 1972, "n": "Burning Love", "a": "Elvis Presley"}, {"r": "w", "y": 1972, "n": "Always on My Mind", "a": "Elvis Presley"}, {"r": "w", "y": 1973, "n": "Desperado", "a": "Eagles"}, {"r": "w", "y": 1973, "n": "Free Bird", "a": "Lynyrd Skynyrd"}, {"r": "w", "y": 1973, "n": "Let's Get It On", "a": "Marvin Gaye"}, {"r": "w", "y": 1973, "n": "Killing Me Softly", "a": "Roberta Flack"}, {"r": "w", "y": 1973, "n": "The Way We Were", "a": "Barbra Streisand"}, {"r": "w", "y": 1973, "n": "You Are the Sunshine of My Life", "a": "Stevie Wonder"}, {"r": "w", "y": 1974, "n": "Cat's in the Cradle", "a": "Harry Chapin"}, {"r": "w", "y": 1974, "n": "Lady Marmalade", "a": "LaBelle"}, {"r": "w", "y": 1975, "n": "Shining Star", "a": "Earth, Wind & Fire"}, {"r": "w", "y": 1975, "n": "Landslide", "a": "Fleetwood Mac"}, {"r": "w", "y": 1976, "n": "December, 1963 (Oh, What a Night)", "a": "The Four Seasons"}, {"r": "w", "y": 1976, "n": "If You Leave Me Now", "a": "Chicago"}, {"r": "w", "y": 1977, "n": "We Are the Champions", "a": "Queen"}, {"r": "w", "y": 1977, "n": "Dreams", "a": "Fleetwood Mac"}, {"r": "w", "y": 1977, "n": "Best of My Love", "a": "Eagles"}, {"r": "w", "y": 1977, "n": "Dust in the Wind", "a": "Kansas"}, {"r": "w", "y": 1977, "n": "Give a Little Bit", "a": "Supertramp"}, {"r": "w", "y": 1978, "n": "Baker Street", "a": "Gerry Rafferty"}, {"r": "w", "y": 1978, "n": "What a Fool Believes", "a": "The Doobie Brothers"}, {"r": "w", "y": 1978, "n": "Miss You", "a": "The Rolling Stones"}, {"r": "w", "y": 1979, "n": "Highway to Hell", "a": "AC/DC"}, {"r": "w", "y": 1979, "n": "Ring My Bell", "a": "Anita Ward"}, {"r": "w", "y": 1979, "n": "Hot Stuff", "a": "Donna Summer"}, {"r": "w", "y": 1979, "n": "We Are Family", "a": "Sister Sledge"}, {"r": "w", "y": 1979, "n": "Don't Bring Me Down", "a": "ELO"}, {"r": "w", "y": 1980, "n": "Celebration", "a": "Kool & The Gang"}, {"r": "w", "y": 1980, "n": "The Winner Takes It All", "a": "ABBA"}, {"r": "w", "y": 1981, "n": "Start Me Up", "a": "The Rolling Stones"}, {"r": "w", "y": 1981, "n": "Call Me", "a": "Blondie"}, {"r": "w", "y": 1982, "n": "Come On Eileen", "a": "Dexys Midnight Runners"}, {"r": "w", "y": 1982, "n": "Gloria", "a": "Laura Branigan"}, {"r": "w", "y": 1982, "n": "I Love Rock 'N' Roll", "a": "Joan Jett & the Blackhearts"}, {"r": "w", "y": 1983, "n": "Flashdance… What a Feeling", "a": "Irene Cara"}, {"r": "w", "y": 1983, "n": "99 Luftballons", "a": "Nena"}, {"r": "w", "y": 1984, "n": "When Doves Cry", "a": "Prince"}, {"r": "w", "y": 1984, "n": "Material Girl", "a": "Madonna"}, {"r": "w", "y": 1984, "n": "Holding Out for a Hero", "a": "Bonnie Tyler"}, {"r": "w", "y": 1985, "n": "Shout", "a": "Tears for Fears"}, {"r": "w", "y": 1985, "n": "Money for Nothing", "a": "Dire Straits"}, {"r": "w", "y": 1986, "n": "Sledgehammer", "a": "Peter Gabriel"}, {"r": "w", "y": 1986, "n": "Take My Breath Away", "a": "Berlin"}, {"r": "w", "y": 1987, "n": "Here I Go Again", "a": "Whitesnake"}, {"r": "w", "y": 1987, "n": "Forever Young", "a": "Alphaville"}, {"r": "w", "y": 1988, "n": "Smooth Criminal", "a": "Michael Jackson"}, {"r": "w", "y": 1988, "n": "Man in the Mirror", "a": "Michael Jackson"}, {"r": "w", "y": 1988, "n": "The Way You Make Me Feel", "a": "Michael Jackson"}, {"r": "w", "y": 1988, "n": "Every Rose Has Its Thorn", "a": "Poison"}, {"r": "w", "y": 1989, "n": "Eternal Flame", "a": "The Bangles"}, {"r": "w", "y": 1989, "n": "We Didn't Start the Fire", "a": "Billy Joel"}, {"r": "w", "y": 1989, "n": "Love Shack", "a": "The B-52's"}, {"r": "w", "y": 1990, "n": "Ice Ice Baby", "a": "Vanilla Ice"}, {"r": "w", "y": 1990, "n": "U Can't Touch This", "a": "MC Hammer"}, {"r": "w", "y": 1990, "n": "Wind of Change", "a": "Scorpions"}, {"r": "w", "y": 1991, "n": "More Than Words", "a": "Extreme"}, {"r": "w", "y": 1991, "n": "Come as You Are", "a": "Nirvana"}, {"r": "w", "y": 1992, "n": "What Is Love", "a": "Haddaway"}, {"r": "w", "y": 1992, "n": "To Be with You", "a": "Mr. Big"}, {"r": "w", "y": 1993, "n": "What's Up", "a": "4 Non Blondes"}, {"r": "w", "y": 1994, "n": "Black Hole Sun", "a": "Soundgarden"}, {"r": "w", "y": 1994, "n": "Don't Speak", "a": "No Doubt"}, {"r": "w", "y": 1994, "n": "I Swear", "a": "All-4-One"}, {"r": "w", "y": 1995, "n": "Common People", "a": "Pulp"}, {"r": "w", "y": 1996, "n": "Un-Break My Heart", "a": "Toni Braxton"}, {"r": "w", "y": 1996, "n": "Return of the Mack", "a": "Mark Morrison"}, {"r": "w", "y": 1997, "n": "Barbie Girl", "a": "Aqua"}, {"r": "w", "y": 1997, "n": "Torn", "a": "Natalie Imbruglia"}, {"r": "w", "y": 1997, "n": "I'll Be Missing You", "a": "Puff Daddy & Faith Evans"}, {"r": "w", "y": 2000, "n": "It's My Life", "a": "Bon Jovi"}, {"r": "w", "y": 2000, "n": "Bye Bye Bye", "a": "*NSYNC"}, {"r": "w", "y": 2001, "n": "How You Remind Me", "a": "Nickelback"}, {"r": "w", "y": 2001, "n": "Fallin'", "a": "Alicia Keys"}, {"r": "w", "y": 2002, "n": "Numb", "a": "Linkin Park"}, {"r": "w", "y": 2002, "n": "White Flag", "a": "Dido"}, {"r": "w", "y": 2003, "n": "Vertigo", "a": "U2"}, {"r": "w", "y": 2003, "n": "Boulevard of Broken Dreams", "a": "Green Day"}, {"r": "w", "y": 2004, "n": "American Idiot", "a": "Green Day"}, {"r": "w", "y": 2004, "n": "She Will Be Loved", "a": "Maroon 5"}, {"r": "w", "y": 2005, "n": "Photograph", "a": "Nickelback"}, {"r": "w", "y": 2005, "n": "Because of You", "a": "Kelly Clarkson"}, {"r": "w", "y": 2005, "n": "Wake Me Up When September Ends", "a": "Green Day"}, {"r": "w", "y": 2006, "n": "Before He Cheats", "a": "Carrie Underwood"}, {"r": "w", "y": 2007, "n": "Big Girls Don't Cry", "a": "Fergie"}, {"r": "w", "y": 2008, "n": "Hot N Cold", "a": "Katy Perry"}, {"r": "w", "y": 2008, "n": "So What", "a": "P!nk"}, {"r": "w", "y": 2009, "n": "Empire State of Mind", "a": "Jay-Z & Alicia Keys"}, {"r": "w", "y": 2009, "n": "Just Dance", "a": "Lady Gaga"}, {"r": "w", "y": 2010, "n": "TiK ToK", "a": "Kesha"}, {"r": "w", "y": 2010, "n": "Hey, Soul Sister", "a": "Train"}, {"r": "w", "y": 2010, "n": "Love The Way You Lie", "a": "Eminem feat. Rihanna"}, {"r": "w", "y": 2011, "n": "Set Fire to the Rain", "a": "Adele"}, {"r": "w", "y": 2011, "n": "Party Rock Anthem", "a": "LMFAO"}, {"r": "w", "y": 2011, "n": "Give Me Everything", "a": "Pitbull"}, {"r": "w", "y": 2011, "n": "Born This Way", "a": "Lady Gaga"}, {"r": "w", "y": 2012, "n": "Payphone", "a": "Maroon 5 feat. Wiz Khalifa"}, {"r": "w", "y": 2012, "n": "Diamonds", "a": "Rihanna"}, {"r": "w", "y": 2012, "n": "Stay", "a": "Rihanna feat. Mikky Ekko"}, {"r": "w", "y": 2012, "n": "Some Nights", "a": "fun."}, {"r": "w", "y": 2012, "n": "Ho Hey", "a": "The Lumineers"}, {"r": "w", "y": 2012, "n": "I Knew You Were Trouble", "a": "Taylor Swift"}, {"r": "w", "y": 2012, "n": "We Are Never Ever Getting Back Together", "a": "Taylor Swift"}, {"r": "w", "y": 2012, "n": "Gangnam Style", "a": "PSY"}, {"r": "w", "y": 2013, "n": "Thrift Shop", "a": "Macklemore & Ryan Lewis"}, {"r": "w", "y": 2013, "n": "Demons", "a": "Imagine Dragons"}, {"r": "w", "y": 2013, "n": "Clarity", "a": "Zedd feat. Foxes"}, {"r": "w", "y": 2013, "n": "Story of My Life", "a": "One Direction"}, {"r": "w", "y": 2013, "n": "Let It Go", "a": "Idina Menzel", "tag": "Frozen"}, {"r": "w", "y": 2014, "n": "All About That Bass", "a": "Meghan Trainor"}, {"r": "w", "y": 2014, "n": "Rather Be", "a": "Clean Bandit feat. Jess Glynne"}, {"r": "w", "y": 2015, "n": "Cheerleader", "a": "OMI"}, {"r": "w", "y": 2015, "n": "Lean On", "a": "Major Lazer & DJ Snake"}, {"r": "w", "y": 2015, "n": "7 Years", "a": "Lukas Graham"}, {"r": "w", "y": 2016, "n": "Stitches", "a": "Shawn Mendes"}, {"r": "w", "y": 2017, "n": "Something Just Like This", "a": "The Chainsmokers & Coldplay"}, {"r": "w", "y": 2018, "n": "Sunflower", "a": "Post Malone & Swae Lee"}, {"r": "w", "y": 2019, "n": "Señorita", "a": "Shawn Mendes & Camila Cabello"}, {"r": "w", "y": 2019, "n": "Circles", "a": "Post Malone"}, {"r": "cn", "y": 1997, "n": "回家", "a": "顺子"}, {"r": "cn", "y": 2007, "n": "王妃", "a": "萧敬腾"}, {"r": "cn", "y": 2002, "n": "蓝莲花", "a": "许巍"}, {"r": "cn", "y": 2004, "n": "曾经的你", "a": "许巍"}, {"r": "cn", "y": 2007, "n": "红色高跟鞋", "a": "蔡健雅"}, {"r": "cn", "y": 2017, "n": "说散就散", "a": "袁娅维"}, {"r": "cn", "y": 2018, "n": "沙漠骆驼", "a": "展展与罗罗"}, {"r": "cn", "y": 2019, "n": "少年", "a": "梦然"}, {"r": "cn", "y": 2016, "n": "理想三旬", "a": "陈鸿宇"}, {"r": "cn", "y": 1992, "n": "鬼迷心窍", "a": "李宗盛"}, {"r": "cn", "y": 1990, "n": "弯弯的月亮", "a": "刘欢"}, {"r": "cn", "y": 1995, "n": "常回家看看", "a": "陈红"}]

SONGS += [{"r": "cn", "y": 1984, "n": "爱的根源", "a": "谭咏麟"}, {"r": "cn", "y": 1993, "n": "一路上有你", "a": "张学友"}, {"r": "cn", "y": 1992, "n": "分手总要在雨天", "a": "张学友"}, {"r": "cn", "y": 1992, "n": "还是觉得你最好", "a": "张学友"}, {"r": "cn", "y": 1992, "n": "相思风雨中", "a": "张学友&汤宝如"}, {"r": "cn", "y": 1985, "n": "遥远的她", "a": "张学友"}, {"r": "cn", "y": 1985, "n": "月半弯", "a": "张学友"}, {"r": "cn", "y": 1999, "n": "她来听我的演唱会", "a": "张学友"}, {"r": "cn", "y": 1994, "n": "追", "a": "张国荣"}, {"r": "cn", "y": 1999, "n": "左右手", "a": "张国荣"}, {"r": "cn", "y": 1989, "n": "风再起时", "a": "张国荣"}, {"r": "cn", "y": 1994, "n": "夏日倾情", "a": "黎明"}, {"r": "cn", "y": 1994, "n": "哪有一天不想你", "a": "黎明"}, {"r": "cn", "y": 1994, "n": "狂野之城", "a": "郭富城"}, {"r": "cn", "y": 1996, "n": "因为爱", "a": "刘德华"}, {"r": "cn", "y": 1994, "n": "天意", "a": "刘德华"}, {"r": "cn", "y": 1998, "n": "笨小孩", "a": "刘德华"}, {"r": "cn", "y": 1991, "n": "来生缘", "a": "刘德华"}, {"r": "cn", "y": 1990, "n": "如果你是我的传说", "a": "刘德华"}, {"r": "cn", "y": 1993, "n": "我恨我痴心", "a": "刘德华"}, {"r": "cn", "y": 2001, "n": "有没有一首歌会让你想起我", "a": "周华健"}, {"r": "cn", "y": 2000, "n": "冷酷到底", "a": "羽泉"}, {"r": "cn", "y": 1990, "n": "爱我的人和我爱的人", "a": "裘海正"}, {"r": "cn", "y": 1992, "n": "问", "a": "陈淑桦"}, {"r": "cn", "y": 1990, "n": "滚滚红尘", "a": "陈淑桦"}, {"r": "cn", "y": 1998, "n": "解脱", "a": "张惠妹"}, {"r": "cn", "y": 1999, "n": "我可以抱你吗", "a": "张惠妹"}, {"r": "cn", "y": 2008, "n": "类似爱情", "a": "萧亚轩"}, {"r": "cn", "y": 2005, "n": "不想长大", "a": "S.H.E"}, {"r": "cn", "y": 2001, "n": "恋人未满", "a": "S.H.E"}, {"r": "cn", "y": 2004, "n": "第一次爱的人", "a": "王心凌"}, {"r": "cn", "y": 2004, "n": "遗失的美好", "a": "张韶涵"}, {"r": "cn", "y": 2006, "n": "左边", "a": "杨丞琳"}, {"r": "cn", "y": 2009, "n": "情歌", "a": "梁静茹"}, {"r": "cn", "y": 2000, "n": "任逍遥", "a": "任贤齐"}, {"r": "cn", "y": 2000, "n": "突然的自我", "a": "伍佰"}, {"r": "cn", "y": 2004, "n": "再见", "a": "张震岳"}, {"r": "cn", "y": 2001, "n": "我爱的人", "a": "陈小春"}, {"r": "cn", "y": 1998, "n": "蒙娜丽莎的眼泪", "a": "林志炫"}, {"r": "cn", "y": 1995, "n": "恋恋风尘", "a": "老狼"}, {"r": "cn", "y": 2003, "n": "生如夏花", "a": "朴树"}, {"r": "cn", "y": 1998, "n": "故乡", "a": "许巍"}, {"r": "cn", "y": 2002, "n": "完美生活", "a": "许巍"}, {"r": "cn", "y": 1982, "n": "鹿港小镇", "a": "罗大佑"}, {"r": "cn", "y": 1988, "n": "爱人同志", "a": "罗大佑"}, {"r": "cn", "y": 1991, "n": "东方之珠", "a": "罗大佑"}, {"r": "cn", "y": 1985, "n": "潇洒的走", "a": "凤飞飞"}, {"r": "cn", "y": 1976, "n": "路边的野花不要采", "a": "邓丽君"}, {"r": "cn", "y": 1980, "n": "你怎么说", "a": "邓丽君"}, {"r": "cn", "y": 1983, "n": "独上西楼", "a": "邓丽君"}, {"r": "cn", "y": 1983, "n": "几多愁", "a": "邓丽君"}, {"r": "cn", "y": 1992, "n": "红茶馆", "a": "陈慧娴"}, {"r": "cn", "y": 1992, "n": "飘雪", "a": "陈慧娴"}, {"r": "cn", "y": 1989, "n": "灰色轨迹", "a": "Beyond"}, {"r": "cn", "y": 1989, "n": "冷雨夜", "a": "Beyond"}, {"r": "w", "y": 1959, "n": "Dream Lover", "a": "Bobby Darin"}, {"r": "w", "y": 1959, "n": "El Paso", "a": "Marty Robbins"}, {"r": "w", "y": 1960, "n": "I Am Woman", "a": "Helen Reddy"}, {"r": "w", "y": 1961, "n": "Moon River", "a": "Henry Mancini"}, {"r": "w", "y": 1961, "n": "King of the Road", "a": "Roger Miller"}, {"r": "w", "y": 1962, "n": "I Can't Help Myself", "a": "Four Tops"}, {"r": "w", "y": 1963, "n": "She Loves You", "a": "The Beatles"}, {"r": "w", "y": 1964, "n": "Baby Love", "a": "The Supremes"}, {"r": "w", "y": 1964, "n": "My Guy", "a": "Mary Wells"}, {"r": "w", "y": 1964, "n": "Dancing in the Street", "a": "Martha & The Vandellas"}, {"r": "w", "y": 1965, "n": "Stop! In the Name of Love", "a": "The Supremes"}, {"r": "w", "y": 1965, "n": "Ticket to Ride", "a": "The Beatles"}, {"r": "w", "y": 1966, "n": "I'm a Believer", "a": "The Monkees"}, {"r": "w", "y": 1966, "n": "You Keep Me Hangin' On", "a": "The Supremes"}, {"r": "w", "y": 1967, "n": "All You Need Is Love", "a": "The Beatles"}, {"r": "w", "y": 1967, "n": "Windy", "a": "The Association"}, {"r": "w", "y": 1968, "n": "Jumpin' Jack Flash", "a": "The Rolling Stones"}, {"r": "w", "y": 1968, "n": "Honky Tonk Women", "a": "The Rolling Stones"}, {"r": "w", "y": 1968, "n": "Gimme Shelter", "a": "The Rolling Stones"}, {"r": "w", "y": 1968, "n": "Hey Jude", "a": "The Beatles"}, {"r": "w", "y": 1969, "n": "Get Back", "a": "The Beatles"}, {"r": "w", "y": 1969, "n": "Something", "a": "The Beatles"}, {"r": "w", "y": 1969, "n": "You Can't Always Get What You Want", "a": "The Rolling Stones"}, {"r": "w", "y": 1970, "n": "ABC", "a": "The Jackson 5"}, {"r": "w", "y": 1971, "n": "Without You", "a": "Nilsson"}, {"r": "w", "y": 1971, "n": "What Is Life", "a": "George Harrison"}, {"r": "w", "y": 1971, "n": "Tiny Dancer", "a": "Elton John"}, {"r": "w", "y": 1972, "n": "Crocodile Rock", "a": "Elton John"}, {"r": "w", "y": 1972, "n": "I Can See Clearly Now", "a": "Johnny Nash"}, {"r": "w", "y": 1972, "n": "The Joker", "a": "Steve Miller Band"}, {"r": "w", "y": 1973, "n": "Goodbye Yellow Brick Road", "a": "Elton John"}, {"r": "w", "y": 1973, "n": "Daniel", "a": "Elton John"}, {"r": "w", "y": 1973, "n": "Bennie and the Jets", "a": "Elton John"}, {"r": "w", "y": 1973, "n": "Knockin' on Heaven's Door", "a": "Bob Dylan"}, {"r": "w", "y": 1973, "n": "Let's Stay Together", "a": "Al Green"}, {"r": "w", "y": 1973, "n": "She's Gone", "a": "Daryl Hall & John Oates"}, {"r": "w", "y": 1974, "n": "Bennie and the Jets", "a": "Elton John"}, {"r": "w", "y": 1974, "n": "You Ain't Seen Nothing Yet", "a": "Bachman-Turner Overdrive"}, {"r": "w", "y": 1975, "n": "Philadelphia Freedom", "a": "Elton John"}, {"r": "w", "y": 1975, "n": "Someone Saved My Life Tonight", "a": "Elton John"}, {"r": "w", "y": 1975, "n": "Love Will Keep Us Together", "a": "Captain & Tennille"}, {"r": "w", "y": 1975, "n": "Sara Smile", "a": "Daryl Hall & John Oates"}, {"r": "w", "y": 1976, "n": "The Boys Are Back in Town", "a": "Thin Lizzy"}, {"r": "w", "y": 1976, "n": "Rock and Roll All Nite", "a": "KISS"}, {"r": "w", "y": 1977, "n": "Rich Girl", "a": "Daryl Hall & John Oates"}, {"r": "w", "y": 1979, "n": "Emotional Rescue", "a": "The Rolling Stones"}, {"r": "w", "y": 1980, "n": "Keeping the Faith", "a": "Billy Joel"}, {"r": "w", "y": 1981, "n": "Private Eyes", "a": "Daryl Hall & John Oates"}, {"r": "w", "y": 1982, "n": "1999", "a": "Prince"}, {"r": "w", "y": 1982, "n": "Dirty Diana", "a": "Michael Jackson"}, {"r": "w", "y": 1983, "n": "Billie Jean", "a": "Michael Jackson"}, {"r": "w", "y": 1984, "n": "Like a Virgin", "a": "Madonna"}, {"r": "w", "y": 1985, "n": "Part-Time Lover", "a": "Stevie Wonder"}, {"r": "w", "y": 2002, "n": "Without Me", "a": "Eminem"}, {"r": "w", "y": 2004, "n": "Vertigo", "a": "U2"}, {"r": "w", "y": 2010, "n": "Dynamite", "a": "Taio Cruz"}, {"r": "w", "y": 2013, "n": "Roar? no", "a": "Katy Perry"}, {"r": "w", "y": 2015, "n": "Sugar", "a": "Maroon 5"}, {"r": "w", "y": 2016, "n": "One Dance", "a": "Drake"}, {"r": "w", "y": 2017, "n": "Attention", "a": "Charlie Puth"}, {"r": "w", "y": 2018, "n": "Better Now", "a": "Post Malone"}, {"r": "w", "y": 2019, "n": "Dance Monkey", "a": "Tones and I"}, {"r": "w", "y": 2013, "n": "Take Me to Church", "a": "Hozier"}, {"r": "w", "y": 2012, "n": "Too Good", "a": "Drake"}, {"r": "w", "y": 2011, "n": "Super Bass", "a": "Nicki Minaj"}]

SONGS += [{"r": "cn", "y": 1995, "n": "真永远", "a": "刘德华"}, {"r": "cn", "y": 1996, "n": "相思成灾", "a": "刘德华"}, {"r": "cn", "y": 2000, "n": "男人哭吧不是罪", "a": "刘德华"}, {"r": "cn", "y": 2000, "n": "练习", "a": "刘德华"}, {"r": "cn", "y": 2002, "n": "无间道", "a": "刘德华", "tag": "无间道"}, {"r": "cn", "y": 1994, "n": "风雨无阻", "a": "周华健"}, {"r": "cn", "y": 1999, "n": "雨一直下", "a": "张宇"}, {"r": "cn", "y": 1998, "n": "月亮惹的祸", "a": "张宇&十一郎"}, {"r": "cn", "y": 1998, "n": "信仰", "a": "张信哲"}, {"r": "cn", "y": 1996, "n": "太想爱你", "a": "张信哲"}, {"r": "cn", "y": 1995, "n": "宽容", "a": "张信哲"}, {"r": "cn", "y": 2003, "n": "断桥残雪", "a": "许嵩"}, {"r": "cn", "y": 2007, "n": "城府", "a": "许嵩"}, {"r": "cn", "y": 2009, "n": "素颜", "a": "许嵩&何曼婷"}, {"r": "cn", "y": 2006, "n": "清明雨上", "a": "许嵩"}, {"r": "cn", "y": 2011, "n": "千百度", "a": "许嵩"}, {"r": "cn", "y": 2009, "n": "庐州月", "a": "许嵩"}, {"r": "cn", "y": 1997, "n": "等你爱我", "a": "陈明"}, {"r": "cn", "y": 1997, "n": "亚洲雄风", "a": "刘欢&韦唯"}, {"r": "cn", "y": 1987, "n": "少年壮志不言愁", "a": "刘欢"}, {"r": "cn", "y": 1997, "n": "从头再来", "a": "刘欢"}, {"r": "cn", "y": 2014, "n": "时间都去哪儿了", "a": "王铮亮"}, {"r": "cn", "y": 1990, "n": "爱我的人和我爱的人", "a": "裘海正"}, {"r": "cn", "y": 1992, "n": "问", "a": "陈淑桦"}, {"r": "cn", "y": 1990, "n": "滚滚红尘", "a": "陈淑桦"}, {"r": "cn", "y": 1997, "n": "愚人码头", "a": "熊天平"}, {"r": "cn", "y": 1995, "n": "白天不懂夜的黑", "a": "那英"}, {"r": "cn", "y": 1994, "n": "哭砂", "a": "黄莺莺"}, {"r": "cn", "y": 1993, "n": "谁的眼泪在飞", "a": "孟庭苇"}, {"r": "cn", "y": 1994, "n": "我是不是你最疼爱的人", "a": "潘越云"}, {"r": "cn", "y": 1997, "n": "回家", "a": "顺子"}, {"r": "cn", "y": 2007, "n": "王妃", "a": "萧敬腾"}, {"r": "cn", "y": 2002, "n": "蓝莲花", "a": "许巍"}, {"r": "cn", "y": 2004, "n": "曾经的你", "a": "许巍"}, {"r": "cn", "y": 2007, "n": "红色高跟鞋", "a": "蔡健雅"}, {"r": "cn", "y": 2017, "n": "说散就散", "a": "袁娅维"}, {"r": "cn", "y": 2018, "n": "沙漠骆驼", "a": "展展与罗罗"}, {"r": "cn", "y": 2019, "n": "少年", "a": "梦然"}, {"r": "cn", "y": 2016, "n": "理想三旬", "a": "陈鸿宇"}, {"r": "cn", "y": 1992, "n": "鬼迷心窍", "a": "李宗盛"}, {"r": "cn", "y": 1990, "n": "弯弯的月亮", "a": "刘欢"}, {"r": "cn", "y": 1995, "n": "常回家看看", "a": "陈红"}, {"r": "cn", "y": 2013, "n": "山丘", "a": "李宗盛"}, {"r": "cn", "y": 2016, "n": "追光者", "a": "岑宁儿"}, {"r": "cn", "y": 2017, "n": "起风了", "a": "买辣椒也用券"}, {"r": "cn", "y": 2018, "n": "沙漠骆驼", "a": "展展与罗罗"}, {"r": "cn", "y": 2019, "n": "少年", "a": "梦然"}, {"r": "cn", "y": 2016, "n": "理想三旬", "a": "陈鸿宇"}, {"r": "w", "y": 1959, "n": "Dream Lover", "a": "Bobby Darin"}, {"r": "w", "y": 1959, "n": "El Paso", "a": "Marty Robbins"}, {"r": "w", "y": 1960, "n": "I Am Woman", "a": "Helen Reddy"}, {"r": "w", "y": 1961, "n": "Moon River", "a": "Henry Mancini"}, {"r": "w", "y": 1961, "n": "King of the Road", "a": "Roger Miller"}, {"r": "w", "y": 1962, "n": "I Can't Help Myself", "a": "Four Tops"}, {"r": "w", "y": 1963, "n": "She Loves You", "a": "The Beatles"}, {"r": "w", "y": 1964, "n": "Baby Love", "a": "The Supremes"}, {"r": "w", "y": 1964, "n": "My Guy", "a": "Mary Wells"}, {"r": "w", "y": 1964, "n": "Dancing in the Street", "a": "Martha & The Vandellas"}, {"r": "w", "y": 1965, "n": "Stop! In the Name of Love", "a": "The Supremes"}, {"r": "w", "y": 1965, "n": "Ticket to Ride", "a": "The Beatles"}, {"r": "w", "y": 1966, "n": "I'm a Believer", "a": "The Monkees"}, {"r": "w", "y": 1966, "n": "You Keep Me Hangin' On", "a": "The Supremes"}, {"r": "w", "y": 1967, "n": "All You Need Is Love", "a": "The Beatles"}, {"r": "w", "y": 1967, "n": "Windy", "a": "The Association"}, {"r": "w", "y": 1968, "n": "Jumpin' Jack Flash", "a": "The Rolling Stones"}, {"r": "w", "y": 1968, "n": "Honky Tonk Women", "a": "The Rolling Stones"}, {"r": "w", "y": 1968, "n": "Gimme Shelter", "a": "The Rolling Stones"}, {"r": "w", "y": 1968, "n": "Hey Jude", "a": "The Beatles"}, {"r": "w", "y": 1969, "n": "Get Back", "a": "The Beatles"}, {"r": "w", "y": 1969, "n": "Something", "a": "The Beatles"}, {"r": "w", "y": 1969, "n": "You Can't Always Get What You Want", "a": "The Rolling Stones"}, {"r": "w", "y": 1970, "n": "ABC", "a": "The Jackson 5"}, {"r": "w", "y": 1971, "n": "Without You", "a": "Nilsson"}, {"r": "w", "y": 1971, "n": "What Is Life", "a": "George Harrison"}, {"r": "w", "y": 1971, "n": "Tiny Dancer", "a": "Elton John"}, {"r": "w", "y": 1972, "n": "Crocodile Rock", "a": "Elton John"}, {"r": "w", "y": 1972, "n": "I Can See Clearly Now", "a": "Johnny Nash"}, {"r": "w", "y": 1972, "n": "The Joker", "a": "Steve Miller Band"}, {"r": "w", "y": 1973, "n": "Goodbye Yellow Brick Road", "a": "Elton John"}, {"r": "w", "y": 1973, "n": "Daniel", "a": "Elton John"}, {"r": "w", "y": 1973, "n": "Bennie and the Jets", "a": "Elton John"}, {"r": "w", "y": 1973, "n": "Knockin' on Heaven's Door", "a": "Bob Dylan"}, {"r": "w", "y": 1973, "n": "Let's Stay Together", "a": "Al Green"}, {"r": "w", "y": 1973, "n": "She's Gone", "a": "Daryl Hall & John Oates"}, {"r": "w", "y": 1974, "n": "Bennie and the Jets", "a": "Elton John"}, {"r": "w", "y": 1974, "n": "You Ain't Seen Nothing Yet", "a": "Bachman-Turner Overdrive"}, {"r": "w", "y": 1975, "n": "Philadelphia Freedom", "a": "Elton John"}, {"r": "w", "y": 1975, "n": "Someone Saved My Life Tonight", "a": "Elton John"}, {"r": "w", "y": 1975, "n": "Love Will Keep Us Together", "a": "Captain & Tennille"}, {"r": "w", "y": 1975, "n": "Sara Smile", "a": "Daryl Hall & John Oates"}, {"r": "w", "y": 1976, "n": "The Boys Are Back in Town", "a": "Thin Lizzy"}, {"r": "w", "y": 1976, "n": "Rock and Roll All Nite", "a": "KISS"}, {"r": "w", "y": 1977, "n": "Rich Girl", "a": "Daryl Hall & John Oates"}, {"r": "w", "y": 1979, "n": "Emotional Rescue", "a": "The Rolling Stones"}, {"r": "w", "y": 1980, "n": "Keeping the Faith", "a": "Billy Joel"}, {"r": "w", "y": 1981, "n": "Private Eyes", "a": "Daryl Hall & John Oates"}, {"r": "w", "y": 1982, "n": "1999", "a": "Prince"}, {"r": "w", "y": 1982, "n": "Dirty Diana", "a": "Michael Jackson"}, {"r": "w", "y": 1983, "n": "Billie Jean", "a": "Michael Jackson"}, {"r": "w", "y": 1984, "n": "Like a Virgin", "a": "Madonna"}, {"r": "w", "y": 1985, "n": "Part-Time Lover", "a": "Stevie Wonder"}, {"r": "w", "y": 2002, "n": "Without Me", "a": "Eminem"}, {"r": "w", "y": 2004, "n": "Vertigo", "a": "U2"}, {"r": "w", "y": 2010, "n": "Dynamite", "a": "Taio Cruz"}, {"r": "w", "y": 2015, "n": "Sugar", "a": "Maroon 5"}, {"r": "w", "y": 2016, "n": "One Dance", "a": "Drake"}, {"r": "w", "y": 2017, "n": "Attention", "a": "Charlie Puth"}, {"r": "w", "y": 2018, "n": "Better Now", "a": "Post Malone"}, {"r": "w", "y": 2019, "n": "Dance Monkey", "a": "Tones and I"}, {"r": "w", "y": 2013, "n": "Take Me to Church", "a": "Hozier"}, {"r": "w", "y": 2011, "n": "Super Bass", "a": "Nicki Minaj"}]

SONGS += [{"r": "cn", "y": 1983, "n": "一样的月光", "a": "苏芮"}, {"r": "cn", "y": 1983, "n": "酒干倘卖无", "a": "苏芮"}, {"r": "cn", "y": 1986, "n": "女儿情", "a": "吴静", "tag": "西游记"}, {"r": "cn", "y": 1993, "n": "新鸳鸯蝴蝶梦", "a": "黄安", "tag": "包青天"}, {"r": "cn", "y": 1993, "n": "纤夫的爱", "a": "尹相杰&于文华"}, {"r": "cn", "y": 1993, "n": "走四方", "a": "韩磊"}, {"r": "cn", "y": 1994, "n": "当爱已成往事", "a": "李宗盛&林忆莲", "tag": "霸王别姬"}, {"r": "cn", "y": 1994, "n": "爱江山更爱美人", "a": "李丽芬"}, {"r": "cn", "y": 1994, "n": "灰姑娘", "a": "郑钧"}, {"r": "cn", "y": 1994, "n": "追", "a": "张国荣"}, {"r": "cn", "y": 1994, "n": "天意", "a": "刘德华"}, {"r": "cn", "y": 1996, "n": "因为爱", "a": "刘德华"}, {"r": "cn", "y": 1998, "n": "笨小孩", "a": "刘德华"}, {"r": "cn", "y": 1991, "n": "来生缘", "a": "刘德华"}, {"r": "cn", "y": 1990, "n": "如果你是我的传说", "a": "刘德华"}, {"r": "cn", "y": 1993, "n": "我恨我痴心", "a": "刘德华"}, {"r": "cn", "y": 1990, "n": "李香兰", "a": "张学友"}, {"r": "cn", "y": 1993, "n": "一路上有你", "a": "张学友"}, {"r": "cn", "y": 1992, "n": "分手总要在雨天", "a": "张学友"}, {"r": "cn", "y": 1992, "n": "还是觉得你最好", "a": "张学友"}, {"r": "cn", "y": 1992, "n": "相思风雨中", "a": "张学友&汤宝如"}, {"r": "cn", "y": 1985, "n": "遥远的她", "a": "张学友"}, {"r": "cn", "y": 1985, "n": "月半弯", "a": "张学友"}, {"r": "cn", "y": 1999, "n": "她来听我的演唱会", "a": "张学友"}, {"r": "cn", "y": 1994, "n": "夏日倾情", "a": "黎明"}, {"r": "cn", "y": 1994, "n": "哪有一天不想你", "a": "黎明"}, {"r": "cn", "y": 1994, "n": "狂野之城", "a": "郭富城"}, {"r": "cn", "y": 2001, "n": "有没有一首歌会让你想起我", "a": "周华健"}, {"r": "cn", "y": 2000, "n": "冷酷到底", "a": "羽泉"}, {"r": "cn", "y": 1990, "n": "爱我的人和我爱的人", "a": "裘海正"}, {"r": "cn", "y": 2001, "n": "记得", "a": "张惠妹"}, {"r": "cn", "y": 2001, "n": "绿光", "a": "孙燕姿"}, {"r": "cn", "y": 2001, "n": "恋人未满", "a": "S.H.E"}, {"r": "cn", "y": 2005, "n": "不想长大", "a": "S.H.E"}, {"r": "cn", "y": 2004, "n": "第一次爱的人", "a": "王心凌"}, {"r": "cn", "y": 2004, "n": "遗失的美好", "a": "张韶涵"}, {"r": "cn", "y": 2006, "n": "左边", "a": "杨丞琳"}, {"r": "cn", "y": 2009, "n": "情歌", "a": "梁静茹"}, {"r": "cn", "y": 2010, "n": "她说", "a": "林俊杰"}, {"r": "cn", "y": 2013, "n": "修炼爱情", "a": "林俊杰"}, {"r": "w", "y": 1962, "n": "The Loco-Motion", "a": "Little Eva"}, {"r": "w", "y": 1963, "n": "Surfin' U.S.A.", "a": "The Beach Boys"}, {"r": "w", "y": 1963, "n": "She Loves You", "a": "The Beatles"}, {"r": "w", "y": 1965, "n": "Ticket to Ride", "a": "The Beatles"}, {"r": "w", "y": 1964, "n": "Dancing in the Street", "a": "Martha & The Vandellas"}, {"r": "w", "y": 1969, "n": "Sugar, Sugar", "a": "The Archies"}, {"r": "w", "y": 1970, "n": "Venus", "a": "The Shocking Blue"}, {"r": "w", "y": 1970, "n": "All Right Now", "a": "Free"}, {"r": "w", "y": 1972, "n": "School's Out", "a": "Alice Cooper"}, {"r": "w", "y": 1972, "n": "Layla", "a": "Derek & The Dominos"}, {"r": "w", "y": 1974, "n": "Kung Fu Fighting", "a": "Carl Douglas"}, {"r": "w", "y": 1975, "n": "SOS", "a": "ABBA"}, {"r": "w", "y": 1975, "n": "Mamma Mia", "a": "ABBA"}, {"r": "w", "y": 1976, "n": "Fernando", "a": "ABBA"}, {"r": "w", "y": 1977, "n": "Chiquitita", "a": "ABBA"}, {"r": "w", "y": 1978, "n": "Shadow Dancing", "a": "Andy Gibb"}, {"r": "w", "y": 1981, "n": "Endless Love", "a": "Diana Ross & Lionel Richie"}, {"r": "w", "y": 1984, "n": "Jump", "a": "Van Halen"}, {"r": "w", "y": 1990, "n": "Vogue", "a": "Madonna"}, {"r": "w", "y": 1992, "n": "Tears in Heaven", "a": "Eric Clapton"}, {"r": "w", "y": 1992, "n": "End of the Road", "a": "Boyz II Men"}, {"r": "w", "y": 1994, "n": "I'll Make Love to You", "a": "Boyz II Men"}, {"r": "w", "y": 1995, "n": "Kiss Me", "a": "Sixpence None the Richer"}, {"r": "w", "y": 1996, "n": "Return of the Mack", "a": "Mark Morrison"}, {"r": "w", "y": 1997, "n": "Torn", "a": "Natalie Imbruglia"}, {"r": "w", "y": 1998, "n": "Iris", "a": "The Goo Goo Dolls"}, {"r": "w", "y": 2000, "n": "Bye Bye Bye", "a": "*NSYNC"}, {"r": "w", "y": 2001, "n": "How You Remind Me", "a": "Nickelback"}, {"r": "w", "y": 2002, "n": "A Thousand Miles", "a": "Vanessa Carlton"}, {"r": "w", "y": 2003, "n": "Stacy's Mom", "a": "Fountains of Wayne"}, {"r": "w", "y": 2004, "n": "Vertigo", "a": "U2"}, {"r": "w", "y": 2004, "n": "Boulevard of Broken Dreams", "a": "Green Day"}, {"r": "w", "y": 2005, "n": "Photograph", "a": "Nickelback"}, {"r": "w", "y": 2005, "n": "Wake Me Up When September Ends", "a": "Green Day"}, {"r": "w", "y": 2006, "n": "Before He Cheats", "a": "Carrie Underwood"}, {"r": "w", "y": 2007, "n": "Big Girls Don't Cry", "a": "Fergie"}, {"r": "w", "y": 2008, "n": "Hot N Cold", "a": "Katy Perry"}, {"r": "w", "y": 2008, "n": "So What", "a": "P!nk"}, {"r": "w", "y": 2009, "n": "Empire State of Mind", "a": "Jay-Z & Alicia Keys"}, {"r": "w", "y": 2010, "n": "Dynamite", "a": "Taio Cruz"}, {"r": "w", "y": 2010, "n": "Hey, Soul Sister", "a": "Train"}, {"r": "w", "y": 2010, "n": "Grenade", "a": "Bruno Mars"}, {"r": "w", "y": 2011, "n": "Set Fire to the Rain", "a": "Adele"}, {"r": "w", "y": 2011, "n": "Party Rock Anthem", "a": "LMFAO"}, {"r": "w", "y": 2011, "n": "Give Me Everything", "a": "Pitbull"}, {"r": "w", "y": 2011, "n": "Born This Way", "a": "Lady Gaga"}, {"r": "w", "y": 2012, "n": "Payphone", "a": "Maroon 5 feat. Wiz Khalifa"}, {"r": "w", "y": 2012, "n": "Diamonds", "a": "Rihanna"}, {"r": "w", "y": 2012, "n": "Stay", "a": "Rihanna feat. Mikky Ekko"}, {"r": "w", "y": 2012, "n": "Some Nights", "a": "fun."}, {"r": "w", "y": 2012, "n": "Ho Hey", "a": "The Lumineers"}, {"r": "w", "y": 2012, "n": "I Knew You Were Trouble", "a": "Taylor Swift"}, {"r": "w", "y": 2012, "n": "We Are Never Ever Getting Back Together", "a": "Taylor Swift"}, {"r": "w", "y": 2012, "n": "Gangnam Style", "a": "PSY"}, {"r": "w", "y": 2013, "n": "Thrift Shop", "a": "Macklemore & Ryan Lewis"}, {"r": "w", "y": 2013, "n": "Demons", "a": "Imagine Dragons"}, {"r": "w", "y": 2013, "n": "Clarity", "a": "Zedd feat. Foxes"}, {"r": "w", "y": 2013, "n": "Story of My Life", "a": "One Direction"}, {"r": "w", "y": 2013, "n": "Let It Go", "a": "Idina Menzel", "tag": "Frozen"}, {"r": "w", "y": 2014, "n": "All About That Bass", "a": "Meghan Trainor"}, {"r": "w", "y": 2014, "n": "Rather Be", "a": "Clean Bandit feat. Jess Glynne"}, {"r": "w", "y": 2014, "n": "Rude", "a": "Magic!"}, {"r": "w", "y": 2015, "n": "Cheerleader", "a": "OMI"}, {"r": "w", "y": 2015, "n": "Lean On", "a": "Major Lazer & DJ Snake"}, {"r": "w", "y": 2015, "n": "7 Years", "a": "Lukas Graham"}, {"r": "w", "y": 2016, "n": "Stitches", "a": "Shawn Mendes"}, {"r": "w", "y": 2017, "n": "Something Just Like This", "a": "The Chainsmokers & Coldplay"}, {"r": "w", "y": 2018, "n": "Sunflower", "a": "Post Malone & Swae Lee"}, {"r": "w", "y": 2019, "n": "Señorita", "a": "Shawn Mendes & Camila Cabello"}, {"r": "w", "y": 2019, "n": "Circles", "a": "Post Malone"}]

SONGS += [{"r": "cn", "y": 1994, "n": "风雨无阻", "a": "周华健"}, {"r": "cn", "y": 1999, "n": "雨一直下", "a": "张宇"}, {"r": "cn", "y": 1998, "n": "月亮惹的祸", "a": "张宇&十一郎"}, {"r": "cn", "y": 1998, "n": "信仰", "a": "张信哲"}, {"r": "cn", "y": 1996, "n": "太想爱你", "a": "张信哲"}, {"r": "cn", "y": 1995, "n": "宽容", "a": "张信哲"}, {"r": "cn", "y": 2003, "n": "断桥残雪", "a": "许嵩"}, {"r": "cn", "y": 2007, "n": "城府", "a": "许嵩"}, {"r": "cn", "y": 2009, "n": "素颜", "a": "许嵩&何曼婷"}, {"r": "cn", "y": 2006, "n": "清明雨上", "a": "许嵩"}, {"r": "cn", "y": 2011, "n": "千百度", "a": "许嵩"}, {"r": "cn", "y": 2009, "n": "庐州月", "a": "许嵩"}, {"r": "cn", "y": 1997, "n": "等你爱我", "a": "陈明"}, {"r": "cn", "y": 1997, "n": "亚洲雄风", "a": "刘欢&韦唯"}, {"r": "cn", "y": 1987, "n": "少年壮志不言愁", "a": "刘欢"}, {"r": "cn", "y": 1997, "n": "从头再来", "a": "刘欢"}, {"r": "cn", "y": 2014, "n": "时间都去哪儿了", "a": "王铮亮"}, {"r": "cn", "y": 1990, "n": "爱我的人和我爱的人", "a": "裘海正"}, {"r": "cn", "y": 1992, "n": "问", "a": "陈淑桦"}, {"r": "cn", "y": 1990, "n": "滚滚红尘", "a": "陈淑桦"}, {"r": "cn", "y": 1997, "n": "愚人码头", "a": "熊天平"}, {"r": "cn", "y": 1995, "n": "白天不懂夜的黑", "a": "那英"}, {"r": "cn", "y": 1994, "n": "哭砂", "a": "黄莺莺"}, {"r": "cn", "y": 1993, "n": "谁的眼泪在飞", "a": "孟庭苇"}, {"r": "cn", "y": 1994, "n": "我是不是你最疼爱的人", "a": "潘越云"}, {"r": "cn", "y": 1997, "n": "回家", "a": "顺子"}, {"r": "cn", "y": 2007, "n": "王妃", "a": "萧敬腾"}, {"r": "cn", "y": 2002, "n": "蓝莲花", "a": "许巍"}, {"r": "cn", "y": 2004, "n": "曾经的你", "a": "许巍"}, {"r": "cn", "y": 2007, "n": "红色高跟鞋", "a": "蔡健雅"}, {"r": "cn", "y": 2017, "n": "说散就散", "a": "袁娅维"}, {"r": "cn", "y": 2018, "n": "沙漠骆驼", "a": "展展与罗罗"}, {"r": "cn", "y": 2019, "n": "少年", "a": "梦然"}, {"r": "cn", "y": 2016, "n": "理想三旬", "a": "陈鸿宇"}, {"r": "cn", "y": 1992, "n": "鬼迷心窍", "a": "李宗盛"}, {"r": "cn", "y": 1990, "n": "弯弯的月亮", "a": "刘欢"}, {"r": "cn", "y": 1995, "n": "常回家看看", "a": "陈红"}, {"r": "cn", "y": 2013, "n": "山丘", "a": "李宗盛"}, {"r": "cn", "y": 2016, "n": "追光者", "a": "岑宁儿"}, {"r": "cn", "y": 2017, "n": "起风了", "a": "买辣椒也用券"}, {"r": "w", "y": 1962, "n": "Green Onions", "a": "Booker T. & the M.G.'s"}, {"r": "w", "y": 1964, "n": "A Hard Day's Night", "a": "The Beatles"}, {"r": "w", "y": 1967, "n": "Let's Spend the Night Together", "a": "The Rolling Stones"}, {"r": "w", "y": 1968, "n": "Crimson and Clover", "a": "Tommy James & the Shondells"}, {"r": "w", "y": 1969, "n": "Spinning Wheel", "a": "Blood, Sweat & Tears"}, {"r": "w", "y": 1973, "n": "Love Train", "a": "The O'Jays"}, {"r": "w", "y": 1975, "n": "Fame", "a": "David Bowie"}, {"r": "w", "y": 1979, "n": "Cars", "a": "Gary Numan"}, {"r": "w", "y": 1980, "n": "Funkytown", "a": "Lipps Inc."}, {"r": "w", "y": 1984, "n": "Lucky Star", "a": "Madonna"}, {"r": "w", "y": 1986, "n": "West End Girls", "a": "Pet Shop Boys"}, {"r": "w", "y": 1991, "n": "Black or White", "a": "Michael Jackson"}, {"r": "w", "y": 1994, "n": "Always", "a": "Bon Jovi"}, {"r": "w", "y": 1995, "n": "Kiss Me", "a": "Sixpence None the Richer"}, {"r": "w", "y": 1996, "n": "Killing Me Softly", "a": "Fugees"}, {"r": "w", "y": 1999, "n": "Mambo No. 5", "a": "Lou Bega"}, {"r": "w", "y": 1999, "n": "Angel", "a": "Sarah McLachlan"}, {"r": "w", "y": 2003, "n": "Stacy's Mom", "a": "Fountains of Wayne"}, {"r": "w", "y": 2004, "n": "Wake Me Up When September Ends", "a": "Green Day"}, {"r": "w", "y": 2004, "n": "American Idiot", "a": "Green Day"}, {"r": "w", "y": 2005, "n": "Because of You", "a": "Kelly Clarkson"}, {"r": "w", "y": 2010, "n": "Dynamite", "a": "Taio Cruz"}, {"r": "w", "y": 2011, "n": "It Will Rain", "a": "Bruno Mars"}, {"r": "w", "y": 2012, "n": "One More Night", "a": "Maroon 5"}, {"r": "w", "y": 2014, "n": "Shut Up and Dance", "a": "WALK THE MOON"}, {"r": "w", "y": 2016, "n": "One Dance", "a": "Drake"}, {"r": "w", "y": 1973, "n": "Frankenstein", "a": "Edgar Winter Group"}, {"r": "w", "y": 1974, "n": "Rock the Boat", "a": "Hues Corporation"}, {"r": "w", "y": 1975, "n": "Get Down Tonight", "a": "KC and the Sunshine Band"}, {"r": "w", "y": 1976, "n": "Play That Funky Music", "a": "Wild Cherry"}, {"r": "w", "y": 1977, "n": "Don't Leave Me This Way", "a": "Thelma Houston"}, {"r": "w", "y": 1982, "n": "Hurts So Good", "a": "John Mellencamp"}, {"r": "w", "y": 1983, "n": "She Works Hard for the Money", "a": "Donna Summer"}, {"r": "w", "y": 1985, "n": "We Built This City", "a": "Starship"}, {"r": "w", "y": 1986, "n": "Sara", "a": "Starship"}, {"r": "w", "y": 1987, "n": "Nothing's Gonna Stop Us Now", "a": "Starship"}, {"r": "w", "y": 1988, "n": "Need You Tonight", "a": "INXS"}, {"r": "w", "y": 1990, "n": "Black Velvet", "a": "Alannah Myles"}, {"r": "w", "y": 1992, "n": "Achy Breaky Heart", "a": "Billy Ray Cyrus"}, {"r": "w", "y": 1994, "n": "What's the Frequency, Kenneth?", "a": "R.E.M."}, {"r": "w", "y": 1997, "n": "Tubthumping", "a": "Chumbawamba"}, {"r": "w", "y": 1998, "n": "One Headlight", "a": "The Wallflowers"}, {"r": "w", "y": 2001, "n": "Drops of Jupiter", "a": "Train"}, {"r": "w", "y": 2002, "n": "A Moment Like This", "a": "Kelly Clarkson"}, {"r": "w", "y": 2004, "n": "Take Me Out", "a": "Franz Ferdinand"}]

SONGS += [{"r": "cn", "y": 1983, "n": "一样的月光", "a": "苏芮"}, {"r": "cn", "y": 1983, "n": "酒干倘卖无", "a": "苏芮"}, {"r": "cn", "y": 1986, "n": "女儿情", "a": "吴静", "tag": "西游记"}, {"r": "cn", "y": 1993, "n": "新鸳鸯蝴蝶梦", "a": "黄安", "tag": "包青天"}, {"r": "cn", "y": 1993, "n": "纤夫的爱", "a": "尹相杰&于文华"}, {"r": "cn", "y": 1993, "n": "走四方", "a": "韩磊"}, {"r": "cn", "y": 1994, "n": "当爱已成往事", "a": "李宗盛&林忆莲", "tag": "霸王别姬"}, {"r": "cn", "y": 1994, "n": "爱江山更爱美人", "a": "李丽芬"}, {"r": "cn", "y": 1994, "n": "灰姑娘", "a": "郑钧"}, {"r": "cn", "y": 1994, "n": "追", "a": "张国荣"}, {"r": "cn", "y": 1994, "n": "天意", "a": "刘德华"}, {"r": "cn", "y": 1996, "n": "因为爱", "a": "刘德华"}, {"r": "cn", "y": 1998, "n": "笨小孩", "a": "刘德华"}, {"r": "cn", "y": 1991, "n": "来生缘", "a": "刘德华"}, {"r": "cn", "y": 1990, "n": "如果你是我的传说", "a": "刘德华"}, {"r": "cn", "y": 1993, "n": "我恨我痴心", "a": "刘德华"}, {"r": "cn", "y": 1990, "n": "李香兰", "a": "张学友"}, {"r": "cn", "y": 1993, "n": "一路上有你", "a": "张学友"}, {"r": "cn", "y": 1992, "n": "分手总要在雨天", "a": "张学友"}, {"r": "cn", "y": 1992, "n": "还是觉得你最好", "a": "张学友"}, {"r": "cn", "y": 1992, "n": "相思风雨中", "a": "张学友&汤宝如"}, {"r": "cn", "y": 1985, "n": "遥远的她", "a": "张学友"}, {"r": "cn", "y": 1985, "n": "月半弯", "a": "张学友"}, {"r": "cn", "y": 1999, "n": "她来听我的演唱会", "a": "张学友"}, {"r": "cn", "y": 1994, "n": "夏日倾情", "a": "黎明"}, {"r": "cn", "y": 1994, "n": "哪有一天不想你", "a": "黎明"}, {"r": "cn", "y": 1994, "n": "狂野之城", "a": "郭富城"}, {"r": "cn", "y": 2001, "n": "有没有一首歌会让你想起我", "a": "周华健"}, {"r": "cn", "y": 2000, "n": "冷酷到底", "a": "羽泉"}, {"r": "cn", "y": 1990, "n": "爱我的人和我爱的人", "a": "裘海正"}, {"r": "cn", "y": 2001, "n": "记得", "a": "张惠妹"}, {"r": "cn", "y": 2001, "n": "绿光", "a": "孙燕姿"}, {"r": "cn", "y": 2001, "n": "恋人未满", "a": "S.H.E"}, {"r": "cn", "y": 2005, "n": "不想长大", "a": "S.H.E"}, {"r": "cn", "y": 2004, "n": "第一次爱的人", "a": "王心凌"}, {"r": "cn", "y": 2004, "n": "遗失的美好", "a": "张韶涵"}, {"r": "cn", "y": 2006, "n": "左边", "a": "杨丞琳"}, {"r": "cn", "y": 2009, "n": "情歌", "a": "梁静茹"}, {"r": "cn", "y": 2010, "n": "她说", "a": "林俊杰"}, {"r": "cn", "y": 2013, "n": "修炼爱情", "a": "林俊杰"}, {"r": "w", "y": 1962, "n": "The Loco-Motion", "a": "Little Eva"}, {"r": "w", "y": 1963, "n": "Surfin' U.S.A.", "a": "The Beach Boys"}, {"r": "w", "y": 1963, "n": "She Loves You", "a": "The Beatles"}, {"r": "w", "y": 1965, "n": "Ticket to Ride", "a": "The Beatles"}, {"r": "w", "y": 1964, "n": "Dancing in the Street", "a": "Martha & The Vandellas"}, {"r": "w", "y": 1969, "n": "Sugar, Sugar", "a": "The Archies"}, {"r": "w", "y": 1970, "n": "Venus", "a": "The Shocking Blue"}, {"r": "w", "y": 1970, "n": "All Right Now", "a": "Free"}, {"r": "w", "y": 1972, "n": "School's Out", "a": "Alice Cooper"}, {"r": "w", "y": 1972, "n": "Layla", "a": "Derek & The Dominos"}, {"r": "w", "y": 1974, "n": "Kung Fu Fighting", "a": "Carl Douglas"}, {"r": "w", "y": 1975, "n": "SOS", "a": "ABBA"}, {"r": "w", "y": 1975, "n": "Mamma Mia", "a": "ABBA"}, {"r": "w", "y": 1976, "n": "Fernando", "a": "ABBA"}, {"r": "w", "y": 1977, "n": "Chiquitita", "a": "ABBA"}, {"r": "w", "y": 1978, "n": "Shadow Dancing", "a": "Andy Gibb"}, {"r": "w", "y": 1981, "n": "Endless Love", "a": "Diana Ross & Lionel Richie"}, {"r": "w", "y": 1984, "n": "Jump", "a": "Van Halen"}, {"r": "w", "y": 1990, "n": "Vogue", "a": "Madonna"}, {"r": "w", "y": 1992, "n": "Tears in Heaven", "a": "Eric Clapton"}, {"r": "w", "y": 1992, "n": "End of the Road", "a": "Boyz II Men"}, {"r": "w", "y": 1994, "n": "I'll Make Love to You", "a": "Boyz II Men"}, {"r": "w", "y": 1995, "n": "Kiss Me", "a": "Sixpence None the Richer"}, {"r": "w", "y": 1996, "n": "Return of the Mack", "a": "Mark Morrison"}, {"r": "w", "y": 1997, "n": "Torn", "a": "Natalie Imbruglia"}, {"r": "w", "y": 1998, "n": "Iris", "a": "The Goo Goo Dolls"}]

SONGS += [{"r": "w", "y": 1960, "n": "Wedding Bell Blues", "a": "The 5th Dimension"}, {"r": "w", "y": 1971, "n": "Family Affair", "a": "Sly & The Family Stone"}, {"r": "w", "y": 1972, "n": "Back Stabbers", "a": "The O'Jays"}, {"r": "w", "y": 1972, "n": "Use Me", "a": "Bill Withers"}, {"r": "w", "y": 1973, "n": "Higher Ground", "a": "Stevie Wonder"}, {"r": "w", "y": 1973, "n": "Free Ride", "a": "The Edgar Winter Group"}, {"r": "w", "y": 1983, "n": "She Blinded Me with Science", "a": "Thomas Dolby"}, {"r": "w", "y": 1986, "n": "Your Love", "a": "The Outfield"}, {"r": "w", "y": 1987, "n": "Should I Stay or Should I Go", "a": "The Clash"}, {"r": "w", "y": 1989, "n": "My Prerogative", "a": "Bobby Brown"}, {"r": "w", "y": 1993, "n": "Two Princes", "a": "Spin Doctors"}, {"r": "w", "y": 1997, "n": "Save Tonight", "a": "Eagle-Eye Cherry"}, {"r": "w", "y": 2002, "n": "Hot in Herre", "a": "Nelly"}, {"r": "w", "y": 2002, "n": "Dilemma", "a": "Nelly & Kelly Rowland"}, {"r": "w", "y": 2009, "n": "Meet Me Halfway", "a": "Black Eyed Peas"}, {"r": "cn", "y": 1992, "n": "难以抗拒你容颜", "a": "张信哲"}, {"r": "cn", "y": 1993, "n": "我是真的爱你", "a": "张信哲"}, {"r": "cn", "y": 1997, "n": "心要让你听见", "a": "邰正宵"}, {"r": "cn", "y": 1998, "n": "千纸鹤", "a": "邰正宵"}, {"r": "cn", "y": 2006, "n": "专属天使", "a": "TANK"}, {"r": "cn", "y": 2011, "n": "那些你很冒险的梦", "a": "林俊杰"}, {"r": "cn", "y": 2013, "n": "你不知道的事", "a": "王力宏"}]

# 归一化：支持 dict 或 tuple (r,y,n,a[,tag]) 两种写法
def _norm_song(e):
    if isinstance(e, dict):
        return e
    r, y, n, a = e[0], e[1], e[2], e[3]
    d = {"r": r, "y": y, "n": n, "a": a}
    if len(e) > 4 and e[4]:
        d["tag"] = e[4]
    return d
SONGS = [_norm_song(s) for s in SONGS]

MARK_L = "<!--SONGS:START-->"
MARK_R = "<!--SONGS:END-->"
DATA_L = "/*SONGSDATA:START*/"
DATA_R = "/*SONGSDATA:END*/"
CACHE_FILE = "scripts/covers.json"

# 搜索匹配不到/匹配错误的曲目，在此手工指定 albumMid（QQ音乐专辑hash）
COVER_OVERRIDE = {
    "铁血丹心|罗文&甄妮": "000zzpBQ2MHa5Q",
    "潇洒走一回|叶倩文": "004elsWz3Aa9I9",
    "梦回唐朝|唐朝乐队": "003HIIUT2HzSud",
    "回到拉萨|郑钧": "001OGeUa2raENA",
    "K歌之王|陈奕迅": "004WcjmQ3fOaN9",
    "Super Star|S.H.E": "000T16q900CwBg",
    "The Power of Love|Huey Lewis and the News": "0027USG90EvKmk",
    "Faith|George Michael": "0025oXfJ33YfWZ",
    "Pour Some Sugar on Me|Def Leppard": "001cgkUU0TQszk",
    "(Everything I Do) I Do It for You|Bryan Adams": "000iQbuI10xVHa",
    "My Heart Will Go On|Celine Dion": "003UrQPD42gZkV",
    "Smooth|Santana feat. Rob Thomas": "002m2xkC4XzdmQ",
    "Closer|The Chainsmokers feat. Halsey": "001rWGUJ3Gvypx",
    "两只蝴蝶|庞龙": "001VUVMg2zA3AZ",
}

def qq_url(n, a):
    return "https://y.qq.com/n/ryqq/search?w=" + urllib.parse.quote(f"{n} {a}")

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def singer_match(artist, singers):
    a = artist.lower()
    if "群星" in a:
        return True
    names = " ".join(singers).lower()
    tokens = [t.strip().lower() for t in re.split(r"&|,|feat\.?", a) if len(t.strip()) >= 2]
    tokens.append(a.strip().lower())
    return any(t in names for t in tokens)

def load_cache():
    try:
        import json
        return json.load(open(CACHE_FILE, encoding="utf-8"))
    except Exception:
        return {}

def fetch_meta(n, a, cache):
    import json, time, urllib.request
    key = f"{n}|{a}"
    if key in COVER_OVERRIDE:  # 人工覆盖优先于缓存（缓存里可能存着未匹配）
        m = {"album": COVER_OVERRIDE[key], "smid": "", "songmid": "", "singer": "(override)"}
        cache[key] = m
        return m
    if key in cache:
        return cache[key]
    w = urllib.parse.quote(f"{n} {a}")
    url = f"https://c.y.qq.com/soso/fcgi-bin/client_search_cp?w={w}&format=json&limit=5"
    meta = None
    try:
        req = urllib.request.Request(url, headers={
            "Referer": "https://y.qq.com/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        })
        # 走系统代理时部分请求会挂起，6 秒超时兜底
        with urllib.request.urlopen(req, timeout=6) as resp:
            d = json.loads(resp.read().decode("utf-8", "ignore"))
        for s in (d.get("data") or {}).get("song", {}).get("list") or []:
            singers = [x.get("name", "") for x in (s.get("singer") or [])]
            if singer_match(a, singers):
                meta = {
                    "album": s.get("albummid", ""),
                    "smid": (s.get("singer") or [{}])[0].get("mid", ""),
                    "songmid": s.get("songmid", ""),
                    "singer": "/".join(singers),
                }
                break
    except Exception:
        pass  # 失败也缓存 None，避免反复打失败请求
    cache[key] = meta
    return meta

def prefetch_all(cache):
    from concurrent.futures import ThreadPoolExecutor
    todo = [s for s in SONGS if f'{s["n"]}|{s["a"]}' not in cache]
    print(f"fetching meta for {len(todo)} songs (6 workers)...", flush=True)
    done = [0]
    with ThreadPoolExecutor(max_workers=6) as ex:
        futures = {ex.submit(fetch_meta, s["n"], s["a"], cache): s for s in todo}
        for f in futures:
            f.result()
            done[0] += 1
            if done[0] % 50 == 0 or done[0] == len(todo):
                print(f"  {done[0]}/{len(todo)}", flush=True)
                try:
                    import json
                    open(CACHE_FILE, "w", encoding="utf-8").write(json.dumps(cache, ensure_ascii=False))
                except Exception:
                    pass

def build():
    import json
    cache = load_cache()
    prefetch_all(cache)
    html = open("index.html", encoding="utf-8").read()
    # 去重保护：同歌名同歌手只保留一条
    seen_k = set()
    uniq = []
    for s in SONGS:
        k = (s["n"], s["a"])
        if k in seen_k:
            print(f"  ! 去重跳过: {s['y']} {s['n']} - {s['a']}")
            continue
        seen_k.add(k)
        uniq.append(s)
    # 按 (region, year) 分组，年内保持精选顺序
    blocks = {"cn": [], "w": []}
    misses = []
    for r in ("cn", "w"):
        years = sorted({s["y"] for s in uniq if s["r"] == r})
        for y in years:
            items = [s for s in uniq if s["r"] == r and s["y"] == y]
            lis = []
            for i, s in enumerate(items, 1):
                meta = fetch_meta(s["n"], s["a"], cache) or {}
                if not meta.get("album"):
                    misses.append(f'{s["y"]} {s["n"]} - {s["a"]}')
                q = qq_url(s["n"], s["a"])
                if meta.get("songmid"):
                    q = f"https://y.qq.com/n/ryqq/songDetail/{meta['songmid']}"
                cov = (f'https://y.gtimg.cn/music/photo_new/T002R300x300M000{meta["album"]}.jpg'
                       if meta.get("album") else "")
                av = (f'https://y.gtimg.cn/music/photo_new/T001R300x300M000{meta["smid"]}.jpg'
                      if meta.get("smid") else "")
                tag = f'<span class="tag">{esc(s["tag"])}</span>' if s.get("tag") else ""
                cov_img = (f'<img loading="lazy" src="{esc(cov)}" alt="" onerror="this.classList.add(\'bad\')">'
                           if cov else '<img class="bad" alt="">')
                av_img = (f'<img class="av" loading="lazy" src="{esc(av)}" alt="" onerror="this.classList.add(\'bad\')">'
                          if av else "")
                lis.append(
                    f'<li data-y="{y}" data-search="{esc((s["n"]+" "+s["a"]).lower())}">'
                    f'<span class="cov">{cov_img}</span>'
                    f'<span class="rk">{i}</span>'
                    f'<span class="tx"><span class="tn">{esc(s["n"])}</span>'
                    f'<span class="ta">{av_img}{esc(s["a"])}{tag}</span></span>'
                    f'<span class="pgrp">'
                    f'<a class="qq" href="{q}" target="_blank" rel="noopener" data-en="Play on QQ Music ↗">QQ 音乐播放 ↗</a>'
                    f'<a class="pl" href="https://music.163.com/#/search/m/?s={urllib.parse.quote(s["n"]+" "+s["a"])}" target="_blank" rel="noopener" title="网易云音乐">网易云</a>'
                    f'<a class="pl" href="https://www.kugou.com/yy/html/search.html#searchType=song&searchKey={urllib.parse.quote(s["n"]+" "+s["a"])}" target="_blank" rel="noopener" title="酷狗音乐">酷狗</a>'
                    f'<a class="pl" href="https://www.kuwo.cn/search/list?key={urllib.parse.quote(s["n"]+" "+s["a"])}" target="_blank" rel="noopener" title="酷我音乐">酷我</a>'
                    f'</span></li>'
                )
            blocks[r].append(f'<section class="yr" data-year="{y}"><h3>{y}</h3><ol class="sc">{"".join(lis)}</ol></section>')
    import json as J
    try:
        open(CACHE_FILE, "w", encoding="utf-8").write(J.dumps(cache, ensure_ascii=False, indent=0))
    except Exception as e:
        print("  ! cache write failed:", e)
    new_cards = (MARK_L + '<div class="yrset" id="setCN">' + "".join(blocks["cn"]) + "</div>"
                 + '<div class="yrset" id="setW" hidden>' + "".join(blocks["w"]) + "</div>" + MARK_R)
    html = re.sub(re.escape(MARK_L) + ".*?" + re.escape(MARK_R), lambda m: new_cards, html, flags=re.S)
    new_data = DATA_L + J.dumps([{"r":s["r"],"y":s["y"],"n":s["n"],"a":s["a"],**( {"tag":s["tag"]} if s.get("tag") else {} )} for s in uniq], ensure_ascii=False) + DATA_R
    html = re.sub(re.escape(DATA_L) + ".*?" + re.escape(DATA_R), lambda m: new_data, html, flags=re.S)
    open("index.html", "w", encoding="utf-8").write(html)
    cn = sum(1 for s in SONGS if s["r"]=="cn"); w = len(SONGS)-cn
    print(f"rebuilt: {len(SONGS)} songs (华语 {cn} / 世界 {w}), {len(blocks['cn'])}+{len(blocks['w'])} year sections")
    print(f"covers: {len(SONGS)-len(misses)}/{len(SONGS)} matched")
    if misses:
        print("未匹配（可在 COVER_OVERRIDE 手工指定 albumMid）:")
        for m in misses:
            print("  -", m)

if __name__ == "__main__":
    build()

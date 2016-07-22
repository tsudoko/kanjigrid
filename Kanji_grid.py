#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Contact: frony0@gmail.com

import time,codecs,math,os,unicodedata
from functools import reduce
from aqt import mw
from anki.js import jquery
from aqt.utils import showInfo
from anki.utils import ids2str
from anki.hooks import addHook
from aqt.webview import AnkiWebView
from aqt.qt import *

#_time = None
_pattern = "kanji"
_literal = False
_interval = 180
_thin = 20
_wide = 48
_group = 0
_unseen = True
_tooltips = False
_kanjionly = True
_ignore = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" + \
          "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ" + \
          "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ" + \
          "1234567890１２３４５６７８９０" + \
          "あいうゔえおぁぃぅぇぉかきくけこがぎぐげごさしすせそざじずぜぞ" + \
          "たちつてとだぢづでどなにぬねのはひふへほばびぶべぼぱぴぷぺぽ" + \
          "まみむめもやゃゆゅよょらりるれろわをんっ" + \
          "アイウヴエオァィゥェォカキクケコガギグゲゴサシスセソザジズゼゾ" + \
          "タチツテトダヂヅデドナニヌネノハヒフヘホバビブベボパピプペポ" + \
          "マミムメモヤャユュヨョラリルレロワヲンッ" + \
          "!\"$%&'()|=~-^@[;:],./`{+*}<>?\\_" + \
          "＠「；：」、。・‘｛＋＊｝＜＞？＼＿！”＃＄％＆’（）｜＝．〜～ー＾ ゙゙゚" + \
          "☆★＊○●◎〇◯“…『』#♪ﾞ〉〈→》《π×"
_grades = [ ('Non-Jouyou', ''),
    ('Grade 1', '一右雨円王音下火花貝学気休玉金九空月犬見五口校左三山四子糸字耳七車手十出女小上森人水正生青石赤先千川早草足村大男竹中虫町天田土二日入年白八百文本名木目夕立力林六'),
    ('Grade 2', '引羽雲園遠黄何夏家科歌画会回海絵外角楽活間丸岩顔帰汽記弓牛魚京強教近兄形計元原言古戸午後語交光公工広考行高合国黒今才細作算姉市思止紙寺時自室社弱首秋週春書少場色食心新親図数星晴声西切雪線船前組走多太体台谷知地池茶昼朝長鳥直通弟店点電冬刀東当答頭同道読内南肉馬買売麦半番父風分聞米歩母方北妹毎万明鳴毛門夜野矢友曜用来理里話'),
    ('Grade 3', '悪安暗委意医育員飲院運泳駅央横屋温化荷界開階寒感漢館岸期起客宮急球究級去橋業局曲銀区苦具君係軽決血研県庫湖向幸港号根祭坂皿仕使始指死詩歯事持次式実写者主取守酒受州拾終習集住重宿所暑助勝商昭消章乗植深申真神身進世整昔全想相送息速族他打対待代第題炭短談着柱注丁帳調追定庭笛鉄転登都度島投湯等豆動童農波配倍箱畑発反板悲皮美鼻筆氷表病秒品負部服福物平返勉放味命面問役薬油有由遊予様洋羊葉陽落流旅両緑礼列練路和'),
    ('Grade 4', '愛案以位囲胃衣印栄英塩億加果課貨芽改械害街各覚完官管観関願喜器希旗機季紀議救求泣給挙漁競共協鏡極訓軍郡型径景芸欠結健建験固候功好康航告差最菜材昨刷察札殺参散産残司史士氏試児治辞失借種周祝順初唱松焼照省笑象賞信臣成清静席積折節説戦浅選然倉巣争側束続卒孫帯隊達単置仲貯兆腸低停底的典伝徒努灯働堂得特毒熱念敗梅博飯費飛必標票不付夫府副粉兵別変辺便包法望牧末満未脈民無約勇要養浴利陸料良量輪類令例冷歴連労老録'),
    ('Grade 5', '圧易移因営永衛液益演往応恩仮価可河過賀解快格確額刊幹慣眼基寄規技義逆久旧居許境興均禁句群経潔件券検険減現限個故護効厚構耕講鉱混査再妻採災際在罪財桜雑賛酸師志支枝資飼似示識質舎謝授修術述準序承招証常情条状織職制勢性政精製税績責接設絶舌銭祖素総像増造則測属損態貸退団断築張提程敵適統導銅徳独任燃能破判版犯比肥非備俵評貧婦富布武復複仏編弁保墓報豊暴貿防務夢迷綿輸余預容率略留領'),
    ('Grade 6', '異遺域宇映延沿我灰拡閣革割株巻干看簡危揮机貴疑吸供胸郷勤筋敬系警劇激穴憲権絹厳源呼己誤后孝皇紅鋼降刻穀骨困砂座済裁策冊蚕姿私至視詞誌磁射捨尺若樹収宗就衆従縦縮熟純処署諸除傷将障城蒸針仁垂推寸盛聖誠宣専泉洗染善創奏層操窓装臓蔵存尊宅担探誕暖段値宙忠著庁潮頂賃痛展党糖討届難乳認納脳派俳拝背肺班晩否批秘腹奮並閉陛片補暮宝訪亡忘棒枚幕密盟模訳優郵幼欲翌乱卵覧裏律臨朗論'),
    ('JuniorHS', '亜哀握扱依偉威尉慰為維緯違井壱逸稲芋姻陰隠韻渦浦影詠鋭疫悦謁越閲宴援炎煙猿縁鉛汚凹奥押欧殴翁沖憶乙卸穏佳嫁寡暇架禍稼箇華菓蚊雅餓介塊壊怪悔懐戒拐皆劾慨概涯該垣嚇核殻獲穫較郭隔岳掛潟喝括渇滑褐轄且刈乾冠勘勧喚堪寛患憾換敢棺款歓汗環甘監緩缶肝艦貫還鑑閑陥含頑企奇岐幾忌既棋棄祈軌輝飢騎鬼偽儀宜戯擬欺犠菊吉喫詰却脚虐丘及朽窮糾巨拒拠虚距享凶叫峡恐恭挟況狂狭矯脅響驚仰凝暁斤琴緊菌襟謹吟駆愚虞偶遇隅屈掘靴繰桑勲薫傾刑啓契恵慶憩掲携渓継茎蛍鶏迎鯨撃傑倹兼剣圏堅嫌懸献肩謙賢軒遣顕幻弦玄孤弧枯誇雇顧鼓互呉娯御悟碁侯坑孔巧恒慌抗拘控攻更江洪溝甲硬稿絞綱肯荒衡貢購郊酵項香剛拷豪克酷獄腰込墾婚恨懇昆紺魂佐唆詐鎖債催宰彩栽歳砕斎載剤咲崎削搾索錯撮擦傘惨桟暫伺刺嗣施旨祉紫肢脂諮賜雌侍慈滋璽軸執湿漆疾芝赦斜煮遮蛇邪爵酌釈寂朱殊狩珠趣儒寿需囚愁秀臭舟襲酬醜充柔汁渋獣銃叔淑粛塾俊瞬准循旬殉潤盾巡遵庶緒叙徐償匠升召奨宵尚床彰抄掌昇晶沼渉焦症硝礁祥称粧紹肖衝訟詔詳鐘丈冗剰壌嬢浄畳譲醸錠嘱飾殖触辱伸侵唇娠寝審慎振浸紳薪診辛震刃尋甚尽迅陣酢吹帥炊睡粋衰遂酔随髄崇枢据杉澄瀬畝是姓征牲誓請逝斉隻惜斥析籍跡拙摂窃仙占扇栓潜旋繊薦践遷鮮漸禅繕塑措疎礎租粗訴阻僧双喪壮捜掃挿曹槽燥荘葬藻遭霜騒憎贈促即俗賊堕妥惰駄耐怠替泰滞胎袋逮滝卓択拓沢濯託濁諾但奪脱棚丹嘆淡端胆鍛壇弾恥痴稚致遅畜蓄逐秩窒嫡抽衷鋳駐弔彫徴懲挑眺聴超跳勅朕沈珍鎮陳津墜塚漬坪釣亭偵貞呈堤帝廷抵締艇訂逓邸泥摘滴哲徹撤迭添殿吐塗斗渡途奴怒倒凍唐塔悼搭桃棟盗痘筒到謄踏逃透陶騰闘洞胴峠匿督篤凸突屯豚曇鈍縄軟尼弐如尿妊忍寧猫粘悩濃把覇婆廃排杯輩培媒賠陪伯拍泊舶薄迫漠爆縛肌鉢髪伐罰抜閥伴帆搬畔繁般藩販範煩頒盤蛮卑妃彼扉披泌疲碑罷被避尾微匹姫漂描苗浜賓頻敏瓶怖扶敷普浮符腐膚譜賦赴附侮舞封伏幅覆払沸噴墳憤紛雰丙併塀幣弊柄壁癖偏遍舗捕穂募慕簿倣俸奉峰崩抱泡砲縫胞芳褒邦飽乏傍剖坊妨帽忙房某冒紡肪膨謀僕墨撲朴没堀奔翻凡盆摩磨魔麻埋膜又抹繭慢漫魅岬妙眠矛霧婿娘銘滅免茂妄猛盲網耗黙戻紋厄躍柳愉癒諭唯幽悠憂猶裕誘雄融与誉庸揚揺擁溶窯謡踊抑翼羅裸頼雷絡酪欄濫吏履痢離硫粒隆竜慮虜了僚寮涼猟療糧陵倫厘隣塁涙累励鈴隷零霊麗齢暦劣烈裂廉恋錬炉露廊楼浪漏郎賄惑枠湾腕'),
    ('New Jouyou', '挨宛闇椅畏萎茨咽淫臼唄餌怨艶旺岡臆俺苛牙崖蓋骸柿顎葛釜鎌瓦韓玩伎畿亀僅巾錦駒串窟熊稽詣隙桁拳鍵舷股虎乞勾喉梗頃痕沙挫塞采阪埼柵拶斬鹿叱嫉腫呪蹴拭尻芯腎須裾凄醒戚脊煎羨腺詮膳曽狙遡爽痩捉袖遜汰唾堆戴誰旦綻酎捗椎潰爪鶴諦溺填貼妬賭藤憧瞳栃頓奈那謎鍋匂虹捻罵剥箸斑氾汎眉膝肘媛阜蔽蔑蜂貌頬睦勃昧枕蜜冥麺餅冶弥湧妖沃嵐藍梨璃侶瞭瑠呂賂弄麓脇丼傲刹哺喩嗅嘲毀彙恣惧慄憬拉摯曖楷鬱璧瘍箋籠緻羞訃諧貪踪辣錮'),
    ('Jinmeiyou (regular)', '丑丞乃之乎也云亘亙些亦亥亨亮仔伊伍伽佃佑伶侃侑俄俠俣俐倭俱倦倖偲傭儲允兎兜其冴凌凜凛凧凪凰凱函劉劫勁勿匡廿卜卯卿厨厩叉叡叢叶只吾吞吻哉啄哩喬喧喰喋嘩嘉嘗噌噂圃圭坐尭堯坦埴堰堺堵塙塡壕壬夷奄奎套娃姪姥娩嬉孟宏宋宕宥寅寓寵尖尤屑峨峻崚嵯嵩嶺巌巖已巳巴巷巽帖幌幡庄庇庚庵廟廻弘弛彌彗彦彪彬徠忽怜恢恰恕悌惟惚悉惇惹惺惣慧憐戊或戟托按挺挽掬捲捷捺捧掠揃摑摺撒撰撞播撫擢孜敦斐斡斧斯於旭昂昊昏昌昴晏晃晄晒晋晟晦晨智暉暢曙曝曳曾朋朔杏杖杜李杭杵杷枇柑柴柘柊柏柾柚桧檜栞桔桂栖桐栗梧梓梢梛梯桶梶椛梁棲椋椀楯楚楕椿楠楓椰楢楊榎樺榊榛槙槇槍槌樫槻樟樋橘樽橙檎檀櫂櫛櫓欣欽歎此殆毅毘毬汀汝汐汲沌沓沫洸洲洵洛浩浬淵淳渚淀淋渥湘湊湛溢滉溜漱漕漣澪濡瀕灘灸灼烏焰焚煌煤煉熙燕燎燦燭燿爾牒牟牡牽犀狼猪獅玖珂珈珊珀玲琢琉瑛琥琶琵琳瑚瑞瑶瑳瓜瓢甥甫畠畢疋疏瘦皐皓眸瞥矩砦砥砧硯碓碗碩碧磐磯祇祢禰祐禄祿禎禱禽禾秦秤稀稔稟稜穣穰穿窄窪窺竣竪竺竿笈笹笙笠筈筑箕箔篇篠簞簾籾粥粟糊紘紗紐絃紬絆絢綺綜綴緋綾綸縞徽繫繡纂纏羚翔翠耀而耶耽聡肇肋肴胤胡脩腔膏臥舜舵芥芹芭芙芦苑茄苔苺茅茉茸茜莞荻莫莉菅菫菖萄菩萌萠萊菱葦葵萱葺萩董葡蓑蒔蒐蒼蒲蒙蓉蓮蔭蔣蔦蓬蔓蕎蕨蕉蕃蕪薙蕾蕗藁薩蘇蘭蝦蝶螺蟬蟹蠟衿袈袴裡裟裳襖訊訣註詢詫誼諏諄諒謂諺讃豹貰賑赳跨蹄蹟輔輯輿轟辰辻迂迄辿迪迦這逞逗逢遥遙遁遼邑祁郁鄭酉醇醐醍醬釉釘釧鋒鋸錐錆錫鍬鎧閃閏閤阿陀隈隼雀雁雛雫霞靖鞄鞍鞘鞠鞭頁頌頗頰顚颯饗馨馴馳駕駿驍魁魯鮎鯉鯛鰯鱒鱗鳩鳶鳳鴨鴻鵜鵬鷗鷲鷺鷹麒麟麿黎黛鼎'),
    ('Jinmeiyou (variant)', '亞惡爲衞谒緣應櫻奧橫溫價祸壞懷樂渴卷陷寬氣僞戲虛峽狹曉勳薰惠揭鷄藝擊縣儉劍險圈檢顯驗嚴廣恆黃國黑碎雜兒濕壽收從澁獸縱緖敍將涉燒獎條狀乘淨剩疊孃讓釀眞寢愼盡粹醉穗瀨齊靜攝專戰纖禪壯爭莊搜巢裝騷增藏臟卽帶滯單團彈晝鑄廳徵聽鎭轉傳燈盜稻德拜賣髮拔晚祕拂佛步飜每默藥與搖樣謠來賴覽龍綠淚壘曆歷鍊郞錄')
    ]
_css = "body { background: #ccc url(/img/noise.png); }" + \
    ".info-wrapper { height: auto; width: 500px; margin: 4em auto; padding: 0 0 2em 0; position: relative; }" + \
    ".info { max-height: 120px; height: auto; padding: .5em 0; border-bottom: solid 1px #fff; border-radius: 0 0 1em 1em;" + \
    "	overflow: hidden; position: relative; transition: 1s; } p { margin: 1em; }" + \
    ".info:after, .aftershadow { bottom: 0; width: 100%; height: 3em; border-radius: 0 0 1em 1em; position: absolute;" + \
    "	background: linear-gradient(rgba(192,192,192,0), #ccc); content: ''; }" + \
    ".aftershadow { filter: progid:DXImageTransform.Microsoft.gradient(startColorstr=#00cccccc, endColorstr=#ffcccccc); }" + \
    ".info-wrapper input[type=checkbox] { display: none; } .info-wrapper label { left: 50%; bottom: 1.5em; width: 9em;" + \
    "	height: 1.25em; margin:  0 0 0 -4.5em; border-bottom: solid 1px #fff; border-radius: 0 0 1em 1em; overflow: hidden;" + \
    "	position: absolute; font: 700 .67em/1.25em Arial; text-align: center; text-shadow: 0 1px 0 #fff; cursor: pointer; }" + \
    ".info-wrapper label .more { margin: -.1em 0 .35em; transition: 1s; } .info-wrapper .switch { width: 4em; display: inline-block; }" + \
    ".info-wrapper input[type=checkbox]:checked ~ .info { max-height: 15em; } .info-wrapper input[type=checkbox]:checked + label .more { margin-top: -1.65em; }"

class TestedUnit:
    def __init__(self, value):
        self.idx = 0
        self.value = value
        self.avg_interval = 0.0
        self.due = 0.0
        self.odue = 0.0
        self.count = 0
        self.mod = 0

    def addDataFromCard(self, idx, card, timeNow):
        if card.type > 0:
            newTotal = (self.avg_interval * self.count) + card.ivl

            self.count += 1
            self.avg_interval = newTotal / self.count
        if card.type == 2:
            if card.due < self.due or self.due == 0:
                self.due = card.due

            if card.odue < self.odue or self.odue == 0:
                self.odue = card.odue
                self.mod = self.odue

        if idx < self.idx or self.idx == 0:
            self.idx = idx

def isKanji(unichar):
    try:
        return unicodedata.name(unichar).find('CJK UNIFIED IDEOGRAPH') >= 0
    except ValueError:
        # a control character
        return False

def scoreAdjust(score):
    score += 1
    return 1 - 1 / (score * score)

def addUnitData(units, unitKey, i, card, timeNow):
    validKey = _ignore.find(unitKey) == -1 and (not _kanjionly or isKanji(unitKey))
    if validKey:
        if unitKey not in units:
            unit = TestedUnit(unitKey)
            units[unitKey] = unit

        units[unitKey].addDataFromCard(i, card, timeNow)

def hsvrgbstr(h, s=0.8, v=0.9):
    _256 = lambda x: round(x*256)
    i = int(h*6.0)
    f = (h*6.0) - i
    p = v*(1.0 - s)
    q = v*(1.0 - s*f)
    t = v*(1.0 - s*(1.0-f))
    i = i%6
    if i == 0: return "#%0.2X%0.2X%0.2X" % (_256(v),_256(t),_256(p))
    if i == 1: return "#%0.2X%0.2X%0.2X" % (_256(q),_256(v),_256(p))
    if i == 2: return "#%0.2X%0.2X%0.2X" % (_256(p),_256(v),_256(t))
    if i == 3: return "#%0.2X%0.2X%0.2X" % (_256(p),_256(q),_256(v))
    if i == 4: return "#%0.2X%0.2X%0.2X" % (_256(t),_256(p),_256(v))
    if i == 5: return "#%0.2X%0.2X%0.2X" % (_256(v),_256(p),_256(q))

class KanjiGrid:
    def __init__(self, mw):
        if mw:
            self.menuAction = QAction("Generate Kanji Grid", mw, triggered=self.setup)
            mw.form.menuTools.addSeparator()
            mw.form.menuTools.addAction(self.menuAction)

    def generate(self, units, timeNow, saveMode=False):
        deckname = mw.col.decks.name(self.did).rsplit('::',1)[-1]
        if saveMode: cols = _wide
        else: cols = _thin
        self.html  = "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"/>\n"
        self.html += "<html><head><title>Anki Kanji Grid</title></head><body bgcolor=\"#FFF\">\n"
        self.html += "<span style=\"font-size: 3em;color: #888;\">Kanji Grid - %s</span><br>\n" % deckname
        self.html += "<div style=\"margin-bottom: 24pt;padding: 20pt;\"><p style=\"float: left\">Key:</p>"
        self.html += "<style type=\"text/css\">.key{display:inline-block;width:3em}a,a:visited{color:#000;text-decoration:none;}</style>"
        self.html += "<p style=\"float: right\">Weak&nbsp;"
        for c in [n/6.0 for n in range(6+1)]:
            self.html += "<span class=\"key\" style=\"background-color: %s;\">&nbsp;</span>" % hsvrgbstr(c/2)
        self.html += "&nbsp;Strong</p></div>\n"
        self.html += "<div style=\"clear: both;\"><br><hr style=\"border-style: dashed;border-color: #666;width: 60%;\"><br></div>\n"
        self.html += "<center>\n"
        if _group == 4:
            gc = 0
            kanji = list([u.value for u in units.values()])
            for i in range(1,len(_grades)):
                self.html += "<h2 style=\"color:#888;\">%s Kanji</h2>\n" % _grades[i][0]
                table = "<table width='85%'><tr>\n"
                count = -1
                for unit in [units[c] for c in _grades[i][1] if c in kanji]:
                    if unit.count != 0 or _unseen:
                        score = "NaN"
                        count += 1
                        if count % cols == 0 and count != 0: table += "</tr>\n<tr>\n"
                        if unit.count != 0: bgcolour = hsvrgbstr(scoreAdjust(unit.avg_interval / _interval)/2)
                        else: bgcolour = "#FFF"
                        if _tooltips:
                            tooltip  = "Character: %s | Count: %s | " % (unicodedata.name(unit.value), unit.count)
                            tooltip += "Avg Interval: %s | Score: %s | " % (unit.avg_interval, score)
                            tooltip += "Background: %s | Index: %s" % (bgcolour, count)
                            table += "\t<td align=center valign=top style=\"background:%s;\" title=\"%s\">" % (bgcolour, tooltip)
                        else: table += "\t<td align=center valign=top style=\"background:%s;\">" % (bgcolour)
                        table += "<a href=\"http://www.csse.monash.edu.au/~jwb/cgi-bin/wwwjdic.cgi?1MMJ%s\">%s</a></td>\n" % (2*(unit.value,))
                table += "</tr></table>\n"
                n = count+1
                t = len(_grades[i][1])
                gc += n
                if _unseen:
                    table += "<details><summary>Missing kanji</summary><table style=\"max-width:75%;\"><tr>\n"
                    count = -1
                    for char in [c for c in _grades[i][1] if c not in kanji]:
                        score = "NaN"
                        count += 1
                        if count % cols == 0: table += "</tr>\n<tr>\n"
                        if _tooltips:
                            tooltip  = "Character: %s" % (unicodedata.name(char))
                            table += "\t<td align=center valign=top style=\"background:#EEE;color:#FFF;\" title=\"%s\">" % (tooltip)
                        else: table += "\t<td align=center valign=top style=\"background:#EEE;color:#FFF;\">"
                        table += "<a href=\"http://www.csse.monash.edu.au/~jwb/cgi-bin/wwwjdic.cgi?1MMJ%s\" style=\"color:#888;\">%s</a></td>\n" % (2*(char,))
                    if count == -1: table += "<strong style=\"color:#CCC\">None</strong>"
                    table += "</tr></table></details>\n"
                self.html += "<h4 style=\"color:#888;\">%d of %d - %0.2f%%</h4>\n" % (n, t, n*100.0/t)
                self.html += table

            chars = reduce(lambda x,y: x+y, dict(_grades).values())
            self.html += "<h2 style=\"color:#888;\">%s Kanji</h2>" % _grades[0][0]
            table = "<table width='85%'><tr>\n"
            count = -1
            for unit in [u for u in units.values() if u.value not in chars]:
                if unit.count != 0 or _unseen:
                    score = "NaN"
                    count += 1
                    if count % cols == 0 and count != 0: table += "</tr>\n<tr>\n"
                    if unit.count != 0: bgcolour = hsvrgbstr(scoreAdjust(unit.avg_interval / _interval)/2)
                    else: bgcolour = "#FFF"
                    if _tooltips:
                        tooltip  = "Character: %s | Count: %s | " % (unicodedata.name(unit.value), unit.count)
                        tooltip += "Avg Interval: %s | Score: %s | " % (unit.avg_interval, score)
                        tooltip += "Background: %s | Index: %s" % (bgcolour, count)
                        table += "\t<td align=center valign=top style=\"background:%s;\" title=\"%s\">" % (bgcolour, tooltip)
                    else: table += "\t<td align=center valign=top style=\"background:%s;\">" % (bgcolour)
                    table += "<a href=\"http://www.csse.monash.edu.au/~jwb/cgi-bin/wwwjdic.cgi?1MMJ%s\">%s</a></td>\n" % (2*(unit.value,))
            table += "</tr></table>\n"
            n = count+1
            self.html += "<h4 style=\"color:#888;\">%d of %d - %0.2f%%</h4>\n" % (n, gc, n*100.0/gc)
            self.html += table
        else:
            table = "<table width='85%'><tr>\n"
            if _group == 0: # Order found
                unitsList = sorted( units.values(), key=lambda unit: (unit.idx, unit.count) )
            if _group == 1: # Unicode index
                unitsList = sorted( units.values(), key=lambda unit: (unicodedata.name(unit.value), unit.count) )
            if _group == 2: # Character score
                unitsList = sorted( units.values(), key=lambda unit: (scoreAdjust(unit.avg_interval / _interval), unit.count), reverse=True)
            if _group == 3: # Deck frequency
                unitsList = sorted( units.values(), key=lambda unit: (unit.count, scoreAdjust(unit.avg_interval / _interval)), reverse=True)
            count = -1
            for unit in unitsList:
                if unit.count != 0 or _unseen:
                    score = "NaN"
                    count += 1
                    if count % cols == 0 and count != 0: table += "</tr>\n<tr>\n"
                    if unit.count != 0: bgcolour = hsvrgbstr(scoreAdjust(unit.avg_interval / _interval)/2)
                    else: bgcolour = "#FFF"
                    if _tooltips:
                        tooltip  = "Character: %s | Count: %s | " % (unicodedata.name(unit.value), unit.count)
                        tooltip += "Avg Interval: %s | Score: %s | " % (unit.avg_interval, score)
                        tooltip += "Background: %s | Index: %s" % (bgcolour, count)
                        table += "\t<td align=center valign=top style=\"background:%s;\" title=\"%s\">" % (bgcolour, tooltip)
                    else: table += "\t<td align=center valign=top style=\"background:%s;\">" % (bgcolour)
                    table += "<a href=\"http://www.csse.monash.edu.au/~jwb/cgi-bin/wwwjdic.cgi?1MMJ%s\">%s</a></td>\n" % (2*(unit.value,))
            table += "</tr></table>\n"
            self.html += "<h4 style=\"color:#888;\">%d total unique kanji</h4>\n" % (count+1)
            self.html += table
        self.html += "</center></body></html>\n"

    def displaygrid(self, units, timeNow):
        self.generate(units, timeNow)
        #print("%s: %0.3f" % ("HTML generated",time.time()-_time))
        self.win = QDialog(mw)
        self.wv = AnkiWebView()
        vl = QVBoxLayout()
        vl.setContentsMargins(0, 0, 0, 0)
        vl.addWidget(self.wv)
        self.wv.stdHtml(self.html)
        hl = QHBoxLayout()
        vl.addLayout(hl)
        sh = QPushButton("Save HTML", clicked=self.savehtml)
        hl.addWidget(sh)
        sp = QPushButton("Save Image", clicked=self.savepng)
        hl.addWidget(sp)
        bb = QPushButton("Close", clicked=self.win.reject)
        hl.addWidget(bb)
        self.win.setLayout(vl)
        self.win.resize(500, 400)
        #print("%s: %0.3f" % ("Window complete",time.time()-_time))
        return 0

    def savehtml(self):
        fileName = QFileDialog.getSaveFileName(self.win, "Save Page", QStandardPaths.standardLocations(QStandardPaths.DesktopLocation)[0], "Web Page (*.html *.htm)")[0]
        if fileName != "":
            mw.progress.start(immediate=True)
            if not ".htm" in fileName:
                fileName += ".html"
            fileOut = codecs.open(fileName, 'w', 'utf-8')
            (units, timeNow) = self.kanjigrid()
            self.generate(units, timeNow, True)
            fileOut.write(self.html)
            fileOut.close()
            mw.progress.finish()
            showInfo("Page saved to %s!" % os.path.abspath(fileOut.name))
        return
    
    def savepng(self):
        fileName = QFileDialog.getSaveFileName(self.win, "Save Page", QStandardPaths.standardLocations(QStandardPaths.DesktopLocation)[0], "Portable Network Graphics (*.png)")[0]
        if fileName != "":
            mw.progress.start(immediate=True)
            if not ".png" in fileName:
                fileName += ".png"
            p = self.wv.page()
            oldsize = p.viewportSize()
            p.setViewportSize(p.mainFrame().contentsSize())
            image = QImage(p.viewportSize(), QImage.Format_ARGB32)
            painter = QPainter(image)
            p.mainFrame().render(painter)
            painter.end()
            image.save(fileName, "png")
            p.setViewportSize(oldsize)
            mw.progress.finish()
            showInfo("Image saved to %s!" % os.path.abspath(fileName))
        return

    def kanjigrid(self):
        self.did = mw.col.conf['curDeck']

        dids = [self.did]
        for name, id in mw.col.decks.children(self.did):
            dids.append(id)
        #print("%s: %0.3f" % ("Decks selected",time.time()-_time))
        cids = mw.col.db.list("select id from cards where did in %s or odid in %s" % (ids2str(dids),ids2str(dids)))
        #print("%s: %0.3f" % ("Cards selected",time.time()-_time))

        units = dict()
        notes = dict()
        timeNow = time.time()
        for id,i in enumerate(cids):
            card = mw.col.getCard(i)
            if card.nid not in notes.keys():
                keys = card.note().keys()
                unitKey = None
                if _literal:
                    for s,key in ((key.lower(),key) for key in keys):
                        if _pattern == s.lower():
                            unitKey = card.note()[key]
                            break
                else:
                    for s,key in ((key.lower(),key) for key in keys):
                        if _pattern in s.lower():
                            unitKey = card.note()[key]
                            break
                notes[card.nid] = unitKey
            else:
                unitKey = notes[card.nid]
            if unitKey != None:
                for ch in unitKey:
                    addUnitData(units, ch, i, card, timeNow)
        #print("%s: %0.3f" % ("Units created",time.time()-_time))
        return units,timeNow

    def makegrid(self):
        #global _time
        #_time = time.time()
        #print("%s: %0.3f" % ("Start",time.time()-_time))
        (units, timeNow) = self.kanjigrid()
        if units is not None:
            self.displaygrid(units, timeNow)

    def setup(self):
        global _pattern, _literal
        global _interval, _thin, _wide
        global _group, _unseen, _tooltips
        swin = QDialog(mw)
        vl = QVBoxLayout()
        frm = QGroupBox("Settings")
        vl.addWidget(frm)
        il = QVBoxLayout()
        fl = QHBoxLayout()
        field = QLineEdit()
        field.setPlaceholderText("e.g. \"kanji\" or \"sentence-kanji\" (default: \"kanji\")")
        il.addWidget(QLabel("Pattern or Field name to search for (first used, case insensitive):"))
        fl.addWidget(field)
        liter = QCheckBox("Match exactly")
        liter.setChecked(_literal)
        fl.addWidget(liter)
        il.addLayout(fl)
        stint = QSpinBox()
        stint.setRange(1,65536)
        stint.setValue(_interval)
        il.addWidget(QLabel("Card interval considered strong:"))
        il.addWidget(stint)
        ttcol = QSpinBox()
        ttcol.setRange(1,99)
        ttcol.setValue(_thin)
        il.addWidget(QLabel("Number of Columns in the in-app table:"))
        il.addWidget(ttcol)
        wtcol = QSpinBox()
        wtcol.setRange(1,99)
        wtcol.setValue(_wide)
        il.addWidget(QLabel("Number of Columns in the exported table:"))
        il.addWidget(wtcol)
        group = QComboBox()
        group.addItems(["None, sorted by order found",
                        "None, sorted by unicode order",
                        "None, sorted by score",
                        "None, sorted by frequency",
                        "JLPT Grade"])
        group.setCurrentIndex(_group)
        il.addWidget(QLabel("Group by:"))
        il.addWidget(group)
        shnew = QCheckBox("Show units not yet seen")
        shnew.setChecked(_unseen)
        il.addWidget(shnew)
        toolt = QCheckBox("Show informational tooltips")
        toolt.setChecked(_tooltips)
        il.addWidget(toolt)
        frm.setLayout(il)
        hl = QHBoxLayout()
        vl.addLayout(hl)
        gen = QPushButton("Generate", clicked=swin.accept)
        hl.addWidget(gen)
        cls = QPushButton("Close", clicked=swin.reject)
        hl.addWidget(cls)
        swin.setLayout(vl)
        swin.setTabOrder(gen,cls)
        swin.setTabOrder(cls,field)
        swin.setTabOrder(field,liter)
        swin.setTabOrder(liter,stint)
        swin.setTabOrder(stint,ttcol)
        swin.setTabOrder(ttcol,wtcol)
        swin.setTabOrder(wtcol,group)
        swin.setTabOrder(group,shnew)
        swin.setTabOrder(shnew,toolt)
        swin.resize(500, 400)
        if swin.exec_():
            mw.progress.start(immediate=True)
            if len(field.text().strip()) != 0: _pattern = field.text().lower()
            _literal = liter.isChecked()
            _interval = stint.value()
            _thin = ttcol.value()
            _wide = wtcol.value()
            _group = group.currentIndex()
            _unseen = shnew.isChecked()
            _tooltips = toolt.isChecked()
            self.makegrid()
            mw.progress.finish()
            self.win.show()

if __name__ != "__main__":
    # Save a reference to the toolkit onto the mw, preventing garbage collection of PyQT objects
    if mw: mw.kanjigrid = KanjiGrid(mw)
else:
    print("This is a plugin for the Anki Spaced Repition learning system and cannot be run directly.")
    print("Please download Anki2 from <http://ankisrs.net/>")

# vim:expandtab:

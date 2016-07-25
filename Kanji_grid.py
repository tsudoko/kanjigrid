#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Contact: frony0@gmail.com

import time, os, unicodedata, operator
from functools import reduce

from anki.utils import ids2str
from aqt import mw
from aqt.utils import showInfo
from aqt.webview import AnkiWebView
from aqt.qt import QAction, QStandardPaths, \
                   QImage, QPainter, \
                   QFileDialog, QDialog, QHBoxLayout, QVBoxLayout, QGroupBox, \
                   QLineEdit, QLabel, QCheckBox, QSpinBox, QComboBox, QPushButton

#_time = None
_pattern = "kanji"
_literal = False
_interval = 180
_thin = 20
_wide = 48
_groupby = 0
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
_kanken = [ ('Probably Chinese', ''),
    ('Level 10', '一右雨円王音下火花貝学気休玉金九空月犬見五口校左三山四子糸字耳七車手十出女小上森人水正生青石赤先千川早草足村大男竹中虫町天田土二日入年白八百文本名木目夕立力林六'),
    ('Level 9', '引羽雲園遠黄何夏家科歌画会回海絵外角楽活間丸岩顔帰汽記弓牛魚京強教近兄形計元原言古戸午後語交光公工広考行高合国黒今才細作算姉市思止紙寺時自室社弱首秋週春書少場色食心新親図数星晴声西切雪線船前組走多太体台谷知地池茶昼朝長鳥直通弟店点電冬刀東当答頭同道読内南肉馬買売麦半番父風分聞米歩母方北妹毎万明鳴毛門夜野矢友曜用来理里話'),
    ('Level 8', '悪安暗委意医育員飲院運泳駅央横屋温化荷界開階寒感漢館岸期起客宮急球究級去橋業局曲銀区苦具君係軽決血研県庫湖向幸港号根祭坂皿仕使始指死詩歯事持次式実写者主取守酒受州拾終習集住重宿所暑助勝商昭消章乗植深申真神身進世整昔全想相送息速族他打対待代第題炭短談着柱注丁帳調追定庭笛鉄転登都度島投湯等豆動童農波配倍箱畑発反板悲皮美鼻筆氷表病秒品負部服福物平返勉放味命面問役薬油有由遊予様洋羊葉陽落流旅両緑礼列練路和'),
    ('Level 7', '愛案以位囲胃衣印栄英塩億加果課貨芽改械害街各覚完官管観関願喜器希旗機季紀議救求泣給挙漁競共協鏡極訓軍郡型径景芸欠結健建験固候功好康航告差最菜材昨刷察札殺参散産残司史士氏試児治辞失借種周祝順初唱松焼照省笑象賞信臣成清静席積折節説戦浅選然倉巣争側束続卒孫帯隊達単置仲貯兆腸低停底的典伝徒努灯働堂得特毒熱念敗梅博飯費飛必標票不付夫府副粉兵別変辺便包法望牧末満未脈民無約勇要養浴利陸料良量輪類令例冷歴連労老録'),
    ('Level 6', '圧易移因営永衛液益演往応恩仮価可河過賀解快格確額刊幹慣眼基寄規技義逆久旧居許境興均禁句群経潔件券検険減現限個故護効厚構耕講鉱混査再妻採災際在罪財桜雑賛酸師志支枝資飼似示識質舎謝授修術述準序承招証常情条状織職制勢性政精製税績責接設絶舌銭祖素総像増造則測属損態貸退団断築張提程敵適統導銅徳独任燃能破判版犯比肥非備俵評貧婦富布武復複仏編弁保墓報豊暴貿防務夢迷綿輸余預容率略留領'),
    ('Level 5', '異遺域宇映延沿我灰拡閣革割株巻干看簡危揮机貴疑吸供胸郷勤筋敬系警劇激穴憲権絹厳源呼己誤后孝皇紅鋼降刻穀骨困砂座済裁策冊蚕姿私至視詞誌磁射捨尺若樹収宗就衆従縦縮熟純処署諸除傷将障城蒸針仁垂推寸盛聖誠宣専泉洗染善創奏層操窓装臓蔵存尊宅担探誕暖段値宙忠著庁潮頂賃痛展党糖討届難乳認納脳派俳拝背肺班晩否批秘腹奮並閉陛片補暮宝訪亡忘棒枚幕密盟模訳優郵幼欲翌乱卵覧裏律臨朗論'),
    ('Level 4', '握扱依偉威為維緯違井壱稲芋陰隠影鋭越援煙縁鉛汚奥押沖憶暇箇菓雅介壊戒皆獲較刈乾勧歓汗環甘監鑑含奇幾祈輝鬼儀戯詰却脚丘及朽巨拠距凶叫恐況狂狭響驚仰駆屈掘繰傾恵継迎撃兼剣圏堅肩軒遣玄枯誇鼓互御恒抗攻更稿荒項香豪腰込婚鎖彩歳載剤咲惨伺刺旨紫脂雌執芝斜煮釈寂朱狩趣需秀舟襲柔獣瞬旬盾巡召床沼称紹詳丈畳飾殖触侵寝慎振浸薪震尋尽陣吹澄是姓征跡占扇鮮訴僧燥騒贈即俗耐替拓沢濁脱丹嘆淡端弾恥致遅蓄徴跳沈珍堤抵摘滴添殿吐渡途奴怒倒唐塔桃盗到踏逃透闘胴峠突曇鈍弐悩濃杯輩拍泊薄迫爆髪罰抜搬繁般販範盤彼疲被避尾微匹描浜敏怖敷普浮腐膚賦舞幅払噴柄壁舗捕峰抱砲傍坊帽忙冒肪凡盆慢漫妙眠矛霧娘茂猛網黙紋躍雄与誉溶謡踊翼頼雷絡欄離粒慮療隣涙隷麗齢暦劣烈恋露郎惑腕'),
    ('Level 3', '哀慰詠悦閲宴炎欧殴乙卸穏佳嫁架華餓塊怪悔慨概該穫郭隔岳掛滑冠勘喚換敢緩肝貫企岐忌既棋棄軌騎欺犠菊吉喫虐虚峡脅凝斤緊愚偶遇桑刑啓契憩掲携鶏鯨倹賢幻孤弧雇顧娯悟坑孔巧慌拘控甲硬絞綱郊酵克獄墾恨紺魂債催削搾錯撮擦暫施祉諮侍慈軸湿疾赦邪殊寿潤遵徐匠掌昇晶焦衝鐘冗嬢譲錠嘱辱伸審辛炊粋衰遂酔随髄瀬牲請隻惜斥籍摂潜繕措礎粗阻双掃葬遭憎促賊怠滞胎袋逮滝卓択託諾奪胆鍛壇稚畜窒抽鋳駐彫聴超鎮陳墜帝締訂哲塗斗凍痘陶匿篤豚如尿粘婆排陪縛伐伴帆畔藩蛮卑泌碑姫漂苗符赴封伏覆墳紛癖穂募慕簿倣奉崩縫胞芳邦飽乏妨房某膨謀墨没翻魔埋膜又魅婿滅免幽憂誘揚揺擁抑裸濫吏隆了猟糧陵厘励零霊裂廉錬炉廊楼浪漏湾'),
    ('Level Pre-2', '亜尉逸姻韻渦浦疫謁猿凹翁寡禍稼蚊懐拐劾涯垣嚇核殻潟喝括渇褐轄且堪寛患憾棺款缶艦還閑陥頑飢偽宜擬窮糾拒享恭挟矯暁琴菌襟謹吟虞隅靴勲薫慶渓茎蛍傑嫌懸献謙顕弦呉碁侯江洪溝肯衡貢購剛拷酷懇昆佐唆詐宰栽砕斎崎索傘桟嗣肢賜滋璽漆遮蛇爵酌珠儒囚愁臭酬醜充汁渋銃叔淑粛塾俊准循殉庶緒叙償升奨宵尚彰抄渉症硝礁祥粧肖訟詔剰壌浄醸唇娠紳診刃甚迅酢帥睡崇枢据杉畝誓逝斉析拙窃仙栓旋繊薦践遷漸禅塑疎租喪壮捜挿曹槽荘藻霜堕妥惰駄泰濯但棚痴逐秩嫡衷弔懲挑眺勅朕津塚漬坪釣亭偵貞呈廷艇逓邸泥徹撤迭悼搭棟筒謄騰洞督凸屯縄軟尼妊忍寧猫把覇廃培媒賠伯舶漠肌鉢閥煩頒妃扉披罷賓頻瓶扶譜附侮沸憤雰丙併塀幣弊偏遍俸泡褒剖紡僕撲朴堀奔摩磨麻抹繭岬銘妄盲耗戻厄柳愉癒諭唯悠猶裕融庸窯羅酪履痢硫竜虜僚寮涼倫塁累鈴賄枠'),
    ('Level 2', '挨宛闇椅畏萎茨咽淫臼唄餌怨艶旺岡臆俺苛牙崖蓋骸柿顎葛釜鎌瓦韓玩伎畿亀僅巾錦駒串窟熊稽詣隙桁拳鍵舷股虎乞勾喉梗頃痕沙挫塞采阪埼柵拶斬鹿叱嫉腫呪蹴拭尻芯腎須裾凄醒戚脊煎羨腺詮膳曽狙遡爽痩捉袖遜汰唾堆戴誰旦綻酎捗椎潰爪鶴諦溺填貼妬賭藤憧瞳栃頓奈那謎鍋匂虹捻罵剥箸斑氾汎眉膝肘媛阜蔽蔑蜂貌頬睦勃昧枕蜜冥麺餅冶弥湧妖沃嵐藍梨璃侶瞭瑠呂賂弄麓脇丼傲刹哺喩嗅嘲毀彙恣惧慄憬拉摯曖楷鬱璧瘍箋籠緻羞訃諧貪踪辣錮'),
    ('Level Pre-1', '唖娃阿姶逢葵茜穐渥旭葦鯵梓斡姐虻飴絢綾鮎或粟袷庵按鞍杏伊夷惟謂亥郁磯溢鰯允胤蔭吋烏迂卯鵜窺丑碓嘘欝蔚鰻姥厩瓜閏噂云荏叡嬰曳洩瑛盈穎頴榎厭堰奄掩焔燕苑薗鴛於甥襖鴬鴎荻桶牡伽嘉珂禾茄蝦嘩迦霞俄峨臥蛾駕廻恢魁晦芥蟹凱咳碍鎧浬馨蛙蛎鈎劃廓撹赫笠樫橿梶鰍恰鰹叶椛樺鞄兜竃蒲噛鴨茅萱粥苅侃姦柑桓澗潅竿翰莞諌舘巌癌翫贋雁嬉毅稀徽妓祇蟻誼掬鞠吃桔橘砧杵黍仇汲灸笈渠鋸禦亨侠僑兇匡卿喬彊怯蕎饗尭桐粁欣欽禽芹衿倶狗玖矩躯駈喰寓櫛釧屑沓轡窪隈粂栗鍬卦袈祁圭珪慧桂畦繋罫荊頚戟訣倦喧捲牽硯鹸絃諺乎姑狐糊袴胡菰跨鈷伍吾梧檎瑚醐鯉佼倖垢宏巷庚弘昂晃杭浩糠紘肱腔膏砿閤鴻劫壕濠轟麹鵠漉甑忽惚狛此坤昏梱艮些叉嵯瑳裟坐哉犀砦冴堺榊肴鷺朔窄鮭笹匙薩皐鯖捌錆鮫晒撒燦珊纂讃餐仔屍孜斯獅爾痔而蒔汐鴫竺宍雫悉蔀篠偲柴屡蕊縞紗勺杓灼錫惹綬洲繍蒐輯酋什戎夙峻竣舜駿楯淳醇曙渚薯藷恕鋤哨嘗妾娼庄廠捷昌梢樟樵湘菖蒋蕉裳醤鉦鍾鞘丞擾杖穣埴燭蝕晋榛疹秦塵壬訊靭笥諏厨逗翠錐錘瑞嵩趨雛椙菅頗雀摺棲栖脆蹟碩蝉尖撰栴煽穿箭舛賎銑閃糎噌岨曾楚疏蘇鼠叢宋匝惣掻槍漕糟綜聡蒼鎗其揃詑柁舵楕陀騨岱腿苔黛鯛醍鷹啄托琢鐸茸凧蛸只叩辰巽竪辿狸鱈樽坦歎湛箪耽蛋檀弛智蜘馳筑註樗瀦猪苧凋喋寵帖暢牒脹蝶諜銚槌鎚栂掴槻佃柘辻蔦綴鍔椿壷嬬紬吊剃悌挺梯汀碇禎蹄鄭釘鼎擢鏑轍纏甜顛澱兎堵杜菟鍍砥砺塘套宕嶋梼淘涛祷董蕩鐙撞萄鴇涜禿橡椴鳶苫寅酉瀞噸惇敦沌遁呑乍凪薙灘捺楢馴畷楠汝賑廿韮濡禰祢葱撚乃廼之埜嚢膿覗蚤巴播杷琶芭盃牌楳煤狽這蝿秤矧萩柏箔粕曝莫駁函硲肇筈幡畠溌醗筏鳩噺塙蛤隼叛挽磐蕃匪庇斐緋誹樋簸枇毘琵柊稗疋髭彦菱弼畢逼桧紐謬彪瓢豹廟錨鋲蒜蛭鰭彬斌瀕埠斧芙撫葡蕪楓葺蕗淵弗鮒吻扮焚糞頁僻碧瞥箆篇娩鞭鋪圃甫輔戊菩呆峯庖捧朋烹萌蓬鋒鳳鵬鉾吠卜穆釦殆幌哩槙鮪柾鱒亦俣沫迄麿蔓巳箕湊蓑稔粍牟鵡椋姪牝棉緬摸孟蒙儲杢勿尤籾貰悶匁也爺耶靖薮鑓愈佑宥揖柚涌猷祐邑輿傭楊熔耀蓉遥慾淀螺莱洛蘭李裡葎掠劉溜琉亮凌梁稜諒遼淋燐琳鱗麟伶嶺怜玲苓憐漣煉簾聯蓮魯櫓婁牢狼篭聾蝋禄肋倭歪鷲亙亘鰐詫藁蕨椀碗儘兔凰凾厰咒壺峩崕嵳廐廏廚攪檜檮橢濤渕溯漑灌潴皋礦礪龝竈篦纒翆聨苒莵萠葢蘂蕋藪蠣蛛蠅蠏諫讚豎賤迺鉤鎔靱韃韭頸鰺鴈鴦鶯鸚麒麪'),
    ('Level 1', '芦讐屠櫨桝榔弌丐丕丱乂乖舒弍于亟亢亶仍仄仆仂仗仞仭仟价伉佚估佝佗佇佶侈侏侘佻佩佰侑佯侖俔俟俎俘俛俑俚俐俤俥倚倨倔倪倥倅伜俶倡倩倬俾俯們倆偃偕偐偈做偖偬偸傀傚傅傴僉僊僂僖僥僭僣僮僵儁儂儕儔儚儡儺儷儼儻兀兌兢兪冀冉冏冑冓冕冤冢冪冱冽凅凛几凩凭刋刔刎刪刮刳剏剄剋剌剞剔剪剴剳剿剽劈劬劭劼勁勍勗勣勦飭勠匆匈甸匍匐匏匕匚匣匯匱匳卅丗卉卍卮卻厖厥簒叟曼燮叮叨叭叺吁吽听吭吼吮吶吩吝呎咏呵咎呟呱呷呰呻咀呶咄咐咆哇咢咸咥咬哄哈咨咫哂咤哥哦唏唔哽哮哭哢唹啀啣售啜啅啖啗唸唳喙喀喊喟啻啾喘喞啼喃喇喨嗚嗟嗄嗜嗤嗔嘔嗷嘖嗾嗽嘛噎嘴嘶嘸噫噤嘯噬噪嚆嚀嚊嚠嚔嚏嚥嚮嚶囂嚼囁囃囀囈囓囮囹圀囿圄圉嗇圜圦坎圻址坏坩坡坿垓垠垤埃埆埒堊堋堙堝堡塋塒堽塹墅墟壅壑壙壜壟壼夐夥夬夭夲夸夾奕奐奎奚奘奢奠奸妁妝佞妣妲姆姨姜妍姙姚娥娟娑娜娉婀婬婉娵娶婢婪媚媼媾嫋嫂媽嫣嫗嫦嫩嫖嫺嫻嬌嬋嬖嬲嬪嬶嬾孅孀孑孕孚孛孥孩孰孳孵孺宦宸寇寔寐寤寞寥寰尠尨尸尹屁屎屓屏孱屮屶屹岌岑岔岫峙峭峪崟崛崑崔崢崚崙崘嵌嵒嵎嵋嵬嶇嶄嶂嶢嶝嶬嶮嶷嶼巉巍巓巒巫已帚帙帑帛帷幄幃幀幎幗幔幟幢幇幵并幺麼庠廁廂廈廖廝廛廡廨廩廬廱廸彝彜弋弑弖弩弭弸彎弯彗彭彷徂彿徊很徇徙徘徨徭徼忖忻忤忸忱忝忿怡怙怩怎怱怛怕怫怦怏怺恚恁恪恟恊恍恃恤恂恬恫恙悁悍悃悚悄悛悖悒悧悋悸惓悴忰悽惆悵惘慍愕愆惶惷愀惴惺愃惻愍愎慇愾愨愧慊愿愬愴慂慳慷慙慚慫慴慥慟慝慓慵憖憔憚憊憑憫憮懌懊懈懃懆憺懋罹懍懦懣懶懺懴懿懽懼懾戈戉戍戌戔戛戞戡截戮戳扁扎扞扣扛扠扨扼抉找抒抓抖抃抔拗拑抻拏拿拆拈拌拊拇抛挌拮拱挂挈拯拵捐捍捏掖掎掀掫捶掣掏掉掟捫捩掾揩揀揆揣揉揶揄搴搆搓搦搶搗搨搏摧摶摎撕撓撥撩撈撼擒擅撻擘擂擱擠擡抬擣擯攬擲擺攀擽攘攅攤攣攫畋敖敞敝敲斂斃斛斟斫旃旆旁旄旌旒旛旱杲昊昃旻杳昵昶昴昜晏晁晞晤晧晨晟晢晰暈暉暄暘暝曁暹暾曄曚曠昿曦曩曰曷朏朞朦朧霸朮朿朶朸杆杞杠杙杣枉杼杪枌枋枡枅枷柯枴柬枳柩枸柤柞柝柢柮枹柎栞框栩桀栲桎梳栫桙桷桿梟梏梭梔梛梃桴梵梠梺椏椁棊椈棘棍棕椶椒椄棗棣棹棠椚楹楸楫楔楾楮椹椽椰楡楞楝榁槐槁槓榾槎寨槊榻槃榧榑榜榕榴槨樛槿槹槲槧樅榱槭樔樊樒櫁橄橇橙橦橈樸檐檠檄檣檗蘗檻櫃櫂檸檳檬櫟檪櫚櫪欅蘖櫺欒欖欸欷欹歇歃歉歙歔歛歟歿殀殄殃殍殞殤殪殫殯殲殱殷毋毟毬毫毳毯麾氈氓氛汞汕汪沂沍沚沁沛汨沐泄泓沽泗泅泝沮沱沾泛泯泪洟衍洶洫洽洸洵洒洌浣涓浚浹浙涎涕涅淹涵涸淆淬淌淒淅淙淤淪渭湮渙湲渾渣湫渫湍渟湃渺湎渝游溂溘滉溷滓溽滄溲滔滕溏溥滂溟滬滸滾漿滲漱漲滌漾漓滷澆潺潸潯潭澂潘澎潦澳澣澡澹濆澪濬濔濘濛瀉瀋濺瀑瀁瀏濾瀛瀚瀝瀟瀰瀾瀲灑炙炒炯烱炬炸炳炮烟烋烝烙焉烽焜焙煥煕熈煦煢煌煖煬熏燻熄熕熨熬燗熹熾燉燔燎燠燬燧燵燼燹燿爍爛爨爬爰牀牆牋牘牴牾犂犁犇犒犖犢犲狃狆狄狎狒狢狠狡狷倏猗猊猜猖猝猴猯猩猥猾獏獗獪獰獺珈玳玻珀珥珮珞璢琅瑯琥琲琺瑕瑟瑙瑁瑜瑩瑰瑣瑪瑶瑾璋璞瓊瓏瓔瓠瓣瓧瓩瓮瓲瓰瓱瓸瓷甄甃甅甌甎甍甕甓甦畛畚畤畭畸疆疇畴疔疚疝疥疣痂疳痃疵疽疸疼疱痍痊痒痙痣痞痾痿痼瘁痰痺痲痳瘋瘉瘟瘧瘠瘡瘢瘤瘴瘰瘻癇癈癆癜癘癢癨癩癪癧癬癰癲癸皎皖皓皙皚皰皴皸皹皺盂盍盒盞盥盧盪蘯盻眈眇眄眩眥眦眛眷眸睇睚睨睫睛睥睾睹瞎瞋瞑瞠瞞瞰瞿瞼瞽瞻矇矍矚矜矣矮矼砌砒砠硅硼碚碌碣碪磑磋磔碾碼磅磊磬磧磚磽磴礒礑礙礬礫祀祠祗祟祚祓祺禊禝禧禳禹禺秉秕秧秬秣稈稍稠稟禀稷穡穢穹穽窈窕窘窖窩窶竅竄窿邃竇竍竏竕竓站竚竡竢竦竭竰笏笊笆笳笘笙笞笵笨筐筺笄筍笋筌筅筵筥筴筧筰筱筬筮箝箘箍箜箚箒箏筝箙篋篁篌箴篆篝篩簑簔篥簀簇簓篳篷簗簍簣簧簪簟簷簫簽籌籃籔籀籐籟籤籖籥籬籵粃粤粢粨粳粲粱粽糀糅糂糒糜鬻糯糲糴糶糺紆紂紜紕紊絅紮紲紿紵絆絳絖絎絨絮絏絣綉絛綏絽綛綺綮綣綵緇綽綫綢綯綸綟綰緘緝緤緞緲緡縅縊縡縒縟縉縋縢繆繦縻縵縹繃縷縲縺繧繝繖繞繙繚繹繻纃繽辮纈纉纐纓纔纛纜缸罅罌罍罎罕罔罘罟罠罨罩罧羂羆羃羈羇羌羔羝羚羯羲羹羶羸翅翊翕翔翡翦翩翳翹飜耆耄耋耘耙耜耡耨耿聊聆聒聘聚聟聢聳聶聿肄肆肛肓肚肭肬胛胥胙胝胄胚胖胯胱脛脩脣脯腋隋腆脾腓腑胼腱腮腥腴膃膈膊膀膂膠膣腟膩膰膵膾臀臂膺臉臍臑臙臘臚臠臧臻臾舁舂舅舐舫舸舳艀艙艘艝艚艟艤艢艨艪艫艱艸艾芍芒芫芟芻芬苡苣苟苴苳苺莓范苻苹苞茆苜茉苙茵茴茲茱荀茹荐荅茯茫茗茘莅莚莪莟莢茣莎荼荳荵莠莉莨菴菫菎菽萃菘菁菠菲萍萢莽萸葭萼葷蒭蒂葩葆葯萵蒹蒿蒟蓙蓍蒻蓐蓁蓆蓖蒡蔡蓿蓴蔗蔘蔬蔟蔕蔔蓼蕀蕣蕘蕈蕁蕕薀薤薈薑薊薨蕭薔薛薇薜蕷蕾薐藉薺薹藐藕藜藹蘊蘋藾藺蘆蘢蘚蘿虔虧虱蚓蚣蚩蚪蚋蚌蚶蚯蛄蛆蚰蛉蚫蛔蛞蛩蛬蛟蛯蜒蜆蜈蜀蜃蛻蜑蜉蜍蛹蜊蜴蜿蜷蜻蜥蜩蜚蝠蝟蝸蝌蝎蝴蝗蝨蝮蝙蝓蝣螟螂螯蟋螽蟀雖螫蟄螳蟇蟆螻蟯蟠蠍蟾蟶蟷蠎蟒蠑蠖蠕蠢蠡蠱蠹蠧衄衒衙衢衫衾袞衵衽袵衲袂袗袒袙袢袍袤袰袿袱裃裄裔裘裙裹褂裼裴裨裲褄褌褊褓褞褥褪褫襁襄褻褶褸襌褝襠襞襦襤襭襪襯襴襷覃覈覓覘覡覩覦覬覯覲覿觚觜觝觴訖訐訌訛訝訥訶詁詛詒詆詈詼詭詬詢誅誂誄誨誡誑誥誦誚誣諄諍諂諚諳諤諱謔諠諢諷諞諛謌謇謚諡謖謐謗謳鞫謦謫謾謨譁譌譏譎譖譛譚譫譟譬譴讌讎讒讖讙谺豁谿豈豌豕豢豺貂貉貊貎貘貽貲貶賈賁賚賽賺賻贄贅贇贏贍贐齎贓贔贖赧赭赳趁趙跂趾趺跏跚跖跌跛跋跪跫跟跣跼踉跿踝踞踟蹂踵踰踴蹊蹇蹉蹌蹐蹈蹙蹤蹠蹣蹕蹶蹲蹼躁躇躅躄躋躊躓躑躔躙躪躡躬躱躾軈軋軛軼軻軫軾輊輅輒輙輓輜輟輛輌輦輳輻輹轅轂輾轌轆轎轗轜轢轤辜辟辷迚迥迢迪邇迴逅迹逑逕逡逍逞逖逋逧逵迸遏遐遑遒逎遉逾遖遘遨遯遶邂遽邁邀邏邨邯邱邵郢郤扈郛鄂鄒鄙鄲酊酖酣酥酩酳酲醋醂醢醯醪醵醴醺釁釉釐釵鈞釿鈔鈕鈑鉞鉗鉅鉉鉈銕鈿鉋銜銖銓銛鋏銹銷鋩錏鋺錙錚錣錺錵錻鍠鍼鍮鎰鎬鎹鏖鏗鏨鏘鏃鏝鏐鏈鏤鐚鐔鐓鐃鐐鐶鐫鐺鑒鑠鑢鑞鑪鑰鑵鑷鑽鑚鑼鑾钁鑿閂閊閔閘閙閨閧閭閼閻閹閾闊濶闃闍闌闕闔闖闡闥闢阡阨阮阯陂陌陋陜陞陝陟陲陬隍隘隕隗隧隰隴雎雋雉雍襍雜霍雕雹霄霆霈霓霎霑霏霖霙霤霪霰霹霽霾靄靆靂靉靠靤靦靨勒靫鞅靼鞁靺鞆鞋鞏鞐鞜鞨鞦鞣鞳鞴韆韈韋韜齏韲竟韶韵頏頌頤頡頷頽顆顋顫顰顱顴顳颪颯颱颶飄飆飩飫餃餉餒餔餡餞餤餬餮餽餾饂饉饅饐饋饑饒饌饕馗馘馥馭馮駟駛駝駘駑駭駮駱駻駸騁騏騅駢騙騫驂驀驃騾驕驍驟驢驥驤驩驪骭骰骼髀髏髑髢髣髦髯髫髴髱髷髻鬆鬘鬚鬟鬢鬣鬧鬨鬩鬮鬯魄魃魏魍魎魑魘魴鮓鮃鮑鮖鮗鮟鮠鮨鮴鯀鯊鮹鯏鯑鯒鯣鯢鯤鯔鯡鯲鯱鯰鰕鰔鰉鰓鰌鰆鰈鰒鰊鰄鰮鰛鰥鰤鰰鱇鱆鰾鱚鱠鱧鱶鱸鳧鳬鳰鴉鴃鴆鴪鴣鴟鵄鴕鴒鵁鴿鴾鵆鵝鵞鵤鵑鵙鵲鶉鶇鶫鵯鵺鶚鶤鶩鶲鷁鶻鶸鶺鷆鷂鷙鷓鷸鷦鷭鷯鷽鸛鸞鹵鹹麁麈麋麌麕麑麝麩麸麭靡黌黎黏黐黔黜黝黠黥黯黴黶黷黹黻黼黽鼇鼈鼕鼬鼾齔齣齟齠齦齧齬齪齷齲齶龕龠凜熙')
    ]
_jlpt = [ ('Non-JLPT', ''),
    ('JLPT N5', '一右雨円下何火外学間気休金九月見五午後語校行高国今左三山四子時七車十出書女小上食人水生西先千川前大男中長天電土東読南二日入年白八半百父聞母北本毎万名木友来六話'),
    ('JLPT N4', '悪安以意医員飲院運映英駅屋音夏家歌花画会海界開楽漢館帰起急究牛去魚京強教業近銀空兄計建犬研験元言古公口工広考黒作仕使始姉思止死私紙試事字持自室質写社者借主手秋終習週集住重春少場色心新真親図世正青赤切早走送足族多体待貸代台題知地茶着昼注朝町鳥通弟店転田度冬答動同堂道特肉買売発飯病品不風服物文別勉歩方妹味明目問夜野有夕曜洋用理立旅料力'),
    ('JLPT N3', '愛暗位偉易違育因引泳越園演煙遠押横王化加科果過解回皆絵害格確覚掛割活寒完官感慣観関顔願危喜寄幾期機規記疑議客吸求球給居許供共恐局曲勤苦具偶靴君係形景経警迎欠決件権険原現限呼互御誤交候光向好幸更構港降号合刻告込困婚差座最妻才歳済際在罪財昨察殺雑参散産賛残市師指支資歯似次治示耳辞式識失実若取守種酒首受収宿術処初所緒助除勝商招消笑乗常情状職信寝深申神進吹数制性成政晴精声静席昔石積責折説雪絶戦洗船選然全祖組想争相窓草増側息束速続存他太打対退宅達単探断段談値恥置遅調頂直追痛定庭程適点伝徒渡登途都努怒倒投盗当等到逃頭働得突内難任認猫熱念能破馬敗杯背配箱髪抜判反犯晩番否彼悲疲費非飛備美必表貧付夫婦富怖浮負舞部福腹払平閉米変返便捕暮報抱放法訪亡忘忙望末満未民眠務夢娘命迷鳴面戻役約薬優由遊予余与容様葉要陽欲頼落利流留両良類例冷礼列連路労老論和'),
    ('JLPT N2', '圧依囲委移胃衣域印宇羽雲営栄永鋭液延塩汚央奥欧黄億温河荷菓課貨介快改械灰階貝各角革額乾刊巻干患換汗甘管簡缶丸含岸岩希机祈季技喫詰逆久旧巨漁競協叫境挟橋況胸極玉均禁区隅掘訓群軍傾型敬軽芸劇血券県肩賢軒減個固庫戸枯湖雇効厚硬紅耕肯航荒講郊鉱香腰骨根混査砂再採祭細菜材坂咲冊刷札皿算伺刺史枝糸脂詞誌児寺湿捨弱周州拾舟柔祝述準純順署諸召将床承昇焼照省章紹象賞城畳蒸植触伸森臣辛針震勢姓星清税隻籍績跡接設占専泉浅線双層捜掃燥総装像憎臓蔵贈造則測卒孫尊損村帯替袋濯谷担炭短団池築畜竹仲柱虫駐著貯兆庁超沈珍低停底泥滴鉄殿塗党凍塔島湯灯筒導童銅毒届曇鈍軟乳燃悩濃脳農波拝倍泊薄爆麦肌板版般販比皮被鼻匹筆氷秒瓶布府普符膚武封副復幅複沸仏粉兵並片編辺補募包宝豊帽暴棒貿防磨埋枚綿毛門油輸勇郵預幼溶踊浴翌絡乱卵裏陸律略粒了涼療量領緑林輪涙令零齢歴恋練録湾腕'),
    ('JLPT N1', '亜阿哀葵茜握渥旭梓扱絢綾鮎案杏伊威尉惟慰為異維緯遺井亥郁磯壱逸稲芋允姻胤陰隠韻卯丑渦唄浦叡影瑛衛詠疫益悦謁閲宴援沿炎猿縁艶苑鉛於凹往応旺殴翁沖憶乙卸恩穏仮伽価佳嘉嫁寡暇架禍稼箇茄華霞蚊我芽賀雅餓塊壊怪悔懐戒拐魁凱劾慨概涯街該馨垣嚇拡核殻獲穫較郭閣隔岳潟喝括渇滑褐轄且叶樺株鎌茅刈侃冠勘勧喚堪寛幹憾敢棺款歓環監看緩肝艦莞貫還鑑閑陥巌眼頑企伎器基奇嬉岐忌揮旗既棋棄毅汽稀紀貴軌輝飢騎鬼亀偽儀宜戯擬欺犠義誼菊鞠吉橘却脚虐丘及宮弓救朽泣窮級糾拒拠挙虚距亨享凶匡喬峡恭狂狭矯脅興郷鏡響驚仰凝尭暁桐錦斤欣欽琴筋緊芹菌衿襟謹吟句玖駆駒愚虞遇屈熊栗繰桑勲薫郡袈刑啓圭契径恵慶慧憩掲携桂渓系継茎蛍鶏鯨撃激傑潔穴結倹健兼剣圏堅嫌憲懸拳検献絹謙遣顕厳幻弦源玄絃孤己弧故胡虎誇顧鼓伍呉娯悟梧瑚碁護鯉侯倖功后坑孔宏巧康弘恒抗拘控攻昂晃江洪浩溝甲皇稿紘絞綱衡貢購酵鋼項鴻剛拷豪克穀酷獄墾恨懇昆紺魂佐唆嵯沙瑳詐鎖裟債催哉宰彩栽災采砕斎裁載剤冴崎削搾朔策索錯桜笹撮擦皐傘惨桟燦蚕酸暫司嗣士姿志施旨氏祉紫肢至視詩諮賜雌飼侍慈滋爾磁蒔汐鹿軸執漆疾偲芝舎射赦斜煮紗謝遮蛇邪勺尺爵酌釈寂朱殊狩珠趣儒授樹需囚宗就修愁洲秀臭衆襲酬醜充従汁渋獣縦銃叔淑縮粛塾熟俊峻瞬竣舜駿准循旬殉淳潤盾巡遵暑曙渚庶叙序徐恕傷償匠升唱奨宵尚庄彰抄掌捷昌昭晶松梢沼渉焦症硝礁祥称肖菖蕉衝訟証詔詳鐘障丞冗剰壌嬢条浄穣譲醸錠嘱飾殖織辱侵唇娠審慎振晋榛浸秦紳薪診仁刃尋甚尽迅陣須酢垂帥推炊睡粋翠衰遂酔錘随瑞髄崇嵩枢雛据杉澄寸瀬畝是征整牲盛聖製誠誓請逝斉惜斥析碩拙摂窃節舌仙宣扇栓染潜旋繊薦践遷銭銑鮮善漸禅繕塑措疎礎租粗素訴阻僧創倉喪壮奏爽惣挿操曹巣槽綜聡荘葬蒼藻遭霜騒促即俗属賊汰堕妥惰駄耐怠態泰滞胎逮隊黛鯛第鷹滝卓啄択拓沢琢託濁諾只但辰奪脱巽棚丹嘆旦淡端胆誕鍛壇弾暖檀智痴稚致蓄逐秩窒嫡宙忠抽衷鋳猪丁帳弔張彫徴懲挑暢潮眺聴脹腸蝶跳勅朕賃鎮陳津墜椎塚槻漬蔦椿坪紬釣鶴亭偵貞呈堤帝廷悌抵提禎締艇訂逓邸摘敵笛哲徹撤迭典展添吐斗杜奴刀悼搭桃棟痘糖統藤討謄豆踏透陶騰闘憧洞瞳胴峠匿徳督篤独凸寅酉屯惇敦豚奈那凪捺縄楠尼弐虹如尿妊忍寧粘乃之納巴把覇派婆俳廃排肺輩培媒梅賠陪萩伯博拍舶迫漠縛肇鉢伐罰閥鳩隼伴帆搬班畔繁藩範煩頒盤蛮卑妃扉批披斐泌碑秘緋罷肥避尾微眉柊彦姫媛俵彪標漂票評描苗彬浜賓頻敏扶敷腐芙譜賦赴附侮楓蕗伏覆噴墳憤奮紛雰丙併塀幣弊柄陛壁癖碧偏遍弁保舗甫輔穂墓慕簿倣俸奉峰崩朋泡砲縫胞芳萌褒邦飽鳳鵬乏傍剖妨房某冒紡肪膨謀僕墨撲朴牧睦没堀奔翻凡盆摩魔麻槙幕膜柾亦又抹繭麿慢漫魅巳岬密稔脈妙矛霧椋婿盟銘滅免模茂妄孟猛盲網耗黙紋匁也冶耶弥矢厄訳躍靖柳愉癒諭唯佑宥幽悠憂柚湧猶祐裕誘邑雄融誉庸揚揺擁楊窯羊耀蓉謡遥養抑翼羅裸雷酪嵐欄濫藍蘭覧吏履李梨璃痢離率琉硫隆竜慮虜亮僚凌寮猟瞭稜糧諒遼陵倫厘琳臨隣麟瑠塁累伶励嶺怜玲鈴隷霊麗暦劣烈裂廉蓮錬呂炉露廊朗楼浪漏郎禄倭賄惑枠亘侑勁奎崚彗昴晏晨晟暉栞椰毬洸洵滉漱澪燎燿瑶皓眸笙綺綸翔脩茉莉菫詢諄赳迪頌颯黎凜熙')
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
        def kanjitile(char, index, count=0, avg_interval=0, missing=False):
            tile = ""
            score = "NaN"

            if missing:
                colour = "#888"
            else:
                colour = "#000"

            if count != 0:
                bgcolour = hsvrgbstr(scoreAdjust(avg_interval / _interval)/2)
            elif missing:
                bgcolour = "#EEE"
            else:
                bgcolour = "#FFF"

            if _tooltips:
                tooltip = "Character: %s" % unicodedata.name(char)
                if count:
                    tooltip += " | Count: %s | " % count
                    tooltip += "Avg Interval: %s | Score: %s | " % (avg_interval, score)
                    tooltip += "Background: %s | Index: %s" % (bgcolour, index)
                tile += "\t<td align=center valign=top style=\"background:%s;\" title=\"%s\">" % (bgcolour, tooltip)
            else:
                tile += "\t<td align=center valign=top style=\"background:%s;\">" % (bgcolour)
            tile += "<a href=\"http://jisho.org/search/%s%%20%%23kanji\" style=\"color:%s;\">%s</a></td>\n" % (char, colour, char)

            return tile

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
        if _groupby in (4, 5, 6):
            if _groupby == 4:
                _groups = _grades
            elif _groupby == 5:
                _groups = _jlpt
            elif _groupby == 6:
                _groups = _kanken
            gc = 0
            kanji = list([u.value for u in units.values()])
            for i in range(1,len(_groups)):
                self.html += "<h2 style=\"color:#888;\">%s Kanji</h2>\n" % _groups[i][0]
                table = "<table width='85%'><tr>\n"
                count = -1
                for unit in [units[c] for c in _groups[i][1] if c in kanji]:
                    if unit.count != 0 or _unseen:
                        count += 1
                        if count % cols == 0 and count != 0: table += "</tr>\n<tr>\n"
                        table += kanjitile(unit.value, count, unit.count, unit.avg_interval)
                table += "</tr></table>\n"
                n = count+1
                t = len(_groups[i][1])
                gc += n
                if _unseen:
                    table += "<details><summary>Missing kanji</summary><table style=\"max-width:75%;\"><tr>\n"
                    count = -1
                    for char in [c for c in _groups[i][1] if c not in kanji]:
                        count += 1
                        if count % cols == 0: table += "</tr>\n<tr>\n"
                        table += kanjitile(char, count, missing=True)
                    if count == -1: table += "<strong style=\"color:#CCC\">None</strong>"
                    table += "</tr></table></details>\n"
                self.html += "<h4 style=\"color:#888;\">%d of %d - %0.2f%%</h4>\n" % (n, t, n*100.0/t)
                self.html += table

            chars = reduce(lambda x,y: x+y, dict(_groups).values())
            self.html += "<h2 style=\"color:#888;\">%s Kanji</h2>" % _groups[0][0]
            table = "<table width='85%'><tr>\n"
            count = -1
            for unit in [u for u in units.values() if u.value not in chars]:
                if unit.count != 0 or _unseen:
                    score = "NaN"
                    count += 1
                    if count % cols == 0 and count != 0: table += "</tr>\n<tr>\n"
                    table += kanjitile(unit.value, count, unit.count, unit.avg_interval)
            table += "</tr></table>\n"
            n = count+1
            self.html += "<h4 style=\"color:#888;\">%d of %d - %0.2f%%</h4>\n" % (n, gc, n*100.0/gc)
            self.html += table
        else:
            table = "<table width='85%'><tr>\n"
            if _groupby == 0: # Order found
                unitsList = sorted( units.values(), key=lambda unit: (unit.idx, unit.count) )
            if _groupby == 1: # Unicode index
                unitsList = sorted( units.values(), key=lambda unit: (unicodedata.name(unit.value), unit.count) )
            if _groupby == 2: # Character score
                unitsList = sorted( units.values(), key=lambda unit: (scoreAdjust(unit.avg_interval / _interval), unit.count), reverse=True)
            if _groupby == 3: # Deck frequency
                unitsList = sorted( units.values(), key=lambda unit: (unit.count, scoreAdjust(unit.avg_interval / _interval)), reverse=True)
            count = -1
            for unit in unitsList:
                if unit.count != 0 or _unseen:
                    score = "NaN"
                    count += 1
                    if count % cols == 0 and count != 0: table += "</tr>\n<tr>\n"
                    table += kanjitile(unit.value, count, unit.count, unit.avg_interval)
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
            with open(fileName, 'w', encoding='utf-8') as fileOut:
                (units, timeNow) = self.kanjigrid()
                self.generate(units, timeNow, True)
                fileOut.write(self.html)
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
                matches = None
                if _literal:
                    matches = operator.eq
                else:
                    matches = operator.contains
                for keyword in _pattern:
                    for s,key in ((key.lower(),key) for key in keys):
                        if matches(s.lower(), keyword):
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
        global _groupby, _unseen, _tooltips
        swin = QDialog(mw)
        vl = QVBoxLayout()
        frm = QGroupBox("Settings")
        vl.addWidget(frm)
        il = QVBoxLayout()
        fl = QHBoxLayout()
        field = QLineEdit()
        field.setPlaceholderText("e.g. \"kanji\" or \"sentence-kanji\" (default: \"kanji\")")
        il.addWidget(QLabel("Pattern or Field names to search for (case insensitive):"))
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
        groupby = QComboBox()
        groupby.addItems(["None, sorted by order found",
                        "None, sorted by unicode order",
                        "None, sorted by score",
                        "None, sorted by frequency",
                        "Grade",
                        "JLPT Level",
                        "Kanji Kentei Level"])
        groupby.setCurrentIndex(_groupby)
        il.addWidget(QLabel("Group by:"))
        il.addWidget(groupby)
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
        swin.setTabOrder(wtcol,groupby)
        swin.setTabOrder(groupby,shnew)
        swin.setTabOrder(shnew,toolt)
        swin.resize(500, 400)
        if swin.exec_():
            mw.progress.start(immediate=True)
            if len(field.text().strip()) != 0: _pattern = field.text().lower().split()
            _literal = liter.isChecked()
            _interval = stint.value()
            _thin = ttcol.value()
            _wide = wtcol.value()
            _groupby = groupby.currentIndex()
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

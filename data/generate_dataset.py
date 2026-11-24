"""把公开渠道核实到的企业与政策整理成导入用 CSV。

字段来源逐条记在 数据来源说明.md。查不到的字段留空，不填推测值。
运行：python data/generate_dataset.py
"""

import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent

SRC_XIEHUI = "http://zjsia.org.cn/detail/1787728217837432834"
SRC_TENCENT = "https://news.qq.com/rain/a/20250804A07JH300"
SRC_ZJTXXJR = "https://zjtxxjr.cn/company/f41200c6-38fc-5a8d-bf8c-59301c40be89.html"
SRC_QCC_XINMAI = "https://aiqicha.baidu.com/company_shares_26449600667495"
SRC_QCC_BAODING = "https://aiqicha.baidu.com/company_detail_91494627407697?tab=dataAnalysis"
SRC_BAIKE_ZX = "https://baike.baidu.com/item/%E6%9D%AD%E5%B7%9E%E4%B8%AD%E6%AC%A3%E6%99%B6%E5%9C%86%E5%8D%8A%E5%AF%BC%E4%BD%93%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/24529583"
SRC_BAIKE_XZ = "https://baike.baidu.com/item/%E6%9D%AD%E5%B7%9E%E8%8A%AF%E6%AD%A3%E5%BE%AE%E7%94%B5%E5%AD%90%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/68817465"
SRC_WIKI_YOUZHILIAN = "http://newton.com.tw/wiki/%E6%9D%AD%E5%B7%9E%E5%84%AA%E6%99%BA%E8%81%AF%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/51200952"
SRC_AQC_HESHENG = "https://aiqicha.baidu.com/brand/detail?id=643510815&pid=43026046444575"
SRC_36KR_FUXIN = "https://www.36kr.com/p/4016851623694464"
SRC_FULLSEMI = "https://www.fullsemitech.com"
SRC_QCC_CHANGCHUAN = "https://aiqicha.baidu.com/company_news_60428013901716"
SRC_QCC_LIANANG = "https://aiqicha.baidu.com/company_detail_46802366444232"
SRC_BAIKE_WN = "https://baike.baidu.com/item/%E6%9D%AD%E5%B7%9E%E5%BE%AE%E7%BA%B3%E6%A0%B8%E8%8A%AF%E7%94%B5%E5%AD%90%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/62987798"
SRC_JINDT = "https://www.zhangtongshe.com/article.html?id=100205"
SRC_B2B_ZJ = "https://b2b.baidu.com/land/9be646e1daab6f39518a37fd5f5ad318?fid=403116032"
SRC_B2B_HH = "https://b2b.baidu.com/land/cd2fac7239da18d1d95a9042f8bbc92d?fid=403116032"
SRC_SHILAN = "https://www.qcc.com/creport/f07e9f3282b1f253863a67c48cd09189.html"
SRC_GUANGLI = "https://www.qibook.com/company-wiki-s/hangzhouguangliweidianzigufenyouxiangongsi-6abd82e5.html?s=t"
SRC_JIEHUATE = "https://www.qcc.com/cfinance/9f01cd6b671d18c9810cc9d74fecad7a.html"
SRC_XILIJIE = "https://baike.baidu.com/item/%E7%9F%BD%E5%8A%9B%E6%9D%B0%E5%8D%8A%E5%AF%BC%E4%BD%93%E6%8A%80%E6%9C%AF%EF%BC%88%E6%9D%AD%E5%B7%9E%EF%BC%89%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/19995956"
SRC_GUOXIN = "https://www.qibook.com/company-wiki-s/hangzhouguoxinweidianzigufenyouxiangongsi-d1db9e72.html?s=t"
SRC_HUALAN = "https://www.qcc.com/crun/4c54a55a36f0b7039f3b42a56f22b900.html"
SRC_JINGHUA = "https://www.qibook.com/company-wiki-s/hangzhoujinghuaweidianzigufenyouxiangongsi-56dbffcd.html?s=t"
SRC_JIANAN = "https://baike.baidu.com/item/%E5%98%89%E6%A5%A0%E7%A7%91%E6%8A%80/65815117"
SRC_JINGSHENG = "https://www.qibook.com/company-wiki-s/zhejiangjingshengjidiangufenyouxiangongsi-69a9638e.html?s=t"
SRC_ZHONGGUI = "https://www.qibook.com/company-wiki-s/zhongweizhongguihangzhoudianzikejiyouxiangongsi-50e36949.html?s=t"
SRC_PINGTOUGE = "https://www.qibook.com/company-wiki-s/pingtougebandaotiyouxiangongsi-7b1fd28e.html?s=t"
SRC_ZHONGTIAN = "https://www.qibook.com/company-wiki-s/hangzhouzhongtianweixitongyouxiangongsi-b112c434.html?s=t"
SRC_WANGAO = "https://www.qibook.com/company-wiki-s/hangzhouwangaokejigufenyouxiangongsi-dd03be06.html?s=t"
SRC_ZHONGKE = "https://www.qibook.com/company-wiki-s/hangzhouzhongkeweidianziyouxiangongsi-221a8af3.html?s=t"
SRC_ZHENLEI = "https://www.qibook.com/company-wiki-s/zhejiangzhenleikejigufenyouxiangongsi-e5752d39.html?s=t"
SRC_TUOER = "https://www.qibook.com/company-wiki-s/hangzhoutaerweidianziyouxiangongsi-68f4d3a0.html?s=t"
SRC_YOUWANG = "https://www.qibook.com/company-wiki-s/hangzhouyouwangdianziyouxiangongsi-b4039292.html?s=t"
SRC_CHENGXIN = "https://www.qibook.com/company-wiki-s/hangzhouchengxinkejiyouxiangongsi-d3a678bb.html?s=t"
SRC_MEIDIKAI = "https://www.qibook.com/company-wiki-s/hangzhoumeidikaiguangdiankejigufenyouxiangongsi-a524639b.html?s=t"
SRC_CHUANGXIN = "https://www.qibook.com/company-wiki-s/zhejiangchuangxinjichengdianluyouxiangongsi-c44d50bc.html?s=t"
SRC_LIANANGDX = "https://www.qibook.com/company-wiki-s/hangzhouliangdongxinweidianziyouxiangongsi-d2e0071f.html?s=t"
SRC_ZHONGXINJIC = "https://baike.baidu.com/item/%E4%B8%AD%E8%8A%AF%E9%9B%86%E6%88%90%E7%94%B5%E8%B7%AF%E5%88%B6%E9%80%A0%EF%BC%88%E7%BB%8D%E5%85%B4%EF%BC%89%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/51152871"
SRC_HAINA = "https://www.qibook.com/company-wiki-s/zhejianghainabandaotigufenyouxiangongsi-abcab9fc.html?s=t"
SRC_PAIENJIE = "https://www.qibook.com/company-wiki-s/paienjiebandaotizhejiangyouxiangongsi-5d1498b1.html?s=t"
SRC_JIANGFENG = "https://www.qibook.com/company-wiki-s/ningbojiangfengdianzicailiaogufenyouxiangongsi-fb98a6dc.html?s=t"
SRC_JIEMEI = "https://www.qibook.com/company-wiki-s/zhejiangjiemeidianzikejigufenyouxiangongsi-06c4e0b3.html?s=t"
SRC_HAoweiMI = "https://www.qibook.com/company-wiki-s/zhejianghaoweimikejiyouxiangongsi-36ce313e.html?s=t"
SRC_RUIMENG = "https://www.qibook.com/company-wiki-s/hangzhouruimengkejigufenyouxiangongsi-d67b4825.html?s=t"
SRC_SHENGYUAN = "https://www.qibook.com/company-wiki-s/hangzhouchengyuanshujuanquanjishugufenyouxiangongsi-48eb4391.html?s=t"
SRC_DEXIN = "https://www.qibook.com/company-wiki-s/hangzhoudexinkejiyouxiangongsi-5745eb31.html?s=t"
SRC_WEINA = "https://www.qcc.com/cjoblist/b030fa1c453990a7284b7057ae4741c2"
SRC_ZHONGJUXIN = "https://www.qibook.com/company-wiki-s/zhongjuxinkejigufenyouxiangongsi-11fb7bc7.html?s=t"
SRC_XINYUN = "https://baike.baidu.com/item/%E6%9D%AD%E5%B7%9E%E8%8A%AF%E4%BA%91%E5%8D%8A%E5%AF%BC%E4%BD%93%E9%9B%86%E5%9B%A2%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/69643353"
SRC_YONGSHI = "https://www.qibook.com/company-wiki-s/yongxidianziningbogufenyouxiangongsi-45d55c66.html?s=t"
SRC_KANGQIANG = "https://www.qibook.com/company-wiki-s/ningbokangqiangdianzigufenyouxiangongsi-b30f76fa.html?s=t"
SRC_JINRUIHONG = "https://www.qibook.com/company-wiki-s/zhejiangjinruihongkejigufenyouxiangongsi-0a2d0557.html?s=t"
SRC_QUNXIN = "https://www.qibook.com/company-wiki-s/ningboqunxinweidianzigufenyouxiangongsi-9864e6ac.html?s=t"

INDUSTRY = {
    "芯片设计": ("6520", "集成电路设计"),
    "晶圆制造": ("3971", "集成电路制造"),
    "先进封装": ("3972", "集成电路封装测试"),
    "半导体设备": ("3562", "半导体器件专用设备制造"),
    "半导体材料": ("3985", "电子专用材料制造"),
}

HZ = "浙江省杭州市"

# 每条：name, segment, region, founded, legal, capital, employee, revenue,
#       credit, qualifications, events, bases, source, url, note
ENTERPRISES = [
    ("联芸科技(杭州)股份有限公司", "芯片设计", HZ, 2014, "李国阳", 46000, "500-999 人", "1-5 亿元", "91330100320508065U", '{"专利数":247,"资质":["国家级专精特新小巨人","高新技术企业","省级制造业单项冠军"]}', '[{"时间":"2025-09","事件":"在上海设立子公司云帆芯创科技有限公司，作为区域研发中心"}]', '["上海","广州","深圳","苏州","成都"]', "qcc", SRC_ZJTXXJR, "2025 年营收 13.27 亿元，员工 787 人；补齐自 qibook 与 2025 年报"),
    ("芯迈半导体技术(杭州)股份有限公司", "芯片设计", HZ, 2019, "任远程", 5000, "", "10 亿元以上", "", '{"专利数":77,"资质":["国家级专精特新小巨人","高新技术企业","独角兽企业"]}', "", '["上海","深圳","首尔"]', "annual_report", SRC_QCC_XINMAI, "2021 年销售额 18.6 亿元"),
    ("宝鼎乾芯集成电路(杭州)有限公司", "晶圆制造", HZ, 2021, "张亮", 100000, "", "", "91330114MA2KL93H64", "", "", "", "qcc", SRC_QCC_BAODING, "车规级功率器件，规划产能 172 万片/年"),
    ("杭州中欣晶圆半导体股份有限公司", "半导体材料", HZ, 2017, "贺贤汉", 503200, "1000 人以上", "10 亿元以上", "", '{"专利数":285,"资质":["国家级专精特新小巨人"]}', '[{"时间":"2021-06","事件":"丽水 12 英寸抛光片产线通线，首期月产能 15 万片"},{"时间":"2021-09","事件":"完成 33 亿元 B 轮融资"}]', '["杭州","宁夏","上海","丽水"]', "annual_report", SRC_BAIKE_ZX, "2024 年营收 13.35 亿元；补齐自公开转让说明书与百科"),
    ("杭州芯正微电子有限公司", "芯片设计", HZ, 2016, "李雪", "", "", "", "", '{"专利数":13,"资质":["国家级专精特新小巨人","高新技术企业"]}', '[{"轮次":"A轮","时间":"2025-11","金额":"数亿元"}]', '["杭州","成都","北京"]', "annual_report", SRC_BAIKE_XZ, ""),
    ("杭州优智联科技有限公司", "芯片设计", HZ, 2019, "董宗宇", 801.5118, "", "", "", '{"专利数":40,"资质":["省级专精特新","科技型中小企业"]}', '[{"轮次":"A轮","时间":"2025-01"}]', "", "official_site", SRC_WIKI_YOUZHILIAN, "UWB 无线物联网芯片"),
    ("杭州荷声科技有限公司", "芯片设计", HZ, 2023, "", "", "", "", "", "", '[{"轮次":"Pre-A轮","时间":"2025-12","金额":"数千万元"}]', "", "qcc", SRC_AQC_HESHENG, "医疗超声芯片"),
    ("杭州富芯半导体有限公司", "晶圆制造", "浙江省杭州市富阳区", 2019, "", 945000, "500-999 人", "", "", '{"专利数":402,"资质":["国家级专精特新小巨人","独角兽企业"]}', '[{"轮次":"A+轮","投资方":"国家集成电路产业投资基金二期"}]', "", "annual_report", SRC_36KR_FUXIN, "浙江首条 12 英寸模拟芯片产线"),
    ("杭州长川科技股份有限公司", "半导体设备", HZ, 2008, "赵轶", 60432.8728, "1000 人以上", "10 亿元以上", "", '{"专利数":500,"资质":["国家级专精特新小巨人","高新技术企业"]}', "", '["上海","北京","成都","哈尔滨"]', "qcc", SRC_QCC_CHANGCHUAN, "测试机、分选机、探针台、AOI 设备"),
    ("杭州立昂微电子股份有限公司", "半导体材料", HZ, 2002, "王敏文", 77219.9373, "1000-1999 人", "10 亿元以上", "91330100736871634P", '{"专利数":39,"资质":["制造业单项冠军","高新技术企业"]}', '[{"时间":"2018-09","事件":"投资设立金瑞泓微电子(衢州)有限公司，持股 57.44%"},{"时间":"2024-09","事件":"设立金瑞泓昂扬科技(衢州)有限公司"}]', '["杭州","宁波","衢州","嘉兴","海宁"]', "qcc", SRC_QCC_LIANANG, "2025 年营收 35.91 亿元，员工 3827 人；补齐自 2025 年报与股权档案"),
    ("杭州微纳核芯电子科技有限公司", "芯片设计", HZ, 2018, "葛晓欢", "", "", "", "", '{"专利数":89}', '[{"轮次":"B轮","时间":"2025-10","金额":"超亿元"}]', '["无锡","合肥","北京"]', "annual_report", SRC_BAIKE_WN, "三维存算一体 AI 芯片"),
    ("进迭时空(杭州)科技有限公司", "芯片设计", HZ, 2021, "陈志坚", "", "", "", "", "", '[{"轮次":"B轮","时间":"2025-12","金额":"超 6 亿元"}]', "", "annual_report", SRC_JINDT, "RISC-V AI 芯片"),
    ("矽力杰半导体技术(杭州)有限公司", "芯片设计", HZ, 2008, "李雪梅", 10857, "500-999 人", "10 亿元以上", "91330100673960735E", '{"专利数":908,"资质":["国家级专精特新小巨人","高新技术企业","隐形冠军企业","制造业单项冠军"]}', "", "", "qcc", SRC_XILIJIE, "注册资本 10857 万美元；2024 年营收 28.67 亿元"),
    ("杭州士兰微电子股份有限公司", "芯片设计", HZ, 1997, "陈向东", 166407.1845, "5000 人以上", "10 亿元以上", "91330000253933976Q", '{"专利数":739,"资质":["制造业单项冠军","高新技术企业","企业技术中心"]}', "", "", "qcc", SRC_SHILAN, "6/8/12 英寸特色工艺晶圆线；2025 年营收 130.52 亿元；IDM 模式"),
    ("平头哥半导体有限公司", "芯片设计", HZ, 2018, "包文俊", 150, "", "", "91330110MA2CF7XF5H", "", "", "", "qcc", SRC_PINGTOUGE, "阿里巴巴集团旗下；AI 芯片研发；工商登记员工 0 人"),
    ("杭州国芯科技股份有限公司", "芯片设计", HZ, 2001, "黄智杰", 35000, "100-499 人", "", "91330100726616402H", '{"资质":["国家级专精特新小巨人","高新技术企业"]}', '[{"轮次":"B轮","时间":"2019-02","金额":"1.5 亿元","投资方":"国投创合、创新工场"}]', "", "annual_report", SRC_GUOXIN, "现名杭州国芯微电子股份有限公司；数字电视与 AI 语音芯片"),
    ("杭州华澜微电子股份有限公司", "芯片设计", HZ, 2011, "王文奎", 15000, "100-499 人", "1-5 亿元", "91330100577337302L", '{"专利数":149,"资质":["国家级专精特新小巨人","高新技术企业","企业技术中心"]}', '[{"轮次":"股权转让","时间":"2025","金额":"1.12 亿元"}]', "", "qcc", SRC_HUALAN, "存储控制芯片与数据安全"),
    ("杭州中天微系统有限公司", "芯片设计", HZ, 2001, "李春强", 3720.3534, "1-49 人", "", "91330108732421353F", '{"专利数":226,"资质":["国家科技进步二等奖"]}', '[{"轮次":"并购","时间":"2018-04","备注":"阿里巴巴集团全资收购"}]', '["上海","宁波"]', "qcc", SRC_ZHONGTIAN, "自主 C-SKY 指令架构嵌入式 CPU"),
    ("浙江毫微米科技有限公司", "芯片设计", HZ, 2019, "孔秀英", 2500, "1-49 人", "", "91330104MA2GNREH22", '{"资质":["国家级高新技术企业","省级专精特新中小企业"]}', "", "", "qcc", SRC_HAoweiMI, "集成电路芯片技术开发"),
    ("杭州瑞盟科技股份有限公司", "芯片设计", HZ, 2008, "冯炳军", 5527.268, "100-499 人", "", "91330108670622626K", '{"专利数":143,"资质":["国家级专精特新小巨人","高新技术企业","瞪羚企业"]}', '[{"轮次":"战略投资","时间":"2020"}]', '["武汉","深圳"]', "qcc", SRC_RUIMENG, "高性能模拟及数模混合芯片；曾用名杭州瑞盟科技有限公司"),
    ("杭州晟元芯片技术有限公司", "芯片设计", HZ, 2005, "张飞飞", 5400, "1-49 人", "", "91330100779299447B", '{"专利数":223,"资质":["省级隐形冠军"]}', '[{"轮次":"E轮","时间":"2014-06","投资方":"富国投资、东方汇富"}]', "", "annual_report", SRC_SHENGYUAN, "现名杭州晟元数据安全技术股份有限公司；指纹识别芯片"),
    ("杭州万高科技股份有限公司", "芯片设计", HZ, 2006, "崔国宇", 3000, "1-49 人", "", "91330100793670492R", '{"专利数":297,"资质":["国家级高新技术企业","专精特新中小企业","企业技术中心"]}', "", "", "qcc", SRC_WANGAO, "能源物联网专用芯片；曾用名无"),
    ("杭州广立微电子股份有限公司", "芯片设计", HZ, 2003, "郑勇军", 20028.1088, "500-999 人", "1-5 亿元", "91330108751731859U", '{"专利数":239,"资质":["专精特新中小企业","高新技术企业","企业技术中心"]}', '[{"轮次":"IPO","时间":"2022-08","备注":"创业板上市，301095"}]', '["绍兴","武汉"]', "qcc", SRC_GUANGLI, "EDA 软件与晶圆级电性测试设备；2025 年营收 7.35 亿元"),
    ("杭州中科微电子有限公司", "芯片设计", HZ, 2004, "何文涛", 8010, "1-49 人", "1-5 亿元", "91330108768208888P", '{"专利数":134,"资质":["国家级高新技术企业","制造业单项冠军","隐形冠军企业"]}', "", "", "qcc", SRC_ZHONGKE, "北斗导航芯片；控股股东禾润电子科技"),
    ("浙江臻镭科技股份有限公司", "芯片设计", HZ, 2015, "张兵", 29951.4643, "100-499 人", "1-5 亿元", "9133011035243235XH", '{"专利数":46,"资质":["国家级高新技术企业"]}', '[{"轮次":"IPO","时间":"2022-01","备注":"科创板 688270"}]', "", "qcc", SRC_ZHENLEI, "射频前端芯片与微系统；2025 年营收 4.32 亿元"),
    ("杭州地芯科技有限公司", "芯片设计", HZ, 2018, "吴瑞砾", 305.0119, "1-49 人", "", "91330110MA2CFFCHX7", '{"专利数":45,"资质":["国家级专精特新小巨人","高新技术企业","准独角兽企业"]}', '[{"轮次":"B+轮","时间":"2024-07","金额":"近亿元"}]', "", "qcc", SRC_DEXIN, "射频收发机、射频前端及模拟信号链芯片"),
    ("杭州城芯科技有限公司", "芯片设计", HZ, 2016, "陈浔濛", 8400, "1-49 人", "", "91330110MA27X15P6Q", '{"专利数":19,"资质":["国家级高新技术企业","省级专精特新中小企业"]}', "", "", "qcc", SRC_CHENGXIN, "射频收发芯片；臻镭科技全资子公司；替补原名单重复项国芯微电子"),
    ("杭州嘉楠耘智信息科技有限公司", "芯片设计", HZ, 2013, "张楠赓", 30000, "", "", "913301040648566680", '{"专利数":95,"资质":["高新技术企业"]}', '[{"轮次":"IPO","时间":"2019-11","备注":"纳斯达克上市，CAN"}]', "", "annual_report", SRC_JIANAN, "2018 年量产 7nm 芯片；2019 年胡润独角兽榜第 84 位"),
    ("杭州微纳科技股份有限公司", "芯片设计", HZ, 2010, "姚嘉", 1734, "1-49 人", "5000 万-1 亿元", "91330100555181116C", '{"资质":["国家级高新技术企业","省级专精特新中小企业"]}', '[{"轮次":"战略投资","时间":"2013","投资方":"德丰杰、宽带资本"}]', '["深圳","香港"]', "qcc", SRC_WEINA, "智能音频与人机交互芯片；2024 年营收 1.46 亿元"),
    ("杭州拓尔微电子有限公司", "芯片设计", HZ, 2018, "陆鹏飞", 5000, "1-49 人", "", "91330100MA2B1A4X9M", '{"专利数":71,"资质":["国家级高新技术企业","省级专精特新中小企业"]}', "", "", "qcc", SRC_TUOER, "气流传感器与电源管理芯片；控制器全球市场份额约 60%"),
    ("杰华特微电子股份有限公司", "芯片设计", HZ, 2013, "马问问", 45032.1609, "1000-1999 人", "10 亿元以上", "91330100060994115M", '{"专利数":1216,"资质":["国家级专精特新小巨人","高新技术企业","制造业单项冠军","企业技术中心"]}', '[{"轮次":"股权融资","时间":"2025-12"},{"轮次":"IPO","时间":"2023","备注":"科创板 688141"}]', "", "qcc", SRC_JIEHUATE, "模拟芯片虚拟 IDM；2025 年营收 26.55 亿元"),
    ("杭州友旺电子有限公司", "芯片设计", HZ, 1994, "高耿辉", 300, "100-499 人", "1-5 亿元", "9133010060916630XC", '{"专利数":59,"资质":["国家级专精特新小巨人","高新技术企业","企业技术中心"]}', '[{"轮次":"设立","时间":"1994","备注":"台湾友顺科技与士兰微合资"}] ', "", "qcc", SRC_YOUWANG, "注册资本 300 万美元；集成电路与分立器件"),
    ("杭州晶华微电子股份有限公司", "芯片设计", HZ, 2005, "吕汉泉", 12089.1094, "100-499 人", "1-5 亿元", "91330108770816153N", '{"专利数":56,"资质":["国家级专精特新小巨人","高新技术企业"]}', '[{"轮次":"IPO","时间":"2022-07","备注":"科创板 688130"}]', '["上海","成都","深圳"]', "qcc", SRC_JINGHUA, "高性能模拟及数模混合芯片"),
    ("杭州雄迈集成电路技术股份有限公司", "芯片设计", HZ, 2015, "王军", 8695, "1-49 人", "", "913301833418469796", '{"专利数":229,"资质":["国家级知识产权优势企业","省级专精特新中小企业"]}', "", "", "qcc", SRC_CHENGXIN, "现名浙江芯劢微电子股份有限公司；视频音频芯片"),
    ("杭州美迪凯光电科技股份有限公司", "芯片设计", HZ, 2010, "葛文志", 41153.4378, "500-999 人", "", "913301015605619658", '{"专利数":78,"资质":["国家级专精特新小巨人","高新技术企业"]}', '[{"轮次":"IPO","时间":"2021-03","备注":"科创板 688079"}]', "", "qcc", SRC_MEIDIKAI, "光学光电子与半导体微纳电路"),
    ("浙江创芯集成电路有限公司", "晶圆制造", "浙江省杭州市萧山区", 2020, "高大为", 214766.6666, "100-499 人", "", "91330109MA2KC3HB0A", '{"专利数":742,"资质":["国家级专精特新小巨人","高新技术企业"]}', '[{"轮次":"A+轮","时间":"2026-02"}]', "", "qcc", SRC_CHUANGXIN, "12 英寸 55nm CMOS 集成电路公共创新平台；环节按实际制造业务归类"),
    ("杭州立昂东芯微电子有限公司", "先进封装", HZ, 2015, "王敏文", 21645.442, "100-499 人", "", "91330101MA27WBYG98", '{"专利数":8,"资质":["国家级高新技术企业","省级科技型中小企业"]}', '[{"轮次":"A轮"}]', "", "qcc", SRC_LIANANGDX, "6 英寸砷化镓化合物半导体芯片加工"),
    ("甬矽电子(宁波)股份有限公司", "先进封装", "浙江省宁波市", 2017, "王顺波", 45322.389, "5000 人以上", "10 亿元以上", "91330200MA2AFL8H97", '{"专利数":412}', '[{"轮次":"IPO","时间":"2022-11","备注":"科创板 688362"}]', "", "qcc", SRC_YONGSHI, "集成电路先进封装测试；2021 年营收 20.55 亿元"),
    ("中芯集成电路制造(绍兴)有限公司", "晶圆制造", "浙江省绍兴市", 2018, "赵奇", 838268.7172, "5000 人以上", "10 亿元以上", "91330600MA2BDY6H13", "", '[{"轮次":"IPO","时间":"2023-05","备注":"科创板 688469"}]', "", "qcc", SRC_ZHONGXINJIC, "现名芯联集成电路制造股份有限公司；2024 年营收 65.09 亿元"),
    ("浙江晶盛机电股份有限公司", "半导体设备", "浙江省绍兴市", 2006, "曹建伟", 130953.3797, "5000 人以上", "10 亿元以上", "913300007964528296", '{"专利数":728,"资质":["高新技术企业"]}', "", "", "qcc", SRC_JINGSHENG, "晶体生长炉与半导体材料制备设备；2023 年营收 106.38 亿元"),
    ("杭州众硅电子科技有限公司", "半导体设备", HZ, 2018, "尹志尧", 11562.0108, "100-499 人", "", "91330185MA2CC0D69L", '{"专利数":142}', '[{"轮次":"被收购","时间":"2026-03","备注":"中微公司收购 64.69% 股权，交易价 15.76 亿元"}]', '["杭州","上海"]', "qcc", SRC_ZHONGGUI, "现名中微众硅(杭州)电子科技有限公司；12 英寸 CMP 设备"),
    ("杭州海纳半导体有限公司", "半导体材料", "浙江省衢州市", 2002, "何昊", 11525.0576, "500-999 人", "", "913301087429442466", '{"专利数":51}', "", "", "qcc", SRC_HAINA, "现名浙江海纳半导体股份有限公司；单晶硅及半导体材料"),
    ("派恩杰半导体(杭州)有限公司", "半导体材料", HZ, 2024, "黄兴", 10, "1-49 人", "", "91330109MADR697Y55", '{"专利数":3,"资质":["省级科技型中小企业"]}', "", "", "qcc", SRC_PAIENJIE, "碳化硅功率器件；集团主体为派恩杰半导体(浙江)有限公司"),
    ("宁波康强电子股份有限公司", "半导体材料", "浙江省宁波市", 1992, "叶骥", 37528.4, "1000-1999 人", "10 亿元以上", "91330200610260897L", '{"专利数":144,"资质":["国家级专精特新小巨人","制造业单项冠军","隐形冠军企业"]}', '[{"轮次":"IPO","时间":"2007-03","备注":"深交所 002119"}]', "", "qcc", SRC_KANGQIANG, "引线框架与键合丝；2025 年营收 21.99 亿元"),
    ("浙江金瑞泓科技股份有限公司", "半导体材料", "浙江省宁波市", 2000, "李刚", 24236, "500-999 人", "10 亿元以上", "913302007204926720", '{"专利数":64,"资质":["国家级高新技术企业"]}', '[{"轮次":"被收购","时间":"2026","备注":"成为立昂微全资子公司"}]', '["衢州","嘉兴"]', "qcc", SRC_JINRUIHONG, "半导体硅片；曾用名宁波立立电子；2025 年营收 18.95 亿元"),
    ("宁波江丰电子材料股份有限公司", "半导体材料", "浙江省宁波市", 2005, "姚舜", 27597.1083, "1000-1999 人", "10 亿元以上", "91330200772311538P", '{"专利数":1221,"资质":["制造业单项冠军示范企业","高新技术企业"]}', '[{"轮次":"IPO","时间":"2017","备注":"创业板 300666"}]', "", "qcc", SRC_JIANGFENG, "超高纯金属溅射靶材；2025 年营收 46.04 亿元"),
    ("浙江洁美电子科技股份有限公司", "半导体材料", "浙江省湖州市", 2001, "方隽云", 45364.1963, "1000-1999 人", "10 亿元以上", "913305007272208214", '{"资质":["国家级制造业单项冠军示范企业","国家知识产权示范企业"]}', '[{"轮次":"IPO","时间":"2017-04","备注":"深交所 002859"}]', '["马来西亚","菲律宾"]', "qcc", SRC_JIEMEI, "电子封装载带与离型膜；2025 年营收 21.00 亿元"),
    ("宁波群芯微电子股份有限公司", "先进封装", "浙江省宁波市", 2018, "陈益群", 11000, "100-499 人", "1-5 亿元", "91330201MA2CJ1P58E", '{"专利数":99,"资质":["国家级专精特新小巨人","高新技术企业"]}', '[{"轮次":"A轮","时间":"2022"},{"轮次":"A+轮","时间":"2024-06"}]', "", "qcc", SRC_QUNXIN, "光耦与光传感器封装测试；曾用名宁波群芯微电子有限责任公司"),
    ("中巨芯科技股份有限公司", "半导体材料", "浙江省衢州市", 2017, "童继红", 147727.6, "500-999 人", "10 亿元以上", "91330802MA29U4396U", '{"专利数":4,"资质":["国家级科改企业"]}', '[{"轮次":"IPO","时间":"2023-09","备注":"科创板 688549"}]', "", "qcc", SRC_ZHONGJUXIN, "电子湿化学品、电子特气与前驱体材料；2025 年营收 12.12 亿元"),
    ("杭州集成电路测试公共服务中心(杭州芯云半导体技术有限公司)", "先进封装", HZ, 2020, "徐振", 135000, "500-999 人", "10 亿元以上", "91330108MA2HXBHQ77", '{"资质":["国家级高新技术企业","省级专精特新中小企业"]}', "", "", "qcc", SRC_XINYUN, "现名杭州芯云半导体集团有限公司；2025 年营收 20.91 亿元"),
]

ENTERPRISE_HEADER = [
    "name", "credit_code", "founded_year", "legal_person", "reg_capital",
    "employee_scale", "revenue_scale", "industry_code", "industry_name",
    "chain_segment", "region", "production_bases", "tech_qualifications",
    "investment_events", "source", "source_url",
]

# title, region, industry, policy_type, issuer, publish_date, eligibility, content, source_url
POLICIES = [
    ("杭州市人民政府办公厅关于促进集成电路产业高质量发展的实施意见", "浙江省杭州市", "集成电路", "研发补贴", "杭州市人民政府办公厅", "2022-07-15", "重点支持领域的高端芯片产品", "对重点支持领域的高端芯片产品，首次流片费用 1000 万元以上的，按照不超过其流片费用的 15% 给予补助，最高补助 2000 万元。", "https://www.hangzhou.gov.cn/art/2022/7/15/art_1229063382_1822591.html"),
    ("杭州市集成电路产业关键材料与核心设备研发投入补助", "浙江省杭州市", "集成电路", "研发补贴", "杭州市人民政府办公厅", "2022-07-15", "关键材料、核心设备自主研发投入 5000 万元以上并实现销售", "对集成电路关键材料、核心设备等自主研发投入 5000 万元以上并实现实际销售的，按照不超过其研发投入的 15% 给予补助，最高补助 5000 万元。", "https://www.hangzhou.gov.cn/art/2022/7/15/art_1229063382_1822591.html"),
    ("杭州市集成电路 EDA 工具技术攻关补助", "浙江省杭州市", "集成电路", "研发补贴", "杭州市人民政府办公厅", "2022-07-15", "EDA 工具自主研发投入 1000 万元以上并实现销售", "对开展 EDA 工具技术攻关，自主研发投入 1000 万元以上并实现实际销售的，按照不超过其自主研发投入的 15% 给予补助，最高补助 2000 万元。", "https://www.hangzhou.gov.cn/art/2022/7/15/art_1229063382_1822591.html"),
    ("杭州市集成电路重大项目用地与人才要素保障", "浙江省杭州市", "集成电路", "用地保障", "杭州市人民政府办公厅", "2022-07-15", "通过国家行业指导的市重大产业项目", "推荐重点项目纳入省重大项目库，对通过国家行业指导的市重大产业项目，统筹市区两级现有政策，做好项目用地、人才等要素保障。", "https://www.hangzhou.gov.cn/art/2022/7/15/art_1229063382_1822591.html"),
    ("关于进一步鼓励集成电路产业加快发展专项政策", "浙江省杭州市", "集成电路", "研发补贴", "杭州市人民政府办公厅", "2018-07-11", "集成电路产业研发投入 300 万元以上项目", "对集成电路产业研发投入超过 300 万元（含）以上项目，给予其实际研发投入的 20%、最高不超过 1000 万元的补助。", "https://zfgb.hangzhou.gov.cn/upload/default/bigfile/2025/06/04/20250604_c923fd6357be5772469d63b1714620e4.pdf"),
    ("杭州市集成电路企业购买 IP 补助", "浙江省杭州市", "集成电路", "研发补贴", "杭州市人民政府办公厅", "2018-07-11", "购买 IP 开展高端芯片、先进或特色工艺研发的企业", "对购买 IP 开展高端芯片、先进或特色工艺研发的集成电路企业，给予其购买 IP 直接费用的 30%、最高不超过 200 万元的补助。", "https://zfgb.hangzhou.gov.cn/upload/default/bigfile/2025/06/04/20250604_c923fd6357be5772469d63b1714620e4.pdf"),
    ("杭州市集成电路企业流片费用补助", "浙江省杭州市", "集成电路", "研发补贴", "杭州市人民政府办公厅", "2018-07-11", "进行重点支持领域工程产品流片的企业", "对进行重点支持领域工程产品流片的集成电路企业，给予其该款产品掩膜版制作费用的 50% 或首轮流片费用的 30%、最高不超过 300 万元的补助。", "https://zfgb.hangzhou.gov.cn/upload/default/bigfile/2025/06/04/20250604_c923fd6357be5772469d63b1714620e4.pdf"),
    ("杭州高新区（滨江）集成电路企业房租补贴", "浙江省杭州市", "集成电路", "租金补贴", "杭州高新区管委会", "2025-01-01", "新设立或新引进的集成电路企业，经芯火平台审核通过", "对新设立或新引进的集成电路企业，经芯火平台审核通过后，按照房租补贴人均面积和单价标准，给予最长三年、最高全额的房租补贴。", "http://www.hicc.org.cn/news-detail-580691.html"),
    ("杭州高新区（滨江）集成电路企业购买 EDA 工具补助", "浙江省杭州市", "集成电路", "研发补贴", "杭州高新区管委会", "2025-01-01", "集成电路企业购买 EDA 工具", "对集成电路企业购买 EDA 工具的，按照不超过实际发生费用的 20% 给予补贴，每家企业年度最高补贴 100 万元。", "https://zjjcmspublic.oss-cn-hangzhou-zwynet-d01-a.internet.cloud.zj.gov.cn/jcms_files/jcms1/web2945/site/attach/0/cd1d68feb5a7405098f73adbe3e001c5.pdf"),
    ("杭州高新区（滨江）芯片模组终端应用补贴", "浙江省杭州市", "集成电路", "落户奖励", "杭州高新区管委会", "2025-01-01", "终端厂商试用非关联集成电路企业首次上市的芯片或模组，年度采购 300 万元以上", "芯片、模组类当年度采购金额累计达 300 万元以上，按照最高不超过当年采购金额的 30% 给予补贴，每家企业最高补贴 150 万元。", "http://www.hicc.org.cn/news-detail-580691.html"),
]

POLICY_HEADER = [
    "title", "region", "industry", "policy_type", "issuer", "publish_date",
    "eligibility", "content", "source_url",
]


def write_csv(path, header, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def main():
    ent_rows = []
    for e in ENTERPRISES:
        (name, seg, region, founded, legal, capital, employee, revenue,
         credit, quals, events, bases, source, url, note) = e
        code, ind_name = INDUSTRY[seg]
        ent_rows.append([
            name, credit, founded, legal, capital, employee, revenue,
            code, ind_name, seg, region, bases, quals, events, source, url,
        ])
    write_csv(BASE / "企业数据.csv", ENTERPRISE_HEADER, ent_rows)

    write_csv(BASE / "政策数据.csv", POLICY_HEADER, POLICIES)
    print("企业数据.csv:", len(ent_rows), "条")
    print("政策数据.csv:", len(POLICIES), "条")

    from collections import Counter
    print("环节分布:", dict(Counter(r[9] for r in ent_rows)))


if __name__ == "__main__":
    main()

#coding:cp936
import xml.etree.ElementTree as ET
import fileinput
import re
import xml.dom.minidom as minidom

##utf8_encode = lambda x: x.encode("utf8") if type(x) == unicode else x
##utf8_decode = lambda x: x.decode("utf8") if type(x) == str else x
##loghead_pat = re.compile(r".*\[com.pos.http.dao.impl.DB_SALEDAOImpl\]-<\?xml version=\"1.0\" encoding=\"UTF-8\"\?>")
##xml_head = "<?xml version=\"1.0\"?>"
##print xml_head

#well_xml = r"d:\well.xml"
##logfile = r"d:\tcweb0302a.log"
##for line in fileinput.input(logfile):
##    m_loghead = loghead_pat.search(line)
##    if m_loghead:
##        utf8loghead = m_loghead.group(0)
##        line = line.replace(utf8loghead,xml_head)
#tree = ET.parse(well_xml)
#root = tree.getroot()
#for child in root:
#    print child.tag,'------------------'
#    for child2 in child:
#        print child2.tag,':',child2.text
    
#cdata = '20150302045757/HNCYX-75/52/1432410506110669/20150302051000/20150302115959/1/100/1/1432410506110669/0D5D3A529529F437309A42AB2156B54A/卓占力/1/1980-10-25/1/410222198010254517/卓占力/1/1980-10-25/1/410222198010254517/1/法定////23393481/0/无'
#data = cdata.split('/')
#n = 0
#for i in data:
#    print n,':',i
#    n+=1

def init_values():
    """ 返回一个值为空的输入项字典 """

    g.boxValue = g.boxPos.copy()
    for k in g.boxValue.keys():
        g.boxValue[k] = ''
    return g.boxValue


def change_xml_head(line):
    m_loghead = g.loghead_pat.search(line)
    if m_loghead:
        original_head = m_loghead.group()
        line = line.replace(original_head,g.xml_head)
        return line
    return 0


def parse_xml(logfile):
    """ 解析日志 """
    for line in fileinput.input(logfile):
        line = change_xml_head(line)
        if line:
            f=open(r"d:\temp.xml",'w')
            f.write(line)
            f.close()
            tree = ET.parse(r"d:\temp.xml")
            root = tree.getroot()
            for info_tag in root:
                for child in info_tag:
                    g.tag[child.tag] = child.text
            g.boxValue['posid'] = g.tag['POS_ID']
            g.boxValue['operid'] =  g.tag['OPER_ID']
            g.boxValue['opername'] = g.tag['OPER_NAME']
            parse_cdata(g.tag['REC_LIST'])
        for i in g.boxValue:
            print i

def parse_cdata(cdata):
    data = cdata.split('/')
    saledate = trans_date(data[0]) # 销售日期
    policyid = data[1]+data[2] # 方案代码
    voucherid = data[3] # 单证号码
    startdate = trans_date(data[4]) # 保单起期
    enddate = trans_date(data[5]) # 保单止期
    feeamt = data[7] # 保费
    bdid = data[9] # 保单号
    tbrname = data[11] # 投保人姓名
    tbridno = data[15] # 投保人id号码
    g.boxValue['voucherid'] = voucherid
    g.boxValue['bdid'] = bdid
    g.boxValue['policyid'] = policyid
    g.boxValue['saledate'] = saledate
    g.boxValue['startdate'] = startdate
    g.boxValue['enddate'] = enddate
    g.boxValue['feeamt'] = feeamt
    g.boxValue['tbrname'] = tbrname
    g.boxValue['tbridno'] = tbridno
    
def trans_date(date_str):
    date_pat = re.compile("(....)(..)(..)(..)(..)(..)")
    match = date_pat.search(date_str)
    year = match.group(1)
    month = match.group(2)
    day = match.group(3)
    hour = match.group(4)
    min = match.group(5)
    sec = match.group(6)
    return year+'-'+month+'-'+day+' '+hour+':'+min+':'+sec

class g(object):
    boxPos = {}
    boxValue = {}
    btnConfirmPos = [763,653] # 确定按钮的位置
    loghead_pat = re.compile(r".*\[com.pos.http.dao.impl.DB_SALEDAOImpl\]-<\?xml version=\"1.0\" encoding=\"UTF-8\"\?>")
    xml_head = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
    logfile = r"d:\well2.xml"
    tag = {}

g.boxPos = {
    # 该字典容纳保单录入各项在页面中的位置
    'voucherid':[575,204], # 单证号码
    'bdid':[1035,200], # 保单号
    'posid':[543,229], # 终端ID
    'policyid':[1027,229], # 业务方案代码
    'saledate':[540,258], # 销售日期
    'startdate':[531,282], # 保险起期
    'enddate':[1027,285], # 保险终期
    'operid':[576,313], # 操作员id
    'opername':[1023,312], # 操作员姓名
    'feeamt':[1017,338], # 保费（分）
    'tbrname':[534,365], # 投保人姓名
    'tbridno':[1022,391] # 投保人证件号码
    }

parse_xml(g.logfile)
for k,v in g.boxValue.items():
    print k,v
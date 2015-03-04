#coding:cp936
import xml.etree.ElementTree as ET
import fileinput
import re
import xml.dom.minidom as minidom

#utf8_encode = lambda x: x.encode("utf8") if type(x) == unicode else x
#utf8_decode = lambda x: x.decode("utf8") if type(x) == str else x
#loghead_pat = re.compile(r".*\[com.pos.http.dao.impl.DB_SALEDAOImpl\]-<\?xml version=\"1.0\" encoding=\"UTF-8\"\?>")
#xml_head = "<?xml version=\"1.0\"?>"
#print xml_head

well_xml = r"d:\well.xml"
#logfile = r"d:\tcweb0302a.log"
#for line in fileinput.input(logfile):
#    m_loghead = loghead_pat.search(line)
#    if m_loghead:
#        utf8loghead = m_loghead.group(0)
#        line = line.replace(utf8loghead,xml_head)
tree = ET.parse(well_xml)
root = tree.getroot()
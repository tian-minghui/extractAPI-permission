# coding=utf-8
'''
解析manifest.xml文件，将其中调用的权限读取出来
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
'''
import logging
import xml.sax
import os

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='log.log',
                    filemode='w')


class manifestHandler(xml.sax.ContentHandler):

    def __init__(self):
        self.currentdata=''
        self.permission=''

    def startElement(self, name, attrs):
        self.currentdata=name
        if self.currentdata=='uses-permission':
            permission=attrs['android:name']
            self.permission=permission

    def endElement(self, name):
        if self.currentdata=='uses-permission':
            permissionlist.append(self.permission)


def getxml(file):
    fs=os.listdir(file)
    for f in fs:
        if f=='AndroidManifest.xml':
            return os.path.join(file,f)
    return None

path=r'C:\Users\lenovo\Desktop\decompileresult\normal'
savepath=r'C:\Users\lenovo\Desktop\api&permission\permission\normal'
parser=xml.sax.make_parser()
parser.setContentHandler(manifestHandler())
files=os.listdir(path)
for file in files:
    print '正在处理%s'%file
    permissionlist=[]
    savefile=os.path.join(savepath,file)+'.txt'
    file=os.path.join(path,file)
    xmlfile=getxml(file)
    if xmlfile==None:
        logging.info('%s下无 AndroidManifest.xml'%file)
        continue
    parser.parse(xmlfile)
    with open(savefile,'w') as f:
        for permission in permissionlist:
            f.write(permission+'\n')
print 'end'

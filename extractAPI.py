# coding=utf-8

'''
从smali文件中抽取API调用
把此种个格式匹配出来，Landroid/os/Message;
'''

import re
import os
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='log.log',
                    filemode='w')


def getsmali(sourcepath):  # 遍历得到单个反编译产生文件夹下的所有smali文件
    if os.path.isfile(sourcepath) and sourcepath.endswith('.smali'):
        smalipath.append(sourcepath)
    else:
        files=os.listdir(sourcepath)
        for f in files:
            f=os.path.join(sourcepath,f)
            if os.path.isdir(f):
                getsmali(f)
            else:
                if f.endswith(".smali"):
                    smalipath.append(f)


def getapi(smalifile):    # 抽取单个文件的api，存入set中
    # Landroid/support/v4/content/LocalBroadcastManager$1;  含有$
    pattern=r'Landroid/[^;]+;'  # 匹配API的正字表达式
    try:
        with open(smalifile,'r') as f:
            for line in f:
                if '$' in line:
                    parts=line.split('$')
                    for part in parts:
                        list=re.findall(pattern,part)
                        for i in list:
                            apiset.add(i[1:len(i)-1])
                else:
                    list=re.findall(pattern,line)
                    for i in list:
                        apiset.add(i[1:len(i)-1])
    except IOError:
        logging.error(smalifile)
        return -1


path=r'C:\Users\lenovo\Desktop\decompileresult\normal'
savepath=r'C:\Users\lenovo\Desktop\api&permission\api\malware'
defiles=os.listdir(path)
for defile in defiles:
    defile=os.path.join(path,defile)
    if len(os.listdir(defile))==0:
        logging.info("%s为空"%defile)
    print '正在处理%s'%defile
    smalipath=[]
    apiset=set()
    getsmali(defile)
    for smalifile in smalipath:
        getapi(smalifile)
        if getapi(smalifile)==-1:
            continue
    savefile=os.path.join(savepath,os.path.split(defile)[1])+'.txt'
    with open(savefile,'w') as f:
        for api in apiset:
            f.write(api+'\n')

print 'end'
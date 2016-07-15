# coding=utf-8
import os
import ConfigParser
apkList=[]


def getAllApk(sourcepath):         # 递归得到所有apk文件
    if os.path.isfile(sourcepath):## and sourcepath.endswith('.apk'):
        if os.path.getsize(sourcepath)<16000000:
            apkList.append(sourcepath)
    else:
        files=os.listdir(sourcepath)
        for f in files:
            f=os.path.join(sourcepath,f)
            if os.path.isfile(f): ##and sourcepath.endswith('.apk'):
                if os.path.getsize(sourcepath)<2400000:
                    apkList.append(f)
            else:
                getAllApk(f)
    return


def decompile(apkFile,savepath):   # 用apktool反编译单个apk文件
    global successnum
    global failturenum
    apkFile=apkFile.encode('gbk')
    os.chdir(savepath)    # 切换到要保存的路径
    cmd="apktool d %s"%apkFile       # 执行两个连续的命令
    process=os.popen(cmd)
    text=process.read()
    process.close()
    result=text.decode('gbk')
    if 'Copying' in result:
        successnum=successnum+1
        print '%s success'%apkFile.decode('gbk')
    else:
        failturenum=failturenum+1
        print '%s decompilation Failure'%apkFile.decode('gbk')            # 反编译失败会产生空的文件夹
        # print result

config=ConfigParser.ConfigParser()
config.read('init.ini')
sourcepath=unicode(config.get('Opcode','sourcepath'),'utf-8')
savepath=config.get('Opcode','savepath')
print "The sourcepath is "+sourcepath
print "The savepath is "+savepath

successnum=0
failturenum=0
getAllApk(sourcepath)
for apk in apkList:
    decompile(apk,savepath)
print '-----------------------------------------------'
print '总apk数为'+str(len(apkList))
print '以下统计仅供参考'
print '反编译成功%s个'%successnum
print '反编译失败%s个'%failturenum
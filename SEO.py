import argparse
import sys
import requests
import re

#参数自定义

parser = argparse.ArgumentParser()
parser.add_argument('-r', dest='read', help='path file')
parser.add_argument('-u',dest='read',help='targetdomain')
parser_args = parser.parse_args()
#爬虫模块查询

def askurl(target_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'
    }


    #baidu权重
    baidu_url=f"https://rank.chinaz.com/{target_url}"
    baidu_txt=requests.get(url=baidu_url,headers=headers)
    baidu_html=baidu_txt.content.decode('utf-8')
    baidu_PC=re.findall('PC端</i><img src="//csstools.chinaz.com/tools/images/rankicons/baidu(.*?).png"></a></li>',baidu_html,re.S)
    baidu_moblie=re.findall('移动端</i><img src="//csstools.chinaz.com/tools/images/rankicons/bd(.*?).png"></a></li>',baidu_html,re.S)
    #分割线
    print("*"*60)

    #如果查询html中有正则出来到权重关键字就输出，否则将不输出
    if len(baidu_PC) > 0:
        print('百度_PC:', baidu_PC[0])
    if len(baidu_moblie) > 0:
        print('百度_moblie:', baidu_moblie[0])
    else:
        print("百度无权重")


    #360权重
    url=f"https://rank.chinaz.com/sorank/{target_url}/"
    text = requests.get(url=url,headers=headers)
    html=text.content.decode('utf-8')
    sorank360_PC=re.findall('PC端</i><img src="//csstools.chinaz.com/tools/images/rankicons/360(.*?).png"></a><',html,re.S)
    sorank360_Mobile=re.findall('移动端</i><img src="//csstools.chinaz.com/tools/images/rankicons/360(.*?).png"',html,re.S)

    # 如果查询html中有正则出来到权重关键字就输出，否则将不输出
    if len(sorank360_PC) > 0:
        print("360_PC:", sorank360_PC[0])
    if len(sorank360_Mobile) > 0:
        print("360_moblie:", sorank360_Mobile[0])
    else:
        print("360无权重")



    #搜狗权重
    sogou_url = f"https://rank.chinaz.com/sogoupc/{target_url}"
    sougou_txt = requests.get(url=sogou_url, headers=headers)
    sougou_html = sougou_txt.content.decode('utf-8')
    sougou_PC = re.findall('PC端</i><img src="//csstools.chinaz.com/tools/images/rankicons/sogou(.*?).png"></a></li>',sougou_html, re.S)
    sougou_moblie = re.findall('移动端</i><img src="//csstools.chinaz.com/tools/images/rankicons/sogou(.*?).png"></a></li>',sougou_html, re.S)

    # 如果查询html中有正则出来到权重关键字就输出，否则将不输出
    if len(sougou_PC) > 0:
        print('搜狗_PC：', sougou_PC[1])
    if len(sougou_moblie) > 0 :
        print('搜狗_moblie：', sougou_moblie[1])
    else:
        print('搜狗无权重')



    #神马权重
    shenma_url=f'https://rank.chinaz.com/smrank/{target_url}'
    shenma_txt=requests.get(url=shenma_url,headers=headers)
    shenma_html=shenma_txt.content.decode('utf-8')
    shenma_PC=re.findall('class="tc mt5"><img src="//csstools.chinaz.com/tools/images/rankicons/shenma(.*?).png"></a></li>',shenma_html,re.S)

    # 如果查询html中有正则出来到权重关键字就输出，否则将不输出
    if len(shenma_PC) > 0:
        print('神马权重为：', shenma_PC[1])
    else:
        print("神马无权重")


    #头条权重
    toutiao_url=f'https://rank.chinaz.com/toutiao/{target_url}'
    toutiao_txt=requests.get(url=toutiao_url,headers=headers)
    toutiao_html=toutiao_txt.content.decode('utf-8')
    toutiao_PC=re.findall('class="tc mt5"><img src="//csstools.chinaz.com/tools/images/rankicons/toutiao(.*?).png"></a></li>',toutiao_html,re.S)

    # 如果查询html中有正则出来到权重关键字就输出，否则将不输出
    if len(toutiao_PC) > 0:
        print('头条权重为：', toutiao_PC[1])
    else:
        print("头条无权重")



    #备案信息、title、企业性质
    beian_url=f"https://seo.chinaz.com/{target_url}"
    beian_txt=requests.get(url=beian_url,headers=headers)
    beian_html=beian_txt.content.decode('utf-8')

    beian_info=re.findall('target="_blank" style="color:#4192E7">(.*?)</a>',beian_html,re.S)
    title=re.findall('<title>站长工具 -(.*?)的SEO综合查询</title>',beian_html)
    Enterprise=re.findall('<span class="mr50">性质：<i class="color-63">(.*?)</i></span>',beian_html,re.S)
    ip=re.findall(r'[0-9]+(?:\.[0-9]+){3}',beian_html,re.S)
    try:
        print("备案信息:","名称:",beian_info,"网站首页Title：",title,"企业性质：",Enterprise,"IP地址为：",ip[1])
        print("*"*60)
    except:
        print("没有查询到有效信息！")




def url_batch():
    #读取-r参数传入的数值
    path_file=parser_args.read
    print('输入文件路径为：',path_file)
    munber = 1
    #读取文件，处理字符，去除http/https字符
    #try:
    with open(path_file,'r',encoding='UTF-8') as file:
        lin = file.readlines()
        for i in lin:
            urls = i.strip(f"\n")
            if 'http://' in urls:
                file = urls[7:]
            elif 'https://' in urls:
                file = urls[8:]
            else:
                file = urls
            print(f'正在查询第{munber}个网站查询：',file)
            munber += 1
            askurl(file)

#单次domain检测
def url():
    urls = parser_args.read
    try:
        if "http://" in urls:
            url = urls[7:]
        elif "https://" in urls:
            url = urls[8:]
        askurl(url)
    except:
        print(" [*] Please enter the complete domain name!")

def main():
    try:
        ls = sys.argv[1]
        if '-r' in ls:
            url_batch()
        else:
            url()
    except:
        parser.print_help()


if __name__ == '__main__':
    main()



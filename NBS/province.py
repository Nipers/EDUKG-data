import requests
import time
import pandas as pd
import os
import json
import warnings
import socket
import socks
agent={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
basepath='province'
if not os.path.exists(basepath):
    os.mkdir(basepath)
warnings.filterwarnings('ignore')#对应后文verify=false,这样就不用每次运行都跳出来一个warning
baseurl='https://data.stats.gov.cn/easyquery.htm'
dbcode,wdcode,rowcode,colcode='fsnd','zb','zb','sj'
def retry(url,params,headers):
    socks.set_default_proxy(socks.SOCKS5, "tps339.kdlapi.com", 20818)
    socket.socket = socks.socksocket
    while True:
        try:
            req=requests.get(url,params=params,headers=headers,verify=False)
            req.encoding=req.apparent_encoding
            trans_dict=json.loads(req.text)
            break
        except:#请求的html网页均为json型，如果解析出错，则为请求过多暂未相应，等待并持续请求即可
            time.sleep(2)
            print('服务器繁忙')
    return trans_dict
#定义爬取函数
def packcsv(valuecode,path):
    zhibiao_info={'m':'getOtherWds','dbcode':dbcode,'rowcode':'reg','colcode':colcode,
                  'wds':'[{"wdcode":"zb","valuecode":"%s"}]'%valuecode,'dfwds':'[]',
                  'k1':str(int(time.time()*1000))}
    trans_dict=retry(baseurl,zhibiao_info,agent)
    choose_range=trans_dict['returndata'][0]['nodes']
    matchdict={each['code']:each['name'] for each in choose_range}
    count_time=0
    for each in matchdict:
        zb_name=matchdict[each]
        each_csv=pd.DataFrame(columns=['省份编码','省份','年份',zb_name])
        base_can={'m':'QueryData','dbcode':dbcode,'rowcode':'reg','colcode':colcode,
                  'wds':'[{"wdcode":"zb","valuecode":"%s"}]'%each,
                  'dfwds':'[{"wdcode":"zb","valuecode":"%s"},{"wdcode":"sj","valuecode":"2000-2019"}]'%each,
                  'k1':str(int(time.time()*1000))}
        trans_dict=retry(baseurl,base_can,agent)
        province_code=trans_dict['returndata']['wdnodes'][1]['nodes']
        province_dict={each['code']:each['cname'] for each in province_code}
        totaldata=trans_dict['returndata']['datanodes']
        for i in totaldata:
            match_year=int(i['wds'][2]['valuecode'])
            match_code=i['wds'][1]['valuecode']
            match_province=province_dict[match_code]
            if i['data']['hasdata']:
                match_data=i['data']['data']
            else:
                match_data=float('nan')
            each_csv=each_csv.append({'省份编码':match_code,'省份':match_province,
                                      '年份':match_year,zb_name:match_data},ignore_index=True)
        try:
            csv=pd.merge(csv,each_csv,on=['省份','年份','省份编码'],how='outer')
        except NameError:
            csv=each_csv
        count_time+=1
        print('写表完成%.2f%%'%(100*count_time/len(matchdict)))
    csv.to_csv(path,index=False)
code_path={'zb':basepath}
while code_path:
    each_root={}
    for each in code_path:
        add_can={'id':each,'dbcode':dbcode,'wdcode':wdcode,'m':'getTree'}
        root_req=retry(baseurl,add_can,agent)
        for i in root_req:
            rootname=i['name'].replace('/','每')
            idsign=i['id']
            makedir=code_path[each]+'/'+rootname
            if i['isParent']:
                if not os.path.exists(makedir):
                    os.mkdir(makedir)
                    print('已创建路径%s'%makedir)
                else:
                    print('已有路径%s'%makedir)
                each_root[idsign]=makedir
            else:
                print('正在写表,对应路径为%s'%(makedir+'.csv'))
                packcsv(idsign,makedir+'.csv')
                print('写表完成')
    code_path=each_root
import requests
import time
import pandas as pd
import os
import json
import warnings

import socket
import socks

agent={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
basepath='national'
if not os.path.exists(basepath):
    os.mkdir(basepath)
warnings.filterwarnings('ignore')
baseurl='https://data.stats.gov.cn/easyquery.htm'
dbcode,wdcode,rowcode,colcode='hgnd','zb','zb','sj'
def retry(url,params,headers):
    
    socks.set_default_proxy(socks.SOCKS5, "tps339.kdlapi.com", 20818)
    socket.socket = socks.socksocket
    while True:
        try:
            req=requests.get(url,params=params,headers=headers,verify=False)
            req.encoding=req.apparent_encoding
            trans_dict=json.loads(req.text)
            break
        except:
            time.sleep(2)
            print('服务器繁忙')
    return trans_dict
#定义爬取函数
def packcsv(valuecode,path):
    base_can={'m':'QueryData','dbcode':dbcode,'rowcode':rowcode,'colcode':colcode,
              'wds':'[]','dfwds':'[{"wdcode":"zb","valuecode":"%s"},{"wdcode":"sj","valuecode":"2000-2019"}]'%valuecode,
              'k1':str(int(time.time()*1000))}
    trans_dict=retry(baseurl,base_can,agent)
    row_loc=trans_dict['returndata']['wdnodes'][0]['nodes']
    totaldata=trans_dict['returndata']['datanodes']
    frame_dict={each['code']:pd.DataFrame(columns=['年份',each['cname']]) for each in row_loc}
    for i in totaldata:
        match_year=int(i['wds'][1]['valuecode'])
        match_code=i['wds'][0]['valuecode']
        match_row=list(frame_dict[match_code].columns)[-1]
        if i['data']['hasdata']:
            match_data=i['data']['data']
        else:
            match_data=float('nan')
        eachcsv=frame_dict[match_code]
        eachcsv=eachcsv.append({'年份':match_year,match_row:match_data},ignore_index=True)
        frame_dict[match_code]=eachcsv
    for i in frame_dict:
        try:
            csv=pd.merge(csv,frame_dict[i],how='outer',on=['年份'])
        except NameError:
            csv=frame_dict[i]
    csv['年份']=csv['年份'].astype("int64")
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

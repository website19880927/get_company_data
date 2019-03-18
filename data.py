#获取集团公司内部文件爬虫
import json,re

import requests

s = 0
while s<19000:
    try:
        data={
        "start": s,
        "limit":50
        }
        headers={
                 "Host":"echdoc.ztjs.cn",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                "Referer": "http://techdoc.ztjs.cn/sgsz/pages/byproject.htm?command=detail&node=root",
                "Cookie": "JSESSIONID=29FE395C43BBDDF64DBDEEA223E91E99"}
        url='http://techdoc.ztjs.cn/sgsz/pages/byproject.htm?command=grid&node=root&searchtype=0'
        html=requests.post(url,data=data,headers=headers)
        text= html.text.encode('latin-1').decode('unicode_escape')
        dic = json.loads(text)['results']
        for n in dic:
            print(n['id'])

            res = requests.get('http://techdoc.ztjs.cn/sgsz/pages/sgsz/view/'+str(n['id'])+'.htm', headers=headers).text
            inner_id = re.findall(r'objid=(.*?)&', res)[0]
            print("inner_id",inner_id)
            url3 = 'http://techdoc.ztjs.cn/sgsz/pages/sgsz/doc/' + str(inner_id) + '.htm'
            res2 = requests.get(url3, headers=headers).text
            transfer_id = re.findall(r'javascript:viewDoc\((.*?)\)', res2)[0]
            print("transfer_id",transfer_id)
            url4 = 'http://techdoc.ztjs.cn/sgsz/commons/attachment/viewpdf/' +transfer_id + '.pdf'

            res3 = requests.get(url4, headers=headers).content
            path = r'./file/' + transfer_id + '.pdf'

            with open(path, 'wb') as f:
                f.write(res3)

        print('time',s)
        s+=50
    except Exception as e:
        print('error...',e)
        pass
        s += 50

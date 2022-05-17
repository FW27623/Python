# -*- coding = utf-8 -*-

import json
import re
import time
import datetime
import requests
from requests_toolbelt import SSLAdapter
s = requests.Session()
adapter = SSLAdapter('TLSv1')
s.mount('https://', adapter)
result = s.get(url='https://lib-seat.chu.edu.cn', verify=False)


def main():
    cur_time = time.strftime("%H:%M:%S", time.localtime())
    flag = True
    while cur_time < '00:10:00':
        if flag is True:
            print('当前时段暂不可预约')
            flag = False
        cur_time = time.strftime("%H:%M:%S", time.localtime())
    cur_date = datetime.date.today()
    tor_date = cur_date + datetime.timedelta(days=1)
    tor_date = str(tor_date)
    session, header = login()
    v_number = validation(session, header)
    reserve(v_number, session, header, tor_date, 50)


# 用于验证登录是否成功
def verify_login(url):
    order_page = ''
    if url == order_page:
        print('登录成功')
    else:
        print('登录失败')


# 该登录函数利用客户端的cookie信息完成登录，首次使用需要手动登录并获取cookie
def login(cookies=None):
    session = requests.session()
    if cookies is None:
        cookies = 'ASP.NET_SessionId=zczis3uo2mh1lgz2oemp4e23; _d_id=a6421249b13e7b73f2093536ec85a8'  # 这里是cookies

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        'Connection': 'keep-alive',
        'Cookie': 'ASP.NET_SessionId=zczis3uo2mh1lgz2oemp4e23; _d_id=a6421249b13e7b73f2093536ec85a8'
    }
    order_page = 'https://lib-seat.chu.edu.cn/ClientWeb/xcus/ic2/Default.aspx'  # 这里是预约系统的URl地址
    res = session.get(url=order_page, headers=header)
    verify_login(res.url)
    return session, header


# 该函数用于获得验证码的取值
def validation(session, header):
    valid_page = ''
    val_params = {
        'act': 'SetNumberCode'
    }
    res = session.get(url=valid_page, params=val_params, headers=header)
    res_text = json.loads(res.text)
    pic_num = []
    v_number = 0
    for i in range(4):
        tmp = re.search(r'(\D*)(\d)(\D*)', res_text['data'][i])
        pic_num.append(int(tmp.group(2)))
    if res_text['data'][4] == '-':
        v_number = pic_num[0] * 10 + pic_num[1] - (pic_num[2] * 10 + pic_num[3])
    else:
        v_number = pic_num[0] * 10 + pic_num[1] + (pic_num[2] * 10 + pic_num[3])
    return v_number


# 目前仅支持西土城校区401室，4S-001-4S-072号座位的选择
# 若未指定座位号则默认搜索所有可用座位
def reserve(v_number, session, header, date, seat_num=None):
    tot_num = 73
    flag = True
    reserve_page = ''
    if seat_num is not None:
        dev_id = seat_num + 100455385
        res_param = {
            'dialogid': '',
            'dev_id': str(dev_id),
            'lab_id': '100455370',
            'kind_id': '100455359',
            'room_id': '100455376',
            'type': 'dev',
            'prop': '1',
            'test_id': '',
            'term': '',
            'Vnumber': str(v_number),
            'classkind': '',
            'test_name': '',
            'start': date + ' 05:30',
            'end': date + ' 21:00',
            'start_time': '0530',
            'end_time': '2100',
            'up_file': '',
            'memo': '',
            'act': 'get_rsv_sta'
        }
        res = session.get(url=reserve_page, headers=header, params=res_param)
        tmp = json.loads(res.text)
        if tmp['msg'] == '操作成功！':
            print('------------------------')
            print('预约成功')
            print('座位号：', '4S-%03d' % seat_num)
            print('------------------------')
            return
        else:
            print(tmp['msg'])
            print('正在搜索其他座位...')
            flag = False
    for seat_num in range(20, tot_num):
        dev_id = seat_num + 105107154
        res_param = {
            'dialogid': '',
            'dev_id': str(dev_id),
            'lab_id': '',
            'kind_id': '',
            'room_id': '',
            'type': 'dev',
            'prop': '',
            'test_id': '',
            'term': '',
            'Vnumber': str(v_number),
            'classkind': '',
            'test_name': '',
            'start': date + ' 08:00',
            'end': date + ' 21:00',
            'start_time': '0800',
            'end_time': '2100',
            'up_file': '',
            'memo': '',
            'act': 'set_resv'
        }
        res = session.get(url=reserve_page, headers=header, params=res_param)
        tmp = json.loads(res.text)
        if tmp['msg'] == '操作成功！':
            print('------------------------')
            print('预约成功')
            print('座位号：', '4S-%03d' % seat_num)
            print('------------------------')
            return
        else:
            if flag is True:
                print('搜索全部座位...')
                flag = False
            else:
                print('进度：%.2f%%' % (seat_num * 100.0 / (tot_num - 1)))
    print('当天已无可预约座位')


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print('耗时：%.2fs' % (end_time - start_time))

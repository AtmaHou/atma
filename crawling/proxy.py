# coding=utf-8
import datetime
import urllib2
import time
import random
import requests
file_proxy_list_path = './available_proxies.txt'


def random_sleep(min_sleep=0, max_sleep=1, sleep=True):
    if not sleep:
        return 0
    sleep_time = random.random() * (max_sleep - min_sleep) + min_sleep
    # print 'sleeping %f seconds' % sleep_time
    time.sleep(sleep_time)
    return sleep_time


def now_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def mark(s):
    print now_time() + ":  " + s


class Crawler:
    proxys = []
    proxy_id = 0
    error_int = []
    succ_hint = []
    cnt = 0
    threshold = 0

    def __init__(self, proxy_lst, error_hint, succ_hint, start_point, threshold=1000):
        # proxy list source  ----   http://www.cnproxy.com/proxy4.html
        self.proxys = proxy_lst[:]  # to get a totally new list
        # print 'Good proxy: %d' % len(self.proxys)
        self.error_hint = error_hint
        self.succ_hint = succ_hint
        self.threshold = threshold
        self.proxy_id = start_point

    def change_proxy(self):
        self.proxy_id = (self.proxy_id + 1) % len(self.proxys)
        self.cnt = 0
        # print 'change to proxy %d' % self.proxy_id

    def fetch(self, url):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, peerdist',
            'Accept-Language': 'en-US,en;q=0.8,zh;q=0.6,zh-CN;q=0.4',
            'Connection': 'keep-alive',
            'Cookie': '''mt.v=2.800341339.1484641866969; NVTC=248326808.0001.412401979.1484641866.1486545307.1490419272.3; s_fid=32F3F49644163CD6-3715DBD5117087C9; s_pers=%20productnum%3D2%7C1493011287346%3B%20s_vs%3D1%7C1490421088995%3B%20gpv_pv%3Dhomepage%7C1490421089003%3B%20s_nr%3D1490419289007-Repeat%7C1521955289007%3B%20gpvch%3Dbrowsing%7C1490421089010%3B; utag_main=_st:1490421088557$dc_visit:3$ses_id:1490420214940%3Bexp-session$dc_event:2%3Bexp-session$dc_region:us-east-1%3Bexp-session; s_vi=[CS]v1|2C3EEB2605193C7F-40000602E00011D5[CE]; _ga=GA1.2.375131326.1484641869; __utma=248326808.375131326.1484641869.1484641869.1486545310.2; __utmz=248326808.1484641869.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); spid=B8838794-3BCF-476C-B3A3-BFD11922E669; needlepin=N190d148464187178400013007c8abe4c7c8abe4c00000000000000000000000000000000; __gads=ID=98601ecb817002c8:T=1484641873:S=ALNI_MYcaQSi-s3Qu9yIt4zrcweqWw_QRQ; _sckey=mb6-589ae1a577b217.10048629; NV%5FDVINFO=#5%7B%22Sites%22%3A%7B%22USA%22%3A%7B%22Values%22%3A%7B%22w19%22%3A%22Y%22%7D%2C%22Exp%22%3A%221490505673%22%7D%7D%7D; NV%5FSPT=0-0-0; NV_NVTCTIMESTAMP=1490419284; s_sess=%20s_cpc%3D0%3B%20s_ev3%3Dnon-internal%2520campaign%3B; s_cc=true; mt.visits=%7B%22lastVisit%22:1490419288511,%22visits%22:%5B1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0%5D%7D; NV%5FCOUNTRY=#5%7B%22Sites%22%3A%7B%22USA%22%3A%7B%22Value%22%3A%22U%22%2C%22Exp%22%3A%221493011274%22%7D%7D%7D; _gat=1; needleopt=Saant0-usOnly; NV%5FCONFIGURATION=#5%7B%22Sites%22%3A%7B%22USA%22%3A%7B%22Values%22%3A%7B%22wd%22%3A%220%22%2C%22w58%22%3A%22USD%22%2C%22w57%22%3A%22USA%22%7D%2C%22Exp%22%3A%221576819285%22%7D%7D%7D; mp_newegg_mixpanel=%7B%22distinct_id%22%3A%20%22159ab8d1d1ecb9-0a54333130ef888-20d1644-108924-159ab8d1d1ff57%22%7D; _scsess=sess-8-58d5fe5a41a802.74806601; NV%5FLOCALSTORAGE={"w3":{"value":"[\"N82E16834299753|56751288\",\"N82E16834317469|32633610\"]","date":1486545336752},"w59":{"value":"\"0\"","date":1490419285158},"w8":{"value":"\"expand\"","date":1486545337713}}; s=undefined; ADCOOKIE=2''',
            'Host': 'www.newegg.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586'
        }
        if self.cnt > self.threshold:
            self.change_proxy()

        raw_html = ''
        # while True:
        max_try = 10
        for i in range(max_try):
            try:
                # print 'fetching with ', self.proxys[self.proxy_id]
                # there are several possible proxy type: http, socks5, socks4 (Note that there is no https) --- Atma
                proxy_url = self.proxys[self.proxy_id][1].lower() + '://' + self.proxys[self.proxy_id][0]
                proxy_dict = {"https": proxy_url, "http": proxy_url}
                raw_html = requests.get(url, headers=headers, timeout=10, proxies=proxy_dict).content  # .decode('utf-8')
                self.cnt += 1
                is_succ = True
                for error_hint in self.error_hint:
                    if raw_html.find(error_hint) >= 0:
                        random_sleep(min_sleep=3, max_sleep=10)
                        is_succ = False
                        print 'wrong page error: %s' % error_hint
                for succ_hint in self.succ_hint:
                    if raw_html.find(succ_hint) < 0:
                        random_sleep(min_sleep=3, max_sleep=10)
                        is_succ = False
                    else:
                        is_succ = True
                        break
                if is_succ:
                    break
            except Exception as e:
                # print '*** Exception error ***\n', e, '\n****************\n'
                random_sleep(min_sleep=3, max_sleep=10)
            self.change_proxy()
        time.sleep(1)
        return raw_html


if __name__ == '__main__':
    test_proxy_lst = []
    with open(file_proxy_list_path, 'r') as reader:
        for line in reader:
            test_proxy_lst.append(line.split('\t')[0])
    start_pos = random.randint(0, len(test_proxy_lst) - 1)
    test_proxy = Crawler(
        proxy_lst=test_proxy_lst,
        error_hint=["Of course you're not", '502 error', '500 error', 'are robot'],
        succ_hint=['newegg'],
        start_point=start_pos,
        threshold=3
    )
    # test_url = 'https://www.newegg.com/'
    test_url = r'https://www.newegg.com/Product/Product.aspx?Item=9SIA8X55CJ0960&cm_re=Touch-Screen_All-In-One_i3-_-9SIA8X55CJ0960-_-Product'
    print '==============test crawler==============='
    print test_proxy.fetch(test_url).split('\n')[:10]

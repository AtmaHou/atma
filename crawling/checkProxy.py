# coding=utf-8
import requests
import socket
import sys
import proxy
import time
import random
from multiprocessing import Process, Queue, current_process, freeze_support, Manager
N_THREAD = 30
file_proxy_list_path = './available_proxies.txt'
# url = r'http://www.cnproxy.com/proxy1.html'
# host = 'www.cnproxy.com'
# success_mark = "IP:Port"
url = r'https://www.newegg.com/Product/Product.aspx?Item=9SIA8X55CJ0960&cm_re=Touch-Screen_All-In-One_i3-_-9SIA8X55CJ0960-_-Product'
host = 'www.newegg.com'
success_mark = "Windows 10 operating system"

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'en-US,en;q=0.8,zh;q=0.6,zh-CN;q=0.4',
    'Connection': 'keep-alive',
    # 'Cookie': '''__gads=ID=4b42b08f519692dd:T=1483078845:S=ALNI_MaSgejQU-fJOXCO9rzj825KTBSlFQ; sr_browser_id=8cbcf2aa-5b55-4902-9f9f-769800532a06; s=undefined; XCLGFbrowser=CxcsM1h6PUkEFFiqGIk; _sckey=mb5-587dbc0342e0e3.74144148; __utma=248326808.125608968.1486542211.1487148263.1487220057.7; __utmz=248326808.1486897823.4.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); NV%5FNEWGOOGLE%5FANALYTICS=#5%7B%22Sites%22%3A%7B%22USA%22%3A%7B%22Values%22%3A%7B%22w14%22%3A%221%22%7D%2C%22Exp%22%3A%221491374501%22%7D%7D%7D; NV%5FCOUNTRY=#5%7B%22Sites%22%3A%7B%22USA%22%3A%7B%22Value%22%3A%22U%22%2C%22Exp%22%3A%221491374502%22%7D%7D%7D; NV%5FSPT=0-0-0; _scsess=sess-2-58cf68cda6f816.66960875; TT3bl=false; TURNTO_VISITOR_SESSION=1; inptime0_147_us=0; aam_uuid=46035231921600107160626138908001972026; NV%5FDVINFO=#5%7B%22Sites%22%3A%7B%22USA%22%3A%7B%22Values%22%3A%7B%22w19%22%3A%22Y%22%2C%22w51%22%3A%22T%255FtxwRzebUCEBreeu1ptc0LN6pvImivl65o3%252B0LEVXdCYxrUEQvT5XHdvpbpsUgLUZ%22%7D%2C%22Exp%22%3A%221490374400%22%7D%7D%7D; s_sq=%5B%5BB%5D%5D; TURNTO_TEASER_SHOWN=1490290072618; spid=3D231A5D-1DF6-4B6B-96B2-46DAD9BC7372; NV%5FCONFIGURATION=#5%7B%22Sites%22%3A%7B%22USA%22%3A%7B%22Values%22%3A%7B%22wd%22%3A%220%22%2C%22w58%22%3A%22USD%22%2C%22w57%22%3A%22USA%22%2C%22w39%22%3A%226676%22%7D%2C%22Exp%22%3A%221576722809%22%7D%7D%7D; NV%5FLOCALSTORAGE={"w3":{"value":"[\"34-154-494|964225\",\"34-295-406|0\",\"34-100-881|72705826\",\"34-100-880|74720887\",\"1TS-000A-00DC8|33442025\",\"0VG-0041-00056|59293752\",\"34-735-072|271623\",\"83-285-460|66989257\",\"N82E16883285461|66895647\",\"2TS-0008-001N7|1591449\",\"1TS-000D-00Z43|56446755\",\"83-286-052|1910577\",\"1VK-001E-04H22|57674432\",\"0EJ-004A-00041|53941909\",\"1TS-000D-01G86|72715371\"]","date":1490290072147},"w59":{"value":"\"0\"","date":1490322809966},"w8":{"value":"\"expand\"","date":1490290072418},"w2":{"value":"\"10|MSI GL62M,dell xps,macbook,dell opt,surface 4gb,surface 4bg,surface,suface,HP - 23.8\\\" Touch-Screen All-In-One i3,acer\"","date":1490288007654},"w4":{"value":"\"10|MSI GL62M,dell xps,macbook,dell opt,surface 4gb,surface 4bg,suface,HP - 23.8\\\" Touch-Screen All-In-One i3,Samsung Galaxy Tab A,acer\"","date":1490288008518}}; NVTC=248326808.0001.536543056.1486542207.1490290071.1490322809.24; NV_NVTCTIMESTAMP=1490322809; s_cc=true; mt.visits=%7B%22lastVisit%22:1490322810595,%22visits%22:%5B1,5,2,0,1,0,0,0,0,0,0,0,0,0,0,0,4,2,2,0,0,0,0,0,0,0,0,0,0,0%5D%7D; mt.v=2.1468950765.1486542207683; _ga=GA1.2.125608968.1486542211; _gat=1; mp_newegg_mixpanel=%7B%22distinct_id%22%3A%20%2215a1cd20aee6c-00675d7da988d9-3d654d08-140000-15a1cd20aef461%22%7D; utag_main=_st:1490324610722$dc_visit:24$ses_id:1490323697566%3Bexp-session$dc_event:1%3Bexp-session$dc_region:us-east-1%3Bexp-session; cid_csid=4fbc818f-2246-4208-8778-6df5a6b115d8; ADCOOKIE=11; s_vi=[CS]v1|2C4D6AC1050303D7-60001187A0007A6D[CE]; NV%5FPRDLIST=#5%7B%22Sites%22%3A%7B%22USA%22%3A%7B%22Values%22%3A%7B%22w32%22%3A%22g%22%2C%22wg%22%3A%2236%22%2C%22wl%22%3A%22BESTMATCH%22%2C%22wn%22%3A%22Y%22%7D%2C%22Exp%22%3A%221576688008%22%7D%7D%7D; NV%5FTHIRD%5FPARTY=#5%7B%22Sites%22%3A%7B%22USA%22%3A%7B%22Values%22%3A%7B%22wu%22%3A%22https%253A%252F%252Fwww.newegg.com%252FProduct%252FProductList.aspx%253FSubmit%253DENE%2526DEPA%253D0%2526Order%253DBESTMATCH%2526Description%253DMSI%252BGL62M%2526N%253D-1%2526isNodeId%253D1%22%7D%2C%22Exp%22%3A%221492880012%22%7D%7D%7D; needleopt=Saant0-usOnly; needlepin=N190d1486542212420000214007c89457c7c89457c00000000000000000000000000000000; s_fid=0756D8EFC355DE87-12356BB15920B484; s_sess=%20c_m%3Dundefinedwww.google.co.jpNatural%2520Search%3B%20s_evar36%3Dnatural%257Cgoogle%3B%20s_eVar37%3Dnatural%257Cgoogle%3B%20s_campaign%3Dnatural%257Cgoogle%3B%20s_stv%3Dmsi%2520gl62m%3B%20s_cpc%3D1%3B%20s_ev3%3Dnon-internal%2520campaign%3B; s_pers=%20s_ns_persist%3DNatural%257CGoogle%7C1492843382212%3B%20s_ev19%3D%255B%255B%2527natural%25257Cgoogle%2527%252C%25271490251382226%2527%255D%255D%7C1648017782226%3B%20productnum%3D56%7C1492914810427%3B%20s_vs%3D1%7C1490324621345%3B%20gpv_pv%3Dhomepage%7C1490324621350%3B%20s_nr%3D1490322821352-Repeat%7C1521858821352%3B%20gpvch%3Dbrowsing%7C1490324621353%3B''',
    'Host': host,
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}


def random_sleep(min_sleep=0, max_sleep=1, sleep=True):
    if not sleep:
        return 0
    sleep_time = random.random() * (max_sleep - min_sleep) + min_sleep
    # print 'sleeping %f seconds' % sleep_time
    time.sleep(sleep_time)
    return sleep_time


def check_one(proxy):
    proxy_url = proxy[1].lower() + '://' + proxy[0]
    proxy_dict = {"https": proxy_url, "http": proxy_url}
    max_try = 2
    for i in range(max_try):
        try:
            t0 = time.time()
            data = requests.get(url, headers=headers, timeout=10, proxies=proxy_dict).content  # .decode('utf-8')
            if success_mark in data:
                # print proxy_url
                return ['succ', str(time.time() - t0)]
            else:
                if i >= max_try - 1:
                    return ['wrong content', data]
        except Exception as e:
            if i >= max_try - 1:
                return [e]
            random_sleep(min_sleep=1, max_sleep=5)


def proxy_check_thread(task_queue, done_queue):
    for t_proxy in iter(task_queue.get, 'STOP'):
        ret = check_one(t_proxy)
        if ret[0] == 'succ':
            # print ret, t_proxy
            succ_proxy = t_proxy + ret
            print 'succ: ', succ_proxy
            done_queue.put(succ_proxy)
        elif ret[0] == 'wrong content':
            print '\n********** wrong content:\n', ret
            pass
        else:
            # print '\n********** Exceptions:\n', ret
            done_queue.put([])
        random_sleep(min_sleep=0, max_sleep=1)


def proxy_check():
    task_queue, done_queue, task_n = Queue(), Queue(), 0
    result = []
    try_count = 30
    with open('proxyedulist.txt') as reader:
        for line in reader:
            t_proxy = line.strip().split('\t')[:2]
            task_queue.put(t_proxy)
            task_n += 1
            if task_n >= try_count and False:
                break
    print "Start multi-thread Processing"
    for t in range(N_THREAD):
        task_queue.put('STOP')
    for t in range(N_THREAD):
        Process(target=proxy_check_thread, args=(task_queue, done_queue)).start()
    # collect the results below
    with open(file_proxy_list_path, 'w') as writer:
        for t in range(task_n):
            thread_return = done_queue.get()
            if thread_return:
                # print thread_return
                #  output format: { proxy address:port }\t{ proxy type }
                writer.write('\t'.join(thread_return) + '\n')
                result.append(thread_return)
            if t % 20 == 0:
                print t, 'proxy check finish'
    print 'Get good proxy:', len(result)


if __name__ == "__main__":
    proxy_check()


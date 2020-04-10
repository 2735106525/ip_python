import requests
import parsel
import time

class Kuaidaili():

    def headers(self):
        self.headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}



    def nextpage(self):
        self.url=[]
        for i in range(1,6):
            url='https://www.kuaidaili.com/free/inha/{}/'.format(i)
            self.url.append(url)



    def parsing(self):
        self.proxies_list = []
        self.ip_num=[]
        self.port_num=[]
        for url in self.url:
            print(url)
            response=requests.get(url,headers=self.headers)
            # print(response.text)
            html_data = parsel.Selector(response.text)
            parse_list = html_data.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')
            # print(parse_list)
            for tr in parse_list:
                proxies_dict = {}
                http_type = tr.xpath('./td[4]/text()').extract_first()  # 类型
                ip_num = tr.xpath('./td[1]/text()').extract_first()  # ip
                port_num = tr.xpath('./td[2]/text()').extract_first()  # 端口
                # print(http_type,ip_num,port_num)
                proxies_dict[http_type] = ip_num + ":" + port_num
                # self.proxies_list.append(proxies_dict)
                self.ip_num.append(ip_num)
                self.port_num.append(port_num)
            time.sleep(1)



    def detection(self):
        url='https://www.baidu.com/'
        for ip_num, port_num in zip(self.ip_num,self.port_num):
            proxy=ip_num+':'+port_num
            # print(proxy)
            proxies = {
                'http':'http://'+ proxy,
                'https': 'http://' + proxy,
            }
            print(proxies)
            try:
                response = requests.get(url,headers=self.headers,proxies=proxies,timeout=0.1)  # 测试ip的网址
                if response.status_code == 200:
                    print('可以用')
            except Exception as e:
                print('不可用')



if __name__ == '__main__':
    kdl=Kuaidaili()
    kdl.headers()
    kdl.nextpage()
    kdl.parsing()
    kdl.detection()
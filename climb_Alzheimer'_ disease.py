import requests
import pandas as pd
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import re

class Climb_Disease:
    def __init__(self):
        self.name_list = []
        self.describe_list = []
        self.insurance_list = []
        self.infect_rate_list = []
        self.infect_people_list = []
        self.infect_way_list = []
        self.department_list = []
        self.period_list = []
        self.cure_rate_list = []
        self.drug_list = []
        self.money_list = []
        self.cause_list = []
        self.prevent_list = []
        self.prevent_type_list = []
        self.neopathy_list = []
        self.symptom_list = []
        self.inspect_list = []
        self.diagnosis_list = []
        self.treat_list = []
        self.treat_type_list = []
        self.nursing_list = []
        self.nursing_type_list = []
        self.food_list = []
        self.data = []
        self.disease_type = []

    def MyRequests(self,url):
        sess = requests.Session()
        sess.keep_alive = False
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            'Connection': 'close'
        }
        resp = requests.get(url=url, headers=headers,stream=True, verify=False, timeout=(5,5))
        return resp

    def describe_spider(self):
        try: # 防止出现错误
            describe_url = f'https://jib.xywy.com/il_sii/gaishu/{882}.htm'
            resp = self.MyRequests(describe_url)
            html = etree.HTML(resp.text)
            name = ''.join(html.xpath('/html/body/div[5]/div/text()'))
            insurance = ''.join(html.xpath('/html/body/div[6]/div/div/div[2]/div[2]/p[1]/span[2]/text()')).strip('\n').strip()
            infect_rate = ''.join(html.xpath('/html/body/div[6]/div/div/div[2]/div[2]/p[2]/span[2]/text()')).strip('\n').strip()
            infect_people = ''.join(html.xpath('/html/body/div[6]/div/div/div[2]/div[2]/p[3]/span[2]/text()')).strip('\n').strip()
            infect_way = ''.join(html.xpath('/html/body/div[6]/div/div/div[2]/div[2]/p[4]/span[2]/text()')).strip('\n').strip()
            neopathy = ' '.join(html.xpath('/html/body/div[6]/div/div/div[2]/div[2]/p[5]/span[2]/a/text()')).strip('\n').strip()
            department = ''.join(html.xpath('/html/body/div[6]/div/div/div[2]/div[3]/p[1]/span[2]/text()')).strip('\n').strip()
            treat_type = ''.join(html.xpath('/html/body/div[6]/div/div/div[2]/div[3]/p[2]/span[2]/text()')).strip('\n').strip()
            period = ''.join(html.xpath('/html/body/div[6]/div/div/div[2]/div[3]/p[3]/span[2]/text()')).strip('\n').strip()
            cure_rate = ''.join(html.xpath('/html/body/div[6]/div/div/div[2]/div[3]/p[4]/span[2]/text()')).strip('\n').strip()
            drug = ' '.join(html.xpath('/html/body/div[6]/div/div/div[2]/div[3]/p[5]/span[2]/a/text()')).strip('\n').strip()
            try:
                money = ''.join(html.xpath('/html/body/div[6]/div/div/div[2]/div[3]/p[6]/span[2]/text()')).strip('\n').strip()
            except:
                money = ''.join(html.xpath('/html/body/div[6]/div/div/div[2]/div[3]/p[5]/span[2]/text()')).strip('\n').strip()
            describe = ''.join(html.xpath('/html/body/div[6]/div/div/div[2]/div[1]/p/text()')).strip('\r\n\t').strip().strip('\r\n\n\n')
            # print(name,insurance,infect_rate,infect_people,infect_way,neopathy,department,treat,period,cure_rate,drug,money,describe)
            # exit()
            self.name_list.append(name)
            self.describe_list.append(describe)
            self.insurance_list.append(insurance)
            self.infect_rate_list.append(infect_rate)
            self.infect_people_list.append(infect_people)
            self.infect_way_list.append(infect_way)
            self.neopathy_list.append(neopathy)
            self.department_list.append(department)
            self.treat_type_list.append(treat_type)
            self.period_list.append(period)
            self.cure_rate_list.append(cure_rate)
            self.drug_list.append(drug)
            self.money_list.append(money)
            resp.close()
        except Exception as e:
            print(e)

    def cause_spider(self):
        try:
            cause_url = f'https://jib.xywy.com/il_sii/cause/{882}.htm'
            resp = self.MyRequests(cause_url)
            html = etree.HTML(resp.text)
            div = ''.join(html.xpath('/html/body/div[6]/div/div/div[2]/p//text()')).strip('\n').strip().replace('\r\n\t','') #div[2]/div[1]/text()
            obj = re.compile(r'.*?、(?P<name>.*?)：.*?',re.S)
            disease_type1 = ' '.join(html.xpath('/html/body/div[6]/div/div/div[2]/p/a/text()')).strip('\n').strip().replace('\r\n\t','').replace('：',' ')
            disease_type2 = ' '.join(obj.findall(div))
            disease_type = disease_type1 + disease_type2
            self.cause_list.append(disease_type)
            resp.close()
        except Exception as e:
            print(e)

    def prevent_spider(self):
        try:
            prevent_url = f'https://jib.xywy.com/il_sii/prevent/{882}.htm'
            resp = self.MyRequests(prevent_url)
            html = etree.HTML(resp.text)
            prevent_type = ' '.join(html.xpath('/html/body/div[6]/div[1]/div[1]/div[2]/p/strong/text()')).strip('\r\n\t').strip().replace('\r\n\t','')
            prevent_content = ''.join(html.xpath('/html/body/div[6]/div[1]/div[1]/div[2]/p//text()')).strip('\r\n\t').strip().replace('\r\n\t','')
            obj = re.compile('.*?、(?P<name>[\u4e00-\u9fa5]+)',re.S)
            prevent = ' '.join(obj.findall(prevent_content))
            # print(prevent)
            resp.close()
            self.prevent_list.append(prevent)
            self.prevent_type_list.append(prevent_type)
        except Exception as e:
            print(e)

    # def neopathy_spider(self):
    #     try:
    #         neopathy_url = f'https://jib.xywy.com/il_sii/neopathy/{882}.htm'
    #         resp = self.MyRequests(neopathy_url)
    #         html = etree.HTML(resp.text)
    #         neopathy = ' '.join(html.xpath('/html/body/div[6]/div[1]/div[1]/div[2]/span//text()')).strip('\r\n\t').strip().replace('\r\n\t','')
    #         print(neopathy)
    #         resp.close()
    #         exit()
    #         self.neopathy_list.append(neopathy)
    #     except Exception as e:
    #         print(e)

    def symptom_spider(self):
        try:
            symptom_url = f'https://jib.xywy.com/il_sii/symptom/{882}.htm'
            resp = self.MyRequests(symptom_url)
            html = etree.HTML(resp.text)
            symptom = ''.join(html.xpath('/html/body/div[6]/div[1]/div[1]/div[2]/p/text()')).strip('\r\n\t').strip().replace('\r\n\t','')
            # print(symptom)
            resp.close()
            self.symptom_list.append(symptom)
        except Exception as e:
            print(e)

    def inspect_spider(self):
        try:
            inspect_url = f'https://jib.xywy.com/il_sii/inspect/{882}.htm'
            resp = self.MyRequests(inspect_url)
            html = etree.HTML(resp.text)
            inspect = ''.join(html.xpath('/html/body/div[6]/div[1]/div[1]/div[2]/p/text()')).strip('\r\n\t').strip().replace('\r\n\t', '')
            # print(inspect)
            resp.close()
            self.inspect_list.append(inspect)
        except Exception as e:
            print(e)

    def diagnosis_spider(self):
        try:
            diagnosis_url = f'https://jib.xywy.com/il_sii/diagnosis/{882}.htm'
            resp = self.MyRequests(diagnosis_url)
            html = etree.HTML(resp.text)
            diagnosis_content = ''.join(html.xpath('/html/body/div[6]/div[1]/div[1]/div[2]/p//text()')).strip('\r\n\t').strip().replace('\r\n\t', '')
            obj = re.compile('.*?\d、(?P<name>.*?)。',re.S)
            diagnosis = ' '.join(obj.findall(diagnosis_content))
            # print(diagnosis)
            resp.close()
            self.diagnosis_list.append(diagnosis)
        except Exception as e:
            print(e)

    def treat_spider(self):
        try:
            treat_url = f'https://jib.xywy.com/il_sii/treat/{882}.htm'
            resp = self.MyRequests(treat_url)
            html = etree.HTML(resp.text)
            treat_content = ''.join(html.xpath('/html/body/div[6]/div[1]/div[1]/div[2]/div[2]/p/text()')).strip('\r\n\t').strip().replace('\r\n\t', '')
            # treat_type = ''.join(html.xpath('/html/body/div[6]/div[1]/div[1]/div[2]/div[2]/p/b/text()')).strip('\r\n\t').replace('：',' ').replace('\r\n\t', '')
            obj = re.compile('.*?(?P<name>[\u4e00-\u9fa5]+)：',re.S)
            treat = ' '.join(obj.findall(treat_content))
            # print(treat)
            resp.close()
            self.treat_list.append(treat)
            print(self.treat_list,len(self.treat_list))
        except Exception as e:
            print(e)

    def nursing_spider(self):
        try:
            nursing_url = f'https://jib.xywy.com/il_sii/nursing/{882}.htm'
            resp = self.MyRequests(nursing_url)
            html = etree.HTML(resp.text)
            nursing_type = ' '.join(html.xpath('/html/body/div[6]/div[1]/div[1]/div[2]/p/strong/text()')).strip('\r\n\t').strip().replace('\r\n\t', '')
            nursing_content = ''.join(html.xpath('/html/body/div[6]/div[1]/div[1]/div[2]/p//text()')).strip('\r\n\t').strip().replace('\r\n\t', '')
            obj1 = re.compile('.*?\(\d\)(?P<name>.*?)。',re.S)
            obj2 = re.compile('.*?一般护理\d、(?P<name>.*?)。', re.S)
            nursing1 = ' '.join(obj1.findall(nursing_content))
            nursing2 = ' '.join(obj2.findall(nursing_content))
            nursing = nursing1 + ' ' + nursing2
            # print(nursing)
            # [\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]
            resp.close()
            self.nursing_type_list.append(nursing_type)
            self.nursing_list.append(nursing)
        except Exception as e:
            print(e)

    def food_spider(self):
        try:
            food_url = f'https://jib.xywy.com/il_sii/food/{882}.htm'
            resp = self.MyRequests(food_url)
            html = etree.HTML(resp.text)
            food_content = ''.join(html.xpath('/html/body/div[6]/div[1]/div[1]/div[2]/div/div[2]/div[1]/p//text()')).strip('\r\n\t').strip().replace('\r\n\t', '')
            obj = re.compile('.*?患者适宜吃的食物：(?P<name>.*?)腐竹的营养价值高。',re.S)
            food = ''.join(obj.findall(food_content)).replace('3、','。3、')
            resp.close()
            self.food_list.append(food)
            # print(self.food_list)
        except Exception as e:
            print(e)

    def print_info(self):
        print(len(self.name_list),len(self.insurance_list),len(self.infect_rate_list),
              len(self.infect_people_list),len(self.infect_way_list),len(self.department_list),
              len(self.period_list),len(self.cure_rate_list),len(self.drug_list),len(self.money_list),len(self.describe_list),
              len(self.cause_list),len(self.prevent_list),len(self.prevent_type_list),len(self.neopathy_list),len(self.symptom_list),
              len(self.diagnosis_list),len(self.inspect_list),
              len(self.treat_list),len(self.treat_type_list),len(self.inspect_list),
              len(self.nursing_type_list),len(self.food_list))

    def data_process(self):
        self.data = pd.DataFrame({
            'name': self.name_list,
            'insurance': self.insurance_list,
            'infect_rate': self.infect_rate_list,
            'infect_people': self.infect_people_list,
            'infect_way': self.infect_way_list,
            'department': self.department_list,
            'period': self.period_list,
            'cure_rate': self.cure_rate_list,
            'drug': self.drug_list,
            'money': self.money_list,
            'describe': self.describe_list,
            'cause': self.cause_list,
            'prevent': self.prevent_list,
            'prevent_type': self.prevent_type_list,
            'neopathy': self.neopathy_list,
            'symptom': self.symptom_list,
            'inspect': self.inspect_list,
            'diagnosis': self.diagnosis_list,
            'treat': self.treat_list,
            'treat_type': self.treat_type_list,
            'nursing': self.nursing_list,
            'nursing_type': self.nursing_type_list,
            'food': self.food_list,
        })
        return self.data

    def run(self):
        with ThreadPoolExecutor(2) as t: #开辟2个线程
            for i in [self.describe_spider,self.cause_spider,self.prevent_spider,
                      self.symptom_spider,self.inspect_spider,self.diagnosis_spider,self.treat_spider,
                      self.nursing_spider,self.food_spider]:
                t.submit(i) # 需要注意的是submit里面的函数不能带括号

if __name__ == '__main__':
    AD_spider = Climb_Disease()
    AD_spider.run()
    AD_spider.print_info()
    data = AD_spider.data_process()
    print(data)
    data.to_csv('data/AD.csv',encoding='utf-8-sig')

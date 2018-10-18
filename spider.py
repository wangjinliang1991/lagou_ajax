import re
import time

import requests
from lxml import etree


headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        'Referer': 'https://www.lagou.com/jobs/list_python?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput=',
        'Cookie': 'user_trace_token=20180919142124-f0c0ff82-e557-4761-ba03-c6077f8ba5fc; _ga=GA1.2.1201022637.1537338089; LGUID=20180919142129-3e8ff586-bbd4-11e8-a229-525400f775ce; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22166206c7f5c5e9-01a75e4e2d3a1e-8383268-1327104-166206c7f5e7ed%22%2C%22%24device_id%22%3A%22166206c7f5c5e9-01a75e4e2d3a1e-8383268-1327104-166206c7f5e7ed%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=17; index_location_city=%E6%88%90%E9%83%BD; JSESSIONID=ABAAABAAAFCAAEG9F3FD70472E0A331D9E4DED330B5D799; _gid=GA1.2.584271127.1539848034; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1538142275,1538732915,1539310634,1539848034; _putrc=04052370D69AE6AB; LGSID=20181018163625-e60cf8ed-d2b0-11e8-8169-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%3Fcity%3D%25E6%2588%2590%25E9%2583%25BD%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F5001543.html; login=true; unick=%E7%8E%8B%E9%87%91%E4%BA%AE; gate_login_token=7253feaf1d459642bef1bb213be079532af2f7fd3f9e4f01; SEARCH_ID=cbc3921575a54380a094dc9cb8a408b6; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1539852518; LGRID=20181018164837-9ac64d8b-d2b2-11e8-816d-525400f775ce; TG-TRACK-CODE=search_code',
          'Origin': 'https://www.lagou.com'
    }

def request_list_page():
    url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E6%88%90%E9%83%BD&needAddtionalResult=false'

    data = {
        'first': 'false',
        'pn': 1,
        'kd': 'python'
    }
    for x in range(1,14):
        data['pn'] = x
        response = requests.post(url, headers=headers, data=data)
        result = response.json()
        time.sleep(1)
        positions = result['content']['positionResult']['result']
        for position in positions:
            positionId = position['positionId']
            position_url = 'https://www.lagou.com/jobs/%s.html'%positionId
            parse_position_detail(position_url)



def parse_position_detail(url):
    positions = []
    response = requests.get(url,headers=headers)
    text = response.text
    html = etree.HTML(text)
    position_name = html.xpath('//span[@class="name"]/text()')[0]

    job_request_spans = html.xpath('//dd[@class="job_request"]//span')
    salary = job_request_spans[0].xpath('.//text()')[0].strip()
    city = job_request_spans[1].xpath('.//text()')[0].strip()
    city = re.sub(r"[\s/]","",city)
    work_years = job_request_spans[2].xpath('.//text()')[0].strip()
    work_years = re.sub(r"[\s/]", "", work_years)
    education = job_request_spans[3].xpath('.//text()')[0].strip()
    education = re.sub(r"[\s/]", "", education)
    desc = "".join(html.xpath('//dd[@class="job_bt"]//text()')).strip()
    company_name = html.xpath('//h2[@class="fl"]/text()')[0].strip()
    position = {
        'name': position_name,
        'company': company_name,
        'salary': salary,
        'city': city,
        'work_years': work_years,
        'education': education,
        'desc': desc
    }
    positions.append(position)
    print(positions)



def main():
    request_list_page()


if __name__ == '__main__':
    main()
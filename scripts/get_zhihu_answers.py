"""
20210305
"""
import os
import re
import time
import json
import copy

import requests
import html2text
from bs4 import BeautifulSoup


def replace_invalid_filename_char(filename, new_char='_'):
    assert isinstance(new_char, str)
    control_chars = ''.join((map(chr, range(0x00, 0x20))))
    pattern = r'[\\/*?:"<>|{}]'.format(control_chars)
    return re.sub(pattern, new_char, filename)
    

class ZhiHu(object):
    def __init__(self):
         self.request_content = None

    def request(self, url, retry_times=10):
        header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
            'Host': 'www.zhihu.com',
            'authority': 'www.zhihu.com',
            'origin': 'https://www.zhihu.com',
            'referer': url,
        }
        times = 0
        while retry_times > 0:
            times += 1
            print('request %s, times: %d' %(url, times))
            try:
                self.request_content = requests.get(url, headers=header, timeout=10).content
            except Exception as e:
                print(e)
                retry_times -= 1
            else:
                return self.request_content

    def get_single_answer_content(self, answer_url, save_dir):
        all_content = {}
        question_id, answer_id = re.findall('https://www.zhihu.com/question/(\d+)/answer/(\d+)', answer_url)[0]

        html_content = self.request(answer_url)
        if html_content:
            all_content['main_content'] = html_content
        else:
            raise  ValueError('request failed, quit......')

        ajax_answer_url = 'https://www.zhihu.com/api/v4/answers/{}'.format(answer_id)
        ajax_content = self.request(ajax_answer_url)
        if ajax_content:
            all_content['ajax_content'] = json.loads(ajax_content)
        else:
            raise ValueError('request failed, quit......')
        data = self.parse_content(all_content)
        self.transform_to_markdown(data, save_dir)
        
    def prepare_for_markdown(self, soup, interested_tag):
        if interested_tag is None:
            return
        soup = copy.copy(soup)
        soup.body.extract()
        soup.head.insert_after(soup.new_tag("body"))
        soup.body.append(interested_tag)
        
        img_tags = soup.find_all("img", class_="content_image lazy")
        for img_tag in img_tags:
            img_tag["src"] = img_tag["data-actualsrc"]
        img_tags = soup.find_all("img", class_="origin_image zh-lightbox-thumb lazy")
        for img_tag in img_tags:
            img_tag["src"] = img_tag["data-actualsrc"]
        img_tags = soup.find_all("img")
        for img_tag in img_tags:
            if img_tag['src'].startswith('https://www.zhihu.com/equation?tex='):
                span_tag = soup.new_tag("span")
                img_tag.insert_after(span_tag)
                img_tag.extract()
                formula = img_tag['alt']
                if formula.startswith('\\['):
                    formula = formula[2:]
                if formula.endswith('\\]'):
                    formula = formula[:-2]
                formula = formula.strip()
                if span_tag.parent.text.strip() == '':
                    span_tag.string = r'$${}$$'.format(formula)
                else:
                    span_tag.string = '${}$'.format(formula)
        noscript_tags = soup.find_all("noscript")
        for noscript_tag in noscript_tags:
            noscript_tag.extract()
        script_tags = soup.find_all("script")
        for script_tag in script_tags:
            script_tag.extract()
        return soup
        
    def parse_content(self, content):
        main_content = content.get('main_content')
        ajax_content = content.get('ajax_content')
        
        author_name = ajax_content.get('author').get('name')
        answer_id = ajax_content.get('id')
        question_id = ajax_content.get('question').get('id')
        question_title = ajax_content.get('question').get('title')
        create_time = time.localtime(ajax_content.get('created_time'))

        soup = BeautifulSoup(main_content, "lxml")
        answer = soup.find("span", class_="RichText ztext CopyrightRichText-richText")
        answer = self.prepare_for_markdown(soup, answer)

        data = {}
        data['answer_content'] = answer
        data['author_name'] = author_name
        data['answer_id'] = answer_id
        data['question_id'] = question_id
        data['question_title'] = question_title
        data['create_time'] = create_time
        return data

    def transform_to_markdown(self, data, save_dir):
        answer_content = data['answer_content']
        author_name = data['author_name']
        question_title = data['question_title']
        create_time = data['create_time']
        answer_id = data['answer_id']
        question_id = data['question_id']
        origin_url = 'https://www.zhihu.com/question/{}/answer/{}'.format(question_id, answer_id)
        answer_text = html2text.html2text(answer_content.decode('utf-8'))

        create_time_str = time.strftime("%Y%m%d", create_time)
        question_title_valid = replace_invalid_filename_char(question_title)
        filename = '{} {}.md'.format(create_time_str, question_title_valid)
        os.makedirs(save_dir, exist_ok=True)
        fullname = os.path.join(save_dir, filename)
        with open(fullname, "w", encoding='utf-8') as f:
            f.write("#! {}\n\n".format(origin_url))
            f.write("[comment]: <> (Answer URL: {})\n".format(origin_url))
            f.write("[comment]: <> (Question Title: {})\n".format(question_title))
            f.write("[comment]: <> (Author Name: {})\n".format(author_name))
            f.write("[comment]: <> (Create Time: {})\n\n".format(time.strftime("%Y-%m-%d %H:%M:%S", create_time)))
            f.write(answer_text)
       
       
def load_list(filename, encoding='utf-8', start=0, stop=None, step=1):
    assert isinstance(start, int) and start >= 0
    assert (stop is None) or (isinstance(stop, int) and stop > start)
    assert isinstance(step, int) and step >= 1
    
    lines = []
    with open(filename, 'r', encoding=encoding) as f:
        for _ in range(start):
            f.readline()
        for k, line in enumerate(f):
            if (stop is not None) and (k + start > stop):
                break
            if k % step == 0:
                lines.append(line.rstrip())
    return lines
    
    
if __name__ == '__main__':
    zhihu = ZhiHu()
    answer_urls = load_list('../_local/answer_urls.txt')
    save_dir = '../_local/answer_markdowns'
    for k, url in enumerate(answer_urls):
        print('[{}/{}] {}'.format(k+1, len(answer_urls), url))
        zhihu.get_single_answer_content(url, save_dir)
        time.sleep(3)


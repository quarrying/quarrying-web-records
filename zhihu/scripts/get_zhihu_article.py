"""
20210307
"""
import os
import re
import time
import json
import copy

import requests
import html2text
from bs4 import BeautifulSoup
from selenium import webdriver


def replace_invalid_filename_char(filename, new_char='_'):
    assert isinstance(new_char, str)
    control_chars = ''.join((map(chr, range(0x00, 0x20))))
    pattern = r'[\\/*?:"<>|{}]'.format(control_chars)
    return re.sub(pattern, new_char, filename)
    

class ZhiHu(object):
    def __init__(self):
         pass

    def request(self, url):
        chrome_opt = webdriver.ChromeOptions()
        chrome_opt.add_argument('--disable-gpu')
        browser = webdriver.Chrome(chrome_options=chrome_opt)
        browser.get(url)
        return browser.page_source
        
    def get_article_content(self, article_url, save_dir):
        html_content = self.request(article_url)
        soup = BeautifulSoup(html_content, 'html.parser')
        article_title = soup.find("h1", class_="Post-Title")
        article_content = soup.find("div", class_="RichText ztext Post-RichText")
        article_content = self.prepare_for_markdown(soup, article_content)
        data = {}
        data['url'] = article_url
        data['title'] = article_title.text
        data['content'] = article_content
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
                formula = img_tag['data-formula']
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
        
    def transform_to_markdown(self, data, save_dir):
        article_url = data['url']
        article_title = data['title']
        article_content = data['content']
        article_text = html2text.html2text(article_content.decode('utf-8'))

        article_title_valid = replace_invalid_filename_char(article_title)
        filename = '{}.md'.format(article_title_valid)
        os.makedirs(save_dir, exist_ok=True)
        fullname = os.path.join(save_dir, filename)
        with open(fullname, "w", encoding='utf-8') as f:
            f.write("#! {}\n\n".format(article_url))
            f.write('# {}\n'.format(article_title))
            f.write(article_text)
       
      
if __name__ == '__main__':
    zhihu = ZhiHu()
    save_dir = '../_local/article_markdowns'
    zhihu.get_article_content('https://zhuanlan.zhihu.com/p/147901986', save_dir)
    zhihu.get_article_content('https://zhuanlan.zhihu.com/p/146076139', save_dir)
    zhihu.get_article_content('https://zhuanlan.zhihu.com/p/144589742', save_dir)

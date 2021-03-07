import os
import glob
import json
from collections import OrderedDict


def load_as_json(filename, encoding='utf-8'):
    with open(filename, 'r', encoding=encoding) as f:
        content = json.load(f, object_pairs_hook=OrderedDict)
    return content


def save_list(filename, list_obj, encoding=None, append_break=True):
    with open(filename, 'w', encoding=encoding) as f:
        if append_break:
            for item in list_obj:
                f.write(str(item) + '\n')
        else:
            for item in list_obj:
                f.write(str(item))


if __name__ == '__main__':
    filenames = glob.glob('../local/answer_jsons/*.json')
    answer_urls = []
    for k, name in enumerate(filenames):
        print('[{}/{}] {}'.format(k+1, len(filenames), name))
        data = load_as_json(name)['data']
        for item in data:
            answer_id = item['id']
            question_id = item['question']['id']
            url = 'https://www.zhihu.com/question/{}/answer/{}'.format(question_id, answer_id)
            answer_urls.append(url)
    print(len(answer_urls))
    answer_urls = list(set(answer_urls))
    print(len(answer_urls))
    save_list('../_local/answer_urls.txt', answer_urls)
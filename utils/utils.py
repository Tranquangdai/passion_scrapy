import string
import os
import datetime
import hashlib
from utils import utils

from os.path import join, exists
from urllib.request import urlopen
from urllib.parse import unquote, urlparse
from settings import ROOT_DIR
from models.passion_mysql import LinkProduct


def download_obj_from_url(url_save_path):
    url, save_path = url_save_path.split('*')
    if not exists(save_path):
        with open(save_path, 'wb') as writer:
            writer.write(urlopen(url).read())
            print('a')


def preprocessing_text(text):
    text = text.replace("♔♔", "")
    text = text.replace('.', '').strip()
    for punc in string.punctuation:
        text = text.strip(punc)
    text = text.strip().replace(',', '').strip()
    return text


def get_current_datetime():
    return datetime.datetime.strftime(datetime.datetime.now(), format='%Y-%m-%d %H:%m:%S')


def hash_url(url):
    return hashlib.md5(url.encode('utf-8')).hexdigest()


def split_list_by_product(l):
    split_list = []
    html_pos = []
    for i, link in enumerate(l):
        if 'html' in link:
            html_pos.append(i)
    html_pos.append(len(l) + 1)

    for i in range(len(html_pos) - 1):
        split_list.append(l[html_pos[i]: html_pos[i + 1]])
    return split_list


def parse_category_from_product_link(url):
    path = urlparse(url).path
    return unquote(path).split('/')[-1].capitalize()


def list_link_in_model(model):
    return [i.link for i in model.select(model.link).execute()]


def select_distinct_value_from_field_model(model, field):
    return [getattr(i, field) for i in model.select(getattr(model, field)).distinct().execute()]


def make_dirs(list_dir, sub_dir):
    for l in list_dir:
        parent_dir = join(ROOT_DIR, '_image', l)
        if not exists(parent_dir):
            os.makedirs(parent_dir)

        for s in sub_dir:
            child_dir = join(parent_dir, s)
            if not exists(child_dir):
                os.makedirs(child_dir)


def download_images():
    query = LinkProduct.select(LinkProduct.name, LinkProduct.category, LinkProduct.image)\
        .where(LinkProduct.name.contains('mai-phuong'))\
        .execute()
    data = []
    for r in query:
        image = eval(r.image)
        for i in range(len(image)):
            save_path = join(ROOT_DIR, '_image', r.category, r.name, str(i) + '.jpg')
            url = image[i]
            data.append(url + '*' + save_path)
    # print(data)
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(download_obj_from_url, data)

    return True


def list_non_empty_dir():
    parent_dir = [join(ROOT_DIR, '_image', cate) for cate in
                  utils.select_distinct_value_from_field_model(LinkProduct, 'category')]
    count = 0
    for path in parent_dir:
        for sub_dir in os.listdir(path):
            sub_dir_path = join(path, sub_dir)
            if len(os.listdir(sub_dir_path)) > 0:
                print(sub_dir_path)
                count += 1
    print(count)


if __name__ == '__main__':
    # from models.passion_mysql import LinkProduct
    # select_distinct_value_from_field_model(LinkProduct, 'category')

    # make_dirs(utils.select_distinct_value_from_field_model(LinkProduct, 'category'),
    #           utils.select_distinct_value_from_field_model(LinkProduct, 'name'))
    download_images()
    # list_non_empty_dir()
    # pass

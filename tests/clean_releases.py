"""Cleaner of releases in the github"""
from requests import get, delete


def get_by_url(url):
    d = dict(url=url)
    responce = get(**d)
    content = responce.json()
    return content


if __name__ == '__main__':
    token = '?access_token='
    base_url = 'https://api.github.com/repos/demid5111/approximate-enthropy'

    for i in range(0, 10):
        content = get_by_url(url='{}/releases{}'.format(base_url, token))
        print(str(i) + str(len(content)))
        for el in content:
            rel_to_save = []
            if el['url'] in rel_to_save:
                continue
            tmp_d = dict(url='{}{}'.format(el['url'], token))
            r = delete(**tmp_d)
            print(str(i), r.content)

    for i in range(0, 10):
        content = get_by_url(url='{}/tags{}'.format(base_url, token))
        print(str(i) + str(len(content)))
        for el in content:
            tags_to_save = []
            if el['name'] in tags_to_save:
                continue
            delete_url = '{}/git/refs/tags/{}'.format(base_url, el['name'])
            tmp_d = dict(url='{}{}'.format(delete_url, token))
            r = delete(**tmp_d)
            print(str(i), r.content)

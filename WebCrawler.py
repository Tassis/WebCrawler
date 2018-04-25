import webbrowser
import requests
import bs4
import wget
import csv

seed_url_list = []


def get_seed_url(url):
    try:
        # Get list page's element
        page = requests.get(url)
        objSoup = bs4.BeautifulSoup(page.text, 'lxml')

        # Get video_page from element
        element = objSoup.select('tr .title a')
        video_page_url = "https://share.dmhy.org%s" % element[1].get('href')
        page = requests.get(video_page_url)

    except Exception as e:
        raise Exception('取得網址異常')
        return None
    else:
        # Get Seed
        objSoup = bs4.BeautifulSoup(page.text, 'lxml')
        element = objSoup.select('#resource-tabs p a')
        result_url = element[0].get('href')
        return 'https:' + result_url


def search_anime_list(fn):
    print('動畫清單載入開始.....')
    with open(fn) as csvFile:
        for line in csvFile:
            data = line.split(',')
            seed_url = get_seed_url(data[0])
            if (seed_url is not None):
                print('加入 %s %s 至清單' % (seed_url, data[1]))
                seed_url_list.append(seed_url)


search_anime_list('seed_list.csv')

print('開始下載種子....')
for seed in seed_url_list:
    wget.download(seed, 'seed')
print('\n種子下載完成....')

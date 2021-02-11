# Adapted from https://towardsdatascience.com/a-better-way-for-asynchronous-programming-asyncio-over-multi-threading-3457d82b3295
#code from https://gist.github.com/lqian5/9059404d42d979f9728ae2b203464fe9#file-fetch_url_multi_threading-py
import time
import requests
import logging
from concurrent import futures

logging.getLogger().setLevel(logging.INFO)


def fetch_url(im_url):
    try:
        resp = requests.get(im_url)
    except Exception as e:
        logging.info(e)
        logging.info('Could not fetch {}'.format(im_url))
    else:
        return resp.content


def fetch_all(url_list):
    with futures.ThreadPoolExecutor() as executor:
        responses = executor.map(fetch_url, url_list)
    return responses


if __name__ == '__main__':
    url = ''
    for ntimes in [1, 10, 100, 500, 1000]:
        start_time = time.time()
        responses = fetch_all([url] * ntimes)
        logging.info('Fetch %s urls takes %s seconds',ntimes, time.time() - start_time)

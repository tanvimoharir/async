# code adapted from https://gist.github.com/lqian5/f6dda4816a166d7223b11600fdb3d692#file-fetch_urls-py
import logging
import time

import asyncio
from aiohttp import ClientSession,ClientResponseError

logging.getLogger().setLevel(logging.INFO)

async def fetch(session,url):
    try:
        async with session.get(url) as response:
            resp=await response.read()
    except ClientResponseError as e:
        logging.warning(e.status)
    except asyncio.TimeoutError:
        logging.warning('Timeout')
    except Exception as e:
        logging.warning(e)
    else:
        return resp
    return

async def fetch_async(loop,r):
    url='https://images.unsplash.com/photo-1444080748397-f442aa95c3e5?ixlib=rb-1.2.1'
    tasks=[]
    async with ClientSession() as session:
        for i in range(r):
            task=asyncio.ensure_future(fetch(session,url))
            tasks.append(task)
        #awaiting response outside loop
        responses=await asyncio.gather(*tasks)
    return responses

if __name__=='__main__':
    for ntimes in [1,10,100,500,1000]:
        start_time=time.time()
        loop=asyncio.get_event_loop()
        future=asyncio.ensure_future(fetch_async(loop,ntimes))
        loop.run_until_complete(future)
        responses=future.result()
        logging.info('Fetch %s usls takes %s seconds',ntimes,str(time.time()-start_time))
        logging.info('{} urls were read sucessfully'.format(len(responses)))







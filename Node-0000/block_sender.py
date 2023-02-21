import aiohttp
import asyncio

from block import Block
from chain import Chain
import database
import sync


async def broadcast_block(new_block):
    block_info_dict = new_block.to_dict()

    # Initialise a database object from the local directory
    db = database.node_db()
    db.sync_local_dir()

    accepted = []
    rejected = []
    dead = []

    aiohttp.ClientTimeout(total=2, connect=2, sock_connect=2, sock_read=2)
    async with aiohttp.ClientSession() as session:
        for addr in db.active_nodes:
            url = f'http://{addr}/mined'
            print(url)
            try:
                async with session.post(url, json=block_info_dict) as response:
                    # if response.status == 200:
                    # status = await response.json()

                    print(response.status)

            except aiohttp.ClientConnectorError as e:
                print(f'Peer at {addr} not running')


if __name__ == '__main__':
    block = sync.sync_local_dir().latest_block()

    print(block)

    text = asyncio.run(broadcast_block(block))

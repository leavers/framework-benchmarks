import asyncio

import asyncpg


async def get_connection_pool():
    pool = await asyncpg.create_pool(
        user='postgres',
        password='123456',
        database='test',
        host='127.0.0.1',
        port=5432
    )
    return pool


async def main():
    pool = await get_connection_pool()

    async with pool.acquire() as conn:
        v = await conn.fetchval('select 1 as v')
        print(v)


if __name__ == '__main__':
    asyncio.run(main())

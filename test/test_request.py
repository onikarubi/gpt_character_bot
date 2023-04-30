import asyncio
import datetime


async def func1():
    await asyncio.sleep(3)
    return 'result func1!!'

async def main():
    task = asyncio.create_task(func1())

    while not task.done():
        now = datetime.datetime.now()
        if now.second % 2 == 0:
            print('\rwaiting...', '/', end='', flush=True)

        else:
            print('\rwaiting...', '\\', end='', flush=True)

        await asyncio.sleep(1)
        print(now.second)

    print()
    result = task.result()
    print('end', result)

asyncio.run(main())

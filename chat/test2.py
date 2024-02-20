import asyncio

class AsyncList:
    def __init__(self):
        self._list = []

    async def append_async(self):
        # 使用future模拟耗时操作
        for i in range(100000):
            self._list.append(i)
            await asyncio.sleep(0.5)

    def get_list(self):
        return self._list

    async def run(self):
        
        await asyncio.gather(self.append_async())

# 使用示例
async def main():
    async_list = AsyncList()
    asyncio.create_task(async_list.run())  # 开启一个任务来异步添加元素

    while True:
        print("Current list: ", async_list.get_list())
        await asyncio.sleep(0.2)  # 模拟其他操作或等待时间

asyncio.run(main())
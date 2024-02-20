from http import HTTPStatus
import dashscope
from openai import OpenAI
import asyncio
from dao import apiDao, modelDao
import time

# qianwen: "sk-00817ca06cb34a57bebe7a6d13c19b16"

class GetResponseDict(object):
    def __init__(self, responseGenerator):
        self.mydict = {"textList": [], "tokens": 0}
        self.responseGenerator = responseGenerator

    async def append_(self):
        
        headIdx = 0
        for response in self.responseGenerator:
            
            output = response.output
            if not output:
                continue

            paragraph = output.choices[0].message.content
            text = f"\r{paragraph[headIdx:len(paragraph)]}"
            print(1,text)
            
            self.mydict["textList"].append(text)
            self.mydict["tokens"] = response.usage.total_tokens
            
            if(paragraph.rfind('\n') != -1):
                headIdx = paragraph.rfind('\n') + 1

    def getDict(self):
        return self.mydict

    async def run(self):
        await self.append_() 


class GptResponse(object):
    def __init__(self, stream, messages):
        api = apiDao.getApifromSelected(selected=1)[0]
        apiId = api.id

        self.platform = api.platform
        self.key = api.key
        self.host = api.host

        self.model = modelDao.getModelFromApiIdAndSelected(apiId=apiId, selected=1)[0].name
        
        self.stream = stream
        self.messages = messages
        
        print(self.platform, self.key)

    async def getResponse(self):
        if self.platform.strip().lower() == "qianwen":
            responseGenerator = dashscope.Generation.call(
                model=self.model,
                stream=self.stream,
                top_p=0.8,
                api_key=self.key,
                messages=self.messages,
                result_format='message'
                )

            if self.stream:
                print(1)
                return responseGenerator

async def main():
    messages=[{'role': 'system', 'content': '用英文回答我的问题'}, {'role': 'user', 'content': '如何做炒西红柿鸡蛋？'}]
    gptRp =GptResponse(stream=True, messages=messages)
    gptRp1 = GetResponseDict(await gptRp.getResponse())
    asyncio.create_task(gptRp1.run())

    while True:
        await asyncio.sleep(0.5)  # 使用 asyncio.sleep 替换 time.sleep
        print("Current response dictionary:", gptRp1.getDict())  # 在每次循环时获取并打印字典内容
        
if __name__ == "__main__":
    asyncio.run(main())
    


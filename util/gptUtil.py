from http import HTTPStatus
import dashscope
from openai import OpenAI
from dao import apiDao, modelDao
import tiktoken
from typing import Union, List, Generator

class GptResponse(object):
    def __init__(self, stream=True, prompt="please reply my question."):
        api = apiDao.getApifromSelected(selected=1)[0]
        apiId = api.id

        self.platform = api.platform.strip().lower()
        self.key = api.key.strip()
        self.host = api.host.strip()

        self.model = modelDao.getModelFromApiIdAndSelected(apiId=apiId, selected=1)[0].name
        
        self.stream = stream
        self.messages = [{'role': 'system', 'content': prompt}]
        
        # debug
        print(self.platform, self.key)

        self.inputTokens = 0
        self.outputTokens = 0
        self.totalTokens = 0

    def getResponse(self, input: str) -> Union[List[str], Generator[str, None, None]]:
        
        self.messages.append({'role': 'user', 'content': input})

        if self.platform == "qianwen":
            try:
                self.response = dashscope.Generation.call(
                    model=self.model,
                    stream=self.stream,
                    top_p=0.8,
                    api_key=self.key,
                    messages=self.messages,
                    result_format='message'
                    )
            except Exception as e:
                self.messages.pop()
                return [e]

            return self.qwenTextReplyGenerator() if self.stream else self.qwenTextReply()
            
        elif self.platform == "openai":
            try:
                self.response = OpenAI(api_key=self.key, base_url=self.host).chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                    stream=self.stream,
                )
            except Exception as e:
                self.messages.pop()
                return [e]

            if self.stream:
                return self.openaiTextReplyGenerator()

            return self.openaiTextReply()

        
    def qwenTextReplyGenerator(self):
        headIdx = 0
        for qwStreamResponse in self.response:
            if qwStreamResponse.status_code != HTTPStatus.OK:
                self.messages.pop()
                yield f"Request id: {qwStreamResponse.request_id}, Status code: {qwStreamResponse.status_code}, error code: {qwStreamResponse.code}, error message: {qwStreamResponse.message}"
                return

            paragraph = qwStreamResponse.output.choices[0].message.content
            streamOut = f"{paragraph[headIdx:]}"
            headIdx = len(paragraph)

            self.inputTokens += qwStreamResponse.usage.input_tokens
            self.outputTokens += qwStreamResponse.usage.output_tokens
            self.totalTokens += (self.inputTokens + self.outputTokens)

            yield streamOut

        self.messages.append({'role': qwStreamResponse.output.choices[0].message.role, 'content': paragraph})

    def qwenTextReply(self):
        if self.response.status_code != HTTPStatus.OK:
            self.messages.pop()
            return f"Request id: {self.response.request_id}, Status code: {self.response.status_code}, error code: {self.response.code}, error message: {self.response.message}"

        self.inputTokens += self.response.usage.input_tokens
        self.outputTokens += self.response.usage.output_tokens
        self.totalTokens += (self.inputTokens + self.outputTokens)

        out = self.response.output.choices[0].message.content

        self.messages.append({'role': self.response.output.choices[0].message.role, 'content': out})

        return [out]

    def openaiTextReplyGenerator(self):
        if self.response.response.status_code != 200:
            self.messages.pop()
            yield f"{self.response.response.raise_for_status()}"
            return

        out = ""
        for streamResponse in self.response:
            resText = streamResponse.choices[0].delta.content or ""
            out += resText
            yield resText

        self.inputTokens = num_tokens_from_string(self.messages[-1]['content'])
        self.outputTokens = num_tokens_from_string(out)
        self.totalTokens = self.inputTokens + self.outputTokens

        self.messages.append({'role': "assistant", 'content': out})
    
    def openaiTextReply(self):
        try:
            out = self.response.choices[0].message.content or ""
        except Exception as e:
            self.messages.pop()
            return [e]
        self.inputTokens = self.response.usage.prompt_tokens
        self.outputTokens = self.response.usage.completion_tokens
        self.totalTokens = self.inputTokens + self.outputTokens

        self.messages.append({'role': "assistant", 'content': out})
        return [out]


def num_tokens_from_string(string: str, encoding_name: str = "r50k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(string))


if __name__ == "__main__":
    rp =GptResponse(stream=False)
    rp1 = rp.getResponse("请回复123456789123456789")
    for i in rp1:
        print(i, end="")
    print(rp.outputTokens, rp.messages)
# sk-00817ca06cb34a57bebe7a6d13c19b16
from http import HTTPStatus
import dashscope
dashscope.api_key="sk-00817ca06cb34a57bebe7a6d13c19b16"

model = ["qwen-turbo", "qwen-plus", "qwen-max", "qwen-max-1201", "qwen-max-longcontext"]



def sample_sync_call_streaming():
    response_generator = dashscope.Generation.call(
        model='qwen-max-longcontext',
        stream=True,
        top_p=0.8,
        messages=[{'role': 'system', 'content': '用英文回答我的问题'}, {'role': 'user', 'content': '如何做炒西红柿鸡蛋？'}],
        result_format='message'
        )

    # head_idx = 0
    # for response in response_generator:
    #     # print(response.output.choices[0].message.content)
    #     # print(response.output.finish_reason)

    #     output = response.output
    #     if not output:
    #         continue
        
    #     paragraph = output.choices[0].message.content
    #     print(f"\r{paragraph[head_idx:len(paragraph)]}", end='')
    #     if(paragraph.rfind('\n') != -1):
    #         head_idx = paragraph.rfind('\n') + 1
    
    retDict  = {"streamText": []}
    
    for response in response_generator:
        pass
    
    



def call_with_messages():
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': '如何做炒西红柿鸡蛋？'}]

    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_turbo,
        messages=messages,
        result_format='message',  # set the result to be "message" format.
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))

"""
stream: False
response:

{
    "status_code": 200,
    "request_id": "9da1ba31-b22a-9540-be18-793672d1ac8f",
    "code": "",
    "message": "",
    "output": {
        "text": null,
        "finish_reason": null,
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": "做西红柿鸡蛋的步骤如下：\n\n材料：\n- 鸡蛋 3 个\n- 西红柿 2 个\n-葱 适量\n- 蒜 适量\n- 盐 适量\n- 生抽 适量\n- 糖 适量\n- 胡椒粉 适量\n- 水淀粉 适量\n\n步骤：\n1. 西红柿去皮，切块；鸡蛋打散，加入适量盐和胡椒粉调味；\n2. 锅中加入适量油，倒入鸡蛋液，炒散；\n3. 加入葱蒜末，翻炒均匀；\n4. 加入西红柿块，翻炒至软烂；\n5. 加入适量生抽和糖，翻炒均匀；\n6. 最后加入适量水淀粉，翻炒均匀即可。"
                }
            }
        ]
    },
    "usage": {
        "input_tokens": 31,
        "output_tokens": 183
    }
}

stream = True
for resp in response

{
    "status_code": 200, 
    "request_id": "c8829094-dca8-9c74-8b01-7ceaf0aa1f32",
    "code": "", 
    "message": "", 
    "output":{
        "text": null, 
        "finish_reason": null, 
        "choices": [
                    {
                    "finish_reason": "null", 
                    "message": {
                        "role": "assistant", 
                        "content": "To make Stir-Fried Tomatoes and Eggs, follow these steps:\n\nIngredients:\n"
                        }
                    }
        ]
    }, 
    "usage": {
                "input_tokens": 15, 
                "output_tokens": 16, 
                "total_tokens": 31
            }
}
"""

if __name__ == "__main__":
    sample_sync_call_streaming()
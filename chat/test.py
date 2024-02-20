from openai import OpenAI
CLIENT = OpenAI(api_key="sk-ZIr0NobW1Q8OwuLLikwYjHDqc77FzuszL8iaL2BIqLBrRIb4",
                base_url="https://api.chatanywhere.tech/v1", max_retries=2)


def getResponse():
    response = CLIENT.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."}, {
            "role": "user", "content": "我在测试，请回复1"}],
        stream=False,
    )
    return response


"""
stream = False
response.model_dump_json():str 

{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "The 2020 World Series was played in Texas at Globe Life Field in Arlington.",
        "role": "assistant"
      },
      "logprobs": null
    }
  ],
  "created": 1677664795,
  "id": "chatcmpl-7QyqpwdfhqwajicIEznoc6Q47XAyW",
  "model": "gpt-3.5-turbo-0613",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 17,
    "prompt_tokens": 57,
    "total_tokens": 74
  }
}

stream = True
for resp in response:
    resp.model_dump_json():str 

{
    "id":"chatcmpl-8tr6wM9VMuZO0dcpg5lpAOdyeF2Hg",
    "choices":[
        {
            "delta":{
                "content":"1",
                "function_call":null,
                "role":null,"tool_calls":
                null
                },
            "finish_reason":null,
            "index":0,"logprobs":null
        }
    ],
    "created":1708322890,
    "model":"gpt-3.5-turbo-0613",
    "object":"chat.completion.chunk",
    "system_fingerprint":null
}

"""
if __name__ == "__main__":
    rps = getResponse()
    # print(rps.usage)
    # for chunk in rps:
    #     print(chunk.model_dump_json())
    # print(dir(rps.response))
    """'aclose', 'aiter_bytes', 'aiter_lines', 'aiter_raw', 'aiter_text', 'aread', 'charset_encoding', 'close', 'content', 'cookies', 'default_encoding', 'elapsed', 'encoding', 'extensions', 'has_redirect_location', 'headers', 'history', 'http_version', 'is_client_error', 'is_closed', 'is_error', 'is_informational', 'is_redirect', 'is_server_error', 'is_stream_consumed', 'is_success', 'iter_bytes', 'iter_lines', 'iter_raw', 'iter_text', 'json', 'links', 'next_request', 'num_bytes_downloaded', 'raise_for_status', 'read', 'reason_phrase', 'request', 'status_code', 'stream', 'text', 'url']"""
    # print(rps.response.raise_for_status())
    # for chunk in rps:
      # print(dir(chunk))
      # """'choices', 'construct', 'copy', 'created', 'dict', 'from_orm', 'id', 'json', 'model', 'model_computed_fields', 'model_config', 'model_construct', 'model_copy', 'model_dump', 'model_dump_json', 'model_extra', 'model_fields', 'model_fields_set', 'model_json_schema', 'model_parametrized_name', 'model_post_init', 'model_rebuild', 'model_validate', 'model_validate_json', 'model_validate_strings', 'object', 'parse_file', 'parse_obj', 'parse_raw', 'schema', 'schema_json', 'system_fingerprint', 'update_forward_refs', 'validate'"""
      # print(chunk.model_json_schema())
    print(dir(rps))

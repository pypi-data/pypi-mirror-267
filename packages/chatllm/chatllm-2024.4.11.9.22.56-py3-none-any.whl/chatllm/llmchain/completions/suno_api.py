#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : suno_api
# @Time         : 2024/4/3 16:46
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://suno.gcui.art/docs


from meutils.pipe import *

base_url = os.getenv("SUNO_BASE_URL")


def custom_generate_audio(payload):
    """
    {
      "prompt": "歌词",
      "tags": "pop metal male melancholic",
      "title": "歌名",
      "make_instrumental": False,
      "wait_audio": False,
    }

    :param payload:
    :return:
    """
    url = f"{base_url}/api/custom_generate"
    response = httpx.post(url, json=payload)
    return response.json()


def generate_audio_by_prompt(payload):
    """
    {
        "prompt": "A popular heavy metal song about war, sung by a deep-voiced male singer, slowly and melodiously. The lyrics depict the sorrow of people after the war.",
        "make_instrumental": False,
        "wait_audio": False
    }
    :param payload:
    :return:
    """
    url = f"{base_url}/api/generate"
    response = httpx.post(url, json=payload)
    return response.json()


def get_audio_information(audio_ids):
    url = f"{base_url}/api/get?ids={audio_ids}"
    response = httpx.get(url)
    return response.json()


def get_quota_information():
    url = f"{base_url}/api/get_limit"
    response = httpx.get(url)
    return response.json()


def song_info(df):
    """
    #   'audio_url': 'https://cdn1.suno.ai/63c85335-d8ec-4e17-882a-e51c2f358b2d.mp3',
    #   'video_url': 'https://cdn1.suno.ai/25c7e34b-6986-4f7c-a5f2-537dd80e370c.mp4',
    # https://cdn1.suno.ai/image_bea09d9e-be4a-4c27-a0bf-67c4a92d6e16.png
    :param df:
    :return:
    """
    df['🎵音乐链接'] = df['id'].map(
        lambda x: f"**请两分钟后试听**[🎧音频](https://cdn1.suno.ai/{x}.mp3)[▶️视频](https://cdn1.suno.ai/{x}.mp4)"
    )
    df['专辑图'] = df['image_url'].map(lambda x: f"![🖼]({x})")

    df_ = df[["created_at", "model_name", "🎵音乐链接", "专辑图"]]

    return f"""
🎵 **「{df['title'][0]}」**

`风格: {df['tags'][0]}`

```toml
{df['lyric'][0]}
```


{df_.to_markdown(index=False).replace('|:-', '|-').replace('-:|', '-|')}
    """


from meutils.pipe import *
from meutils.cache_utils import ttl_cache
from meutils.decorators.retry import retrying
from meutils.queues.smooth_queue import SmoothQueue

from meutils.notice.feishu import send_message

from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk

from chatllm.llmchain.completions import openai_completions
from chatllm.schemas.openai_api_protocol import ChatCompletionRequest, UsageInfo
from chatllm.schemas.suno_types import SunoRequest
from chatllm.schemas.openai_types import chat_completion, chat_completion_chunk

from chatllm.utils.openai_utils import to_openai_completion_params, openai_response2sse


class Completions(object):

    def __init__(self, api_key):
        self.httpx_aclient = httpx.AsyncClient(
            base_url=os.getenv("SUNO_BASE_URL", api_key),
            follow_redirects=True,
            timeout=30)

    async def acreate(self, request: ChatCompletionRequest):
        async for content in self._acreate(request):
            chat_completion_chunk.choices[0].delta.content = content
            yield chat_completion_chunk
        # 结束标识
        chat_completion_chunk.choices[0].delta.content = ""
        chat_completion_chunk.choices[0].finish_reason = "stop"
        yield chat_completion_chunk

    async def _acreate(self, request: ChatCompletionRequest):

        prompt = request.messages[-1]["content"]
        if prompt.startswith(("使用四到五个字直接返回这句话的简要主题",)):
            return

        if request.model.startswith("suno-custom"):  # todo: gpt解析入参
            payload = {
                "prompt": prompt,
                # "tags": "歌曲风格（英文）",
                # "title": "歌名",
            }
            df = await self.custom_generate(payload)
        else:
            payload = {
                "prompt": prompt,
                "make_instrumental": False,
                "wait_audio": False
            }
            df = await self.generate_by_prompt(payload)

        ids = ','.join(df['id'].tolist())

        yield f"""```\nTask ids: {ids}\n```\n\n"""
        yield f"""[音乐任务]("""

        for i in range(100):
            yield f"""{'🎵' if i % 2 else '🔥'}"""
            await asyncio.sleep(1)

            if i > 10:  # 5秒后才开始回调
                await asyncio.sleep(3)
                df = await self.get_information(ids)

                logger.debug("回调歌曲")

                if all(df.status == 'streaming'):  # 歌词生成
                    yield f""") ✅\n\n"""
                    _ = song_info(df)
                    yield _
                    send_message(_)
                    break
                elif all(df.status == 'error'):
                    yield f""") ❎\n\n"""
                    yield f"""⚠️触发内容审查，请修改后重试"""
                    send_message(df.to_markdown())
                    break

    def create_sse(self, request: ChatCompletionRequest):
        return openai_response2sse(self.acreate(request), redirect_model=request.model)

    @retrying
    async def custom_generate(self, payload):
        response = await self.httpx_aclient.post("/api/custom_generate", json=payload)
        return pd.DataFrame(response.json())

    @retrying
    async def generate_by_prompt(self, payload):
        response = await self.httpx_aclient.post("/api/generate", json=payload)
        return pd.DataFrame(response.json())

    @retrying
    async def get_information(self, ids):
        response = await self.httpx_aclient.get(f"/api/get?ids={ids}")
        return pd.DataFrame(response.json())


if __name__ == '__main__':
    data = generate_audio_by_prompt({
        "prompt": "A popular heavy metal song about war, sung by a deep-voiced male singer, slowly and melodiously. The lyrics depict the sorrow of people after the war.",
        "make_instrumental": False,
        "wait_audio": False
    })

    ids = f"{data[0]['id']},{data[1]['id']}"
    print(f"ids: {ids}")

    for _ in range(60):
        data = get_audio_information(ids)
        if data[0]["status"] == 'streaming':
            print(f"{data[0]['id']} ==> {data[0]['audio_url']}")
            print(f"{data[1]['id']} ==> {data[1]['audio_url']}")
            break
        # sleep 5s
        time.sleep(5)

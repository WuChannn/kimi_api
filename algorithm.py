import simplejson
from pathlib import Path
from openai import OpenAI


class FileExtrator:
    def __init__(self):

        self.client = OpenAI(
            api_key = "YOUR_API_KEY",
            base_url= "https://api.moonshot.cn/v1",
        )

    def extract(self, file_info):

        if isinstance(file_info, str):
            """file_info 是文件路径"""
            file_object = self.client.files.create(file=Path(file_info), purpose="file-extract")
        else:
            raise Exception("file_info type error")

        file_content = self.client.files.content(file_id=file_object.id).text

        # 把它放进请求中
        messages = [
            {
                "role": "system",
                "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。",
            },
            {
                "role": "system",
                "content": file_content,
            },
            {
                "role": "user",
                "content": "深吸一口气，好好理解一下文件内容，正确得出这份文件所盖的公章名称、外包公司和服务法人公司；然后，好好看看服务人员的姓名及对应的证件号码，正确得出服务人员信息的完整列表，注意，必须是包括所有服务人员的完整信息列表。将上述的所有结果以json格式输出，不说其他废话。"
            },
        ]

        # 然后调用 chat-completion, 获取 Kimi 的回答
        completion = self.client.chat.completions.create(
        model="moonshot-v1-32k",
        messages=messages,
        temperature=0.3,
        )

        response_str = completion.choices[0].message.content[8:-3]
        response_json = simplejson.loads(response_str)

        return response_json


file_extarcotr = FileExtrator()
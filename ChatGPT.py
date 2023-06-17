# coding='utf-8'
import ast
import sys
import json
import time
import Image
import openai
import numpy as np
from functions import functions
from WeatherInquiry import Weather


class ChatGpt:
    def __init__(self):
        openai.api_key = ''
        self.avatar = {"system": "\U0001F916", "user": "\U0001F600", "assistant": "\U0001F916", "function": "\U0001F4DD"}
        self.conversations = {}
        self.time_max_wait = 1000  # second
        self.system_content = "如果需要显示公式，请使用matplotlib能渲染的格式"
        self.img_url = None
        self.img = None
        self.print_str = None

    def msg_maker(self, user, msgs=None, action='question'):
        if action == 'omission':
            self.conversations[user].pop()
            while self.conversations[user][-1]["role"] == "user":
                self.conversations[user].pop()
            action = 'question'
        if action == 'question':
            if user not in self.conversations or time.time() - self.conversations[user][0] > self.time_max_wait:
                self.conversations[user] = [time.time(), {"role": "system", "content": self.system_content}]
            for msg in msgs:
                self.conversations[user].append({"role": "user", "content": msg})
            self.conversations[user][0] = int(time.time())
        elif action == 'answer':
            self.conversations[user].append({"role": "assistant", "content": msgs})
        elif action == 'requestFail':
            while self.conversations[user][-1]["role"] != "user":
                self.conversations[user].pop()
            while self.conversations[user][-1]["role"] == "user":
                self.conversations[user].pop()
        return self.conversations[user][1:]

    def get_response(self, user='tester', questions=['hello'], omission=False, messages=None):
        for question in questions:
            print(f'{self.avatar["user"]}:{question}')
        try:
            if messages:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-0613",
                    messages=messages
                )
            else:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-0613",
                    messages=self.msg_maker(user, questions, 'omission' if omission else 'question'),
                    functions=functions,
                    function_call="auto",
                )
            res = self.response_analyze(response, user)
            if messages is None:
                self.msg_maker(user, self.print_str, 'answer')
        except Exception as e:
            print(f'{sys._getframe().f_code.co_name} {e}')
            res = f"获取信息失败，请稍后重试。"
            self.msg_maker(user, action='requestFail')
        print(f'{self.avatar["assistant"]}:{self.print_str}\n')
        return res

    def response_analyze(self, response, user):
        message = response["choices"][0]["message"]
        if message.get("function_call"):
            function_name = message["function_call"]["name"]
            function = getattr(self, function_name, None) or getattr(Weather(), function_name, None)
            if function is None:
                print(f'函数：{function_name}未找到')
                self.print_str = f"调用函数{function_name}失败"
                return self.print_str
            arguments = ast.literal_eval(message['function_call']['arguments'])
            function_response = function(**arguments)
            if type(function_response) is np.ndarray:
                self.msg_maker(user, self.img_url, 'answer')
                self.print_str = self.img_url
                res = function_response
            elif type(function_response) is dict:
                self.conversations[user].append(message)
                self.conversations[user].append({"role": "function", "name": function_name, "content": json.dumps(function_response)})
                res = self.get_response(user, questions=[json.dumps(function_response)], messages=self.conversations[user][1:])
        else:
            res = message['content'].strip()
            self.print_str = res
        return res

    def img_generation(self, image_description, image_num=1, size="1024x1024"):
        print(f'作画描述：{image_description}')
        try:
            response = openai.Image.create(
                prompt=image_description,
                n=int(image_num),
                size=size
            )
            self.img_url = response['data'][0]['url']
            self.img = Image.get_img_for_url(self.img_url)
        except Exception as e:
            self.img_url = '作画失败，我的画笔还未准备好，请稍后重试'
            self.img = self.img_url
            print(f'{self.img_url}\n{e}')

        return self.img

    def show_conversations(self):
        for user, conversations in self.conversations.items():
            print(user.window_text())
            for conversation in conversations[1:]:
                print(f'{self.avatar[conversation["role"]]}:{conversation["content"]}')
            print()


if __name__ == '__main__':
    chatgpt = ChatGpt()
    chatgpt.get_response(questions=['南宁市的天气如何'])

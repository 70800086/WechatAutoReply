# coding='utf-8'
import time
import Image
import openai


class ChatGpt:
    def __init__(self):
        openai.api_key = ''
        self.avatar = {"system": "\U0001F916", "user": "\U0001F600", "assistant": "\U0001F916"}
        self.conversations = {}
        self.time_max_wait = 300  # second
        self.system_content = "如果需要显示公式，请使用matplotlib能渲染的格式"
        self.draw_key = ['画', '找']
        self.img_url = None
        self.img = None

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
            while self.conversations[user][-1]["role"] == "user":
                self.conversations[user].pop()
        return self.conversations[user][1:]

    def get_response(self, user='tester', questions=['hello'], omission=False):
        for question in questions:
            print(f'{self.avatar["user"]}:{question}')
        # img
        if len(questions) == 1 and questions[0][0] in self.draw_key:
            self.img_generation(questions[0])
            self.msg_maker(user, questions, 'question')
            self.msg_maker(user, self.img_url, 'answer')
            print(f'{self.avatar["assistant"]}:{self.img_url}\n')
            return self.img
        # text
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.msg_maker(user, questions, 'omission'if omission else'question')
            )
            res = response['choices'][0]['message']['content'].strip()
            self.msg_maker(user, res, 'answer')
        except Exception as e:
            print(e)
            res = f"获取信息失败，请稍后重试。"
            self.msg_maker(user, action='requestFail')
        print(f'{self.avatar["assistant"]}:{res}\n')
        return res

    def img_generation(self, image_description):
        try:
            response = openai.Image.create(
                prompt=image_description,
                n=1,
                size="256x256"
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
    chatgpt.get_response(questions=['画一只可爱的猫'])

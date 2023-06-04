# coding='utf-8'
import re
import sys

import numpy as np
import uiautomation
from Render import Render
from pyperclip import copy
from ChatGPT import ChatGpt
from Image import copy_image_to_clipboard


class Wechat:
    def __init__(self):
        self.WechatWindow = uiautomation.WindowControl(ClassName='WeChatMainWndForPC')
        self.SessionList = self.WechatWindow.ListControl(Name='会话')
        self.EditMsg = self.WechatWindow.EditControl(Name='输入')
        self.chatgpt = ChatGpt()
        self.Render = Render()
        self.msgs = {}
        self.name = self.WechatWindow.ButtonControl().Name
        self.chat_is_group = False

    def at_user(self, user):
        # 实际上不能触发微信@提醒
        copy(f'@{user}\u2005')
        self.EditMsg.SendKeys('{Ctrl}v', waitTime=0)

    def is_formula(self, msg):
        if type(msg) is not str:
            return False
        pattern = r'\$.*?\$'
        return bool(re.search(pattern, msg))

    def send_msg(self, msg, at_user=None):
        self.WechatWindow.EditControl(Name='输入').Click(simulateMove=False)
        self.EditMsg.SendKeys('{Ctrl}a', waitTime=0)
        if at_user:
            self.at_user(at_user)
        if type(msg) is np.ndarray:
            copy_image_to_clipboard(msg)
        else:
            copy(msg)
        self.EditMsg.SendKeys('{Ctrl}v', waitTime=0)
        if self.is_formula(msg):
            try:
                self.Render.formula_conversion(msg)
            except Exception as e:
                copy('\n\n公式转换图片出错！请上报bug！')
                print(e)
            self.EditMsg.SendKeys('{Ctrl}v', waitTime=0)

        self.EditMsg.SendKeys('{Enter}', waitTime=0)

    def get_msgs(self):
        messages = self.WechatWindow.ListControl(Name='消息')
        msgs_unread = {}  # who: [msgs]
        self.chat_is_group = self.is_group()
        try:
            for message in messages.GetChildren():
                content = message.Name
                if self.chat_is_group:
                    if f'@{self.name}' in content:  # 艾特了我
                        nickname = message.TextControl().Name
                        if nickname in msgs_unread.keys():
                            msgs_unread[nickname].append(content.replace(f'@{self.name}\u2005', ''))
                        else:
                            msgs_unread[nickname] = [content.replace(f'@{self.name}\u2005', '')]
                    else:  # 检查是否回复
                        for at_name in msgs_unread.keys():
                            if f'@{at_name}' in content:
                                if message.GetChildren()[0].GetChildren()[2].Name:  # 我回复了Ta
                                    del msgs_unread[at_name]
                                    break
                else:
                    if content not in ["查看更多消息", "以下为新消息"]:
                        details = message.GetChildren()[0].GetChildren()
                        if len(details) != 0:  # 时间
                            nickname, detail, me = details
                            if nickname.Name:
                                if nickname.Name in msgs_unread.keys():
                                    msgs_unread[nickname.Name].append(content)
                                else:
                                    msgs_unread[nickname.Name] = [content]
                            elif me.Name:
                                msgs_unread = {}
        except Exception as e:
            print(f'get_msgs error {e}')
        return msgs_unread

    def has_unread_msgs(self):
        unread = self.SessionList.EditControl(searchDepth=3)
        if not unread.Exists(0):
            unread = self.SessionList.EditControl(SubName="有人@我", searchDepth=5)
            if unread.Exists(0) is False:
                # self.SessionList.GetChildren()[0].Click(simulateMove=False)
                if self.get_msgs() is {}:
                    return False
                else:
                    try:
                        name_button = self.WechatWindow.GetChildren()[1].GetChildren()[1].GetChildren()[
                            2].ButtonControl()
                        return name_button.Name
                    except Exception as e:
                        print(f'{sys._getframe().f_code.co_name} {e}')
                        return True
        unread.Click(simulateMove=False)
        parent2 = unread.GetParentControl().GetParentControl()
        return parent2.Name or parent2.GetParentControl().GetParentControl().Name

    def msg_omission(self, user):
        try:
            msgs = self.get_msgs()
            if msgs[user] != self.msgs[user]:
                print(f'new msgs: {msgs}')
                print(f'old msgs: {self.msgs}')
                self.msgs = msgs
                return True
            return False
        except Exception as e:
            print(f'{sys._getframe().f_code.co_name} {e}, 是否正在切换对话框')
            return False

    def is_group(self):
        try:
            name_button = self.WechatWindow.GetChildren()[1].GetChildren()[1].GetChildren()[2].ButtonControl()
            number_of_group = name_button.GetNextSiblingControl()
            if number_of_group:
                pattern = r'^\s*\(\d+\)$'
                return bool(re.match(pattern, number_of_group.Name))
        except Exception as e:
            print(f'{sys._getframe().f_code.co_name} {e}')
            return False
        return False

    def get_first_key(self):
        return sorted(self.msgs.keys())[0]

    def run(self):
        while True:
            user = self.has_unread_msgs()
            if user:
                self.msgs = self.get_msgs()
                while self.msgs != {}:
                    first_key = self.get_first_key()
                    if self.chat_is_group:
                        user = f'{user}_{first_key}'
                    response = self.chatgpt.get_response(user, self.msgs[first_key])
                    while self.msg_omission(first_key):
                        response = self.chatgpt.get_response(user, self.msgs[first_key], omission=True)
                    self.send_msg(response, first_key if user != first_key else None)
                    del self.msgs[first_key]


if __name__ == '__main__':
    wechat = Wechat()
    wechat.run()

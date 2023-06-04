# WechatAutoReply/微信自动回复
<details open>
<summary>下载代码并安装环境</summary>

下载
```bash
git clone https://github.com/70800086/WechatAutoReply.git  # clone
```
安装
```bash
cd WechatAutoReply
pip install -r requirements.txt  # install
```
</details>

<details open>
<summary>介绍</summary>

- 模拟键鼠操作微信
- 调用chatgpt实现自动回复
  - 文字中存在公式时使用图片渲染并发送
- 调用DALL·E模型生成图片
</details>

<details open>
<summary>运行</summary>

1.在ChatGPT.py的openai.api_key中填上自己的key。
如果不清楚自己key可以打开[链接](https://platform.openai.com/account/api-keys)查询或生成

2.运行下列代码
```bash
python WeChat.py
```
</details>
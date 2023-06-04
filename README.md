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

<details open>
<summary>效果展示</summary>

![](https://raw.githubusercontent.com/70800086/imgs/master/WechatAutoReply/%E5%BE%AE%E4%BF%A1%E8%87%AA%E5%8A%A8%E5%9B%9E%E5%A4%8D%E6%95%88%E6%9E%9C%E5%9B%BE.jpg)

![](https://raw.githubusercontent.com/70800086/imgs/master/WechatAutoReply/%E6%AC%A7%E6%8B%89%E5%85%AC%E5%BC%8F%E5%9B%9E%E5%A4%8D%E5%9B%BE%E7%89%87.png)

![](https://raw.githubusercontent.com/70800086/imgs/master/WechatAutoReply/%E6%97%A5%E8%90%BD%E5%9B%BE%E7%89%87.png)
</details>
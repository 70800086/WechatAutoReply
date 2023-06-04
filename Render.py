# coding='utf-8'
import cv2
import numpy as np
from PIL import Image
import win32clipboard
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg


class Render:
    def __init__(self, fig_size=(20, 20), font_size=12, blank=15):
        plt.rcParams["font.sans-serif"] = ["SimSun"]  # 设置字体
        plt.rcParams['mathtext.fontset'] = 'stix'
        plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题
        plt.rcParams['font.size'] = font_size
        # plt.rcParams['text.usetex'] = True
        self.fig_size = fig_size
        self.blank = blank
        self.replacements = {
            '\n\n$$\n': '\n\n$',
            '\n$$\n\n': '$\n\n',
            '$$': '$',
            '\text': '\mathrm',
            '\a': '\\a',
            '\b': '\\b',
            '\f': '\\f',
            '\r': '\\r',
            '\t': '\\t',
            '\v': '\\v',
            '\le': '<=',
            'boldsymbol': 'mathbf',
            '\limits': ''
        }

    def text_replace(self, text):
        for old, new in self.replacements.items():
            text = text.replace(old, new)
        return text

    def text2img(self, text, show):

        fig, ax = plt.subplots(figsize=self.fig_size)
        ax.text(0, 1, text, verticalalignment='top', wrap=True)
        ax.axis('off')
        canvas = FigureCanvasAgg(fig)
        canvas.draw()

        img = cv2.cvtColor(np.array(canvas.renderer.buffer_rgba()), cv2.COLOR_RGB2BGR)
        h, w, c = img.shape

        mask = img > 128
        row_mask = mask.all(axis=(1, 2))
        col_mask = mask.all(axis=(0, 2))
        y0 = row_mask.argmin()
        y1 = h - row_mask[::-1].argmin()
        x0 = col_mask.argmin()
        x1 = w - col_mask[::-1].argmin()

        x0 = max(0, x0 - self.blank)
        y0 = max(0, y0 - self.blank)
        x1 = min(w - 1, x1 + self.blank)
        y1 = min(h - 1, y1 + self.blank)
        crop = img[y0: y1, x0: x1]
        if show:
            cv2.imshow('img', img)
            cv2.imshow('crop', crop)
            cv2.waitKey(0)
        return crop

    def copy_image_to_clipboard(self, img):
        output = BytesIO()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img)
        img_pil.save(output, format='BMP')
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

    def formula_conversion(self, formula, show=False):
        text_formatted = self.text_replace(formula)
        img = self.text2img(text_formatted, show)
        self.copy_image_to_clipboard(img)


if __name__ == '__main__':
    formula = "根据有关规范，岩石饱和单轴抗压强度的标准值应使用下列公式计算：\n\n$$\sigma_{ci}=c+0.8\sigma_{ti}$$\n\n其中，$\sigma_{ci}$为岩石饱和单轴抗压强度标准值，$c$为岩石内聚力标准值，$\sigma_{ti}$为岩石饱和单轴抗张强度标准值。\n\n根据试验结果，8个试样的平均值为：\n\n$$\bar{\sigma_t}=\frac{15+13+17+13+15+12+14+15}{8}=14.25 MPa$$\n\n则岩石饱和单轴抗张强度的标准值为：\n\n$$\sigma_{ti}=0.72\bar{\sigma_t}=0.72\times14.25=10.26 MPa$$\n\n为了估算内聚力$c$，可以使用一般规律，即岩石内聚力与饱和单轴抗压强度的关系为$c = k\sigma_{ci}$。根据经验，取$k=0.1$，则有：\n\n$$c = 0.1\sigma_{ci}$$\n\n入前面的公式，可得：\n\n$$\sigma_{ci}=c+0.8\sigma_{ti}=0.1\sigma_{ci}+0.8\times10.26$$\n\n化简可得：\n\n$$\sigma_{ci}=90.54 MPa$$\n\n因此，该岩石地基的岩石饱和单轴抗压强度标准值为$90.54 MPa$。"
    render = Render()
    render.formula_conversion(formula=formula, show=True)


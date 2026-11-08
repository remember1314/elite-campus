# -*- coding: utf-8 -*-
"""生成方版二维码卡（1080x1080）：评论区缩略图也能看清。

    python make_qr_card.py <URL> [输出路径]

和 poster.py 的区别：这张只放二维码，缩略图更大更清楚，
适合单独发一条评论（长图海报缩略图太小，别人容易看不清码）。
"""
import sys

import qrcode
from PIL import Image, ImageDraw, ImageFont

SERIF = r"C:\Windows\Fonts\simsun.ttc"
SANS = r"C:\Windows\Fonts\msyh.ttc"

INK = (23, 19, 14)
PAPER = (241, 234, 217)
RED = (191, 44, 34)
MUTED = (110, 100, 84)

W = H = 1080
M = 64


def F(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)


def center_text(d, s, font, y, fill):
    w = d.textbbox((0, 0), s, font=font)[2]
    d.text(((W - w) // 2, y), s, font=font, fill=fill)


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else "https://remember1314.github.io/elite-campus/"
    out = sys.argv[2] if len(sys.argv) > 2 else "qr_card.png"

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # 双线边框
    d.rectangle([M, M, W - M, H - M], outline=INK, width=3)
    d.rectangle([M + 10, M + 10, W - M - 10, H - M - 10], outline=(203, 193, 173), width=1)

    # 标题
    center_text(d, "实力至上主义校园", F(SERIF, 56), M + 40, INK)
    center_text(d, "校 园 打  ·  扫 码 入 学", F(SANS, 24), M + 116, MUTED)

    # 二维码：先探测模块数，再整数倍放大，保证模块等宽
    probe = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=1, border=2)
    probe.add_data(url)
    probe.make(fit=True)
    modules = probe.modules_count + 4
    box = max(2, 540 // modules)
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=box, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    qimg = qr.make_image(fill_color=INK, back_color="white").convert("RGB")
    qs = qimg.size[0]

    qx = (W - qs) // 2
    qy = M + 200
    d.rectangle([qx - 16, qy - 16, qx + qs + 16, qy + qs + 16], fill="white", outline=INK, width=3)
    img.paste(qimg, (qx, qy))

    # 底部文字从画框底部往上锚定，避免压线
    center_text(d, "扫码即玩 · 手机竖屏 · 不用下载", F(SANS, 34), H - M - 160, INK)
    center_text(d, "扫不了码：浏览器里输入下面这行", F(SANS, 22), H - M - 108, MUTED)
    center_text(d, url.split("://")[-1].rstrip("/"), F(SANS, 26), H - M - 66, RED)

    img.save(out, quality=95)
    print("saved", out, img.size)


if __name__ == "__main__":
    main()




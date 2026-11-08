# -*- coding: utf-8 -*-
"""生成 B 站评论区用的二维码海报：纸感底 + 宋体标题 + 朱红印章 + 二维码。

用法：
    python poster.py https://你的用户名.github.io/elite-campus/
输出：poster.png（1080x1440），B 站评论图 / 动态图都能直接用。
"""
import sys, pathlib
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter

URL = sys.argv[1] if len(sys.argv) > 1 else "https://example.github.io/elite-campus/"
OUT = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else pathlib.Path(r"D:\dp\elite-campus\publish\poster.png")

INK = (23, 19, 14)
PAPER = (241, 234, 217)
RED = (191, 44, 34)
MUTED = (110, 100, 84)
SERIF = r"C:\Windows\Fonts\simsun.ttc"
SANS = r"C:\Windows\Fonts\msyh.ttc"

W, H = 1080, 1440

def F(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)

# ---------- 底：纸色 + 横纹 + 暗角 ----------
img = Image.new("RGB", (W, H), PAPER)
pen = ImageDraw.Draw(img)
for y in range(0, H, 28):
    pen.line([(0, y), (W, y)], fill=(233, 226, 210), width=1)

mask = Image.new("L", (W, H), 0)
md = ImageDraw.Draw(mask)
for i in range(170):
    md.rectangle([i, i, W - i, H - i], outline=int(30 * (1 - i / 170)))
mask = mask.filter(ImageFilter.GaussianBlur(28))
img = Image.composite(Image.new("RGB", (W, H), (206, 196, 175)), img, mask)

d = ImageDraw.Draw(img)

# ---------- 框 ----------
m = 56
d.rectangle([m, m, W - m, H - m], outline=INK, width=3)
d.rectangle([m + 10, m + 10, W - m - 10, H - m - 10], outline=INK, width=1)

def center(s, f, y, fill):
    d.text(((W - d.textbbox((0, 0), s, font=f)[2]) // 2, y), s, font=f, fill=fill)

# ---------- 抬头 ----------
f_small = F(SANS, 20)
d.text((m + 44, m + 40), "校务会备案号：瞎编的", font=f_small, fill=MUTED)
d.text((m + 44, m + 70), "校园打 App v1.0.0", font=f_small, fill=MUTED)

# ---------- 标题 ----------
f_title = F(SERIF, 92)
d.text((m + 44, m + 128), "实力至上", font=f_title, fill=INK)
d.text((m + 44, m + 228), "主义校园", font=f_title, fill=INK)
d.text((m + 48, m + 340), "T H E   C A M P U S   O F   A B I L I T Y", font=F(SANS, 16), fill=MUTED)
d.text((m + 48, m + 364), "S U P R E M A C Y", font=F(SANS, 16), fill=MUTED)

# ---------- 引文 ----------
f_body = F(SANS, 27)
d.line([(m + 48, m + 424), (m + 51, m + 500)], fill=RED, width=4)
d.text((m + 78, m + 428), "「战斗对身体的锻炼效率，", font=f_body, fill=INK)
d.text((m + 78, m + 468), "　是跑步的 1.8 倍。」", font=f_body, fill=INK)

# ---------- 玩法 ----------
d.text((m + 48, m + 518), "12 周 · 每周必须打一场 · 积分第一去打校长副本", font=F(SANS, 30), fill=INK)
d.text((m + 48, m + 566), "手机竖屏可玩，打开就打，不用下载", font=F(SANS, 24), fill=MUTED)

# ---------- 二维码 ----------
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=2)
qr.add_data(URL)
qr.make(fit=True)
qimg = qr.make_image(fill_color=INK, back_color="white").convert("RGB")

QS = 380
qimg = qimg.resize((QS, QS), Image.NEAREST)
cx, cy = (W - QS) // 2, 700
pad = 14
d.rectangle([cx - pad - 4, cy - pad - 4, cx + QS + pad + 4, cy + QS + pad + 4], fill=INK)
d.rectangle([cx - pad, cy - pad, cx + QS + pad, cy + QS + pad], fill=(255, 255, 255))
img.paste(qimg, (cx, cy))

center("扫码即玩 · 长按图片识别二维码", F(SANS, 32), cy + QS + 42, INK)

f_url = F(SANS, 21)
u = URL.replace("https://", "").replace("http://", "").rstrip("/")
if len(u) > 48:
    u = u[:46] + "…"
center(u, f_url, cy + QS + 90, MUTED)

# ---------- 印章（2x2 篆刻感） ----------
S = 190
stamp = Image.new("RGBA", (S, S), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rectangle([6, 6, S - 6, S - 6], outline=RED + (235,), width=6)
f_ch = F(SERIF, 58)
chars = ["扫", "码", "入", "学"]
# 横排两行，读作「扫码入学」
pos = [(24, 20), (100, 20), (24, 98), (100, 98)]
for ch, (x, y) in zip(chars, pos):
    sd.text((x, y), ch, font=f_ch, fill=RED + (240,))
stamp = stamp.rotate(-7, expand=True, resample=Image.BICUBIC)
img.paste(stamp, (W - S - 96, 150), stamp)

# ---------- 页脚 ----------
f_foot = F(SANS, 19)
d.text((m + 48, H - 150), "本作依据 B 站视频《欢迎来到实力至上主义校园》改编，纯属虚构，", font=f_foot, fill=MUTED)
d.text((m + 48, H - 120), "与任何真实学校、真实 App 以及达尔文先生无关。", font=f_foot, fill=MUTED)

OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT, "PNG")
print("saved", OUT, img.size)



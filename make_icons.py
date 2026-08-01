#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 PWA 图标：暗底 + 金色地球经纬线 + 五区色点。"""
import os, math
from PIL import Image, ImageDraw

OUT = os.path.dirname(os.path.abspath(__file__))
BG = (15, 17, 21)          # #0f1115
PANEL = (23, 26, 33)       # #171a21
ACCENT = (240, 180, 41)    # #f0b429
REGION = [(79,140,255),(46,204,155),(181,126,220),(232,87,74),(255,140,66)]

def draw_icon(size, pad_ratio=0.0, bg=BG):
    S = 1024
    img = Image.new("RGBA", (S, S), (0,0,0,0))
    d = ImageDraw.Draw(img)
    # 圆角背景
    r = int(S*0.22)
    d.rounded_rectangle([0,0,S-1,S-1], radius=r, fill=bg)
    cx, cy = S//2, int(S*0.44)
    R = int(S*0.26)
    lw = max(6, int(S*0.012))
    # 地球外圈
    d.ellipse([cx-R, cy-R, cx+R, cy+R], outline=ACCENT, width=lw)
    # 经线（竖向椭圆）
    for f in (0.5, 1.0):
        rw = int(R*f)
        if rw>0:
            d.ellipse([cx-rw, cy-R, cx+rw, cy+R], outline=ACCENT, width=max(3,lw//2))
    # 纬线（横线）
    for fy in (-0.5, 0.0, 0.5):
        yy = int(cy + R*fy)
        half = int(math.sqrt(max(0, R*R - (R*fy)**2)))
        d.line([cx-half, yy, cx+half, yy], fill=ACCENT, width=max(3,lw//2))
    # 底部五区色点
    n = len(REGION)
    dot = int(S*0.05)
    gap = int(S*0.035)
    total = n*dot + (n-1)*gap
    x0 = (S-total)//2
    y0 = int(S*0.80)
    for i,c in enumerate(REGION):
        x = x0 + i*(dot+gap)
        d.ellipse([x, y0, x+dot, y0+dot], fill=c)
    # maskable 安全区留白：整体缩放
    if pad_ratio>0:
        inner = int(S*(1-2*pad_ratio))
        content = img.resize((inner, inner), Image.LANCZOS)
        base = Image.new("RGBA",(S,S), bg+(255,))
        base.paste(content, ((S-inner)//2,(S-inner)//2), content)
        img = base
    return img.resize((size,size), Image.LANCZOS)

specs = [
    ("icon-192.png", 192, 0.0),
    ("icon-512.png", 512, 0.0),
    ("icon-512-maskable.png", 512, 0.14),
    ("apple-touch-icon.png", 180, 0.06),
    ("favicon-32.png", 32, 0.0),
]
for name, sz, pad in specs:
    ic = draw_icon(sz, pad)
    if name.startswith("apple"):
        ic = ic.convert("RGB")  # iOS 不喜欢透明/alpha
    ic.save(os.path.join(OUT, name))
    print("wrote", name, sz)
print("done")

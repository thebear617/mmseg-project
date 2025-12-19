# -*- coding: utf-8 -*-
"""
Demo：语义分割标注(mask)按调色盘上色，并叠加到原图上显示
1）可以批量/单张
2）可以按顺序抽取,可以随机抽取
3）可以选择是否添加颜色图例 (legend)
========================================================

✅ 你要可视化其他数据集时，通常只需要替换下面这些地方：
1) PATH_IMAGE：训练/验证/测试的原图目录
2) PATH_MASKS：对应的掩码目录（单通道类别索引图：0..K-1）
3) IMG_SUFFIX / MASK_SUFFIX：图像与掩码后缀
4) PALETTE：类别名+RGB颜色（长度=类别数K；mask里的像素值必须在[0, K-1]）
5) （可选）alpha：叠加透明度；bg_transparent：背景是否透明

# 命令行中常需要替换的
1）path to script: 该文件的实际路径
2）--save: 输出路径
3）--name: 单张图片 stem（不含后缀）

使用示例：
1) 单张可视化（显示窗口）：
   python my_scripts/D_vis_overlay.py --mode single --name 04_35-2 --alpha 0.55

2) 批量 n×n 网格可视化（显示窗口）：
   python my_scripts/D_vis_overlay.py --mode batch --n 4 --alpha 0.55

3) 批量随机抽样：
   python my_scripts/D_vis_overlay.py --mode batch --n 4 --shuffle

4) 保存结果图（单张 or 批量）：
   python my_scripts/D_vis_overlay.py --mode single --name 04_35-2 --save outputs/one.png
   python my_scripts/D_vis_overlay.py --mode batch  --n 4           --save outputs/grid.png

5) 显示图例（单张/批量都支持）：
   python my_scripts/D_vis_overlay.py --mode single --name 04_35-2 --legend
   python my_scripts/D_vis_overlay.py --mode batch  --n 4 --legend --save outputs/grid_with_legend.png
"""

import os
import argparse
import random
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


# ============ 需要你根据数据集替换的部分（本数据集已填好） ============
PATH_IMAGE = "data/Watermelon87_Semantic_Seg_Mask/img_dir/train"
PATH_MASKS = "data/Watermelon87_Semantic_Seg_Mask/ann_dir/train"
IMG_SUFFIX = ".jpg"
MASK_SUFFIX = ".png"

PALETTE = [
    ["background",  [127, 127, 127]],
    ["red",         [200,   0,   0]],
    ["green",       [0,   200, 0]],
    ["white",       [144, 238, 144]],
    ["seed-black",  [30,  30,  30]],
    ["seed-white",  [220,   220, 220]],
]
# ================================================================


def build_color_lut(palette):
    """把 PALETTE 转成 (K,3) 的 uint8 查找表，mask值=类别索引，直接查颜色。"""
    colors = np.array([c for _, c in palette], dtype=np.uint8)  # (K,3)
    names = [n for n, _ in palette]
    return colors, names


def load_pair(stem, img_dir, mask_dir, img_suf, mask_suf):
    """按同名 stem 加载 (image, mask)。stem 例如 '04_35-2'（不含后缀）。"""
    img_path = os.path.join(img_dir, stem + img_suf)
    msk_path = os.path.join(mask_dir, stem + mask_suf)
    if not os.path.isfile(img_path):
        raise FileNotFoundError(f"找不到图像：{img_path}")
    if not os.path.isfile(msk_path):
        raise FileNotFoundError(f"找不到掩码：{msk_path}")
    img = np.array(Image.open(img_path).convert("RGB"), dtype=np.uint8)      # (H,W,3)
    msk = np.array(Image.open(msk_path), dtype=np.uint8)                     # (H,W)
    return img, msk, img_path, msk_path


def mask_to_rgb(mask, color_lut):
    """单通道 mask -> RGB 伪彩色图。mask像素值作为索引查表。"""
    return color_lut[mask]  # (H,W,3)


def overlay(image_rgb, mask_rgb, mask_idx, alpha=0.55, bg_transparent=True):
    """
    叠加：overlay = image*(1-a) + mask_rgb*a
    - bg_transparent=True：背景类(=0)不叠加颜色，透明显示原图
    """
    img = image_rgb.astype(np.float32)
    msk = mask_rgb.astype(np.float32)

    if bg_transparent:
        a = (mask_idx > 0).astype(np.float32) * float(alpha)  # 背景0透明
    else:
        a = np.ones(mask_idx.shape, dtype=np.float32) * float(alpha)

    a = a[..., None]  # (H,W,1)
    out = img * (1.0 - a) + msk * a
    return np.clip(out, 0, 255).astype(np.uint8)


def list_stems(img_dir, img_suf):
    """列出图像目录里所有 stem（不含后缀）。"""
    stems = []
    for fn in os.listdir(img_dir):
        if fn.lower().endswith(img_suf.lower()):
            stems.append(os.path.splitext(fn)[0])
    stems.sort()
    return stems


def add_legend(fig, class_names, color_lut):
    """
    最简洁的图例：用 Patch 画颜色块 + 类别名，放在画布右侧。
    """
    handles = []
    for i, name in enumerate(class_names):
        rgb = (color_lut[i] / 255.0).tolist()
        handles.append(Patch(facecolor=rgb, edgecolor="none", label=f"{i}: {name}"))
    fig.legend(handles=handles, loc="center left", bbox_to_anchor=(1.02, 0.5),
               frameon=False, borderaxespad=0.0)


def show_single(stem, args, color_lut, class_names):
    """功能1：单张叠加显示（可保存）。"""
    img, msk, img_path, msk_path = load_pair(
        stem, PATH_IMAGE, PATH_MASKS, IMG_SUFFIX, MASK_SUFFIX
    )

    k = len(class_names)
    mx = int(msk.max())
    if mx >= k:
        raise ValueError(f"mask最大值={mx} 超出类别数K={k}，请检查PALETTE或标注编码！")

    out = overlay(img, mask_to_rgb(msk, color_lut), msk,
                  alpha=args.alpha, bg_transparent=not args.show_bg)

    fig = plt.figure(figsize=(10, 6))
    plt.imshow(out)
    plt.axis("off")
    plt.title(f"{stem} | alpha={args.alpha} | img={os.path.basename(img_path)} | mask={os.path.basename(msk_path)}")

    if args.legend:
        add_legend(fig, class_names, color_lut)
        plt.tight_layout(rect=[0, 0, 0.82, 1])  # 给右侧 legend 留空间
    else:
        plt.tight_layout()

    if args.save:
        plt.savefig(args.save, dpi=200, bbox_inches="tight", pad_inches=0)
        print(f"[Saved] {args.save}")
    plt.show()


def show_batch(args, color_lut, class_names):
    """功能2：批量 n×n 叠加显示（可保存）。"""
    stems = list_stems(PATH_IMAGE, IMG_SUFFIX)
    if args.shuffle:
        random.shuffle(stems)

    n = int(args.n)
    stems = stems[: n * n]

    fig = plt.figure(figsize=(3.2 * n, 3.2 * n))
    for i, stem in enumerate(stems, start=1):
        img, msk, *_ = load_pair(stem, PATH_IMAGE, PATH_MASKS, IMG_SUFFIX, MASK_SUFFIX)

        k = len(class_names)
        mx = int(msk.max())
        if mx >= k:
            raise ValueError(f"[{stem}] mask最大值={mx} 超出类别数K={k}，请检查PALETTE或标注编码！")

        out = overlay(img, mask_to_rgb(msk, color_lut), msk,
                      alpha=args.alpha, bg_transparent=not args.show_bg)

        ax = plt.subplot(n, n, i)
        ax.imshow(out)
        ax.set_title(stem, fontsize=10)
        ax.axis("off")

    if args.legend:
        add_legend(fig, class_names, color_lut)
        plt.tight_layout(rect=[0, 0, 0.82, 1])
    else:
        plt.tight_layout()

    if args.save:
        plt.savefig(args.save, dpi=200, bbox_inches="tight", pad_inches=0)
        print(f"[Saved] {args.save}")
    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["single", "batch"], required=True,
                        help="single: 单张；batch: 批量网格")
    parser.add_argument("--name", type=str, default="",
                        help="单张模式下的文件名stem（不含后缀），例如 04_35-2")
    parser.add_argument("--n", type=int, default=3,
                        help="批量模式下网格大小 n×n")
    parser.add_argument("--alpha", type=float, default=0.55,
                        help="叠加透明度（0~1）")
    parser.add_argument("--shuffle", action="store_true",
                        help="批量模式下随机抽样（否则取排序后的前n*n张）")
    parser.add_argument("--show_bg", action="store_true",
                        help="是否也把背景类(0)上色叠加（默认背景透明只显示原图）")
    parser.add_argument("--legend", action="store_true",
                        help="是否显示颜色图例（类别名+颜色块）")
    parser.add_argument("--save", type=str, default="",
                        help="保存输出图路径（可选）")
    args = parser.parse_args()

    color_lut, class_names = build_color_lut(PALETTE)

    if args.mode == "single":
        if not args.name:
            raise ValueError("single 模式必须指定 --name（不含后缀）")
        show_single(args.name, args, color_lut, class_names)
    else:
        show_batch(args, color_lut, class_names)


if __name__ == "__main__":
    main()
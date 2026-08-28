# -*- coding: utf-8 -*-
"""공통 그림 스타일 + 블록도(scheme) 작도 헬퍼.

색은 dataviz 스킬의 검증된 기본 팔레트를 그대로 사용한다(고정 순서, 순환 금지).
인쇄 지면(백색)에 대해 validate_palette.js 로 검증 완료:
  - 4슬롯 인접쌍: CVD dE 9.1 / 정상시야 dE 22.9  → PASS
  - 3슬롯 전체쌍: CVD dE 9.2 / 정상시야 dE 24.0  → PASS
  - aqua/yellow 는 백색 대비 3:1 미만 → 직접 라벨(relief rule) 필수
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np

# ── 팔레트 (고정 순서) ────────────────────────────────────────────────
S1, S2, S3, S4 = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"   # blue, orange, aqua, yellow
SERIES = [S1, S2, S3, S4]
SEQ = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]

INK      = "#0b0b0b"   # primary
INK2     = "#52514e"   # secondary
MUTED    = "#898781"   # axis / tick labels
GRID     = "#e1e0d9"
AXIS     = "#c3c2b7"
SURFACE  = "#ffffff"   # 인쇄 지면
BAND     = "#f0efec"   # 중립 음영 (규격대역, 적분구간 등)
CRIT     = "#d03b3b"   # status: critical  (한계선 전용)
GOOD     = "#0ca30c"   # status: good

FIGDIR = "figures"


def use_style():
    plt.rcParams.update({
        "font.family": "Noto Sans CJK KR",
        "font.size": 8.5,
        "axes.unicode_minus": False,
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "axes.edgecolor": AXIS,
        "axes.linewidth": 0.8,
        "axes.labelcolor": INK2,
        "axes.labelsize": 8.5,
        "axes.titlesize": 9.5,
        "axes.titleweight": "bold",
        "axes.titlecolor": INK,
        "axes.titlepad": 7,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": GRID,
        "grid.linewidth": 0.6,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.labelsize": 7.8,
        "ytick.labelsize": 7.8,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "legend.frameon": False,
        "legend.fontsize": 7.8,
        "legend.labelcolor": INK2,
        "legend.handlelength": 1.9,
        "legend.borderpad": 0.2,
        "lines.linewidth": 2.0,
        "lines.markersize": 5.5,
        "lines.solid_capstyle": "round",
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.06,
    })


def tidy(ax, top=False, right=False):
    """축을 후퇴시킨다: 불필요한 spine 제거."""
    ax.spines["top"].set_visible(top)
    ax.spines["right"].set_visible(right)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(AXIS)
    return ax


def note(ax, x, y, text, ha="left", va="center", size=7.4, color=INK2, weight=None, **kw):
    """주석 텍스트는 항상 잉크 토큰으로(시리즈 색 금지)."""
    return ax.text(x, y, text, ha=ha, va=va, fontsize=size, color=color,
                   fontweight=weight, **kw)


def marker_line(ax, x, y, text, dx=0, dy=0, ha="left", va="bottom", size=7.4):
    """데이터 포인트를 가리키는 직접 라벨(잉크색) + 얇은 지시선."""
    ax.annotate(text, xy=(x, y), xytext=(x + dx, y + dy), ha=ha, va=va,
                fontsize=size, color=INK2,
                arrowprops=dict(arrowstyle="-", color=AXIS, lw=0.7,
                                shrinkA=0, shrinkB=2))


def save(fig, name):
    path = f"{FIGDIR}/{name}.png"
    fig.savefig(path)
    plt.close(fig)
    print("  fig:", path)
    return path


# ── 블록도(scheme) 헬퍼 ───────────────────────────────────────────────
BOX_FILL = "#f4f7f9"
BOX_EDGE = "#9fbdcc"
DUT_FILL = "#e9f2f8"
DUT_EDGE = "#2a78d6"


def scheme_axes(w=6.3, ylo=0, yhi=40):
    """xlim 은 항상 0..100. 세로 범위를 명시하면 그림 높이가 자동으로 맞춰진다."""
    h = w * (yhi - ylo) / 100.0
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 100)
    ax.set_ylim(ylo, yhi)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.grid(False)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    return fig, ax


def box(ax, x, y, w, h, label, sub=None, kind="normal", size=7.6):
    """중심 (x, y) 기준 라운드 박스."""
    fills = {"normal": (BOX_FILL, BOX_EDGE), "dut": (DUT_FILL, DUT_EDGE),
             "inst": ("#eef4f8", "#6b93a8"), "ghost": (SURFACE, AXIS),
             "warn": ("#fdf3e7", "#d9a55f")}
    fc, ec = fills[kind]
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0,rounding_size=1.4",
                                fc=fc, ec=ec, lw=1.1, zorder=2))
    ty = y + (1.6 if sub else 0)
    ax.text(x, ty, label, ha="center", va="center", fontsize=size,
            color=INK, fontweight="bold", zorder=3)
    if sub:
        ax.text(x, y - 2.2, sub, ha="center", va="center", fontsize=size - 1.1,
                color=INK2, zorder=3)


def arrow(ax, x1, y1, x2, y2, label=None, style="-|>", color=INK2, lw=1.1,
          dashed=False, lsize=7.0, loff=2.4):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                                 mutation_scale=9, color=color, lw=lw,
                                 linestyle="--" if dashed else "-",
                                 shrinkA=1, shrinkB=1, zorder=1))
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + loff, label, ha="center",
                va="bottom", fontsize=lsize, color=INK2, zorder=3)


def refplane(ax, x, y0, y1, label, side="right"):
    """기준면(reference plane) 표시: 파선 + 라벨."""
    ax.plot([x, x], [y0, y1], ls=(0, (3, 2)), color=CRIT, lw=1.0, zorder=4)
    ax.text(x + (1.6 if side == "right" else -1.6), y1, label,
            ha="left" if side == "right" else "right", va="bottom",
            fontsize=6.8, color=CRIT, fontweight="bold", zorder=4)


def caption_title(ax, text):
    """그림 번호와 제목은 본문 캡션이 담당한다. 이미지 안에는 넣지 않는다."""
    return None

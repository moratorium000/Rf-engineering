# -*- coding: utf-8 -*-
"""데이터 플롯 (배치 B) — 스펙트럼 · 성상도 · Load Pull · 통계."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figstyle import *
import numpy as np
from matplotlib.patches import Circle

use_style()
rng = np.random.default_rng(11)
W = 6.3


def _tone(f, f0, amp_db, bw=0.004, floor=-135):
    return 10 ** ((amp_db - 40 * ((f - f0) / bw) ** 2) / 10)


def p10_harmonics():
    f = np.linspace(0.5, 10.5, 6000)
    f0, lv = 2.44, 23.0
    lines = [(f0, lv), (2 * f0, -22.0), (3 * f0, -38.0), (4 * f0, -51.0)]
    y = np.full(f.size, 10 ** (-118 / 10))
    for fc, a in lines:
        y = y + _tone(f, fc, a, bw=0.02)
    fig, axes = plt.subplots(2, 1, figsize=(W, 4.1),
                             gridspec_kw=dict(height_ratios=[1.25, 1], hspace=0.42))
    a0 = axes[0]
    a0.plot(f, 10 * np.log10(y), color=S1, lw=1.1)
    for fc, a in lines:
        lab = "기본파 f0" if fc == f0 else f"{int(round(fc/f0))}f0"
        dbc = a - lv
        a0.plot([fc], [a], "o", color=INK, ms=4, zorder=5)
        dx, ha_ = (0.25, "left") if fc < 3 * f0 else (-0.25, "right")
        a0.annotate(f"{lab}\n{a:.0f} dBm" + ("" if fc == f0 else f"\n({dbc:.0f} dBc)"),
                    xy=(fc, a), xytext=(fc + dx, a + 8), fontsize=6.9, color=INK2, ha=ha_,
                    arrowprops=dict(arrowstyle="-", color=AXIS, lw=0.7, shrinkA=0, shrinkB=2))
    a0.axhline(-41.2, color=CRIT, lw=1.1, ls=(0, (4, 2)))
    note(a0, 0.75, -35, "규제 한계선 (예시) −41.2 dBm", ha="left", size=7.0, color=CRIT)
    a0.set_xlabel("주파수 [GHz]"); a0.set_ylabel("전력 [dBm]")
    a0.set_xlim(0.5, 10.5); a0.set_ylim(-120, 45)
    tidy(a0)
    # (b) 감쇠 판별법
    a1 = axes[1]
    att = np.array([0, 10, 20])
    real = np.array([-22.0, -22.1, -21.9])
    fake = np.array([-22.0, -32.0, -42.0])
    x = np.arange(3)
    base = -52.0
    a1.bar(x - 0.19, real - base, width=0.34, bottom=base, color=S1, zorder=3,
           edgecolor=SURFACE, linewidth=1.0, label="DUT 의 실제 하모닉")
    a1.bar(x + 0.19, fake - base, width=0.34, bottom=base, color=S2, zorder=3,
           edgecolor=SURFACE, linewidth=1.0, label="분석기 내부에서 생성된 왜곡")
    for xi, r, fk in zip(x, real, fake):
        a1.text(xi - 0.19, r + 1.2, f"{r:.0f}", ha="center", fontsize=7.2, color=INK2, zorder=4)
        a1.text(xi + 0.19, fk + 1.2, f"{fk:.0f}", ha="center", fontsize=7.2, color=INK2, zorder=4)
    a1.set_xticks(x); a1.set_xticklabels([f"입력 감쇠 {a} dB" for a in att])
    a1.set_ylabel("표시된 2f0 레벨 [dBm]"); a1.set_ylim(base, -4)
    a1.set_xlim(-0.55, 2.9)
    a1.legend(loc="upper left", ncol=1)
    tidy(a1)
    note(a1, 2.45, -26, "감쇠를 올려도 값이\n그대로면 진짜 신호", ha="center", size=7.0)
    return save(fig, "p10_harmonics")


def p11_twotone():
    f = np.linspace(2.38, 2.50, 6000)
    f1, f2, pt = 2.435, 2.445, -5.0
    im3 = -55.0
    lines = [(2 * f1 - f2, im3), (f1, pt), (f2, pt), (2 * f2 - f1, im3),
             (3 * f1 - 2 * f2, -82.0), (3 * f2 - 2 * f1, -82.0)]
    y = np.full(f.size, 10 ** (-118 / 10))
    for fc, a in lines:
        y = y + _tone(f, fc, a, bw=0.0009)
    fig, ax = plt.subplots(figsize=(W, 2.9))
    ax.plot(f, 10 * np.log10(y), color=S1, lw=1.1)
    xarr = (f1 + f2) / 2
    ax.annotate("", xy=(xarr, pt), xytext=(xarr, im3),
                arrowprops=dict(arrowstyle="<->", color=INK2, lw=1.1))
    note(ax, xarr + 0.0009, (pt + im3) / 2, f"ΔP = {pt - im3:.0f} dB", ha="left", size=7.6,
         color=INK, weight="bold")
    for fc, a, lab in [(f1, pt, "f1"), (f2, pt, "f2"),
                       (2 * f1 - f2, im3, "2f1 − f2"), (2 * f2 - f1, im3, "2f2 − f1"),
                       (3 * f1 - 2 * f2, -82, "3f1 − 2f2"), (3 * f2 - 2 * f1, -82, "3f2 − 2f1")]:
        note(ax, fc, a + 4, lab, ha="center", size=6.9)
    ax.set_xlabel("주파수 [GHz]"); ax.set_ylabel("전력 [dBm]")
    ax.set_xlim(2.40, 2.48); ax.set_ylim(-115, 12)
    tidy(ax)
    note(ax, 2.4015, -110,
         f"OIP3 = Pout + ΔP/2 = {pt:.0f} + {(pt-im3)/2:.0f} = {pt + (pt-im3)/2:.0f} dBm"
         f"      (이득 20 dB 이면 IIP3 = {pt + (pt-im3)/2 - 20:.0f} dBm)", size=7.2, color=INK)
    return save(fig, "p11_twotone_spectrum")


def p12_ip3():
    pin = np.linspace(-45, 5, 200)
    g, iip3 = 12.0, 2.0
    fund = pin + g
    im3 = 3 * pin + g - 2 * iip3
    meas = pin <= -12
    fig, ax = plt.subplots(figsize=(W, 3.0))
    ax.plot(pin[meas], fund[meas], color=S1, label="기본파 (기울기 1)")
    ax.plot(pin[meas], im3[meas], color=S2, label="IM3 (기울기 3)")
    ax.plot(pin, fund, color=S1, lw=1.0, ls=(0, (4, 2)), alpha=0.75)
    ax.plot(pin, im3, color=S2, lw=1.0, ls=(0, (4, 2)), alpha=0.75)
    ax.plot([iip3], [iip3 + g], "o", color=INK, ms=6, zorder=5)
    marker_line(ax, iip3, iip3 + g, f"IP3\nIIP3 = {iip3:.0f} dBm\nOIP3 = {iip3+g:.0f} dBm",
                dx=-5, dy=-14, ha="right", va="top")
    ax.axvspan(-45, -12, color=BAND, zorder=0)
    note(ax, -43, -85, "실측 구간", size=7.0, color=MUTED)
    note(ax, -11, -66, "외삽 구간 (실제로 도달하지 않는다)", size=7.0, color=MUTED)
    ax.set_xlabel("톤당 입력 전력 [dBm]"); ax.set_ylabel("출력 전력 [dBm]")
    ax.set_xlim(-45, 5); ax.set_ylim(-95, 25)
    ax.legend(loc="lower right")
    tidy(ax)
    note(ax, -44, 18, "입력 1 dB 상승 → IM3 는 3 dB 상승.\n기울기가 3이 아니면 측정계 왜곡이거나 이미 압축 영역이다",
         size=7.0)
    return save(fig, "p12_ip3_extrapolation")


def _ofdm_psd(f, fc, bw, floor_db, shoulder_db, knee=9.0, slope=26.0):
    """대역 안은 평탄, 대역 밖은 어깨(shoulder) 레벨에서 시작해 완만히 떨어지는 PSD.
    어깨 레벨을 인접채널 적분값(ACLR)과 같은 dBc 로 두어 그림과 주석이 일치하게 한다."""
    d = np.abs(f - fc) - bw / 2
    y = np.where(d <= 0, 0.0,
                 shoulder_db - slope * np.log10(1 + np.maximum(d, 0) / knee))
    return np.maximum(y, floor_db)


def p13_aclr_sem():
    f = np.linspace(-40, 40, 8000)
    bw, off = 18.0, 20.0
    y = _ofdm_psd(f, 0, bw, -78, -45.0)
    y += rng.normal(0, 0.35, f.size)
    fig, axes = plt.subplots(2, 1, figsize=(W, 4.2), sharex=True,
                             gridspec_kw=dict(hspace=0.14))
    a0 = axes[0]
    a0.plot(f, y, color=S1, lw=0.9)
    for sgn, lab in [(-1, "하위 인접"), (1, "상위 인접")]:
        lo, hi = sgn * off - bw / 2, sgn * off + bw / 2
        a0.axvspan(min(lo, hi), max(lo, hi), color=BAND, zorder=0)
        note(a0, sgn * off, -70, lab, ha="center", size=7.0, color=MUTED)
    a0.axvspan(-bw / 2, bw / 2, color="#e6eef7", zorder=0)
    note(a0, 0, -70, "주 채널", ha="center", size=7.0, color=MUTED)
    for sgn in (-1, 1):
        a0.annotate("", xy=(sgn * off, -46.5), xytext=(sgn * off, -1),
                    arrowprops=dict(arrowstyle="<->", color=INK2, lw=1.1))
        note(a0, sgn * off + 1.6, -24, "ACLR\n−45 dBc", size=7.2, color=INK, weight="bold")
    a0.set_ylabel("전력 스펙트럼 밀도 [dBc]")
    a0.set_ylim(-85, 8)
    tidy(a0)
    a1 = axes[1]
    mask_x = np.array([-40, -22, -22, -12.5, -12.5, -9.5, -9.5, 9.5, 9.5, 12.5, 12.5, 22, 22, 40])
    mask_y = np.array([-60, -60, -50, -50, -32, -32, 3, 3, -32, -32, -50, -50, -60, -60])
    a1.plot(mask_x, mask_y, color=CRIT, lw=1.4, label="스펙트럼 방출 마스크 (SEM)")
    a1.plot(f, y, color=S1, lw=0.9, label="측정 트레이스")
    a1.fill_between(mask_x, mask_y, 8, color="#fdecec", zorder=0)
    a1.set_xlabel("채널 중심 기준 오프셋 [MHz]")
    a1.set_ylabel("전력 [dBc]")
    a1.set_xlim(-40, 40); a1.set_ylim(-85, 8)
    a1.legend(loc="upper left", ncol=1)
    tidy(a1)
    note(a1, 39, -78, "붉은 영역에 트레이스가 닿으면 불합격", ha="right", size=7.0, color=CRIT)
    return save(fig, "p13_aclr_sem")


def _qam16(n, evm, phn=0.0, iqg=0.0, iqp=0.0, comp=0.0, seed=3):
    r = np.random.default_rng(seed)
    lv = np.array([-3, -1, 1, 3])
    s = (r.choice(lv, n) + 1j * r.choice(lv, n)) / np.sqrt(10)
    x = s.copy()
    if iqg or iqp:
        i = x.real * (1 + iqg / 2)
        q = x.imag * (1 - iqg / 2)
        qq = q * np.cos(np.deg2rad(iqp)) + i * np.sin(np.deg2rad(iqp))
        x = i + 1j * qq
    if comp:
        a = np.abs(x); m = a.max()
        gain = 1 / (1 + (a / (m * comp)) ** 4) ** 0.25
        x = x * gain * np.exp(-1j * np.deg2rad(18) * (1 - gain))
    if phn:
        x = x * np.exp(1j * np.deg2rad(r.normal(0, phn, n)))
    x = x + (r.normal(0, evm, n) + 1j * r.normal(0, evm, n)) / np.sqrt(2)
    return s, x


def p14_constellation():
    cases = [("정상", dict(evm=0.015)),
             ("잡음 지배 (SNR 부족)", dict(evm=0.06)),
             ("위상잡음", dict(evm=0.012, phn=4.5)),
             ("I/Q 불균형", dict(evm=0.012, iqg=0.12, iqp=5.0)),
             ("PA 압축 (AM-AM / AM-PM)", dict(evm=0.012, comp=0.92)),
             ("LO 누설 / DC 오프셋", dict(evm=0.012))]
    fig, axes = plt.subplots(2, 3, figsize=(W, 4.3))
    for ax, (title, kw) in zip(axes.ravel(), cases):
        s, x = _qam16(1400, **kw)
        if "LO 누설" in title:
            x = x + (0.11 + 0.075j)
        ax.plot(x.real, x.imag, ".", color=S1, ms=1.6, alpha=0.75, zorder=3)
        ref = (np.array([-3, -1, 1, 3])[:, None] + 1j * np.array([-3, -1, 1, 3])[None, :]).ravel() / np.sqrt(10)
        ax.plot(ref.real, ref.imag, "+", color=INK2, ms=4.5, mew=0.9, zorder=4)
        evm = np.sqrt(np.mean(np.abs(x - s) ** 2) / np.mean(np.abs(s) ** 2)) * 100
        ax.set_title(f"{title}\nEVM {evm:.1f} %", fontsize=7.6, pad=4)
        ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.6, 1.6)
        ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
        ax.grid(False)
        for sp in ax.spines.values():
            sp.set_color(AXIS); sp.set_visible(True)
    fig.subplots_adjust(hspace=0.42, wspace=0.12)
    return save(fig, "p14_constellation")


def p15_backoff():
    pout = np.linspace(14, 32, 200)
    psat = 33.0
    bo = psat - pout
    evm = np.sqrt(0.6 ** 2 + (26 * np.exp(-bo / 2.4)) ** 2)
    aclr = -(64 - 30 * np.exp(-bo / 3.0))
    fig, axes = plt.subplots(2, 1, figsize=(W, 3.7), sharex=True,
                             gridspec_kw=dict(hspace=0.14))
    axes[0].plot(pout, evm, color=S1)
    axes[0].axhline(3.5, color=CRIT, lw=1.0, ls=(0, (3, 2)))
    note(axes[0], 14.4, 3.9, "EVM 규격 3.5 %", size=7.0, color=CRIT)
    axes[0].set_ylabel("EVM [%]"); axes[0].set_ylim(0, 12)
    tidy(axes[0])
    axes[1].plot(pout, aclr, color=S2)
    axes[1].axhline(-45, color=CRIT, lw=1.0, ls=(0, (3, 2)))
    note(axes[1], 14.4, -43.5, "ACLR 규격 −45 dBc", size=7.0, color=CRIT)
    axes[1].set_ylabel("ACLR [dBc]"); axes[1].set_xlabel("평균 출력 전력 [dBm]")
    axes[1].set_xlim(14, 32); axes[1].set_ylim(-68, -30)
    tidy(axes[1])
    pe = pout[np.argmax(evm > 3.5)]
    pa = pout[np.argmax(aclr > -45)]
    lim = min(pe, pa)
    for ax in axes:
        ax.axvline(lim, color=AXIS, lw=0.9, ls=(0, (2, 2)), zorder=0)
    marker_line(axes[1], lim, -45, f"두 규격을 동시에 만족하는\n최대 출력 ≈ {lim:.1f} dBm",
                dx=-1.0, dy=-12, ha="right", va="top")
    return save(fig, "p15_backoff_evm_aclr")


def p16_phase_noise():
    f = np.logspace(1, 7, 600)
    dut = 10 * np.log10(10 ** (-30 / 10) / f ** 3 + 10 ** (-58 / 10) / f ** 2 +
                        10 ** (-136 / 10) + 10 ** (-116 / 10) / f)
    floor = 10 * np.log10(10 ** (-70 / 10) / f ** 2 + 10 ** (-150 / 10))
    fig, ax = plt.subplots(figsize=(W, 3.0))
    ax.semilogx(f, dut, color=S1, label="DUT 위상잡음 L(f)")
    ax.semilogx(f, floor, color=S2, ls=(0, (5, 2)), label="계측기 잡음 바닥")
    for fs, a, lab in [(60, -70, "전원 60 Hz 스퍼"), (2.4e5, -108, "DC-DC 스위칭 스퍼")]:
        ax.plot([fs, fs], [dut[np.argmin(abs(f - fs))], a], color=CRIT, lw=1.2)
        note(ax, fs * 1.35, a + 2, lab, size=7.0, color=CRIT, va="bottom")
    for off, lab in [(1e3, "1 kHz"), (1e6, "1 MHz")]:
        v = dut[np.argmin(abs(f - off))]
        ax.plot([off], [v], "o", color=INK, ms=4, zorder=5)
        lab2 = "1 kHz 오프셋" if off == 1e3 else "1 MHz 오프셋"
        note(ax, off * 0.75, v - 7, f"{lab2}\n{v:.0f} dBc/Hz", ha="right", size=6.9)
    ax.set_xlabel("캐리어 기준 오프셋 [Hz]"); ax.set_ylabel("L(f) [dBc/Hz]")
    ax.set_xlim(10, 1e7); ax.set_ylim(-170, -40)
    ax.legend(loc="upper right")
    tidy(ax)
    note(ax, 12, -166, "DUT 곡선이 계측기 바닥에 근접하는 구간의 값은 신뢰할 수 없다.\n측정 전에 계측기 바닥부터 확인한다", size=7.0)
    return save(fig, "p16_phase_noise")


def p17_nf_cascade():
    stages = ["케이블·스위치\nIL 1.2 dB", "BPF\nIL 1.8 dB", "LNA\nNF 1.1 / G 18", "믹서\nNF 9 / G −7", "IF 증폭\nNF 4 / G 20"]
    nf = np.array([1.2, 1.8, 1.1, 9.0, 4.0])
    g = np.array([-1.2, -1.8, 18.0, -7.0, 20.0])
    f_lin = 10 ** (nf / 10); g_lin = 10 ** (g / 10)
    total, gcum, contrib = f_lin[0], g_lin[0], [f_lin[0] - 1]
    for i in range(1, len(nf)):
        c = (f_lin[i] - 1) / gcum
        contrib.append(c); total += c; gcum *= g_lin[i]
    contrib = np.array(contrib)
    share = contrib / contrib.sum() * 100
    fig, ax = plt.subplots(figsize=(W, 2.9))
    x = np.arange(len(stages))
    cols = [S2, S2, S1, S1, S1]
    bars = ax.bar(x, share, width=0.62, color=cols, edgecolor=SURFACE, linewidth=1.2, zorder=3)
    for b, s_ in zip(bars, share):
        ax.text(b.get_x() + b.get_width() / 2, s_ + 1.4, f"{s_:.0f} %",
                ha="center", fontsize=7.4, color=INK2)
    ax.bar(np.nan, 0, color=S2, label="LNA 앞단의 수동 손실")
    ax.bar(np.nan, 0, color=S1, label="능동단")
    ax.legend(loc="upper right", ncol=1)
    ax.set_xticks(x); ax.set_xticklabels(stages, fontsize=7.0)
    ax.set_ylabel("잡음지수 기여도 [%]")
    ax.set_ylim(0, max(share) * 1.52)
    tidy(ax)
    note(ax, -0.45, max(share) * 1.30,
         f"총 잡음지수 {10*np.log10(total):.2f} dB — 이 중 {share[0]+share[1]:.0f} % 가\nLNA 앞단의 수동 손실이다",
         size=7.2, color=INK)
    return save(fig, "p18_nf_cascade")


def p18_sensitivity():
    lv = np.linspace(-100, -78, 400)
    snr_req = 9.0
    nfl = -174 + 10 * np.log10(20e6) + 5.0
    snr = lv - nfl
    per = 1 / (1 + np.exp((snr - snr_req) * 2.1))
    fig, axes = plt.subplots(1, 2, figsize=(W, 2.9), gridspec_kw=dict(width_ratios=[1.1, 1], wspace=0.32))
    a0 = axes[0]
    for dT, c, lab in [(0, S1, "+25 °C"), (1.2, S2, "+85 °C"), (-0.6, S3, "−40 °C")]:
        p = 1 / (1 + np.exp((lv - nfl - dT - snr_req) * 2.1))
        a0.semilogy(lv, np.clip(p, 1e-4, 1), color=c, label=lab)
    a0.axhline(0.01, color=CRIT, lw=1.0, ls=(0, (3, 2)))
    note(a0, -99.6, 0.013, "판정 기준 PER 1 %", size=7.0, color=CRIT)
    sens = nfl + snr_req + 10 * np.log10(99) / 2.1
    a0.set_xlabel("입력 레벨 [dBm]"); a0.set_ylabel("PER")
    a0.set_xlim(-100, -78); a0.set_ylim(1e-4, 1.2)
    a0.legend(loc="upper right", ncol=1)
    tidy(a0)
    note(a0, -99.6, 1.5e-4, "온도가 오르면 곡선이 오른쪽으로 밀린다", size=7.0)
    a1 = axes[1]
    steps = ["열잡음\n−174 dBm/Hz", "대역폭\n20 MHz", "잡음지수\n5 dB", "필요 SNR\n9 dB"]
    vals = [-174, 10 * np.log10(20e6), 5.0, snr_req]
    cum = np.cumsum(vals)
    base = np.concatenate([[-174], cum[:-1]])
    fig_col = [SEQ[2], SEQ[3], SEQ[4], S2]
    for i in range(4):
        lo = base[i] if i else -180
        hi = cum[i]
        a1.bar(i, hi - lo, bottom=lo, width=0.6, color=fig_col[i],
               edgecolor=SURFACE, linewidth=1.2, zorder=3)
        a1.text(i, hi + 1.5, f"{cum[i]:.0f}", ha="center", fontsize=7.2, color=INK2)
    a1.set_xticks(range(4)); a1.set_xticklabels(steps, fontsize=6.9)
    a1.set_ylabel("누적 레벨 [dBm]"); a1.set_ylim(-182, -80)
    a1.axhline(cum[-1], color=CRIT, lw=1.0, ls=(0, (3, 2)))
    note(a1, -0.45, cum[-1] + 3.5, f"이론 감도 {cum[-1]:.0f} dBm", size=7.2, color=CRIT)
    tidy(a1)
    return save(fig, "p19_sensitivity")


def p19_loadpull():
    """Load Pull 등고선을 스칼라장에서 contour 로 추출한다(임의로 그린 타원이 아니다).

    모델:  Pout(Γ) = Pmax − a·|Γ − Γ_P|² / (1 − |Γ|²)
           PAE(Γ)  = PAEmax − b·|Γ − Γ_E|² / (1 − |Γ|²)
    (1 − |Γ|²) 분모가 차트 가장자리에서 성능을 급격히 떨어뜨려, 실제 Load Pull
    등고선이 보이는 비대칭·찌그러진 형태를 만든다.
    """
    n = 800
    gx, gy = np.meshgrid(np.linspace(-1, 1, n), np.linspace(-1, 1, n))
    G = gx + 1j * gy
    den = np.where(np.abs(G) < 0.97, 1 - np.abs(G) ** 2, np.nan)
    gP = 0.40 * np.exp(1j * np.deg2rad(150))
    gE = 0.56 * np.exp(1j * np.deg2rad(108))
    Pout = 34.0 - 8.0 * np.abs(G - gP) ** 2 / den
    PAE = 62.0 - 115.0 * np.abs(G - gE) ** 2 / den

    fig, ax = plt.subplots(figsize=(W * 0.78, W * 0.78))
    ax.set_aspect("equal"); ax.axis("off"); ax.grid(False)
    th = np.linspace(0, 2 * np.pi, 700)
    ax.add_patch(Circle((0, 0), 1, fc=SURFACE, ec=AXIS, lw=1.2, zorder=1))
    for r in (0.2, 0.5, 1.0, 2.0, 5.0):
        c, rad = r / (1 + r), 1 / (1 + r)
        ax.plot(c + rad * np.cos(th), rad * np.sin(th), color=GRID, lw=0.6, zorder=2)
    for xr in (0.2, 0.5, 1.0, 2.0, 5.0):
        for sgn in (1, -1):
            cy, rad = sgn / xr, 1 / xr
            xx, yy = 1.0 + rad * np.cos(th), cy + rad * np.sin(th)
            m = xx ** 2 + yy ** 2 <= 1.0
            ax.plot(xx[m], yy[m], color=GRID, lw=0.6, zorder=2)
    ax.plot([-1, 1], [0, 0], color=GRID, lw=0.6, zorder=2)

    lv_p = [31.0, 32.0, 33.0]
    cp = ax.contour(gx, gy, Pout, levels=lv_p,
                    colors=[SEQ[2], SEQ[4], SEQ[6]], linewidths=1.8, zorder=5)
    ax.clabel(cp, inline=True, fontsize=6.3, fmt="%.0f dBm", colors=INK2,
              manual=[(-0.86, -0.16), (-0.72, -0.06), (-0.55, 0.02)])
    lv_e = [45.0, 55.0]
    ce = ax.contour(gx, gy, PAE, levels=lv_e, colors=[S2, S2], linewidths=1.6,
                    linestyles=[(0, (5, 2)), (0, (5, 2))], zorder=5)
    ax.clabel(ce, inline=True, fontsize=6.3, fmt="%.0f %%", colors=INK2,
              manual=[(-0.20, 0.80), (-0.20, 0.63)])

    ax.plot([gP.real], [gP.imag], "o", color=SEQ[6], ms=7.5, zorder=7,
            markeredgecolor=SURFACE, markeredgewidth=1.1)
    ax.plot([gE.real], [gE.imag], "s", color=S2, ms=7.5, zorder=7,
            markeredgecolor=SURFACE, markeredgewidth=1.1)
    ax.annotate("최대 출력점  Γ_opt,P", xy=(gP.real, gP.imag), xytext=(0.34, -0.40),
                fontsize=7.4, color=INK2, ha="center", zorder=9,
                arrowprops=dict(arrowstyle="-", color=INK2, lw=0.9, shrinkB=7,
                                connectionstyle="arc3,rad=0.12"))
    ax.annotate("최대 효율점  Γ_opt,PAE", xy=(gE.real, gE.imag), xytext=(0.52, 0.70),
                fontsize=7.4, color=INK2, ha="center", zorder=9,
                arrowprops=dict(arrowstyle="-", color=INK2, lw=0.9, shrinkB=7,
                                connectionstyle="arc3,rad=-0.12"))
    ax.plot([0], [0], "+", color=INK2, ms=8, mew=1.2, zorder=7)
    note(ax, 0.05, -0.06, "50 Ω", size=7.0, color=MUTED)
    ax.plot([], [], color=SEQ[4], lw=1.8, label="출력 전력 등고선 (1 dB)")
    ax.plot([], [], color=S2, lw=1.6, ls=(0, (5, 2)), label="PAE 등고선 (10 %)")
    ax.legend(loc="lower right", bbox_to_anchor=(1.02, -0.01), ncol=1)
    ax.set_xlim(-1.05, 1.05); ax.set_ylim(-1.05, 1.05)
    return save(fig, "p20_loadpull_contours")


def p20_corners_yield():
    fig, axes = plt.subplots(1, 2, figsize=(W, 2.8), gridspec_kw=dict(wspace=0.30))
    T = np.array([-40, -20, 0, 25, 55, 85])
    a0 = axes[0]
    for i, (v, c, lab) in enumerate([(3.0, S1, "V_min 3.0 V"), (3.6, S2, "V_nom 3.6 V"),
                                     (4.2, S3, "V_max 4.2 V")]):
        base = 20.0 + (v - 3.6) * 1.15
        p = base - 0.022 * (T - 25) - 0.00028 * (T - 25) ** 2
        a0.plot(T, p, "-o", color=c, ms=4.5, label=lab)
        note(a0, 86, p[-1], lab.split()[0], size=6.9, va="center")
    a0.axhline(18.0, color=CRIT, lw=1.0, ls=(0, (3, 2)))
    note(a0, -44, 18.25, "하한 규격 18.0 dBm", ha="left", size=7.0, color=CRIT)
    a0.set_xlabel("케이스 온도 [°C]"); a0.set_ylabel("출력 전력 [dBm]")
    a0.set_xlim(-45, 100); a0.set_ylim(16.5, 23)
    a0.legend(loc="upper left", ncol=1)
    tidy(a0)
    a1 = axes[1]
    d = rng.normal(20.1, 0.62, 4000)
    a1.hist(d, bins=44, color=SEQ[2], edgecolor=SURFACE, linewidth=0.6, zorder=3)
    ytop = a1.get_ylim()[1]
    a1.axvline(18.0, color=CRIT, lw=1.3, zorder=4)
    a1.text(18.06, ytop * 0.99, "규격 하한 (LSL)\n18.0 dBm", fontsize=6.9, color=CRIT, va="top")
    a1.axvline(18.6, color=INK2, lw=1.2, ls=(0, (3, 2)), zorder=4)
    a1.text(18.66, ytop * 0.46, "시험 한계선 18.6\n(가드밴드 0.6 dB)", fontsize=6.9, color=INK2, va="top")
    mu, sd = d.mean(), d.std()
    cpk = (mu - 18.0) / (3 * sd)
    a1.text(0.98, 0.98, f"μ = {mu:.2f} dBm\nσ = {sd:.2f} dB\nCpk = {cpk:.2f}",
            transform=a1.transAxes, ha="right", va="top", fontsize=7.2, color=INK)
    a1.text(0.98, 0.74, "목표 Cpk 1.33 미달", transform=a1.transAxes,
            ha="right", va="top", fontsize=6.9, color=CRIT)
    a1.set_xlabel("출력 전력 [dBm]"); a1.set_ylabel("개체 수")
    a1.set_xlim(17.6, 22.4)
    tidy(a1)
    return save(fig, "p21_corners_yield")


if __name__ == "__main__":
    os.makedirs("figures", exist_ok=True)
    for fn in [p10_harmonics, p11_twotone, p12_ip3, p13_aclr_sem, p14_constellation,
               p15_backoff, p16_phase_noise, p17_nf_cascade, p18_sensitivity,
               p19_loadpull, p20_corners_yield]:
        fn()
    print("plots B done")

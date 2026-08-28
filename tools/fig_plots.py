# -*- coding: utf-8 -*-
"""데이터 플롯 생성. 모든 곡선은 물리 모델에서 계산한 것이며 임의로 그린 값이 아니다."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figstyle import *
import numpy as np
from scipy import signal

use_style()
rng = np.random.default_rng(7)
W = 6.3   # 본문 폭에 맞춘 그림 너비(inch)


# ─────────────────────────────────────────────────────────────────────
def p01_cable_loss():
    f = np.linspace(0.05, 26.5, 400)                      # GHz
    # 동축 손실 ~ 도체손(√f) + 유전손(f)
    l_test = 2.0 * (0.42 * np.sqrt(f) + 0.010 * f)        # 2 m 시험용 저손실 케이블
    l_cheap = 2.0 * (0.95 * np.sqrt(f) + 0.030 * f)       # 2 m 범용 케이블
    fig, ax = plt.subplots(figsize=(W, 2.5))
    ax.plot(f, l_test, color=S1, label="저손실 시험용 케이블 (2 m)")
    ax.plot(f, l_cheap, color=S2, label="범용 케이블 (2 m)")
    for fx in (2.4, 5.8, 24):
        ax.axvline(fx, color=AXIS, lw=0.7, ls=(0, (2, 2)), zorder=0)
        note(ax, fx, 0.3, f"{fx} GHz", ha="center", size=6.6, color=MUTED, rotation=90, va="bottom")
    ax.set_xlabel("주파수 [GHz]"); ax.set_ylabel("경로 손실 [dB]")
    ax.set_xlim(0, 26.5); ax.set_ylim(0, 12)
    ax.legend(loc="upper left")
    marker_line(ax, 24, np.interp(24, f, l_cheap), f"{np.interp(24,f,l_cheap):.1f} dB",
                dx=-6.5, dy=1.0, ha="right")
    marker_line(ax, 24, np.interp(24, f, l_test), f"{np.interp(24,f,l_test):.1f} dB",
                dx=-6.5, dy=-1.3, ha="right", va="top")
    tidy(ax)
    return save(fig, "p01_cable_loss")


def p02_rbw_noise():
    f = np.linspace(-5, 5, 3000)                          # MHz offset
    def trace(rbw_khz, seed):
        r = np.random.default_rng(seed)
        nf = -110 + 10 * np.log10(rbw_khz / 1.0)          # RBW 에 비례하는 잡음 바닥
        noise = nf + 4.3 * np.log10(-np.log(r.random(f.size)))
        sig = 10 ** ((-30 - ((f / (rbw_khz / 1000.0 * 1.2)) ** 2) * 3) / 10)
        spur = 10 ** ((-96 - ((f - 1.35) / (rbw_khz / 1000.0 * 1.2)) ** 2 * 3) / 10)
        return 10 * np.log10(10 ** (noise / 10) + sig + spur)
    fig, ax = plt.subplots(figsize=(W, 2.6))
    for (rbw, c, lab) in [(300, S1, "RBW 300 kHz"), (30, S2, "RBW 30 kHz"), (3, S3, "RBW 3 kHz")]:
        ax.plot(f, trace(rbw, rbw), color=c, lw=1.1, label=lab)
    ax.set_xlabel("캐리어 기준 오프셋 [MHz]"); ax.set_ylabel("표시 전력 [dBm]")
    ax.set_xlim(-5, 5); ax.set_ylim(-125, -20)
    ax.legend(loc="upper right", ncol=3)
    marker_line(ax, 1.35, -96, "RBW 300 kHz 에서는 잡음에 묻히고\nRBW 3 kHz 에서 드러나는 스퍼", dx=0.55, dy=22)
    note(ax, -4.7, -118, "RBW 를 1/10 로 줄이면 잡음 바닥은 약 10 dB 내려간다", size=7.2)
    tidy(ax)
    return save(fig, "p02_rbw_noise_floor")


def p03_sa_dynamic_range():
    pm = np.linspace(-70, 0, 300)                          # 믹서 입력 레벨 [dBm]
    danl_1khz = -125.0                                     # 1 kHz RBW 환산 잡음 바닥
    toi = 15.0
    noise_dbc = danl_1khz - pm
    d3_dbc = 2 * (pm - toi)
    d2_dbc = 1 * (pm - 45.0)
    fig, ax = plt.subplots(figsize=(W, 2.9))
    ax.plot(pm, noise_dbc, color=S1, label="표시 잡음 바닥 (RBW 1 kHz)")
    ax.plot(pm, d3_dbc, color=S2, label="3차 왜곡 (TOI = +15 dBm)")
    ax.plot(pm, d2_dbc, color=S3, ls=(0, (5, 2)), label="2차 왜곡 (SHI = +45 dBm)")
    x_opt = (danl_1khz + 2 * toi) / 3.0
    y_opt = danl_1khz - x_opt
    ax.plot([x_opt], [y_opt], "o", color=INK, ms=5, zorder=5)
    marker_line(ax, x_opt, y_opt, f"최적 믹서 레벨 ≈ {x_opt:.0f} dBm\n스퓨리어스-프리 다이내믹 레인지 {abs(y_opt):.0f} dB",
                dx=6, dy=-30, ha="left", va="top")
    note(ax, -69, -128, "감쇠를 낮추면 믹서 레벨이 올라간다 → 잡음은 좋아지고 왜곡은 나빠진다", size=7.0)
    ax.set_xlabel("믹서 입력 레벨 = 입력 전력 − 입력 감쇠  [dBm]")
    ax.set_ylabel("캐리어 대비 [dBc]")
    ax.set_xlim(-70, 0); ax.set_ylim(-140, 0)
    ax.legend(loc="upper left")
    tidy(ax)
    return save(fig, "p03_sa_dynamic_range")


def p04_ccdf():
    n = 400000
    x = np.linspace(0, 13, 300)
    ofdm = np.exp(-10 ** (x / 10))                                  # 복소 가우시안 포락선
    r = rng.standard_normal(n) + 1j * rng.standard_normal(n)
    p = np.abs(r) ** 2; p /= p.mean()
    qam = np.array([(10 * np.log10(p) > xx).mean() for xx in x])
    fig, ax = plt.subplots(figsize=(W, 2.6))
    ax.semilogy(x, np.clip(ofdm, 1e-6, 1), color=S1, label="OFDM (이론, 복소 가우시안)")
    ax.semilogy(x, np.clip(qam, 1e-6, 1), color=S2, lw=1.2, ls=(0, (4, 2)),
                label="OFDM (모의 신호 400k 심볼)")
    ax.plot([0, 0], [1e-6, 1], color=S3, lw=2.4)
    marker_line(ax, 0, 3e-4, "CW : 크레스트 팩터 0 dB", dx=1.0, dy=0)
    for pr, lab in [(1e-2, "1 %"), (1e-4, "0.01 %")]:
        xx = 10 * np.log10(-np.log(pr))
        ax.plot([xx], [pr], "o", color=INK, ms=4.5, zorder=5)
        marker_line(ax, xx, pr, f"{lab} 에서 {xx:.1f} dB", dx=0.8, dy=0)
    ax.set_xlabel("평균 전력 대비 [dB]"); ax.set_ylabel("초과 확률")
    ax.set_xlim(-0.6, 13); ax.set_ylim(1e-6, 1.2)
    ax.legend(loc="lower left")
    note(ax, 6.6, 0.35, "CW 용 다이오드 센서로 이 신호를 재면\n제곱법칙 영역을 벗어나 오차가 생긴다 [18]",
         size=7.0)
    tidy(ax)
    return save(fig, "p04_ccdf")


def _bandpass(f, f0=2.44, bw=0.08, order=5, ripple=0.15):
    """해석적 대역통과 (아날로그 체비셰프). f, f0, bw 는 GHz, 내부는 rad/s 로 통일."""
    w1, w2 = 2 * np.pi * (f0 - bw / 2), 2 * np.pi * (f0 + bw / 2)
    b, a = signal.cheby1(order, ripple, [w1, w2], btype="bandpass", analog=True)
    _, h = signal.freqs(b, a, worN=2 * np.pi * f)
    return h


def p05_filter():
    f = np.linspace(2.20, 2.68, 4000)
    h = _bandpass(f)
    s21 = 20 * np.log10(np.abs(h) + 1e-12) - 1.6           # 삽입손실 포함
    ph = np.unwrap(np.angle(h))
    # f 가 GHz 이므로 dφ/dω 의 단위는 이미 ns 이다 (1/(Grad/s) = ns)
    gd = -np.gradient(ph, f * 2 * np.pi)
    s11 = 20 * np.log10(np.clip(np.sqrt(np.clip(1 - np.abs(h) ** 2, 0, 1)) * 0.97, 1e-3, 1))
    fig, axes = plt.subplots(2, 1, figsize=(W, 3.9), sharex=True,
                             gridspec_kw=dict(height_ratios=[1.35, 1], hspace=0.12))
    a0 = axes[0]
    a0.plot(f, s21, color=S1, label="S21 크기 (통과 / 억압)")
    a0.plot(f, s11, color=S2, label="S11 크기 (입력 정합)")
    a0.axhline(-3, color=AXIS, lw=0.8, ls=(0, (3, 2)))
    note(a0, 2.215, -2.0, "−3 dB", size=6.8, color=MUTED)
    a0.axvspan(2.40, 2.48, color=BAND, zorder=0)
    note(a0, 2.44, -76, "통과대역", ha="center", size=7.0, color=MUTED)
    a0.set_ylabel("크기 [dB]"); a0.set_ylim(-85, 8)
    a0.legend(loc="lower right", ncol=1)
    tidy(a0)
    a1 = axes[1]
    # |S21| 이 -30 dB 아래인 구간의 군지연은 수치적으로도 실측으로도 의미가 없다
    m = s21 > -30
    a1.plot(f[m], gd[m], color=S3)
    a1.axvspan(2.40, 2.48, color=BAND, zorder=0)
    i_edge = np.argmin(np.abs(f - 2.404))
    marker_line(a1, f[i_edge], gd[i_edge], "대역 가장자리에서\n군지연이 치솟는다",
                dx=-0.03, dy=-6.5, ha="right", va="top")
    ipb = (f > 2.41) & (f < 2.47)
    note(a1, 2.485, gd[ipb].mean(),
         f"통과대역 평균 {gd[ipb].mean():.1f} ns\n리플 {gd[ipb].max()-gd[ipb].min():.1f} ns p-p",
         size=7.0, va="center")
    a1.set_xlabel("주파수 [GHz]"); a1.set_ylabel("군지연 [ns]")
    a1.set_xlim(2.20, 2.68); a1.set_ylim(0, 30)
    note(a1, 2.215, 2.0, "군지연 애퍼처는 통과대역폭의 0.5~2 % 로 설정한다 — 좁으면 잡음, 넓으면 구조가 뭉개진다",
         size=7.0)
    tidy(a1)
    return save(fig, "p05_filter_s21_gd")


def p06_vswr_family():
    g = np.linspace(0.001, 0.75, 400)
    vswr = (1 + g) / (1 - g)
    rl = -20 * np.log10(g)
    pref = g ** 2 * 100
    fig, axes = plt.subplots(3, 1, figsize=(W, 4.0), sharex=True,
                             gridspec_kw=dict(hspace=0.16))
    for ax, y, c, lab, ylim in [
            (axes[0], vswr, S1, "VSWR", (1, 6)),
            (axes[1], rl, S2, "반사손실 [dB]", (0, 40)),
            (axes[2], pref, S3, "반사 전력 [%]", (0, 50))]:
        ax.plot(g, y, color=c)
        ax.set_ylabel(lab)
        ax.set_ylim(*ylim)
        ax.axvline(1/3, color=CRIT, lw=0.9, ls=(0, (3, 2)), zorder=0)
        tidy(ax)
    note(axes[0], 0.345, 5.2, "VSWR 2.0 (|Γ| = 0.333) — 일반적 합격선", size=7.0, color=CRIT)
    for ax, val, unit in [(axes[0], 2.0, ""), (axes[1], 9.54, " dB"), (axes[2], 11.1, " %")]:
        ax.plot([1/3], [val], "o", color=INK, ms=4.5, zorder=5)
        note(ax, 0.355, val, f"{val:g}{unit}", size=7.0, va="center", weight="bold")
    axes[2].set_xlabel("반사계수 크기 |Γ|")
    axes[2].set_xlim(0, 0.75)
    return save(fig, "p06_vswr_family")


def _pa_model(pin_dbm, gain_db=25.0, psat_dbm=33.0, k=1.6):
    pin = 10 ** (pin_dbm / 10)
    g = 10 ** (gain_db / 10)
    psat = 10 ** (psat_dbm / 10)
    pout = g * pin / (1 + (g * pin / psat) ** (2 * k)) ** (1 / (2 * k))
    return 10 * np.log10(pout)


def p07_compression():
    pin = np.linspace(-25, 12, 500)
    pout = _pa_model(pin)
    gain = pout - pin
    g0 = gain[0]
    idx = np.argmax(gain <= g0 - 1)
    p1db_in, p1db_out = pin[idx], pout[idx]
    fig, axes = plt.subplots(2, 1, figsize=(W, 3.9), sharex=True,
                             gridspec_kw=dict(height_ratios=[1.25, 1], hspace=0.12))
    a0 = axes[0]
    a0.plot(pin, pout, color=S1, label="측정 Pout")
    a0.plot(pin, pin + g0, color=AXIS, lw=1.4, ls=(0, (4, 2)), label="선형 외삽 (소신호 이득)")
    a0.plot([p1db_in], [p1db_out], "o", color=INK, ms=5.5, zorder=5)
    marker_line(a0, p1db_in, p1db_out, f"P1dB\nPout = {p1db_out:.1f} dBm\nPin = {p1db_in:.1f} dBm",
                dx=1.2, dy=-11, ha="left", va="top")
    a0.set_ylabel("출력 전력 [dBm]"); a0.set_ylim(-5, 40); a0.legend(loc="upper left")
    tidy(a0)
    a1 = axes[1]
    a1.plot(pin, gain, color=S2, label="이득")
    a1.axhline(g0, color=AXIS, lw=1.0, ls=(0, (4, 2)))
    a1.axhline(g0 - 1, color=CRIT, lw=1.0, ls=(0, (3, 2)))
    note(a1, -24, g0 + 0.4, f"소신호 이득 {g0:.1f} dB", size=7.0, color=MUTED)
    note(a1, -24, g0 - 1.9, "−1 dB 기준선", size=7.0, color=CRIT)
    a1.axvline(p1db_in, color=AXIS, lw=0.8, ls=(0, (2, 2)), zorder=0)
    a1.set_xlabel("입력 전력 [dBm]"); a1.set_ylabel("이득 [dB]")
    a1.set_xlim(-25, 12); a1.set_ylim(g0 - 7.2, g0 + 2)
    tidy(a1)
    note(a1, -24, g0 - 6.4, "소신호 이득을 이미 압축된 레벨에서 잡으면 P1dB 가 낙관적으로 나온다", size=7.0)
    return save(fig, "p07_gain_compression")


def p08_amam_ampm():
    pin = np.linspace(-25, 12, 400)
    pout = _pa_model(pin)
    gain = pout - pin
    comp = np.clip(gain[0] - gain, 0, None)
    ampm = -6.2 * comp ** 0.85                              # 압축량에 따른 위상 회전
    fig, axes = plt.subplots(2, 1, figsize=(W, 3.6), sharex=True,
                             gridspec_kw=dict(hspace=0.12))
    axes[0].plot(pout, gain, color=S1)
    axes[0].set_ylabel("이득 [dB]  (AM-AM)")
    axes[0].set_ylim(gain.min() - 0.6, gain[0] + 0.8)
    tidy(axes[0])
    axes[1].plot(pout, ampm, color=S2)
    axes[1].set_ylabel("위상 편차 [°]  (AM-PM)")
    axes[1].set_xlabel("출력 전력 [dBm]")
    axes[1].set_xlim(18, pout.max()); axes[1].set_ylim(-26, 3)
    axes[0].set_xlim(18, pout.max())
    tidy(axes[1])
    i1 = np.argmax(gain <= gain[0] - 1)
    for ax in axes:
        ax.axvline(pout[i1], color=AXIS, lw=0.9, ls=(0, (3, 2)), zorder=0)
    note(axes[0], pout[i1] - 0.3, gain[0] - 0.4, "P1dB", ha="right", size=7.0, color=MUTED)
    axes[1].plot([pout[i1]], [ampm[i1]], "o", color=INK, ms=5, zorder=5)
    marker_line(axes[1], pout[i1], ampm[i1], f"P1dB 에서 {ampm[i1]:.1f}°", dx=-1.2, dy=-5.5,
                ha="right", va="top")
    note(axes[1], 18.3, -23.5, "압축이 시작되면 진폭뿐 아니라 위상도 함께 움직인다 →  EVM · ACLR 열화", size=7.0)
    return save(fig, "p08_amam_ampm")


def p09_pae():
    # 단단(single-stage) 전력증폭기: 이득 13 dB. 이득이 낮아야 PAE 와 DE 의 차이가 드러난다.
    pin = np.linspace(4, 24, 500)
    pout = _pa_model(pin, gain_db=13.0, psat_dbm=33.0, k=1.6)
    po_w = 10 ** (pout / 10) / 1000
    pi_w = 10 ** (pin / 10) / 1000
    # AB급: 정지전류 + 구동에 따라 증가하다 포화하는 전류
    pdc = 0.55 + 3.1 * (1 - np.exp(-po_w / 0.75))
    pae = (po_w - pi_w) / pdc * 100
    de = po_w / pdc * 100
    fig, ax = plt.subplots(figsize=(W, 2.7))
    ax.plot(pout, pae, color=S1, label="PAE")
    ax.plot(pout, de, color=S2, ls=(0, (5, 2)), label="드레인 효율 (DE)")
    gain = pout - pin
    p1 = pout[np.argmax(gain <= gain[0] - 1)]
    
    ax.axvline(p1, color=AXIS, lw=0.9, ls=(0, (3, 2)), zorder=0)
    note(ax, p1 - 0.5, 62, "P1dB", ha="right", size=7.0, color=MUTED)
    i = np.argmax(pae)
    ax.plot([pout[i]], [pae[i]], "o", color=INK, ms=5, zorder=5)
    marker_line(ax, pout[i], pae[i], f"최대 PAE {pae[i]:.0f} % @ {pout[i]:.1f} dBm", dx=-3.5, dy=7, ha="right")
    ax.set_xlabel("출력 전력 [dBm]"); ax.set_ylabel("효율 [%]")
    ax.set_xlim(16, 34.5); ax.set_ylim(0, 72); ax.legend(loc="upper left")
    note(ax, 16.4, 3.5, "포화 이후에는 Pout 이 늘지 않는데 Pin 만 늘어 PAE 가 다시 떨어진다", size=7.0)
    tidy(ax)
    return save(fig, "p09_pae")


if __name__ == "__main__":
    os.makedirs("figures", exist_ok=True)
    for fn in [p01_cable_loss, p02_rbw_noise, p03_sa_dynamic_range, p04_ccdf,
               p05_filter, p06_vswr_family, p07_compression, p08_amam_ampm, p09_pae]:
        fn()
    print("plots A done")

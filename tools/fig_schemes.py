# -*- coding: utf-8 -*-
"""블록도(scheme) 생성."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figstyle import *

use_style()


def s01_system():
    fig, ax = scheme_axes(6.3, 0, 44)
    y = 26
    box(ax, 12, y, 20, 13, "계측기", "SG / SA / PM / VNA", kind="inst")
    box(ax, 39, y, 13, 9, "케이블", kind="normal")
    box(ax, 58, y, 13, 9, "감쇠기", "패드 / DC 블록", kind="normal")
    box(ax, 84, y, 20, 13, "DUT", "보드 · 모듈 · 완제품", kind="dut")
    arrow(ax, 22, y, 32.5, y)
    arrow(ax, 45.5, y, 51.5, y)
    arrow(ax, 64.5, y, 74, y)
    refplane(ax, 27, 8, 38, "계측기 기준면")
    refplane(ax, 71, 8, 38, "DUT 기준면 (측정이 정의되는 면)")
    note(ax, 49, 5.5, "이 구간의 손실 L(f) 를 사전 측정하여 보정한다  →  2.4절 경로 손실 교정",
         ha="center", size=7.2)
    caption_title(ax, "그림 2-1  벤치 측정 시스템과 두 개의 기준면")
    return save(fig, "s01_system_reference_plane")


def s02_pathloss():
    fig, ax = scheme_axes(6.3, -12, 60)
    # (a) 교정 단계
    yA = 42
    note(ax, 2, yA + 13, "(a) 교정 : DUT 자리를 직결(Thru)하고 손실을 측정", size=7.8,
         color=INK, weight="bold")
    box(ax, 13, yA, 18, 11, "SG 또는", "VNA 포트 1", kind="inst")
    box(ax, 50, yA, 22, 9, "THRU 연결", "(DUT 자리)", kind="ghost")
    box(ax, 87, yA, 18, 11, "PM 또는", "VNA 포트 2", kind="inst")
    arrow(ax, 22, yA, 39, yA, "케이블 · 감쇠기")
    arrow(ax, 61, yA, 78, yA, "케이블 · 어댑터")
    note(ax, 50, yA - 9.5, "L(f) = 주파수별 총 손실  →  보정 테이블 저장", ha="center", size=7.2)
    # (b) 측정 단계
    yB = 12
    note(ax, 2, yB + 13, "(b) 측정 : 같은 경로에 DUT 를 넣고 L(f) 를 되더한다", size=7.8,
         color=INK, weight="bold")
    box(ax, 13, yB, 18, 11, "SG", kind="inst")
    box(ax, 50, yB, 22, 11, "DUT", kind="dut")
    box(ax, 87, yB, 18, 11, "SA / PM", kind="inst")
    arrow(ax, 22, yB, 39, yB)
    arrow(ax, 61, yB, 78, yB)
    note(ax, 50, yB - 10, "DUT 출력 [dBm] = 계측기 읽은 값 [dBm] + L(f) [dB]",
         ha="center", size=7.4, color=INK, weight="bold")
    caption_title(ax, "그림 2-2  경로 손실 교정의 2단계 구조")
    return save(fig, "s02_path_loss_cal")


def s03_tx_chain():
    fig, ax = scheme_axes(6.3, 2, 40)
    y = 30
    names = [("BB / DAC", "I·Q 생성"), ("믹서", "상향 변환"), ("BPF", "대역 제한"),
             ("드라이버", "전단 이득"), ("PA", "전력 증폭"), ("스위치·듀플렉서", "경로 선택")]
    xs = [10, 26, 40, 54, 69, 88]
    ws = [15, 12, 11, 12, 12, 20]
    for x, w, (n, s) in zip(xs, ws, names):
        box(ax, x, y, w, 12, n, s)
    for i in range(len(xs) - 1):
        arrow(ax, xs[i] + ws[i] / 2, y, xs[i + 1] - ws[i + 1] / 2, y)
    arrow(ax, 98, y, 100, y)
    ax.text(20, 14, "EVM · I/Q 불균형\nLO 누설", ha="center", va="top", fontsize=6.8, color=INK2)
    ax.text(47, 14, "하모닉 · 스퓨리어스\n대역외 방출", ha="center", va="top", fontsize=6.8, color=INK2)
    ax.text(69, 14, "출력 전력 · P1dB\nACLR · PAE", ha="center", va="top", fontsize=6.8, color=INK2)
    ax.text(90, 14, "삽입손실 · 격리도\n스위칭 시간", ha="center", va="top", fontsize=6.8, color=INK2)
    for x in (20, 47, 69, 90):
        ax.plot([x, x], [22.5, 17.5], color=AXIS, lw=0.7, zorder=1)
    caption_title(ax, "그림 4-1  송신 체인과 각 구간에서 지배적인 측정 항목")
    return save(fig, "s03_tx_chain")


def s04_rx_chain():
    fig, ax = scheme_axes(6.3, 2, 50)
    y = 30
    names = [("스위치·듀플렉서", "경로 선택"), ("BPF", "대역 선택"), ("LNA", "저잡음 증폭"),
             ("믹서", "하향 변환"), ("채널 필터", "선택도"), ("ADC / 복조", "데이터 복원")]
    xs = [12, 29, 43, 57, 73, 90]
    ws = [20, 11, 11, 11, 15, 15]
    for x, w, (n, s) in zip(xs, ws, names):
        box(ax, x, y, w, 12, n, s)
    for i in range(len(xs) - 1):
        arrow(ax, xs[i] + ws[i] / 2, y, xs[i + 1] - ws[i + 1] / 2, y)
    arrow(ax, 0, y, 2, y)
    ax.text(43, 14, "잡음지수(NF)\n감도의 지배 요인", ha="center", va="top", fontsize=6.8, color=INK2)
    ax.text(73, 14, "ACS · 차단\n이미지 억압", ha="center", va="top", fontsize=6.8, color=INK2)
    ax.text(90, 14, "BER / PER\nRSSI 확도", ha="center", va="top", fontsize=6.8, color=INK2)
    for x in (43, 73, 90):
        ax.plot([x, x], [22.5, 17.5], color=AXIS, lw=0.7, zorder=1)
    note(ax, 43, 45, "이 지점 이후의 잡음은 되돌릴 수 없다", ha="center", size=7.0, color=CRIT)
    caption_title(ax, "그림 4-2  수신 체인과 각 구간에서 지배적인 측정 항목")
    return save(fig, "s04_rx_chain")


def s05_power_setups():
    fig, ax = scheme_axes(6.3, 2, 74)
    for i, (yy, tag, desc) in enumerate([
            (60, "(a) 직결", "저·중전력. 감쇠기로 센서 정격 이내로 낮춘다"),
            (34, "(b) 커플러", "고전력. 결합도 C(f) 를 보정한다"),
            (8, "(c) 분석기", "스펙트럼을 함께 볼 때. 절대값은 (a)와 교차검증")]):
        note(ax, 2, yy + 11, f"{tag} — {desc}", size=7.6, color=INK, weight="bold")
    y = 60
    box(ax, 14, y, 16, 10, "DUT", kind="dut"); box(ax, 42, y, 14, 8, "감쇠기")
    box(ax, 76, y, 24, 10, "전력 센서 + 전력계", kind="inst")
    arrow(ax, 22, y, 35, y); arrow(ax, 49, y, 64, y)
    y = 34
    box(ax, 14, y, 16, 10, "DUT", kind="dut"); box(ax, 42, y, 16, 8, "디렉셔널 커플러")
    box(ax, 76, y, 24, 10, "전력 센서 + 전력계", kind="inst")
    box(ax, 42, y - 15, 16, 7, "고전력 종단", kind="ghost")
    arrow(ax, 22, y, 34, y); arrow(ax, 50, y + 1, 64, y + 1)
    arrow(ax, 42, y - 4, 42, y - 11.5)
    y = 8
    box(ax, 14, y, 16, 10, "DUT", kind="dut"); box(ax, 42, y, 14, 8, "감쇠기")
    box(ax, 76, y, 24, 10, "스펙트럼 분석기", "Channel Power", kind="inst")
    arrow(ax, 22, y, 35, y); arrow(ax, 49, y, 64, y)
    caption_title(ax, "그림 4-3  출력 전력 측정의 세 가지 표준 셋업")
    return save(fig, "s05_power_setups")


def s06_vna_cal():
    fig, ax = scheme_axes(6.3, -2, 48)
    note(ax, 2, 42, "(a) 무엇을 걷어내는가 — 측정된 것 = 오차항 ⊗ DUT", size=7.8,
         color=INK, weight="bold")
    box(ax, 13, 30, 18, 10, "VNA 수신기", kind="inst")
    box(ax, 38, 30, 16, 10, "오차항 A", "방향성·소스정합\n반사·전달 추적", kind="warn")
    box(ax, 62, 30, 14, 10, "DUT", kind="dut")
    box(ax, 87, 30, 16, 10, "오차항 B", kind="warn")
    for a, b in [(22, 30), (46, 55), (69, 79)]:
        arrow(ax, a, 30, b, 30)
    note(ax, 2, 16, "(b) 교정 표준 — 아는 답으로 오차항을 푼다", size=7.8, color=INK, weight="bold")
    for x, (t, s) in zip([12, 30, 48, 68, 90],
                         [("SHORT", "Γ = −1"), ("OPEN", "Γ = +1"), ("LOAD", "Γ = 0"),
                          ("THRU", "직결"), ("LINE", "TRL 전용")]):
        box(ax, x, 5, 15, 9, t, s, kind="ghost")
    caption_title(ax, "그림 3-1  VNA 오차 보정의 구조와 교정 표준")
    return save(fig, "s06_vna_cal")


def s07_deembed():
    fig, ax = scheme_axes(6.3, -10, 44)
    note(ax, 2, 40, "(a) 포트 확장 — 지연만 이동. 정합 오차는 남는다", size=7.6,
         color=INK, weight="bold")
    box(ax, 14, 29, 16, 9, "동축 교정면", kind="ghost")
    box(ax, 44, 29, 20, 9, "픽스처 (전이부)", kind="warn")
    box(ax, 78, 29, 16, 9, "DUT", kind="dut")
    arrow(ax, 22, 29, 34, 29); arrow(ax, 54, 29, 70, 29)
    arrow(ax, 22, 22, 70, 22, style="<->", color=CRIT, lw=1.0)
    note(ax, 46, 19.5, "지연 τ 만큼 기준면 이동 (위상만 보정)", ha="center", size=6.9, color=CRIT)
    note(ax, 2, 12, "(b) 디임베딩 — 픽스처의 S-파라미터를 수학적으로 제거", size=7.6,
         color=INK, weight="bold")
    box(ax, 14, 3, 16, 9, "동축 교정면", kind="ghost")
    box(ax, 44, 3, 20, 9, "픽스처 모델", "S11·S21·S22", kind="warn")
    box(ax, 78, 3, 16, 9, "DUT", kind="dut")
    arrow(ax, 22, 3, 34, 3); arrow(ax, 54, 3, 70, 3)
    note(ax, 44, -6, "정합 효과까지 제거 → 확도 우수", ha="center", size=6.9, color=GOOD)
    caption_title(ax, "그림 3-2  기준면 이동 : 포트 확장 vs 디임베딩")
    return save(fig, "s07_deembed")


def s08_harmonic_setup():
    fig, ax = scheme_axes(6.3, 0, 40)
    y = 30
    box(ax, 11, y, 16, 11, "DUT", kind="dut")
    box(ax, 33, y, 13, 9, "감쇠기")
    box(ax, 57, y, 24, 11, "HPF 또는 노치", "기본파 억제", kind="warn")
    box(ax, 87, y, 20, 11, "스펙트럼 분석기", kind="inst")
    arrow(ax, 19, y, 26.5, y); arrow(ax, 39.5, y, 45, y); arrow(ax, 69, y, 77, y)
    note(ax, 57, y - 10, "필터 삽입손실 IL(f) 를 하모닉 주파수별로 사전 측정해 보정", ha="center", size=7.0)
    box(ax, 11, 7, 16, 9, "SG", kind="inst")
    box(ax, 36, 7, 18, 9, "LPF", "SG 하모닉 차단", kind="warn")
    box(ax, 63, 7, 16, 9, "DUT 입력", kind="ghost")
    arrow(ax, 19, 7, 27, 7); arrow(ax, 45, 7, 55, 7)
    note(ax, 84, 7, "← 능동 DUT 구동 시 신호원 쪽에는 LPF", ha="left", size=7.0)
    caption_title(ax, "그림 4-4  하모닉 측정 셋업 — HPF와 LPF의 역할은 정반대다")
    return save(fig, "s08_harmonic_setup")


def s09_twotone():
    fig, ax = scheme_axes(6.3, 0, 46)
    box(ax, 11, 38, 13, 9, "SG 1", kind="inst")
    box(ax, 11, 15, 13, 9, "SG 2", kind="inst")
    box(ax, 30, 38, 12, 8, "BPF", kind="warn"); box(ax, 30, 15, 12, 8, "BPF", kind="warn")
    box(ax, 48, 38, 14, 8, "패드/아이솔레이터", kind="warn")
    box(ax, 48, 15, 14, 8, "패드/아이솔레이터", kind="warn")
    box(ax, 68, 26.5, 11, 9, "결합기")
    box(ax, 83, 26.5, 11, 9, "DUT", kind="dut")
    box(ax, 96, 26.5, 8, 9, "SA", kind="inst")
    arrow(ax, 17.5, 38, 24, 38); arrow(ax, 36, 38, 41, 38); arrow(ax, 55, 38, 62.5, 31)
    arrow(ax, 17.5, 15, 24, 15); arrow(ax, 36, 15, 41, 15); arrow(ax, 55, 15, 62.5, 22)
    arrow(ax, 73.5, 26.5, 77.5, 26.5); arrow(ax, 88.5, 26.5, 92, 26.5)
    note(ax, 48, 5, "격리가 부족하면 SG 내부에서 IM 이 생성되어 최대 20 dB 오차 [24]",
         ha="center", size=7.0, color=CRIT)
    caption_title(ax, "그림 4-5  투톤 상호변조 측정 셋업 — 격리와 필터링이 결과를 좌우한다")
    return save(fig, "s09_twotone_setup")


def s10_rx_setup():
    fig, ax = scheme_axes(6.3, 2, 54)
    box(ax, 11, 44, 14, 10, "VSG", "원하는 신호", kind="inst")
    box(ax, 11, 20, 14, 10, "SG", "방해파", kind="inst")
    box(ax, 32, 44, 11, 8, "감쇠기"); box(ax, 32, 20, 11, 8, "BPF", kind="warn")
    box(ax, 50, 32, 11, 9, "결합기")
    box(ax, 66, 32, 11, 8, "감쇠기")
    box(ax, 84, 32, 18, 11, "DUT", "안테나 포트", kind="dut")
    arrow(ax, 18, 44, 26.5, 44); arrow(ax, 37.5, 44, 44.5, 36)
    arrow(ax, 18, 20, 26.5, 20); arrow(ax, 37.5, 20, 44.5, 28)
    arrow(ax, 55.5, 32, 60.5, 32); arrow(ax, 71.5, 32, 75, 32)
    ax.add_patch(FancyBboxPatch((44, 20), 52, 26, boxstyle="round,pad=0,rounding_size=1.5",
                                fc="none", ec=CRIT, lw=1.0, ls=(0, (4, 2)), zorder=0))
    note(ax, 70, 48, "차폐 박스", ha="center", size=7.0, color=CRIT, weight="bold")
    box(ax, 84, 9, 18, 9, "PC", "PER / BER 카운터", kind="inst")
    arrow(ax, 84, 26.5, 84, 13.5, style="<|-|>")
    note(ax, 2, 6, "감도 시험의 확도는 경로 손실 보정 확도를 그대로 상속한다", size=7.0)
    caption_title(ax, "그림 4-6  수신 감도 · 선택도 · 차단 시험 통합 셋업")
    return save(fig, "s10_rx_setup")


def s11_nf_setup():
    fig, ax = scheme_axes(6.3, -9, 48)
    note(ax, 2, 42, "(a) 교정 — 계측기 단독 잡음을 먼저 측정한다", size=7.6, color=INK, weight="bold")
    box(ax, 16, 31, 20, 10, "잡음원", "ENR 성적서", kind="warn")
    box(ax, 55, 31, 22, 10, "NF 분석기 / SA", kind="inst")
    arrow(ax, 26, 31, 44, 31)
    note(ax, 82, 31, "→  계측기의 F, G 확보", ha="left", size=7.2)
    note(ax, 2, 17, "(b) 측정 — DUT 삽입 후 2단 보정으로 DUT 단독 NF 산출", size=7.6,
         color=INK, weight="bold")
    box(ax, 14, 6, 18, 10, "잡음원", kind="warn")
    box(ax, 44, 6, 16, 10, "DUT", kind="dut")
    box(ax, 78, 6, 22, 10, "NF 분석기", kind="inst")
    arrow(ax, 23, 6, 36, 6); arrow(ax, 52, 6, 67, 6)
    note(ax, 50, -4.5, "F_DUT = F_meas - (F_inst - 1) / G_DUT      (Friis 2단 보정)", ha="center",
         size=7.4, color=INK, weight="bold")
    caption_title(ax, "그림 4-7  Y-factor 잡음지수 측정과 2단 보정")
    return save(fig, "s11_nf_setup")


def s12_loadpull():
    fig, ax = scheme_axes(6.3, -2, 42)
    y = 32
    box(ax, 9, y, 12, 10, "SG", kind="inst")
    box(ax, 27, y, 16, 11, "소스 튜너", "Γs 제어", kind="warn")
    box(ax, 45, y, 11, 9, "커플러")
    box(ax, 59, y, 12, 11, "DUT", kind="dut")
    box(ax, 73, y, 11, 9, "커플러")
    box(ax, 89, y, 16, 11, "부하 튜너", "Γl 제어", kind="warn")
    for a, b in [(15, 19), (35, 39.5), (50.5, 53), (65, 67.5), (78.5, 81)]:
        arrow(ax, a, y, b, y)
    arrow(ax, 97, y, 100, y)
    box(ax, 45, 9, 13, 9, "VNA 수신기", kind="inst")
    box(ax, 73, 9, 13, 9, "VNA 수신기", kind="inst")
    arrow(ax, 45, 27.5, 45, 13.5, style="-|>", dashed=True)
    arrow(ax, 73, 27.5, 73, 13.5, style="-|>", dashed=True)
    note(ax, 59, 9, "a·b 파를 DUT 기준면에서 벡터 측정", ha="center", size=6.8)
    box(ax, 10, 9, 18, 9, "DC 전원 (V, I)", kind="inst")
    arrow(ax, 19, 13.5, 55, 26, style="-|>", dashed=True)
    note(ax, 10, 1, "P_DC → PAE", ha="center", size=6.9, color=INK2)
    caption_title(ax, "그림 4-8  Load Pull 측정 시스템 구성")
    return save(fig, "s12_loadpull_setup")


def s13_phasenoise():
    fig, ax = scheme_axes(6.3, -20, 38)
    for x0, title, blocks in [
        (2, "(a) 직접 스펙트럼법", [("DUT", "dut"), ("SA", "inst")]),
        (36, "(b) PLL / 위상검출법", [("DUT", "dut"), ("믹서 + 기준원", "warn"), ("LNA·FFT", "inst")]),
        (70, "(c) 교차상관법", [("DUT", "dut"), ("2채널 경로", "warn"), ("상관 연산", "inst")]),
    ]:
        note(ax, x0, 32, title, size=7.5, color=INK, weight="bold")
        yy = 20
        for i, (nm, kd) in enumerate(blocks):
            box(ax, x0 + 12, yy, 22, 8, nm, kind=kd)
            if i < len(blocks) - 1:
                arrow(ax, x0 + 12, yy - 4, x0 + 12, yy - 8)
            yy -= 12
    note(ax, 2, -14, "감도  (a) < (b) < (c).  교차상관은 상관 횟수 N 에 대해 약 5·log10(N) [dB] 개선 [12]",
         size=7.2, color=INK2)
    caption_title(ax, "그림 4-9  위상잡음 측정의 세 가지 방식")
    return save(fig, "s13_phasenoise_methods")


def s14_ota():
    fig, ax = scheme_axes(6.3, -8, 46)
    ax.add_patch(FancyBboxPatch((6, 4), 66, 38, boxstyle="round,pad=0,rounding_size=2",
                                fc="#f7f9fa", ec=INK2, lw=1.2, zorder=0))
    for i in range(14):
        ax.plot([7 + i * 4.6, 9.3 + i * 4.6], [42, 38.5], color=AXIS, lw=0.8)
        ax.plot([7 + i * 4.6, 9.3 + i * 4.6], [4, 7.5], color=AXIS, lw=0.8)
    for i in range(8):
        ax.plot([6, 9.5], [5 + i * 4.6, 7.3 + i * 4.6], color=AXIS, lw=0.8)
        ax.plot([72, 68.5], [5 + i * 4.6, 7.3 + i * 4.6], color=AXIS, lw=0.8)
    box(ax, 26, 23, 14, 11, "DUT", "θ, φ 회전", kind="dut")
    box(ax, 56, 23, 15, 11, "측정 안테나", "2 편파", kind="inst")
    arrow(ax, 33.5, 23, 48, 23, style="<|-|>")
    note(ax, 41, 27.5, "레인지 길이", ha="center", size=6.8)
    note(ax, 39, 8, "무향실 (전파 흡수체)", ha="center", size=7.0, color=INK2, weight="bold")
    box(ax, 88, 30, 20, 10, "통신 테스터", kind="inst")
    box(ax, 88, 14, 20, 10, "포지셔너 제어", kind="inst")
    arrow(ax, 63.5, 25, 78, 30); arrow(ax, 33, 18, 78, 15, dashed=True)
    note(ax, 2, -2, "기준 안테나로 레인지 경로손실·수신안테나 이득·케이블 손실을 사전 교정한다 [43][44]",
         size=7.0)
    caption_title(ax, "그림 4-10  OTA (TRP / TIS) 측정 배치")
    return save(fig, "s14_ota")


if __name__ == "__main__":
    os.makedirs("figures", exist_ok=True)
    for fn in [s01_system, s02_pathloss, s03_tx_chain, s04_rx_chain, s05_power_setups,
               s06_vna_cal, s07_deembed, s08_harmonic_setup, s09_twotone, s10_rx_setup,
               s11_nf_setup, s12_loadpull, s13_phasenoise, s14_ota]:
        fn()
    print("schemes done")

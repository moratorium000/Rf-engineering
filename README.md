# RF Engineering

RF 벤치 테스트 관련 기술 문서 저장소.

## 문서

두 문서는 짝을 이룬다. 같은 내용을 다른 깊이로 다루며, 입문서 부록 D에 절 단위 대응표가 있다.

| 문서 | 대상 | 설명 | 형식 |
|---|---|---|---|
| `docs/RF_벤치_테스트_입문서` | 비전공자 · 입문자 | 용어부터 설명하는 안내서. dB·임피던스·잡음 같은 기초부터 시작해, 측정 항목을 비유와 이야기로 설명한다. 용어 상자 58개, 함정 상자 68개, 계산 예제, 첫 달 학습 경로, 현장 용어 번역기, 인쇄용 한 장 요약 포함 | `.md` / `.docx` / `.pdf` |
| `docs/RF_벤치_테스트_엔지니어_가이드` | 실무자 | 상세판. 보드/모듈/시스템 레벨 RF 측정 항목 총람 (IC 설계단 제외). Trim, Rx, Harmonics, Power Meter, VNA, Load Pull 등 24개 시험 항목을 목적·셋업·절차·판정·디버깅·함정 골격으로 기술 | `.md` / `.docx` / `.pdf` |

## 빌드

Markdown 원본(`docs/*.md`)에서 DOCX를 생성한다.

```bash
pip install python-docx
python3 tools/build_docx.py docs/<문서>.md docs/<문서>.docx
```

PDF는 LibreOffice Writer로 변환하며, 목차 필드의 페이지 번호를 채우기 위해
UNO 브리지로 인덱스를 갱신한 뒤 내보낸다(`libreoffice-writer`, `python3-uno` 필요).

한글 렌더링에는 `fonts-noto-cjk`(본문, Noto Sans CJK KR)와
`fonts-nanum`(코드 블록, NanumGothicCoding)이 필요하다.

# RF Engineering

RF 벤치 테스트 관련 기술 문서 저장소.

## 문서

| 문서 | 설명 | 형식 |
|---|---|---|
| `docs/RF_벤치_테스트_엔지니어_가이드` | RF 벤치 테스트 엔지니어 실무 가이드 — 보드/모듈/시스템 레벨 RF 측정 항목 총람 (IC 설계단 제외). Trim, Rx, Harmonics, Power Meter, VNA, Load Pull 등 24개 시험 항목을 목적·셋업·절차·판정·디버깅·함정 골격으로 기술 | `.md` / `.docx` / `.pdf` |

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

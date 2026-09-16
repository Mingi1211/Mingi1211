# sensor-logger — 패키징 연습

`Mingi1211/sensor-logger` (public) · 최종 커밋 2026-09-02 `ae641e0 Add README` · 파일 9개

## 무엇

합성 센서 데이터 50개(사인파 + 노이즈)를 만들어 `out/sensor_log.csv` 로 쓰고
`out/sensor_plot.png` 를 렌더하는 최소 파이프라인. **headless matplotlib 백엔드**를 써서
컨테이너 안에서든 데스크톱에서든 동일하게 돌아간다.

## 목적 (README에 명시)

> "Built as a packaging exercise"

- `uv` — 의존성 해석 + `src/` 레이아웃
- `Docker` — 재현 가능한 실행 환경
- Python 3.12+

```bash
uv run python main.py
docker build -t sensor-logger . && docker run --rm -v "$PWD/out:/app/out" sensor-logger
```

## 읽어낼 수 있는 것

`dreamlab-bootcamp`(8월)에서 uv를 익히고, 그 다음 단계로 **Docker 재현성까지 붙인 흐름**(9월).
연구 코드가 아니라 **도구 체계를 갖추는 작업**이다.

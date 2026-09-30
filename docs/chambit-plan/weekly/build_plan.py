import sys
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = sys.argv[1]
FONT = '바탕체'
doc = Document()

# ---------- 기본 서식 ----------
def set_font(rpr_owner, size=10, bold=None):
    rpr = rpr_owner.get_or_add_rPr() if hasattr(rpr_owner, 'get_or_add_rPr') else rpr_owner
    fonts = rpr.find(qn('w:rFonts'))
    if fonts is None:
        fonts = OxmlElement('w:rFonts'); rpr.insert(0, fonts)
    for k in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'):
        fonts.set(qn(k), FONT)

for sname in ('Normal', 'Heading 1', 'Heading 2', 'Title'):
    st = doc.styles[sname]
    st.font.name = FONT
    st.font.color.rgb = RGBColor(0, 0, 0)
    set_font(st.element.get_or_add_rPr())
doc.styles['Normal'].font.size = Pt(10)
doc.styles['Normal'].paragraph_format.space_after = Pt(2)
doc.styles['Normal'].paragraph_format.line_spacing = 1.15
doc.styles['Heading 1'].font.size = Pt(13)
doc.styles['Heading 1'].paragraph_format.space_before = Pt(12)
doc.styles['Heading 1'].paragraph_format.space_after = Pt(4)
doc.styles['Heading 2'].font.size = Pt(11)
doc.styles['Heading 2'].paragraph_format.space_before = Pt(8)
doc.styles['Heading 2'].paragraph_format.space_after = Pt(3)
doc.styles['Title'].font.size = Pt(16)

sec = doc.sections[0]
sec.orientation = WD_ORIENT.LANDSCAPE
sec.page_width, sec.page_height = Cm(29.7), Cm(21.0)
for side in ('left_margin', 'right_margin'):
    setattr(sec, side, Cm(1.8))
sec.top_margin = sec.bottom_margin = Cm(1.6)
USABLE = 29.7 - 3.6


def run(p, text, bold=False, size=10, color=None):
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)
    r.font.name = FONT
    set_font(r._element.get_or_add_rPr())
    if color:
        r.font.color.rgb = RGBColor.from_string(color)
    return r


def para(text='', bold=False, size=10, align=None, after=None):
    p = doc.add_paragraph()
    if align:
        p.alignment = align
    if after is not None:
        p.paragraph_format.space_after = Pt(after)
    add_rich(p, text, bold, size)
    return p


def add_rich(p, text, bold=False, size=10):
    """**굵게** 표기 지원"""
    parts = text.split('**')
    for i, t in enumerate(parts):
        if t:
            run(p, t, bold=bold or (i % 2 == 1), size=size)


def bullet(text, level=0):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Cm(0.5 + 0.6 * level)
    pf.first_line_indent = Cm(-0.4)
    pf.space_after = Pt(1)
    add_rich(p, ('- ' if level == 0 else '· ') + text)
    return p


def heading(text, level=1):
    h = doc.add_heading(level=level)
    run(h, text, bold=True, size=13 if level == 1 else 11)
    return h


def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), hexcolor)
    tcPr.append(shd)


def cell_text(cell, content, bold=False, align=None):
    """content: str 또는 [str,...] (각 항목이 한 문단, '- '로 시작하면 내어쓰기)"""
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER if align else WD_CELL_VERTICAL_ALIGNMENT.TOP
    items = content if isinstance(content, list) else [content]
    first = cell.paragraphs[0]
    for k, item in enumerate(items):
        p = first if k == 0 else cell.add_paragraph()
        pf = p.paragraph_format
        pf.space_after = Pt(1)
        pf.line_spacing = 1.1
        if align:
            p.alignment = align
        if item.startswith('- '):
            pf.left_indent = Cm(0.3)
            pf.first_line_indent = Cm(-0.3)
        add_rich(p, item, bold=bold)


def table(widths_cm, header, rows, header_fill='D9D9D9', first_col_fill=None, center_cols=()):
    t = doc.add_table(rows=1, cols=len(widths_cm))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for i, w in enumerate(widths_cm):
        c = t.rows[0].cells[i]
        c.width = Cm(w)
        cell_text(c, header[i], bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        shade(c, header_fill)
    # 머리행 반복
    trPr = t.rows[0]._tr.get_or_add_trPr()
    th = OxmlElement('w:tblHeader'); th.set(qn('w:val'), 'true'); trPr.append(th)
    for r in rows:
        row = t.add_row()
        cs = OxmlElement('w:cantSplit'); cs.set(qn('w:val'), 'true')
        row._tr.get_or_add_trPr().append(cs)
        cells = row.cells
        for i, w in enumerate(widths_cm):
            cells[i].width = Cm(w)
            al = WD_ALIGN_PARAGRAPH.CENTER if i in center_cols else None
            cell_text(cells[i], r[i], bold=(i == 0 and first_col_fill is not None), align=al)
            if i == 0 and first_col_fill:
                shade(cells[i], first_col_fill)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


# =====================================================================
t = doc.add_paragraph()
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
run(t, 'AI Worker2 협동 박스 운반 프로젝트 — 주간 세부 계획', bold=True, size=16)
p = para('참빛설계학기(로봇인턴십) 2026-2 · 제어 파트 김민기 · 김현대 · 작성 2026-09-30', align=WD_ALIGN_PARAGRAPH.CENTER, after=8)

heading('0. 한눈에 보기')
table([4.2, USABLE - 4.2], ['항목', '내용'], [
    ['활동 기간', '**10/5(월) ~ 11/22(일)** 활동 6주 + 중간고사 1주(10/19~10/25) 제외. 11월 3주차까지 기능 구현·정량 평가 완료'],
    ['이후', '11/23 ~ 12월: 최종결과보고서·발표자료·시연 영상 정리, 성과발표회(개강 후 16주차)'],
    ['교수님 미팅', '매주 주간 상황보고 발표 + 피드백. 보고 형식은 5장 참고'],
    ['1차 면담 일정과 차이', '면담 자료는 9주(10/1~11/30) 계획이었는데 **6주로 압축**했다. 그래서 ① 시뮬레이션과 실로봇 준비를 1주차부터 병렬로 진행하고 ② 시간이 오래 걸리는 선행 작업(2장)을 앞으로 당겼으며 ③ 4주차에 게이트를 두고, 막히면 범위를 줄이는 기준(6장)을 미리 정했다'],
    ['순서 원칙', '면담 자료 19쪽 그대로 — **단일 팔(1대 양팔) 리프트 → 2대 정지 유지 → 동기화 직선 운반.** 앞 단계가 되기 전에 다음 단계를 실로봇에서 시도하지 않는다'],
], first_col_fill='F2F2F2')

# ---------------------------------------------------------------------
heading('1. 역할 분담 (1차 면담안 조정 제안)')
para('1차 면담 자료의 큰 틀(김민기 = Kinematics & Dynamics / 김현대 = Interaction Control & Base)은 그대로 둔다. '
     '다만 **휴머노이드 상반신 whole-body control 진학과 다음 학기 캡스톤에 직접 쓰이는 항목**은 김민기 쪽으로 모았다. '
     '김현대는 "힘을 읽고 부드럽게 반응한다"는 한 줄로 설명되는 일관된 축을 맡는다.')
table([4.0, 9.3, 9.3, USABLE - 22.6], ['영역', '김민기 — 기구학·동역학·전신 작업공간 제어', '김현대 — 상호작용 제어·베이스', '공통'], [
    ['모델·연산',
     ['- URDF 정비, Pinocchio 모델 (FK·해석적 자코비안·RNEA)', '- 페이로드 역산: RNEA 정지 토크 vs 모터 정격 → 박스 최대 중량', '- 관절 토크 모델(τ_model) 노드 제공 → 외력 추정의 기준선'],
     ['- 전류 → 토크 캘리브레이션(관절별 Kt·마찰 오프셋)', '- 외력 추정 신호처리 노드(영점 보정·LPF), ROS 2 Wrench 퍼블리셔', '- (채택 시) 외란 관측기(DOB)'],
     ['- ROS 2·MuJoCo 환경', '- 성능 로그(MCAP/CSV)']],
    ['궤적·IK',
     ['- 박스 중심 단일 가상 강체 5차 다항식 궤적(접근·리프트·운반·하강·해제)', '- 네 팔 목표 pose 분산 매핑', '- 수치 IK(Newton-Raphson/DLS, warm start) → **제약 QP IK로 확장**(관절 위치·속도 한계, 자세 유지 task)', '- **5차 다항식·DLS vs QP 비교** (면담 자료 4쪽 "MPC/QP vs 5차 다항식")'],
     ['- 어드미턴스 형태 임피던스 출력(힘 오차 → 위치 오프셋)을 IK 목표에 더하는 인터페이스'],
     ['']],
    ['힘·협동',
     ['- **그래스프 행렬 기반 하중 분배**: 수직 하중 균등 분배 + 내력(조임력)을 null-space 성분으로 분리 → 팔별 목표 wrench', '- 정지 유지 피드포워드: RNEA 자중 + Jᵀ·(분배된 박스 하중)'],
     ['- 리더-팔로워 **가변 강성 임피던스**(리더 High-K / 팔로워 Low-K, 운반 중 X축 저강성·Z축 고강성)', '- 목표 wrench 추종으로 내력 완화', '- 접촉 판정·정상 체결 판단·미끄러짐/낙하 감지·착지(하중 소멸) 감지'],
     ['']],
    ['베이스·안전',
     ['- 태스크 시퀀서(상태머신): 접근~해제 단계 전이 조건·예외 처리 통합'],
     ['- 2대 네트워크: Chrony 시간 동기화·Fast-DDS', '- 주행 동기화: 오도메트리(엔코더+IMU) 상호 교환 100 Hz, Virtual Tow-bar 리더-팔로워 속도 제어', '- I²t 과열 보호 → Auto-lowering, E-Stop'],
     ['- ros2_control 드라이버 검증', '- 실로봇 실험·영상']],
], first_col_fill='F2F2F2')

heading('1차 면담안에서 바뀐 점과 이유', 2)
table([6.2, 5.0, USABLE - 11.2], ['변경', '면담안', '이유'], [
    ['**하중 분배·협동 내력 완화 → 김민기**', '김현대', '여러 접촉점에 힘을 나누는 문제(그래스프 행렬, 내력 null-space)는 휴머노이드 WBC의 접촉력 분배(TSID 등 접촉력 QP)와 같은 구조이고, 상반신 양팔 조작의 기본 이론이다. 김현대의 임피던스는 이 결과(목표 wrench)를 추종하는 역할로 경계가 깔끔해진다. **김현대 동의 필요**'],
    ['**QP IK 추가 + 다항식 vs QP 비교 → 김민기**', '비교만 언급', 'WBC는 결국 제약이 있는 QP다. DLS로 먼저 동작시키고 QP로 확장해 수치로 비교하면 "왜 QP인가"에 직접 답할 수 있다'],
    ['**페이로드 역산·하중 피드포워드 → 김민기**', '명시 안 됨', 'RNEA 기반 정지 토크 분석은 동역학 역량의 증거이고, 박스 규격을 1주차에 확정해야 하는 선행 작업이기도 하다'],
    ['**태스크 시퀀서 통합 → 김민기**', '명시 안 됨', '전 시퀀스를 묶는 사람이 시스템 전체를 설명할 수 있다. 캡스톤 통합 역할로 바로 이어진다'],
    ['**2대 네트워크 → 김현대 주도**', '공통', '베이스 주행 동기화와 붙어 있는 작업이라 한 사람이 끝까지 맡는 편이 빠르다'],
], center_cols=(1,))
para('분량: 김민기 = 모델·궤적·IK·하중 분배·시퀀서 / 김현대 = 캘리브레이션·외력 추정·임피던스·이벤트 감지·베이스 동기화·안전. '
     '김현대 쪽은 하드웨어 작업 비중이 커서 실로봇 실험 시간은 두 사람이 함께 쓴다.')

# ---------------------------------------------------------------------
heading('2. 미리 해야 하는 일 (선행 작업)')
para('뒤 단계의 **전제 조건**이거나 **리드타임이 긴** 작업이다. 해당 기능을 쓰는 주보다 앞당겨 시작한다.')
table([6.0, 3.0, 2.3, USABLE - 11.3], ['선행 작업', '완료 시점', '담당', '왜 먼저 해야 하나'], [
    ['실로봇 2대 사용 일정·안전수칙 확인, 교수님께 시뮬레이션 환경 수령 요청', '1주차 (10/5~)', '공통', '실로봇 시간이 확보돼야 4주차부터 2대 실험이 가능하다. 시뮬레이션 환경을 1주차에 못 받으면 URDF → MuJoCo를 자체 구성한다'],
    ['박스 규격·중량 확정 (RNEA 페이로드 역산)', '1주차', '김민기', '박스가 있어야 3주차 리프트 실험이 가능하다. 구입 → TA 승인 → 배송까지 1~2주'],
    ['박스·손잡이·무게추 재료 구입 신청', '1주차 신청, 2주차 수령', '김현대', '재료 구입은 **10/6부터 가능**하고 TA 사전 승인 → 개인 선집행 순서다'],
    ['토픽 인터페이스 v0 합의 (5장 표)', '1주차', '김민기 작성, 공동 합의', '두 사람이 따로 개발하다가 3주차에 붙일 때 형식이 어긋나지 않게 한다'],
    ['MCAP 로깅 파이프라인', '1주차', '김현대', '매주 보고할 수치(오차·성공률·지연)가 전부 로그에서 나온다'],
    ['**전류 → 토크 캘리브레이션(Kt)**', '2주차 (중간고사 전)', '김현대 (+ 김민기 RNEA 제공)', 'F/T 센서가 없어서 외력 추정·접촉 판정·체결 판단·착지 감지가 **모두 이 값에 의존**한다. 시험 후 바로 실기로 넘어가려면 시험 전에 끝내야 한다'],
    ['2대 네트워크 시간 동기화(Chrony·Fast-DDS)', '2주차', '김현대', '운반은 5주차지만 네트워크 문제는 원인 찾기가 오래 걸린다. 4주차 무부하 동기 주행의 전제'],
    ['시뮬레이션 접근·파지 완성', '2주차', '김민기', '중간고사 뒤 3주차를 곧바로 리프트(실기)로 시작하기 위함'],
], center_cols=(1, 2))

# ---------------------------------------------------------------------
heading('3. 주간 계획표')
para('각 주의 **완료 기준**을 만족해야 다음 주 실로봇 단계로 넘어간다. [선] = 2장의 선행 작업.')

W = [2.6, 7.6, 7.6, 3.7, USABLE - 21.5]
H = ['주차', '김민기', '김현대', '공통', '완료 기준 / 주간 보고']
weeks = [
    ['**1주차**\n10/5 ~ 10/11\n환경 세팅',
     ['- URDF 정비, Pinocchio 모델 로드, 네 팔 말단·박스 그래스프 프레임 정의', '- FK·해석적 자코비안 구현 → 유한차분 자코비안과 대조 검증', '- [선] RNEA로 파지 자세 정지 토크 계산 → 모터 정격 대비 여유율로 박스 최대 중량 역산', '- [선] 토픽 인터페이스 v0 작성'],
     ['- 1대 ros2_control 드라이버 기동, 관절 위치·속도·전류 읽기', '- [선] MCAP 로깅 파이프라인', '- [선] 박스·손잡이·무게추 재료 구입 신청 (10/6부터 구입 가능)'],
     ['- [선] 실로봇 사용 일정·안전수칙', '- [선] 시뮬레이션 환경 수령 요청', '- GitHub 레포·브랜치 규칙'],
     ['- 1대 관절 상태 로그 기록', '- 자코비안 대조 오차 수치', '- 박스 규격·중량 확정', '보고: 역할 분담 확정안, 박스 규격 근거(토크 여유율 표), 인터페이스 v0']],
    ['**2주차**\n10/12 ~ 10/18\n접근·파지 (시뮬)',
     ['- 작업공간 5차 다항식 궤적 생성기 (위치 + 자세 보간)', '- 접근: pre-grasp → 박스 전방 5 cm부터 45° 대각선 저속 진입', '- 수치 IK(DLS, warm start) 루프 주기 측정 (1 kHz 목표), 수렴 실패율', '- RNEA 토크 노드 공개 → 캘리브레이션에 제공'],
     ['- [선] **Kt 캘리브레이션**: 여러 자세·무게추에서 측정 전류 vs RNEA 토크 → 관절별 Kt·마찰 오프셋', '- 단일 팔 외력 추정 v0: τ_ext = Kt·i − τ_model → Jᵀ 역변환으로 wrench, 영점 보정·LPF', '- [선] 2대 Chrony·Fast-DDS 설정, 지연 측정'],
     ['- 박스 수령·손잡이 조립', '- 중간고사 전 결과 정리'],
     ['- 시뮬에서 네 팔 pre-grasp → 진입 동작', '- IK 주기·실패율', '- 관절별 Kt 표, 추정 오차', '- 2대 간 시각 동기 오차', '보고: 시뮬 접근 영상, Kt 결과']],
    ['**중간고사**\n10/19 ~ 10/25',
     ['활동 없음'], ['활동 없음'], ['교수님 미팅 여부 사전 확인'], ['—']],
    ['**3주차**\n10/26 ~ 11/1\n들어올리기·정지 유지\n(시뮬 → 1대 양팔 실기)',
     ['- 박스 중심 좌표계 5 cm 수직 리프트 궤적 → 강체 변환으로 네 팔 목표 pose 분산 매핑', '- **그래스프 행렬 하중 분배**: 수직 하중 균등 + 내력 null-space 분리 → 팔별 목표 wrench', '- 정지 유지 피드포워드: RNEA 자중 + Jᵀ·박스 하중', '- 1대 양팔로 박스 리프트 실기'],
     ['- 어드미턴스 형태 가변 강성 임피던스(힘 오차 → 위치 오프셋), 리더 High-K / 팔로워 Low-K', '- 접촉 판정·정상 체결 판단 (전류가 예측 토크 대비 오차 범위 안인지)', '- 지면 반력 0 판단 → 리프트 시작 트리거'],
     ['- **중간보고서 [서식 4] 10/31까지**', '- 10월 활동일지'],
     ['- 1대 양팔 5 cm 리프트 성공', '- 박스 기울기, 팔별 수직 하중 편차', '보고: 리프트 영상, 하중 분배 전후 내력(추정 wrench) 비교 그래프']],
    ['**4주차**\n11/2 ~ 11/8\n2대 정지 유지 (실기)\n+ 무부하 동기 주행',
     ['- **제약 QP IK**: 관절 위치·속도 한계, 박스 자세 task + 자세 유지 task 가중합 → DLS와 비교 (허리·리프트 축이 있으면 포함)', '- 2대 네 팔 분산 매핑 실기 적용', '- 시뮬 vs 실기 말단 추종 오차 비교'],
     ['- 미끄러짐·낙하 감지 (부하 전류 급복귀, 엔코더 오차 튐)', '- I²t 누적 과열 보호 → Auto-lowering 트리거', '- 주행 동기화: 오도메트리 상호 교환 100 Hz, Virtual Tow-bar 속도 제어 (박스 없이)', '- E-Stop 토픽 (전 노드 정지 확인)'],
     ['- 2대 네 팔 정지 유지 3분 시험'],
     ['- 2대 정지 유지 낙하 0회', '- 무부하 동기 주행 상대거리·상대각 오차', '- E-Stop 동작 확인', '**게이트**: 2대 정지 유지가 안 되면 6장 컷 라인 적용', '보고: DLS vs QP 비교표']],
    ['**5주차**\n11/9 ~ 11/15\n직선 운반·내리기·해제',
     ['- 태스크 시퀀서: 접근 → 파지 → 리프트 → 유지 → 운반 → 내리기 → 해제 전이 조건·예외 처리', '- 운반 중 박스 자세 유지', '- 내리기 궤적, 해제 45° 대각선 5 cm 후퇴 → 초기 자세 복귀'],
     ['- 운반 중 팔로워 X축 저강성 / Z축 고강성 조정', '- 휠 지연·슬립 외란 흡수 성능 측정', '- 착지(하중 소멸) 감지 인터럽트 → 하강 정지, 조임력 0으로 감쇠'],
     ['- 1 m → 3 m 직선 운반 실기'],
     ['- 3 m 직선 운반 1회 이상 성공', '- 착지 감지 반응 지연', '보고: 운반 영상, 상대거리 오차 그래프']],
    ['**6주차**\n11/16 ~ 11/22\n통합 검증·정량 평가\n(마무리)',
     ['- 평가 스크립트 (MCAP → 지표 자동 산출)', '- 5차 다항식·DLS vs QP 비교 결과 정리', '- 시퀀서 기준 전 시퀀스 반복 운용'],
     ['- 외력 추정 정확도 (무게추 기준값 대비)', '- 동기화 오차·슬립 흡수 성능 정리'],
     ['- 전 시퀀스 10회 반복 시험', '- 시연 영상 촬영', '- 실패 원인 분류'],
     ['- 계획서 정량 목표 대비 달성표', '보고: 최종 수치, 실패 사례와 원인']],
    ['**정리**\n11/23 ~ 12월',
     ['- 최종결과보고서 중 기구학·궤적·하중 분배 부분', '- 발표자료'],
     ['- 최종결과보고서 중 상호작용 제어·베이스 부분'],
     ['- 11월 활동일지, 최종결과보고서 [서식 7]', '- 성과발표회'],
     ['—']],
]
for w in weeks:
    w[0] = w[0].split('\n')
table(W, H, weeks, first_col_fill='F2F2F2')

# ---------------------------------------------------------------------
heading('4. 인터페이스 약속 (v0, 1주차 합의용)')
table([6.5, 4.5, USABLE - 11.0], ['토픽 (가칭)', '보내는 쪽 → 받는 쪽', '내용'], [
    ['/box/target_pose', '김민기 시퀀서 → 김민기 IK', '박스 중심 목표 자세 (5차 다항식 궤적 샘플)'],
    ['/arm_i/target_pose', '김민기 → 김현대 어드미턴스', '팔별 목표 말단 자세 (i = 1~4)'],
    ['/arm_i/pose_offset', '김현대 → 김민기 IK', '임피던스(어드미턴스) 보정량. IK 목표에 더해 위치 제어기로 전송'],
    ['/arm_i/wrench_des', '김민기 하중 분배 → 김현대', '팔별 목표 wrench (하중 분배 + 내력 설정값)'],
    ['/arm_i/tau_model', '김민기 RNEA → 김현대', '관절 모델 토크 (자중 + 박스 하중 피드포워드)'],
    ['/arm_i/wrench_est', '김현대 → 김민기 시퀀서', '전류 기반 추정 외력 (접촉·체결·착지 판단 근거)'],
    ['/task/state', '김민기 시퀀서 → 전체', '현재 단계와 전이 이벤트'],
    ['/base/sync_cmd', '김현대 → 베이스 2대', '리더 속도 프로파일과 팔로워 추종 명령'],
    ['/estop', '김현대 → 전체', '비상정지. 수신 시 모든 노드 즉시 홀드'],
], center_cols=(1,))

# ---------------------------------------------------------------------
heading('5. 교수님 주간 보고 형식 (매주 3~5장)')
bullet('**지난주 한 일** — 계획표 항목 기준으로 완료 / 진행 중 / 미착수 표시')
bullet('**수치** — 이번 주 완료 기준에 해당하는 측정값 (그래프 1장 이상). 영상은 30초 이내')
bullet('**막힌 것** — 원인 가설과 시도한 것. 교수님께 여쭐 질문을 1~2개로 정리')
bullet('**다음 주 계획** — 계획표와 달라진 점이 있으면 이유를 함께')
bullet('**요청사항** — 실로봇 시간, 장비, 선배 도움 등')

# ---------------------------------------------------------------------
heading('6. 지연 시 대응 (컷 라인)')
table([5.0, USABLE - 5.0], ['조건', '대응'], [
    ['1주차에 시뮬레이션 환경을 못 받음', 'URDF → MuJoCo 자체 구성으로 진행. 교수님 환경을 받으면 이식'],
    ['2주차 끝까지 Kt 캘리브레이션 오차가 큼', '외력 추정 기반 판정을 **엔코더 위치 오차 기반 판정**으로 축소하고, 추정 오차는 한계로 보고'],
    ['4주차 끝까지 2대 정지 유지 실패', '운반 실증은 **1대 양팔**로 축소하고, 2대 운반은 시뮬레이션으로 검증'],
    ['5주차 끝까지 3 m 운반 실패', '**1 m**로 정량 평가, 3 m는 시뮬레이션 결과로 대체'],
    ['QP IK가 실시간 주기를 못 맞춤', '실기는 DLS를 쓰고, QP는 오프라인·시뮬 비교 결과로만 제시'],
], first_col_fill='F2F2F2')

# ---------------------------------------------------------------------
heading('7. 김민기 — CV·면접용 정리')
heading('CV 문장 (수치는 결과가 나오면 채움)', 2)
bullet('Formulated object-centric cooperative manipulation for two ROBOTIS FFW-SG2 mobile manipulators (4 arms, closed kinematic chain): box-frame quintic trajectories mapped to each end-effector.')
bullet('Implemented grasp-matrix-based load distribution separating internal (squeeze) forces via the null space, with RNEA gravity and payload feedforward (Pinocchio).')
bullet('Developed constrained QP differential IK (joint position/velocity limits, posture task) running at __ Hz; compared with DLS IK — __% lower tracking error near joint limits.')
bullet('Integrated the full approach-grasp-lift-carry-place-release task sequencer on real hardware; __/10 end-to-end success.')
heading('면접에서 할 이야기', 2)
bullet('**두 로봇이 한 물체를 잡으면 왜 어려운가** — 폐연쇄가 되어 위치 오차가 그대로 내력으로 바뀐다. 그래스프 행렬의 null-space가 내력이고, 이 성분을 따로 다룬 것이 설계의 핵심이다')
bullet('**F/T 센서 없이 힘을 어떻게 다뤘나** — 내 RNEA 모델 토크가 외력 추정의 기준선이다. 모델 오차가 추정 오차로 어떻게 들어가는지 수치로 설명한다')
bullet('**왜 QP인가** — DLS와 같은 조건에서 비교한 결과(관절 한계 근처 추종 오차, 계산 시간)로 답한다')
bullet('**휴머노이드 상반신으로의 연결** — 네 팔 협동은 휴머노이드 양팔 + 허리 축의 다접촉 조작과 같은 구조다. 모바일 베이스를 floating base로 바꾸면 접촉력 QP 기반 WBC로 그대로 확장된다. 다음 학기 캡스톤에서 이 방향으로 확장할 계획')
bullet('**실패 사례 1개** — 원인·수치·해결을 반드시 준비한다 (예: 캘리브레이션 오차 때문에 체결 판단이 틀린 사례)')

# ---------------------------------------------------------------------
heading('8. 확인 필요')
bullet('1장 역할 변경(특히 하중 분배)에 대한 **김현대 동의**')
bullet('교수님 시뮬레이션 환경 전달 시점, 실로봇 2대 사용 가능 시간대')
bullet('FFW-SG2 관절 구성(허리·리프트 축 유무)과 모터 정격 — QP IK의 task 구성과 박스 중량이 여기에 달려 있다')
bullet('면담 자료 15쪽 "파지(F/T 센서에 따른 힘 제어)"는 4쪽 제약(F/T 미사용)과 맞지 않는다. 이 계획은 **전류 기반 추정**으로 통일했다')
bullet('중간고사 주간에 교수님 미팅이 있는지')

doc.save(OUT)
print('saved', OUT)

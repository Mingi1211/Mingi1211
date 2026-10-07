import sys
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = sys.argv[1]
FONT = '바탕체'
doc = Document()

st = doc.styles['Normal']
st.font.name = FONT
st.font.size = Pt(10)
rpr = st.element.get_or_add_rPr()
f = rpr.find(qn('w:rFonts'))
if f is None:
    f = OxmlElement('w:rFonts'); rpr.insert(0, f)
for k in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'):
    f.set(qn(k), FONT)
st.paragraph_format.space_after = Pt(2)
st.paragraph_format.line_spacing = 1.2
st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
sec.left_margin = sec.right_margin = Cm(2.2)
sec.top_margin = sec.bottom_margin = Cm(2.0)


def _run(p, text, bold=False, size=10):
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)
    r.font.name = FONT
    rf = r._element.get_or_add_rPr()
    ff = rf.find(qn('w:rFonts'))
    if ff is None:
        ff = OxmlElement('w:rFonts'); rf.insert(0, ff)
    for k in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'):
        ff.set(qn(k), FONT)
    return r


def _rich(p, text, size=10):
    for i, t in enumerate(text.split('**')):
        if t:
            _run(p, t, bold=(i % 2 == 1), size=size)


def title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_after = Pt(10)
    _run(p, text, bold=True, size=13)


def chap(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    _run(p, text, bold=True, size=11)


def sub(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    _run(p, text, bold=True, size=10)


def b(text):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Cm(0.45)
    pf.first_line_indent = Cm(-0.35)
    _rich(p, '- ' + text)


def eq(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(3)
    _run(p, text)


def cy(text):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Cm(0.45)
    pf.first_line_indent = Cm(-0.35)
    pf.space_before = Pt(2)
    _rich(p, '→ **실습에서**: ' + text)


# =====================================================================
title('Cyclo 실습 MR 개념 정리')

# ---------------------------------------------------------------- 3.2.3
chap('3.2.3 회전의 지수 좌표')
b('어떤 자세든 기준 자세에서 **단위축 ω̂ 둘레로 θ만큼 돌리면** 만들 수 있다. ω̂θ(3-벡터)를 **지수 좌표**라 하고, 회전행렬 대신 쓰는 3개짜리 자세 표현이다.')
b('"지수"인 이유: ω̂를 각속도로 보고 θ초 동안 적분하는 문제이기 때문. 스칼라 ẋ = ax의 해가 x(t) = e^{at}x(0)이듯, 벡터 ẋ = Ax의 해는 x(t) = e^{At}x(0) (**행렬 지수**).')
b('회전하는 벡터 p는 ṗ = ω̂ × p = [ω̂]p를 만족하므로 p(θ) = e^{[ω̂]θ}p(0). 3×3 반대칭 행렬에서는 급수가 닫힌 꼴이 된다(**Rodrigues 공식**).')
eq('Rot(ω̂, θ) = e^{[ω̂]θ} = I + sinθ [ω̂] + (1 − cosθ) [ω̂]²')
b('**exp**: 각속도 ω̂를 θ초 적분해 I에서 R로 간다(적분과 비슷). **log**: R을 만드는 단위 각속도와 시간을 돌려준다(미분과 비슷). log는 Rodrigues 공식을 거꾸로 푸는 알고리즘이다.')
b('회전 관절에서는 ω̂ = 관절축, θ = 관절각.')
cy('자세 보간 R(s) = R_start·exp(log(R_startᵀR_end)·s) (rotationCubic), 자세 오차 log(R_d Rᵀ) (computeDesiredVelocity).')

# ---------------------------------------------------------------- 5.1
chap('5.1 자코비안')
b('자코비안 J는 관절 속도를 말단 속도로 바꾼다: V = J(θ)θ̇. **i번째 열 = 관절 i만 속도 1, 나머지 0일 때의 말단 속도.** 관절 n개면 6×n.')
sub('5.1.1 공간 자코비안 J_s')
b('말단 속도를 공간 좌표계 {s}에서 본 twist V_s로 쓴다: V_s = J_s(θ)θ̇.')
b('관절 i의 열은 **관절 i와 {s} 사이에 있는 관절(1 ~ i−1)의 각도에만** 영향을 받는다. 그 뒤 관절이 움직여도 관절 i와 {s}의 관계는 그대로이기 때문.')
eq('J_s1 = S_1,    J_si = [Ad_{e^{[S_1]θ_1} ⋯ e^{[S_{i−1}]θ_{i−1}}}] S_i')
b('S_i는 영점 자세에서 {s}로 본 관절 i의 스크루 축. 미분이 필요 없고, 말단 좌표계 {b}를 어떻게 잡든 상관없다.')
sub('5.1.2 물체 자코비안 J_b')
b('말단 좌표계 {b}에서 본 twist V_b로 쓴다: V_b = J_b(θ)θ̇. B_i는 영점 자세에서 {b}로 본 관절 i의 스크루 축.')
b('관절 i의 열은 **관절 i와 {b} 사이 관절(i+1 ~ n)에만** 의존한다. 마지막 열 J_bn = B_n. {s}를 어떻게 잡든 상관없다.')
eq('J_bi = [Ad_{e^{−[B_n]θ_n} ⋯ e^{−[B_{i+1}]θ_{i+1}}}] B_i')
b('각 열이 twist이므로 좌표계를 바꾸는 규칙으로 서로 변환된다: J_b = [Ad_{T_bs}] J_s,  J_s = [Ad_{T_sb}] J_b.')
cy('Cyclo(Pinocchio)는 LOCAL_WORLD_ALIGNED — 말단 원점의 속도를 world 축으로 쓴다. 기준점은 {b}, 축은 {s}라서 J_s도 J_b도 아니다.')

# ---------------------------------------------------------------- 5.3
chap('5.3 특이점')
b('자코비안의 두 용도: 관절 속도 → 말단 twist (V = Jθ̇), 말단 렌치 → 관절 토크 (τ = JᵀF).')
b('J는 6×n이라 rank ≤ min(6, n). rank가 min(6, n)이면 **full rank**, 어떤 자세 θ*에서 rank가 최대값보다 작아지면 그 자세는 **특이(singular)**. 특이 자세에서는 **한 방향 이상으로 움직일 능력을 잃는다.**')
b('관절 수로 분류: n < 6 → J가 세로로 김, **운동학적으로 부족**(말단이 임의의 6차원 운동 불가) / n = 6 → 정방, 범용 매니퓰레이터 / n > 6 → J가 가로로 김, **여유(redundant)**. 같은 말단 twist를 다른 관절 속도로 낼 수 있어 말단에 보이지 않는 **내부 운동**이 가능 (손을 고정한 채 팔꿈치를 움직이는 것).')
b('역문제 "v_tip이 주어지면 θ̇는?"는 J가 정방이 아니거나 특이라 역행렬이 없어 쉽지 않다. 여유 로봇은 해가 무수히 많다 → 6장.')
b('평면 3R 팔을 쭉 펴면 rank 2 → 1: 모든 관절이 끝을 수직으로만 움직이고 **수평 속도는 불가**. 대신 수평 힘은 관절 토크 없이 **구조가 수동적으로** 버틴다.')
cy('AI Worker 팔은 7관절이라 6×7(여유 1자유도). C5에서 팔을 끝까지 뻗은 자세가 작업공간 경계 특이점이고, Cyclo는 감쇠 항으로 관절 속도 폭주를 막았다.')

# ---------------------------------------------------------------- 6.2
chap('6.2 수치 역기구학 (+ 6.3 역속도 기구학)')
b('역기구학 = x_d − f(θ_d) = 0을 만족하는 θ_d 찾기 → 근 찾기 문제 → **Newton–Raphson**.')
b('1차원 그림: 현재 추정 θ_0에서 기울기(접선)를 그어 θ축과 만나는 점을 다음 추정 θ_1로 삼고 반복. 함수가 선형이면 한 번에 정확. 해가 여러 개면 **초기값 근처의 해**로 수렴하고, 기울기가 작은 평평한 곳 근처에서 시작하면 멀리 튀어 수렴이 어렵다 → 초기값이 해와 가까워야 한다.')
b('벡터로 일반화: 테일러 1차 근사로 x_d − f(θ_i) = J(θ_i)Δθ → Δθ = J⁻¹(x_d − f(θ_i)). J가 정방이 아니거나 특이하면 **의사역행렬 J†**를 쓴다.')
b('J†의 성질: 해가 여러 개면(여유 로봇) **길이가 가장 짧은 Δθ**, 정확한 해가 없으면(특이점, 관절 부족) **오차가 가장 작은 Δθ**를 준다.')
eq('θ_{i+1} = θ_i + J†(θ_i) e,    e = x_d − f(θ_i),    e가 충분히 작으면 종료')
b('제어기 안에서 쓸 때: 매 시간 갱신된 x_d에 대해 풀고, **직전 해를 초기 추정**으로 쓴다(목표가 조금씩만 바뀌므로).')
b('목표가 변환행렬 T_sd일 때: 오차 e를 **"단위 시간 동안 따라가면 목표에 도착하는 twist"**로 바꾼다. T_bd = T_sb⁻¹T_sd, [V_b] = log(T_bd).')
eq('θ_{i+1} = θ_i + J_b†(θ_i) V_b,    ω_b와 v_b가 충분히 작으면 종료')
b('**역속도 기구학**: 원하는 twist V_d를 내는 관절 속도 θ̇ = J†V_d (J와 V_d는 같은 좌표계). n > 6이면 θ̇ 성분 제곱합이 최소, n < 6이면 twist 오차 제곱합이 최소인 해. 다른 양을 최소화하는 역행렬(가중)도 있다.')
cy('Cyclo는 Newton–Raphson을 수렴할 때까지 돌리지 않고, **매 10 ms 역속도 기구학을 QP(가중치 + 감쇠 + 제약)로 한 번 풀고 적분**한다. kp·Δt = 50 × 0.01 = 0.5라서 "한 주기에 오차를 절반 줄이는 NR 한 걸음"과 비슷하다.')

# ---------------------------------------------------------------- 8.3
chap('8.3 뉴턴–오일러 역동역학 (RNEA)')
b('**입력** 관절 위치·속도·가속도 θ, θ̇, θ̈와 말단이 환경에 가하는 렌치 F_tip → **출력** 필요한 관절 토크 τ.')
b('링크 i의 질량중심에 좌표계 {i}, 말단 {n+1}, 월드 {0}. V_i = 링크 i의 twist ({i} 기준), A_i = {i}에서 본 관절 i의 스크루 축, M_{i,i−1} = 관절 i가 0일 때 {i}에서 본 {i−1}.')
b('**중력**: 베이스 가속도 V̇_0를 중력 반대 방향의 선가속도로 둔다. 중력은 위로 가속하는 것과 구별할 수 없기 때문.')
sub('앞으로 (링크 1 → n): 각 링크의 위치·속도·가속도')
eq('T_{i,i−1} = e^{−[A_i]θ_i} M_{i,i−1}')
eq('V_i = [Ad_{T_{i,i−1}}] V_{i−1} + A_i θ̇_i')
eq('V̇_i = [Ad_{T_{i,i−1}}] V̇_{i−1} + [ad_{V_i}] A_i θ̇_i + A_i θ̈_i')
b('앞 링크의 속도를 내 좌표계로 옮기고, 내 관절이 더하는 속도를 합친다. 가속도에는 속도끼리 곱한 항이 붙는다.')
sub('뒤로 (링크 n → 1): 각 관절이 내야 할 힘·토크')
eq('F_{n+1} = F_tip,    F_i = [Ad_{T_{i+1,i}}]ᵀ F_{i+1} + G_i V̇_i − [ad_{V_i}]ᵀ (G_i V_i)')
eq('τ_i = F_iᵀ A_i')
b('다음 링크가 필요한 렌치를 내 좌표계로 옮기고, 내 링크를 가속하는 데 필요한 렌치(강체 역동역학)를 더한다. 그중 **관절 축 방향 성분만 모터가** 내고, 나머지는 베어링 같은 구조가 버틴다.')
b('장점: 미분이 필요 없고, 재귀라서 계산이 효율적이다.')
cy('C2의 qfrc_bias = MuJoCo가 이 계산을 θ̈ = 0으로 돌린 값 = c(θ, θ̇) + g(θ). 이걸 팔 관절에 더해 중력을 상쇄했다.')

# ---------------------------------------------------------------- 9.1–9.2
chap('9.1 – 9.2 점대점 궤적')
b('**궤적** θ(t), t ∈ [0, T] = **경로** θ(s), s ∈ [0, 1] + **시간 스케일링** s(t). 경로는 어디로 갈지, 시간 스케일링은 얼마나 빨리 갈지.')
eq('θ̇ = (dθ/ds) ṡ,    θ̈ = (dθ/ds) s̈ + (d²θ/ds²) ṡ²')
b('동역학이 θ̈에 의존하므로 θ(s)와 s(t) 모두 **2번 미분 가능**해야 한다.')
sub('경로')
b('**관절 공간 직선** θ(s) = θ_start + s(θ_end − θ_start): 말단은 직선으로 움직이지 않는다. 관절 한계가 서로 독립이면 가능한 관절 영역이 볼록이라 직선이 항상 그 안에 있다.')
b('**작업 공간 직선**: 점마다 역기구학이 필요하고, 직선이 작업 공간 밖을 지나면 실행할 수 없다.')
b('**SE(3)에서 두 자세 사이**: 원소끼리 빼는 건 의미가 없다. 일정한 twist를 따라가는 **스크루 경로** X(s) = X_start exp(log(X_start⁻¹X_end) s). twist가 {start} 기준이라 exp를 오른쪽에 곱한다.')
b('**위치·자세 분리 경로**: 원점은 직선 p(s) = p_start + s(p_end − p_start), 자세는 R(s) = R_start exp(log(R_startᵀR_end) s).')
sub('시간 스케일링')
b('**3차 다항식**: 조건 4개 s(0) = 0, s(T) = 1, ṡ(0) = ṡ(T) = 0.')
eq('s(t) = 3(t/T)² − 2(t/T)³')
b('ṡ는 시작·끝에서 0이지만 **s̈는 t = 0에서 6/T²로 불연속** 점프한다.')
b('**5차 다항식**: 계수 2개가 늘어 s̈(0) = s̈(T) = 0 조건까지 맞춘다 → 시작·끝 가속도 0, 더 부드럽다.')
b('**사다리꼴**: 등가속 → 등속 → 등감속. 3차처럼 가속도가 불연속. **S-curve**: 7구간(일정 jerk 포함), 시작·끝 가속도 0.')
cy('Cyclo MoveL은 **위치·자세 분리 경로 + 3차 스케일링**이다. 5차 함수는 Cyclo에 없다.')

# ---------------------------------------------------------------- 11.3
chap('11.3 속도 입력 운동 제어')
b('관절 **속도를 직접 명령**할 수 있다고 가정한다. 하위 제어기가 요청한 속도를 잘 낸다고 믿을 수 있을 때, 바퀴 로봇처럼 상위가 속도만 명령할 때 쓴다.')
b('**개루프(앞먹임)**: θ̇ = θ̇_d. 위치를 재지 않으므로 오차가 생기면 회복하지 못한다.')
b('**P 제어**: θ̇ = K_p θ_e (K_p > 0). 설정점 제어면 θ̇_e = −K_p θ_e → 시정수 1/K_p, K_p가 클수록 빠르다. 너무 크면 진동하고, 액추에이터 속도 한계에 걸려 선형 모델이 깨진다.')
b('일정 속도 c로 움직이는 목표를 P로 쫓으면 **정상상태 오차 c/K_p**가 남는다. P 제어는 움직이려면 오차가 있어야 하기 때문.')
b('**PI 제어**: θ̇ = K_p θ_e + K_i ∫θ_e. 오차 동역학 θ̈_e + K_p θ̇_e + K_i θ_e = 0 (2차, ζ = K_p / 2√K_i, ω_n = √K_i). 등속 궤적에서도 정상상태 오차 0. **임계 감쇠**(K_i = K_p²/4)가 빠르고 오버슈트가 없어 좋다.')
b('오차가 쌓일 때까지 기다리지 않도록 앞먹임을 더한 것이 **최종 형태**. 다관절이면 벡터, 게인은 양수 × 단위행렬.')
eq('θ̇ = θ̇_d + K_p θ_e + K_i ∫θ_e dt')
sub('11.3.3 작업 공간 운동 제어')
b('목표가 말단 자세 X_d(t)로 주어질 때. 목표 twist [V_d] = X_d⁻¹Ẋ_d ({d} 기준), 실제 twist V_b ({b} 기준).')
eq('V_b = [Ad_{X⁻¹X_d}] V_d + K_p X_e + K_i ∫X_e dt,    [X_e] = log(X⁻¹X_d)')
b('앞먹임: V_d를 **지금 말단 좌표계로 옮겨** 쓴다(X⁻¹X_d = 지금 말단에서 본 목표 자세). 오차 X_e: 빼기 대신 **지금 → 목표로 단위 시간에 가는 twist**. 관절 속도는 θ̇ = J_b† V_b.')
b('**분리형**: 자세 R과 위치 p를 따로. 각속도 앞먹임은 Rᵀ R_d ω_d (지금 말단 기준으로 돌림), 선속도 앞먹임은 그냥 ṗ_d. 오차 X_e = (log(RᵀR_d), p_d − p).')
b('정지한 목표로 갈 때(앞먹임 0, K_i = 0) 결합형은 **일정한 스크루 축을 따라** 움직이고, 분리형은 **원점이 직선**으로 간다.')
cy('Cyclo computeDesiredVelocity는 분리형(K_i = 0, K_p = 50)이고, 자세 오차를 world 기준 log(R_d Rᵀ)로 쓴다.')

# ---------------------------------------------------------------- 11.4
chap('11.4 토크·힘 입력 운동 제어')
b('관절 **토크를 명령**하므로 동역학을 고려해야 한다. 1관절 로봇: τ = Mθ̈ + mgr cosθ + bθ̇ = Mθ̈ + h(θ, θ̇).')
b('**PID**: τ = K_p θ_e + K_i ∫θ_e + K_d θ̇_e. 속도는 보통 엔코더 위치를 수치 미분해 얻는다. K_i = 0이면 **PD**.')
sub('중력이 없을 때 PD')
b('설정점 제어 오차 동역학: Mθ̈_e + (b + K_d)θ̇_e + K_p θ_e = 0. ζ = (b + K_d) / 2√(K_p M), ω_n = √(K_p / M). K_d는 점성 마찰 b와 같은 역할(가상 댐퍼).')
b('K_d > −b, K_p > 0이면 안정, 정상상태 오차 0. 임계 감쇠로 고르고, 게인이 너무 크면 채터링·진동, 실제로는 불안정해질 수도 있다(모델링 안 된 동역학, 이산 시간 구현 등).')
sub('중력이 있을 때')
b('PD만 쓰면 정지 상태에서 **정상상태 오차 = mgr cosθ / K_p**. 중력을 버틸 토크를 비례항이 내야 하는데, 그러려면 오차가 있어야 하기 때문.')
b('**PID**: 적분항이 정상상태에서 중력을 버티는 토크를 내므로 오차 0. 대신 오차 동역학이 3차가 되고 **K_i에 상한**이 생긴다(너무 크면 불안정). 과도응답이 나빠질 수 있어(오버슈트·진동) 로봇에서는 K_i를 0이나 작게 두고 적분값에 상한을 건다.')
sub('모델을 쓰는 제어')
b('**앞먹임만**: τ = M̃ θ̈_d + h̃(θ_d, θ̇_d). 모델이 완벽하지 않으면 오차를 회복하지 못한다.')
b('**Computed torque**: 앞먹임 가속도 + PID 가속도에 모델 M̃를 곱하고, 중력·마찰 h̃를 더한다.')
eq('τ = M̃(θ) (θ̈_d + K_p θ_e + K_i ∫θ_e + K_d θ̇_e) + h̃(θ, θ̇)')
b('모델이 정확하면 동역학이 선형화돼 **임의 궤적에서도** 오차 동역학이 안정·선형이 된다. PID만 쓸 때보다 추종이 좋고 제어 노력(토크 제곱 적분)도 적다. 모델이 나쁘면 오히려 손해, 실시간 계산 부담도 있다.')
b('**간단판: PD + 중력 보상** — 전체 동역학 대신 중력 토크 g̃(θ)만 계산해 더한다. 계산이 훨씬 가볍다.')
b('다관절: θ, τ가 벡터, M̃은 질량행렬, h̃는 코리올리·중력(·마찰). 작업 공간 버전은 F_b = Λ̃(V̇_d + K_p X_e + K_i ∫X_e + K_d V_e) + η̃를 구해 **τ = J_bᵀ F_b**로 관절 토크를 얻는다.')
cy('C1 = 위치 제어만(중력 미보상) → 처짐 = g/K_p만큼 오차. C2 = **PD + 중력 보상**(qfrc_bias) → 오차 0. 다음 단계는 computed torque와 임피던스(현대 파트).')

doc.save(OUT)
print('saved', OUT)

import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, '..', 'plan', 'build_manual.py'), encoding='utf-8').read()
exec(_src.split('# =====')[0])          # 바탕체 10pt, 세로 A4, bullet()/table()/code()


def eq(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    run(p, text, size=10.5)


def ch(title, url):
    heading(title)
    para('영상: ' + url, size=8.5, after=3)


t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
run(t, 'Modern Robotics 강의 요약 — Ch 2.1 ~ 2.5', bold=True, size=14)
para('Kevin Lynch (Northwestern) "Modern Robotics" 재생목록, 영어 자막 기준 정리', size=9, align=WD_ALIGN_PARAGRAPH.CENTER, after=8)

# ---------------------------------------------------------------- 2.1
ch('2.1 강체의 자유도 (Degrees of Freedom of a Rigid Body)', 'https://youtu.be/z29hYlagOYM')
bullet('**형상(configuration)**: 로봇의 모든 점의 위치를 나타낸 것. "로봇이 어디 있나"에 대한 답')
bullet('**형상 공간(C-space)**: 가능한 모든 형상의 공간')
bullet('**자유도(dof)**: C-space의 차원 = 형상을 나타내는 데 필요한 최소 실수 개수')
bullet('로봇은 강체(link)를 관절(joint)로 연결한 것. 링크는 모양이 변하지 않아 숫자 몇 개로 형상을 나타낼 수 있음 (소프트 로봇은 다루지 않음)')
bullet('예: 2관절 로봇 → 각 관절각이 원 위의 한 점 → C-space = **토러스(torus)** 표면, dof = 2')
para('**강체의 자유도 세기 (3차원)**', after=2)
table([2.2, 1.8, 6.4, USABLE - 10.4], ['점', '좌표 수', '제약 수', '실제 자유'], [
    ['A', '3', '0', '3 (x, y, z 아무렇게나)'],
    ['B', '3', '1 (A와의 거리 일정 → A 중심 구면 위)', '2 (위도·경도)'],
    ['C', '3', '2 (A, B 중심 구의 교선 = 원 위)', '1'],
    ['나머지 점', '3', '3', '0 (A, B, C가 한 직선 위가 아니면 고정됨)'],
], first_bold=True, center_cols=(1,))
bullet('공간 강체 dof = 3 + 2 + 1 = **6** (선형 x, y, z 3개 + 각도 roll, pitch, yaw 3개)')
bullet('평면 강체 dof = **3** (선형 2 + 각도 1). 참고: 4차원 공간 강체는 10 (선형 4 + 각도 6)')
para('**일반 규칙 (강체가 아니어도 성립)**', after=2)
eq('dof = (점들의 자유의 합) − (독립 제약의 수)  =  (강체들의 자유의 합) − (강체에 걸린 독립 제약의 수)')
bullet('예: 공간 강체(6)에 "A, B, C의 z좌표 = 0" 제약 3개를 걸면 평면 강체(3)')

# ---------------------------------------------------------------- 2.2
ch('2.2 로봇의 자유도 (Degrees of Freedom of a Robot)', 'https://youtu.be/zI64DyaRUvQ')
bullet('dof = 강체들의 자유의 합 − 제약의 수. 제약은 주로 **관절**에서 옴')
table([3.4, 2.0, 3.2, USABLE - 8.6], ['관절', '자유 f', '제약 c (평면 / 공간)', '비고'], [
    ['회전 R (revolute)', '1', '2 / 5', '가장 흔함. 관절각 하나'],
    ['직동 P (prismatic, linear)', '1', '2 / 5', ''],
    ['나선 H (helical)', '1', '— / 5', '회전과 이동이 연동'],
    ['원통 C (cylindrical)', '2', '— / 4', ''],
    ['유니버설 U (universal)', '2', '— / 4', ''],
    ['구면 S (spherical, ball-and-socket)', '3', '— / 3', 'U의 2 + 축 회전 1'],
], first_bold=True, center_cols=(1, 2))
para('**Grübler 공식**', after=2)
bullet('N: 링크 수 (**지면 포함**), J: 관절 수, m: 강체 하나의 dof (평면 3, 공간 6), f_i: 관절 i의 자유, c_i = m − f_i')
eq('dof = m(N − 1) − Σ c_i  =  m(N − 1 − J) + Σ f_i')
bullet('전제: **관절 제약들이 서로 독립**')
table([4.0, 4.6, USABLE - 8.6], ['예', '계산', '결과'], [
    ['3R 직렬(open-chain) 로봇, 평면', 'm=3, N=4, J=3 → 3(4−1−3) + 3', '3'],
    ['4절 링크(four-bar), 평면 폐연쇄', 'm=3, N=4, J=4 → 3(4−1−4) + 4', '1 (3R 끝을 고정 = 제약 2개 → 3 − 2 = 1)'],
    ['4절 + 링크 1개·관절 2개', '공식은 0', '실제 1 → 제약이 독립이 아니라 공식이 틀림'],
    ['Stewart 플랫폼, 공간', '다리 6개 × (링크 2, U·P·S 관절) → N=14, J=18, Σf=36 → 6(14−1−18) + 36', '6 (윗판이 강체 6자유도로 움직임)'],
], first_bold=True)
bullet('직렬(open-chain): 지면에서 끝까지 경로가 하나 / 폐연쇄(closed-chain): 고리가 있음')
bullet('관절 운동 범위 제한은 dof를 줄이지 않음')
bullet('제약이 독립인지 판정하는 것은 쉽지 않음 (강의에서 다루지 않음)')

# ---------------------------------------------------------------- 2.3.1
ch('2.3.1 C-space의 위상 (Configuration Space Topology)', 'https://youtu.be/FyLNR3edOds')
bullet('dof(차원)가 같아도 **모양(위상, topology)**이 다를 수 있음. 예: 평면과 구면은 둘 다 2차원이지만 구면은 휘어 돌아옴')
bullet('**위상 동치**: 자르거나 붙이지 않고 매끄럽게 변형해 같아지면 같은 위상. 예: 토러스 ≅ 머그컵, 둘 다 평면과는 다름(자르기 필요)')
bullet('위상은 공간 고유의 성질이라 **좌표 선택과 무관**')
bullet('1차원 위상 예: 원, 직선, 닫힌 구간 / 2차원: 평면, 구면, 토러스, 원통')
table([3.6, 3.2, USABLE - 6.8], ['시스템 (C-space 2차원)', '위상', '좌표 표현'], [
    ['평면 위의 점', '평면 E²', '실수 2개 (x, y)'],
    ['구면 진자', '구면 S²', '위도, 경도'],
    ['2R 로봇', '토러스 T² = S¹ × S¹', '각도 2개, 각 [0, 2π)'],
    ['회전 + 미끄러지는 손잡이', '원통 E¹ × S¹', '거리 1개 + 각도 1개'],
], first_bold=True)
bullet('좌표 표현은 공간을 **잘라서** 평면 조각으로 만든 것 → 위상이 달라짐 → 경계에서 불연속')
bullet('2R: 토러스를 두 번 잘라 정사각형 [0, 2π)² → 로봇은 매끄럽게 움직여도 좌표는 0 ↔ 2π에서 **튐**')
bullet('손잡이: 원통을 한 번 잘라 평면 띠 → 각도만 0 ↔ 2π에서 튐')
bullet('구면 진자: 좌표 사각형의 윗변 전체 = 북극 한 점, 아랫변 전체 = 남극 한 점')

# ---------------------------------------------------------------- 2.3.2
ch('2.3.2 C-space의 표현 (Configuration Space Representation)', 'https://youtu.be/PPgJPjCUIXU')
bullet('좌표 표현은 원점·축 같은 **임의 선택**. 표현을 바꿔도 공간(위상)은 그대로')
bullet('평평한 공간(직선, 평면, n차원 유클리드): 원점 + 축 → 좌표. 속도 = 좌표의 시간 미분')
table([3.2, 5.0, USABLE - 8.2], ['', '명시적 매개변수화 (explicit)', '암시적 표현 (implicit)'], [
    ['방법', '최소 개수 좌표 (구면: 위도·경도)', '더 높은 차원에 묻고 좌표 + 제약 (구면: x, y, z + 반지름 일정 제약 1개 → 3 − 1 = 2차원)'],
    ['장점', '좌표 수 최소, 단순', '특이점·불연속 없음'],
    ['단점', '위상이 유클리드와 달라 어딘가에서 나쁜 동작: **특이점**(북극 근처 일정 속도로 걸어도 경도가 무한히 빨리 변함), 북극을 넘는 순간 경도 180° 점프', '표현이 조금 더 복잡'],
], first_bold=True)
bullet('이 특이점은 **표현의 문제**이지 구면 자체의 문제가 아님 (구면은 어디서나 똑같이 생김)')
bullet('MR 책은 암시적 표현을 씀. 특히 강체 자세(휘어진 비유클리드 공간)는 **회전행렬**(특이점 없는 암시적 표현)로')
bullet('정리: 형상을 최소 좌표로 나타내지 않는 경우가 많고, 속도도 좌표의 시간 미분으로 나타내지 않는 경우가 많음')

# ---------------------------------------------------------------- 2.4
ch('2.4 형상 제약과 속도 제약 (Configuration and Velocity Constraints)', 'https://youtu.be/A14ArEZ47LE')
bullet('폐연쇄 로봇은 명시적 매개변수화보다 **암시적 표현**이 쉬움 (직접 유도가 어렵고 숨은 특이점이 있을 수 있음)')
bullet('4절 링크: dof = 1이지만, 관절각 4개 공간에 **고리 닫힘 방정식 3개**(한 바퀴 돌아오면 위치·자세가 처음과 같아야 함)로 묶인 1차원 공간으로 봄')
eq('g(θ) = 0,   θ ∈ ℝⁿ,   g: k개 식')
bullet('**홀로노믹(holonomic) 제약**: C-space의 차원을 줄이는 제약. 변수 n개, 독립 홀로노믹 제약 k개 → dof = n − k')
bullet('g(θ)가 항상 0이면 시간 미분도 0 → **속도 제약**')
eq('A(θ) θ̇ = 0,   A: k × n      ← Pfaffian 제약')
bullet('홀로노믹 제약 = 적분 가능한(integrable) 제약 (속도 제약을 적분하면 형상 제약이 됨)')
bullet('**비홀로노믹(nonholonomic) 제약**: 속도 제약이지만 형상 제약으로 적분이 안 되는 것')
para('**예: 평면 위 자동차 차체**  q = (φ, x, y), φ: 차체 각도, (x, y): 뒷바퀴 사이 중점', after=2)
eq('ẋ = v cos φ,   ẏ = v sin φ   →   ẋ sin φ − ẏ cos φ = 0')
eq('A(q) q̇ = 0,   A(q) = [ 0   sin φ   −cos φ ]   (1 × 3)')
bullet('옆으로 미끄러질 수 없음 → **가능한 속도**는 줄지만 **도달 가능한 형상**은 안 줄어듦 (평행 주차로 옆 이동 가능, 3차원 C-space 어디든 도달)')
bullet('한 로봇에 둘 다 있을 수 있음: 차체를 공간 강체로 보면 평면에 묶는 홀로노믹 제약 3개 + 옆미끄럼 금지 비홀로노믹 1개')
bullet('Pfaffian 제약이 홀로노믹인지 비홀로노믹인지 판정은 13장에서')

# ---------------------------------------------------------------- 2.5
ch('2.5 작업 공간과 워크스페이스 (Task Space and Workspace)', 'https://youtu.be/hTuW51CpUg4')
bullet('**C-space**: 로봇의 모든 가능한 형상')
bullet('**작업 공간(task space)**: 로봇의 작업을 자연스럽게 나타내는 공간. **작업만 알면 정해짐, 로봇과 무관**')
bullet('　예: 보드 위 마커 끝 위치 제어 → 유클리드 평면 / 강체 위치·자세 제어 → 6차원 강체 형상 공간')
bullet('**워크스페이스(workspace)**: 로봇 말단(end-effector)이 도달할 수 있는 형상들. **특정 작업과 무관, 로봇이 정함**')
bullet('　예: 관절 범위 180°, 150°로 제한된 평면 2R 로봇의 도달 영역')
bullet('보통 말단이 닿는 직교좌표 점들로 정의하지만 자세를 포함할 수도 있음')
bullet('**dexterous workspace**: 모든 자세로 도달할 수 있는 위치들의 집합')

doc.save(OUT)
print('saved', OUT)

#!/usr/bin/env python3
"""Gazebo용 설정 패치 (원본은 .orig로 백업, --restore로 원상 복구)

1) ffw_sg2_follower.ros2_control.xacro : 팔 14축에 effort 명령 인터페이스 추가 (use_sim일 때만 → 실물 bringup 영향 없음)
2) ffw_sg2_follower_ai_hardware_controller.yaml : effort 컨트롤러 2개 + 그리퍼 위치 컨트롤러 2개 추가 (기본은 비활성)

사용: python3 setup_sim.py [--ws ~/ros2_ws/src/ai_worker] [--restore]
그다음: cd ~/ros2_ws && colcon build --symlink-install --packages-select ffw_description ffw_bringup
"""
import argparse
import os
import re
import shutil

ap = argparse.ArgumentParser()
ap.add_argument('--ws', default=os.path.expanduser('~/ros2_ws/src/ai_worker'))
ap.add_argument('--restore', action='store_true')
a = ap.parse_args()

XACRO = os.path.join(a.ws, 'ffw_description/ros2_control/ffw_sg2_rev1_follower/ffw_sg2_follower.ros2_control.xacro')
YAML = os.path.join(a.ws, 'ffw_bringup/config/ffw_sg2_rev1_follower/ffw_sg2_follower_ai_hardware_controller.yaml')

for f in (XACRO, YAML):
    if not os.path.exists(f):
        raise SystemExit(f'파일 없음: {f}  (--ws 경로 확인)')
    if a.restore:
        if os.path.exists(f + '.orig'):
            shutil.copy(f + '.orig', f)
            print('복구:', f)
        continue
    if not os.path.exists(f + '.orig'):
        shutil.copy(f, f + '.orig')
        print('백업:', f + '.orig')
if a.restore:
    raise SystemExit(0)

# 1) xacro
s = open(XACRO, encoding='utf-8').read()
if 'MINGI_EFFORT' not in s:
    pat = re.compile(r'(<joint name="arm_[rl]_joint[1-7]">\s*\n(\s*)<command_interface name="position"/>)')
    s, n = pat.subn(r'\1\n\2<xacro:if value="$(arg use_sim)"><command_interface name="effort"/></xacro:if><!-- MINGI_EFFORT -->', s)
    open(XACRO, 'w', encoding='utf-8').write(s)
    print(f'xacro: effort 인터페이스 {n}개 추가 (14개여야 정상)')
else:
    print('xacro: 이미 패치됨')

# 2) controller yaml — 파일이 이미 "/**:" 블록을 여러 번 쓰는 형식이라 같은 형식으로 뒤에 붙인다
y = open(YAML, encoding='utf-8').read()
if 'MINGI_EFFORT' not in y:
    arm = lambda s_: '\n'.join(f'        - arm_{s_}_joint{i}' for i in range(1, 8))  # noqa: E731
    y += f'''
# ===== MINGI_EFFORT: 2번 하위 제어용 (기본 비활성, sim_effort_on.sh로 전환) =====
/**:
  controller_manager:
    ros__parameters:
      arm_r_effort_controller:
        type: forward_command_controller/ForwardCommandController
      arm_l_effort_controller:
        type: forward_command_controller/ForwardCommandController
      gripper_r_position_controller:
        type: forward_command_controller/ForwardCommandController
      gripper_l_position_controller:
        type: forward_command_controller/ForwardCommandController

/**:
  arm_r_effort_controller:
    ros__parameters:
      joints:
{arm('r')}
      interface_name: effort

/**:
  arm_l_effort_controller:
    ros__parameters:
      joints:
{arm('l')}
      interface_name: effort

/**:
  gripper_r_position_controller:
    ros__parameters:
      joints: [gripper_r_joint1]
      interface_name: position

/**:
  gripper_l_position_controller:
    ros__parameters:
      joints: [gripper_l_joint1]
      interface_name: position
'''
    open(YAML, 'w', encoding='utf-8').write(y)
    print('yaml: 컨트롤러 4개 추가')
else:
    print('yaml: 이미 패치됨')
print('다음: cd ~/ros2_ws && colcon build --symlink-install --packages-select ffw_description ffw_bringup')

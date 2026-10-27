#!/usr/bin/env bash
# 사용: source tools.sh  → 아래 함수들 사용
#   effort_on r|l|both   위치 컨트롤러 끄고 effort 컨트롤러 켬 (켜기 전에 impedance_node를 먼저 실행해 둘 것)
#   effort_off r|l|both  원래 위치 컨트롤러로 복귀
#   goal r x y z [T]     손 목표 전송 (base_link, 자세는 현재 유지하려면 qw=1 대신 현재값 — 일단 단위 쿼터니언)
#   imp_run              impedance_node 실행 (params.yaml)
#   imp_mode gravity|spring|task   실행 중 모드 변경
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

_spawn_once() {  # 컨트롤러가 없으면 inactive로 로드
  ros2 control list_controllers | grep -q "^$1 " || ros2 run controller_manager spawner "$1" --inactive
}
effort_on() {
  for s in $( [ "$1" = both ] && echo r l || echo "$1" ); do
    _spawn_once arm_${s}_effort_controller; _spawn_once gripper_${s}_position_controller
    ros2 control switch_controllers --deactivate arm_${s}_controller \
      --activate arm_${s}_effort_controller gripper_${s}_position_controller
  done
  ros2 control list_controllers
}
effort_off() {
  for s in $( [ "$1" = both ] && echo r l || echo "$1" ); do
    ros2 control switch_controllers --deactivate arm_${s}_effort_controller gripper_${s}_position_controller \
      --activate arm_${s}_controller
  done
  ros2 control list_controllers
}
goal() {
  ros2 topic pub --once /impedance/$1/goal geometry_msgs/msg/PoseStamped \
    "{header: {frame_id: base_link}, pose: {position: {x: $2, y: $3, z: $4}, orientation: {w: 1.0}}}"
  [ -n "$5" ] && ros2 param set /impedance_controller duration "$5"
}
imp_run()  { python3 "$HERE/impedance_node.py" --ros-args --params-file "$HERE/params.yaml"; }
imp_mode() { ros2 param set /impedance_controller mode "$1"; }

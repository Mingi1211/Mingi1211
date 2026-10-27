#!/usr/bin/env python3
"""/robot_description을 받아 팔 관절·프레임·질량을 출력 (ee_frame 이름 확인용). Gazebo 실행 중에 사용."""
import pinocchio as pin
import rclpy
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy
from std_msgs.msg import String


class L(Node):
    def __init__(self):
        super().__init__('list_frames')
        qos = QoSProfile(depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL, reliability=ReliabilityPolicy.RELIABLE)
        self.create_subscription(String, '/robot_description', self.cb, qos)

    def cb(self, msg):
        m = pin.buildModelFromXML(msg.data)
        print(f'nq={m.nq} nv={m.nv} 총질량={sum(i.mass for i in m.inertias):.2f} kg')
        for j in range(1, m.njoints):
            n = m.names[j]
            if 'arm' in n or 'lift' in n:
                print(f'  joint {n:20s} idx_v={m.joints[j].idx_v} 링크질량={m.inertias[j].mass:.3f}')
        for f in m.frames:
            if 'end_effector' in f.name or 'link7' in f.name:
                print('  frame', f.name)
        raise SystemExit


rclpy.init()
rclpy.spin(L())

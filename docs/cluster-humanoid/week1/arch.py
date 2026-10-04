import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams['font.family']=['Malgun Gothic','DejaVu Sans']; plt.rcParams['axes.unicode_minus']=False
fig,ax=plt.subplots(figsize=(10,6.2)); ax.set_xlim(0,100); ax.set_ylim(0,62); ax.axis('off')
def box(x,y,w,h,title,body,fc):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.4',fc=fc,ec='#333',lw=1))
    ax.text(x+w/2,y+h-1.6,title,ha='center',va='top',fontsize=9.5,weight='bold')
    ax.text(x+w/2,y+h-5.0,body,ha='center',va='top',fontsize=7.8,linespacing=1.4)
def arrow(x1,y1,x2,y2,label='',lx=None,ly=None):
    ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle='->',lw=1.3,color='#333'))
    if label: ax.text(lx if lx is not None else (x1+x2)/2+0.8, ly if ly is not None else (y1+y2)/2,label,fontsize=8,color='#444',va='center')
box(2,48,28,11,'① 명령 (토픽)','/r_goal_move\nrobotis_interfaces/MoveL\n= 목표 자세 + 시간 T','#E8F0FE')
box(36,44,30,15,'② ROS 노드 (cyclo_motion_controller_ros)','ai_worker_movel_controller_node.cpp\n3차 보간: cubicVector, rotationCubic\n→ 기준 자세 x_ref(t), 속도 v_ff\nv_d = v_ff + kp·e  (kp = 50)','#FEF7E0')
box(70,44,28,15,'③ KinematicsSolver','kinematics_solver.cpp (Pinocchio)\nFK, 자코비안\n(LOCAL_WORLD_ALIGNED)\n자기충돌 거리 (SRDF)','#E6F4EA')
box(36,20,30,19,'④ QP (cyclo_motion_controller_core)','vr_controller.cpp ← qp_base.hpp (OSQP)\n결정변수: qdot + slack s\n비용: |J·qdot - v_d|²_W + w_d|qdot|² + ρΣs\n제약: qdot_min ≤ qdot ≤ qdot_max\n관절 한계 CBF: qdot ≥ -α(q - q_min)\n자기충돌 CBF: d_dot ≥ -α(d - d_safe)','#FCE8E6')
box(2,20,25,15,'⑤ 관절 명령 생성','q_d = q_측정 + qdot·Δt\n(Δt = 0.01 s, 100 Hz)\nJointTrajectory 발행','#F3E8FD')
box(2,2,44,12,'⑥ 출력 → follower','/leader/joint_trajectory_command_broadcaster_right\n/joint_trajectory  →  arm_r_controller (JTC, 100 Hz)\n→ DYNAMIXEL 위치 제어','#EEEEEE')
box(54,2,44,12,'⑦ 상태 피드백','/joint_states (joint_state_broadcaster)\n→ 측정 q가 ②③④⑤로 다시 들어감\n(joint_state_timeout 넘으면 정지·유지)','#EEEEEE')
arrow(30,53.5,36,53.5)
arrow(51,44,51,39.6,'v_d')
arrow(84,44,66.6,33,'J, d',lx=72,ly=36)
arrow(35.6,29,27.6,29,'qdot',lx=29.3,ly=31)
arrow(16,20,16,14.5)
arrow(90,14.5,90,43.4,'q')
fig.savefig('cyclo_arch.png',dpi=170,bbox_inches='tight'); print('ok')

import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams['font.family']=['Malgun Gothic','DejaVu Sans']
fig,ax=plt.subplots(figsize=(10,3.6)); ax.set_xlim(0,100); ax.set_ylim(0,36); ax.axis('off')
def box(x,y,w,h,t,b,fc):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.4',fc=fc,ec='#333'))
    ax.text(x+w/2,y+h-1.5,t,ha='center',va='top',fontsize=9.5,weight='bold')
    ax.text(x+w/2,y+h-5.2,b,ha='center',va='top',fontsize=7.8,linespacing=1.4)
box(1,12,20,14,'T3 터미널','ros2 topic pub\n/r_goal_move\n(MoveL: 자세 + T)','#E8F0FE')
box(26,8,27,22,'T2 실제 Cyclo (C++, 수정 없음)','ai_worker_controller.launch.py\ncontroller_type:=movel\n3차 보간 → v_d → QP(OSQP)\n→ q_d = q + q̇Δt','#FCE8E6')
box(70,8,28,22,'T1 cyclo_mujoco_bridge.py','MuJoCo FFW-SG2 (실시간)\n궤적 → 위치 액추에이터 목표\n/joint_states 100 Hz 발행\n손끝 위치 CSV 기록\n(--gravcomp: 중력 보상)','#E6F4EA')
ax.annotate('',xy=(26,19),xytext=(21.4,19),arrowprops=dict(arrowstyle='->',lw=1.3))
ax.annotate('',xy=(69.6,23),xytext=(53.4,23),arrowprops=dict(arrowstyle='->',lw=1.3))
ax.text(61.5,25,'관절 궤적',ha='center',fontsize=7.8)
ax.annotate('',xy=(53.4,14),xytext=(69.6,14),arrowprops=dict(arrowstyle='->',lw=1.3))
ax.text(61.5,10.2,'/joint_states',ha='center',fontsize=7.5)
ax.text(50,1.5,'실로봇에서는 T1 자리에 follower 로봇(arm_r_controller + joint_state_broadcaster)이 들어간다 → Cyclo는 그대로',ha='center',fontsize=8,color='#444')
fig.savefig('bridge_fig.png',dpi=170,bbox_inches='tight'); print('ok')

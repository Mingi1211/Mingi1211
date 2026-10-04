import mujoco, numpy as np
m = mujoco.MjModel.from_xml_path('ai_worker/ffw_description/mujoco/ffw_sg2/scene.xml')
d = mujoco.MjData(m)
mujoco.mj_forward(m, d)
print('nq =', m.nq, ' nv =', m.nv, ' nu =', m.nu, ' timestep =', m.opt.timestep)
for i in range(1, 8):
    j = m.joint(f'arm_r_joint{i}')
    print(f'arm_r_joint{i}: 축 {j.axis}, 범위 {np.round(j.range, 3)} rad')
a = m.actuator('arm_r_joint1')
print('arm_r_joint1 액추에이터 kp =', a.gainprm[0], ' 힘 범위 =', a.forcerange)
print('오른손 끝(end_effector_r_link) 위치 =', np.round(d.body('end_effector_r_link').xpos, 3))

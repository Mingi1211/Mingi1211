"""브리지 로그(bridge_log.csv)로 오른손 끝 궤적과 목표 대비 오차를 그린다

  python3 plot_bridge.py --log bridge_log.csv --target 0.35 -0.20 0.85 --out C1
"""
import argparse
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument('--log', default='bridge_log.csv')
ap.add_argument('--target', type=float, nargs=3, required=True, help='base_link 기준 목표 [m]')
ap.add_argument('--start', type=float, default=0.0, help='이 시각[s] 이후만 그림 (명령 보낸 시각 근처)')
ap.add_argument('--out', default='bridge')
args = ap.parse_args()

d = np.loadtxt(args.log, delimiter=',', skiprows=1)
d = d[d[:, 0] >= args.start]
t, p = d[:, 0] - d[0, 0], d[:, 1:4]
tgt = np.array(args.target)
err = np.linalg.norm(p - tgt, axis=1) * 1000

fig, ax = plt.subplots(2, 1, figsize=(7, 5), sharex=True)
for k, c in enumerate('xyz'):
    ax[0].plot(t, p[:, k], label=f'{c} (MuJoCo)')
    ax[0].axhline(tgt[k], ls='--', lw=0.8, color=f'C{k}')
ax[0].set_ylabel('EE in base_link [m]'); ax[0].legend(ncol=3, fontsize=7)
ax[0].set_title('Cyclo MoveL in MuJoCo: ' + args.out)
ax[1].plot(t, err); ax[1].set_ylabel('|EE - target| [mm]'); ax[1].set_xlabel('t [s]')
fig.tight_layout(); fig.savefig(args.out + '_bridge.png', dpi=120)
print(f'최종 위치 {np.round(p[-1], 4)} · 목표와의 거리 {err[-1]:.1f} mm · 저장 {args.out}_bridge.png')

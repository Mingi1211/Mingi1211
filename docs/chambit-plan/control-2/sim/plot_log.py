#!/usr/bin/env python3
"""impedance_node CSV → 그래프 (손 위치 vs 목표, 자세 오차, 토크). 사용: python3 plot_log.py ~/impedance_logs/<파일>.csv"""
import sys

import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv(sys.argv[1])
for side, g in df.groupby('side'):
    fig, ax = plt.subplots(3, 1, figsize=(9, 9), sharex=True)
    for c, col in zip('xyz', ['C0', 'C1', 'C2']):
        ax[0].plot(g.t, g[f'p{c}'], col, label=f'{c}')
        ax[0].plot(g.t, g[f'pd{c}'], col + '--', label=f'{c} 목표')
    ax[0].set_ylabel('손 위치 [m]'); ax[0].legend(ncol=3)
    for c in 'xyz':
        ax[1].plot(g.t, g[f'eo{c}'], label=c)
    ax[1].set_ylabel('자세 오차 [rad]'); ax[1].legend()
    for i in range(1, 8):
        ax[2].plot(g.t, g[f'tau{i}'], label=f'j{i}')
    ax[2].set_ylabel('토크 [Nm]'); ax[2].set_xlabel('t [s]'); ax[2].legend(ncol=7, fontsize=7)
    fig.suptitle(f'{sys.argv[1]} — arm {side}')
    out = sys.argv[1].replace('.csv', f'_{side}.png')
    fig.tight_layout(); fig.savefig(out, dpi=120); print('저장:', out)

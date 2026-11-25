"""Figure for Section 5.1: the shortfall's fit as its onset moves, for DESI DR2 with each supernova sample (from results.json)."""
import json, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
R = json.load(open('results.json'))
C = {'Pantheon+': '#2a78d6', 'DES-SN5YR 2024': '#eb6834', 'DES-Dovekie 2026': '#1baf7a'}
INK, MUTED, GRID = '#1f1f1e', '#6b6a66', '#e6e5e0'
plt.rcParams.update({'font.size': 10, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK, 'xtick.color': MUTED, 'ytick.color': MUTED})
fig, axs = plt.subplots(1, 2, figsize=(10, 4.4), sharey=True)
for name, col in C.items():
    if name not in R: continue
    for ax, w_u in zip(axs, (0, 1)):
        sc = np.array(R[name][f'shortfall_wu{w_u}']['scan']); m = sc[:, 0] <= 0.5
        ax.plot(sc[m, 0], sc[m, 1], color=col, lw=2, label=name)
        ax.axhline(R[name]['form']['dchi2'], color=col, lw=1, ls='--')
for ax, t in zip(axs, ('Settled Ocean thins by spreading (w_u = 0)', 'Its current thins (w_u = 1)')):
    ax.axhline(0, color=MUTED, lw=1); ax.set_xlim(0, 0.5); ax.set_ylim(-16, 8)
    ax.set_xlabel('redshift where the shortfall begins'); ax.set_title(t, fontsize=10, color=INK, loc='left')
    ax.grid(axis='y', color=GRID, lw=0.6)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
axs[0].set_ylabel('Δχ² against the settled Ocean held fixed')
axs[0].text(0.49, 0.5, 'held fixed', ha='right', color=MUTED, fontsize=8.5)
axs[0].legend(frameon=False, fontsize=8.5, loc='upper left', title='DESI DR2 distances with:', title_fontsize=8.5)
axs[1].text(0.49, -15.3, "dashed: the two-number form w0 + wa(1 − a), same data", ha='right', color=MUTED, fontsize=8)
fig.tight_layout(); fig.savefig('shortfall_onset.png', dpi=160)

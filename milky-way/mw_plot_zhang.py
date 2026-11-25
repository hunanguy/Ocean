import json, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import mw_fit_zhang as Z
cols={'cdm':('#2a6fb0','cold dark matter'),'parallel':('#c0392b','force parallel to the baryons'),'eddy':('#1e8449','the eddy (Section 6)')}
titles={'rich':'metal-rich','int':'intermediate','poor':'metal-poor'}
fig,ax=plt.subplots(1,3,figsize=(12,3.8)); zz=np.linspace(0.33,1.18,40)
for m,(c,l) in cols.items():
    x=np.array(json.load(open('best_fits.json'))['lisanti_'+m]); az=Z.az_column(m,x[:-3]); chi=Z.chi2(x,m)
    for a,(k,h) in zip(ax,zip(Z.POPS,x[-3:])):
        a.plot(zz,Z.sigma_model(az,zz,h),color=c,lw=2,label=f'{l} (total chi2 {chi:.0f})')
for a,k in zip(ax,Z.POPS):
    zs,s,e=Z.SDAT[k].T; a.errorbar(zs,s,e,fmt='o',ms=3.5,color='k',label='Zhang et al. 2013 (via Lisanti et al. 2023)')
    a.set_title(f'vertical speed spread, {titles[k]} stars'); a.set_xlabel('height above the disk, z (kpc)')
ax[0].set_ylabel('sigma_z (km/s)'); ax[0].legend(fontsize=7,loc='upper left')
plt.tight_layout(); plt.savefig('vertical_test_lisanti_data.png',dpi=140)

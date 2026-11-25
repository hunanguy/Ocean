import json, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import mw_fit as F, mw_data as D
cols={'cdm':('#2a6fb0','cold dark matter'),'parallel':('#c0392b','force parallel to the baryons\n(superfluid dark matter class)'),'eddy':('#1e8449','the eddy (Section 6)')}
fig,ax=plt.subplots(1,2,figsize=(11,4.3))
Rg=np.linspace(4.3,9.0,60); Rr=np.linspace(5,18,80)
for m,(c,l) in cols.items():
    th=np.array(json.load(open('best_fits.json'))['bovyrix_'+m]); p=dict(zip(F.BARYON_KEYS,th[:6]))
    # vertical force curve
    aRb,azb=F.acc_baryon(Rg,1.1,p); aRr,_=F.acc_baryon(Rr,0.0,p)
    if m=='cdm':
        g=F.nfw_g(*th[6:]); az=azb+F.sph_acc(Rg,np.full_like(Rg,1.1),g)[1]; aR=aRr+F.sph_acc(Rr,np.zeros_like(Rr),g)[0]
    elif m=='parallel':
        a0=th[6]*F.GDAG_UNIT; az=azb*F.rar_nu(np.hypot(aRb,azb)/a0); aR=aRr*F.rar_nu(np.abs(aRr)/a0)
    else:
        g=F.eddy_g(sum(F.masses(p)),th[6],F.DEFAULT_FORM,p)[0]; az=azb+F.sph_acc(Rg,np.full_like(Rg,1.1),g)[1]; aR=aRr+F.sph_acc(Rr,np.zeros_like(Rr),g)[0]
    c2=sum(F.chi2_parts(m,th))
    ax[0].plot(Rg,-az/(2*np.pi*F.G)/1e6,color=c,lw=2,label=f'{l}  (chi2 {c2:.0f})')
    ax[1].plot(Rr,np.sqrt(-aR*Rr),color=c,lw=2)
ax[0].errorbar(D.KZ_R,D.KZ,D.KZ_ERR,fmt='o',ms=3,color='k',alpha=.6,label='Bovy & Rix 2013, 43 star populations')
ax[0].set_yscale('log'); ax[0].set_xlabel('distance from the galaxy center, R (kpc)'); ax[0].set_ylabel('vertical force at 1.1 kpc, K_z / 2 pi G (Msun/pc^2)')
ax[0].set_title('Vertical turning near the disk'); ax[0].legend(fontsize=7.5,loc='upper right')
ax[1].errorbar(D.RC_R,D.RC_V,D.RC_ERR,fmt='o',ms=3,color='k',alpha=.6,label='Eilers et al. 2019')
ax[1].set_xlabel('R (kpc)'); ax[1].set_ylabel('circular speed (km/s)'); ax[1].set_title('Radial turning: the rotation curve'); ax[1].set_ylim(195,245); ax[1].legend(fontsize=8)
plt.tight_layout(); plt.savefig('vertical_test.png',dpi=140)

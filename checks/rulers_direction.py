"""
3.13 item 5: rulers that stretch differently by direction, around a spinning hole.
The Ocean's own slicing of a spinning hole is by its phase, the build's clock: theta = mu(t + F(r)),
Delta F' = 2 M r_+ (Sec. 11.8, Boyer-Lindquist coordinates, G = c = 1, M = 1).
 (1) The slices of constant phase are spacelike everywhere outside the hole and through the point of no return
     (grad theta timelike): g^{mu nu} d theta d theta < 0.
 (2) The rulers on those slices (the six push numbers h_ij) are not the same in every direction: the
     Cotton-York tensor of h_ij, zero exactly when some choice of coordinates makes the rulers equal in every
     direction (conformal flatness, in three dimensions), is computed by finite differences. Zero for no spin
     (spherical: always conformally flat), zero at first order in spin, growing as spin squared.
 (3) The outside the frame law gives: Kerr's (the frame law is the teleparallel equivalent of General
     Relativity, item 2 test 1; stationary, axisymmetric, empty outside a regular point of no return: Kerr,
     by the uniqueness theorems). Spot check: the Ricci tensor of Kerr vanishes at sample points.
"""
import numpy as np
M=1.0
def kerr(x,a):
    t,r,th,ph=x; s2=np.sin(th)**2; S=r*r+a*a*np.cos(th)**2; D=r*r-2*M*r+a*a
    g=np.zeros((4,4))
    g[0,0]=-(1-2*M*r/S); g[0,3]=g[3,0]=-2*M*a*r*s2/S
    g[1,1]=S/D; g[2,2]=S; g[3,3]=(r*r+a*a+2*M*a*a*r*s2/S)*s2
    return g
def ginv_kerr(r,th,a):
    s2=np.sin(th)**2; S=r*r+a*a*np.cos(th)**2; D=r*r-2*M*r+a*a; A=(r*r+a*a)**2-a*a*D*s2
    gi=np.zeros((4,4)); gi[0,0]=-A/(S*D); gi[0,3]=gi[3,0]=-2*M*a*r/(S*D); gi[1,1]=D/S; gi[2,2]=1/S
    gi[3,3]=(D-a*a*s2)/(S*D*s2); return gi
def rplus(a): return M+np.sqrt(M*M-a*a)
# (1) spacelike slices: rho^2 g^{theta theta} = [-(r^2+a^2)^2 + a^2 Delta sin^2 + (2 M r_+)^2]/Delta
print("(1) constant-phase slices: largest value of g^{mu nu} d_mu theta d_nu theta (must be < 0)")
for a in (0.0,0.5,0.9,0.998):
    rp=rplus(a); worst=-np.inf
    for r in np.r_[np.linspace(0.3*rp,0.999*rp,200),np.linspace(1.001*rp,60,600)]:
        for th in np.linspace(0.05,np.pi/2,20):
            S=r*r+a*a*np.cos(th)**2; D=r*r-2*M*r+a*a
            val=(-(r*r+a*a)**2+a*a*D*np.sin(th)**2+(2*M*rp)**2)/(D*S)
            worst=max(worst,val)
    print(f"    a = {a:5.3f}: max over 0.3 r_+ to 60 M (point of no return excluded by 0.1%) = {worst:+.3e}")

# induced metric on t + F(r) = const, coordinates (r, th, ph): dt = -F' dr
def h3(y,a):
    r,th=y[0],y[1]; rp=rplus(a); D=r*r-2*M*r+a*a; Fp=2*M*rp/D
    g=kerr((0,r,th,0),a); h=np.zeros((3,3))
    h[0,0]=g[1,1]+g[0,0]*Fp*Fp; h[0,2]=h[2,0]=-g[0,3]*Fp; h[1,1]=g[2,2]; h[2,2]=g[3,3]
    return h
def dmet(f,y,a,hstep):
    """derivatives of a 3-index-free field f(y) w.r.t. (r, th, ph); ph derivative zero (axisymmetric)"""
    out=[]
    for k in range(3):
        if k==2: out.append(np.zeros_like(f(y,a))); continue
        e=np.zeros(3); e[k]=hstep
        out.append((-f(y+2*e,a)+8*f(y+e,a)-8*f(y-e,a)+f(y-2*e,a))/(12*hstep))
    return np.array(out)                     # out[k] = d_k f
def christ(y,a,hs=1e-3):
    h=h3(y,a); hi=np.linalg.inv(h); dh=dmet(h3,y,a,hs)       # dh[k,i,j]
    G=0.5*(np.einsum('il,kjl->ikj',hi,dh)+np.einsum('il,jkl->ikj',hi,dh)-np.einsum('il,lkj->ikj',hi,dh))
    return G                                  # G[i,k,j] = Gamma^i_{kj}
def ricci(y,a):
    G=christ(y,a); dG=dmet(christ,y,a,2e-3)                  # dG[l,i,k,j] = d_l Gamma^i_{kj}
    R=np.einsum('iikj->kj',dG.transpose(1,0,2,3)) if False else None
    Ric=np.zeros((3,3))
    for k in range(3):
        for j in range(3):
            Ric[k,j]=sum(dG[i,i,k,j]-dG[j,i,k,i] for i in range(3)) \
                   +sum(G[i,i,l]*G[l,k,j]-G[i,j,l]*G[l,k,i] for i in range(3) for l in range(3))
    return Ric
def schouten(y,a):
    h=h3(y,a); Ric=ricci(y,a); R=np.einsum('ij,ij',np.linalg.inv(h),Ric)
    return Ric-R*h/4
def cotton_norm(y,a):
    h=h3(y,a); hi=np.linalg.inv(h); G=christ(y,a); S=schouten(y,a); dS=dmet(schouten,y,a,1e-2)   # dS[k,i,j]
    nS=dS-np.einsum('lki,lj->kij',G,S).transpose(0,1,2)*0  # placeholder, replaced below
    # covariant derivative: nabla_k S_ij = d_k S_ij - Gamma^l_{ki} S_lj - Gamma^l_{kj} S_il
    nS=dS-np.einsum('lki,lj->kij',G,S)-np.einsum('lkj,il->kij',G,S)
    C=np.einsum('kij->ijk',nS)-np.einsum('jik->ijk',nS)     # C_ijk = nabla_k S_ij - nabla_j S_ik
    return np.sqrt(abs(np.einsum('ijk,il,jm,kn,lmn',C,hi,hi,hi,C)))

print("\n(2) rulers by direction: Cotton-York size |C| M^3 on the constant-phase slices")
for (r,th) in ((4.0,np.pi/3),(6.0,np.pi/4),(3.0,1.2)):
    vals=[]
    for a in (0.0,0.05,0.1,0.2,0.5,0.9):
        vals.append(cotton_norm(np.array([r,th,0.0]),a))
    sc=[v/(a*a) if a>0 else 0 for v,a in zip(vals,(0.0,0.05,0.1,0.2,0.5,0.9))]
    print(f"    r = {r} M, polar angle {th:.2f}: a=0: {vals[0]:.1e};  " +
          ";  ".join(f"a={a}: {v:.2e} (/a^2 {s:.4f})" for a,v,s in zip((0.05,0.1,0.2,0.5,0.9),vals[1:],sc[1:])))

# (3) Ricci of Kerr in four dimensions vanishes (spot check, finite differences)
def ricci4(x,a,hs=1e-4):
    def chr4(x):
        g=kerr(x,a); gi=np.linalg.inv(g); dg=np.zeros((4,4,4))
        for k in (1,2):
            e=np.zeros(4); e[k]=hs; dg[k]=(-kerr(x+2*e,a)+8*kerr(x+e,a)-8*kerr(x-e,a)+kerr(x-2*e,a))/(12*hs)
        return 0.5*(np.einsum('il,kjl->ikj',gi,dg)+np.einsum('il,jkl->ikj',gi,dg)-np.einsum('il,lkj->ikj',gi,dg))
    G=chr4(x); dG=np.zeros((4,4,4,4))
    for l in (1,2):
        e=np.zeros(4); e[l]=1e-3; dG[l]=(-chr4(x+2*e)+8*chr4(x+e)-8*chr4(x-e)+chr4(x-2*e))/(12e-3)
    Ric=np.zeros((4,4))
    for k in range(4):
        for j in range(4):
            Ric[k,j]=sum(dG[i,i,k,j]-dG[j,i,k,i] for i in range(4))+sum(G[i,i,l]*G[l,k,j]-G[i,j,l]*G[l,k,i] for i in range(4) for l in range(4))
    return np.abs(Ric).max()
print("\n(3) Kerr's Ricci tensor at sample points (should be ~0; scale of single terms ~ M/r^3):",
      ", ".join(f"{ricci4(np.array([0,r,th,0]),0.9):.1e}" for r,th in ((3.0,1.0),(5.0,0.6),(10.0,1.4))))

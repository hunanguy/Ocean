"""Gravity-only gyroscope test for check_ocean_math.py (from the item 1 work, check 1)."""
# Check 1. A gyroscope falling freely beside a mass, with both travelling together through the Ocean at V.
# Linearized geometry (G = c = 1), mass moving at V:  g00 = -1 + 2U,  gij = (1 + 2*gam*U) delta_ij,
#   g0i = -k * U * V_i   (the tilt of the moving mass's surroundings; the Ocean rule gives k = 2 + 2*gam:
#   clock share 2, ruler share 2*gam; a Lorentz boost of the resting mass gives the same).
# Gyroscope: geodesic + parallel transport (exact equations, Christoffels by finite differences).
# Its spin is read in its own rest frame (pure boost from the coordinate frame), and its turning rate
# relative to the coordinate axes is measured. At rest (V = 0) a gyroscope released at rest does not turn.
# Question: with V != 0, does it turn? It must not, if travel through the Ocean leaves no trace.
import numpy as np
M=1e-6; gam=1.0
def metric(X,V,k):
    t,x=X[0],X[1:]; d=x-V*t; U=M/np.linalg.norm(d)
    g=np.diag([-1+2*U]+[1+2*gam*U]*3)
    g[0,1:]=g[1:,0]=-k*U*V
    return g
def christoffel(X,V,k,h=1e-3):
    dg=np.zeros((4,4,4))
    for a in range(4):
        e=np.zeros(4); e[a]=h
        dg[a]=(metric(X+e,V,k)-metric(X-e,V,k))/(2*h)      # dg[a][m,n] = d_a g_mn
    gi=np.linalg.inv(metric(X,V,k))
    G=np.zeros((4,4,4))
    for l in range(4):
        G[l]=0.5*np.einsum('s,smn->mn',gi[l],np.transpose(dg,(1,0,2))+np.transpose(dg,(1,2,0))-dg)
    return G   # G[l,m,n]
def rhs(Y,V,k):
    X,u,S=Y[:4],Y[4:8],Y[8:]
    G=christoffel(X,V,k)
    return np.r_[u,-np.einsum('lmn,m,n->l',G,u,u),-np.einsum('lmn,m,n->l',G,S,u)]
def rest_spin(Y,V,k):
    X,u,S=Y[:4],Y[4:8],Y[8:]
    g=metric(X,V,k)
    P=np.eye(4)+np.outer(u,g@u)            # projector orthogonal to u (u.u = -1)
    E=P[:,1:]                               # projected coordinate directions (columns)
    Gm=E.T@g@E; w,Q=np.linalg.eigh(Gm); Gi=Q@np.diag(w**-0.5)@Q.T
    E=E@Gi                                  # symmetric orthonormalization: no rotation added
    return E.T@g@S                          # spin components on the rest-frame axes
def run(V,k,T=2.0,n=400):
    x0=np.array([1.0,0.3,-0.2])             # gyroscope position relative to the mass
    vel=V.copy()                            # released at rest relative to the mass
    X=np.r_[0.0,x0]; g=metric(X,V,k)
    u=np.r_[1.0,vel]; u=u/np.sqrt(-u@g@u)
    out=[]
    for s0 in [np.array([0,1.0,0,0]),np.array([0,0,1.0,0]),np.array([0,0,0,1.0])]:
        S=s0.copy(); S[0]=-(g@u)[1:]@S[1:]/(g@u)[0]      # make S orthogonal to u
        Y=np.r_[X,u,S]; dt=T/n; s_start=rest_spin(Y,V,k); s_start/=np.linalg.norm(s_start)
        for i in range(n):                  # RK4 in proper time
            k1=rhs(Y,V,k); k2=rhs(Y+dt/2*k1,V,k); k3=rhs(Y+dt/2*k2,V,k); k4=rhs(Y+dt*k3,V,k)
            Y=Y+dt/6*(k1+2*k2+2*k3+k4)
        s_end=rest_spin(Y,V,k); s_end/=np.linalg.norm(s_end)
        out.append((s_start,s_end))
    # turning angle vector: for small rotations ds = Omega x s, solve least squares
    A=[];b=[]
    for s0,s1 in out:
        ds=s1-s0; Mx=np.array([[0,s0[2],-s0[1]],[-s0[2],0,s0[0]],[s0[1],-s0[0],0]])  # Omega x s0 = Mx @ Omega
        A.append(Mx); b.append(ds)
    Om=np.linalg.lstsq(np.vstack(A),np.concatenate(b),rcond=None)[0]
    return Om/T
# Cross-check: carry the travelling case back to the frame in which the mass is at rest (exact Lorentz
# transformation of position, velocity and spin), and read the spin there against that frame's axes.
def boost(Vv):
    v=np.linalg.norm(Vv); g=1/np.sqrt(1-v*v); n=Vv/v
    L=np.eye(4); L[0,0]=g; L[0,1:]=L[1:,0]=-g*Vv; L[1:,1:]+= (g-1)*np.outer(n,n)
    return L                                  # coordinates of a frame moving at Vv
def run_back(V,k,T=2.0,n=400):
    x0=np.array([1.0,0.3,-0.2]); X=np.r_[0.0,x0]; g=metric(X,V,k)
    u=np.r_[1.0,V]; u=u/np.sqrt(-u@g@u); L=boost(V); Z=np.zeros(3)
    pairs=[]
    for s0 in np.eye(3):
        S=np.r_[0.0,s0]; S[0]=-(g@u)[1:]@S[1:]/(g@u)[0]
        Y=np.r_[X,u,S]; dt=T/n
        A0=np.r_[L@Y[:4],L@Y[4:8],L@Y[8:]]; a=rest_spin(A0,Z,0.0); a/=np.linalg.norm(a)
        for i in range(n):
            k1=rhs(Y,V,k); k2=rhs(Y+dt/2*k1,V,k); k3=rhs(Y+dt/2*k2,V,k); k4=rhs(Y+dt*k3,V,k)
            Y=Y+dt/6*(k1+2*k2+2*k3+k4)
        A1=np.r_[L@Y[:4],L@Y[4:8],L@Y[8:]]; b=rest_spin(A1,Z,0.0); b/=np.linalg.norm(b)
        pairs.append((a,b))
    Am=[];bm=[]
    for a,b in pairs:
        Am.append(np.array([[0,a[2],-a[1]],[-a[2],0,a[0]],[a[1],-a[0],0]])); bm.append(b-a)
    Om=np.linalg.lstsq(np.vstack(Am),np.concatenate(bm),rcond=None)[0]
    return Om/T

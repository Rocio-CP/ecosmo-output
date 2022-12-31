# BASE IT ON READ_BIOMASS
from scipy.io import FortranFile
import numpy as np
from itertools import islice

files_dir='/Users/rocio/Dropbox/ECOSMO/ecosmosourcefiles/'

# FORTRAN USES 1-INDEXING!!!
m=177
n=207
ilo=20
nphys=20
nbio=23
nprod=25

khor=8216; khor1=khor+1
ndrei=82108
kasor=8106



# Read the grid info
g = FortranFile( files_dir+'gridinfo', 'r' )
gridinfo_dtype='int32'
# CHECKEAR EL TIPO!!
g1=g.read_reals(dtype=gridinfo_dtype) # Have to check the type!
dt=g1[0]; mm=g1[1]; nn=g1[2]; ilon=g1[3]
g2=g.read_reals(dtype=gridinfo_dtype)
seclist=[ilo,1,1,khor1,khor,khor,n,n]
dz,nhor,ntot,iwet,ldep,lazc,indend,islab,*rest= np.split(g2, np.cumsum(seclist))
g3=g.read_reals(dtype=gridinfo_dtype)
seclist=[1,m,m,m]
dlr,rdln,dlvo,dlvu,*rest= np.split(g3, np.cumsum(seclist))

#print(g1.shape)
#print(g2.shape)
#print(g3.shape)

#common / ind /
#isornr(n), isorsr(n)
#common / vecind / indwet(khor), indver(ndrei), lb(n), le(n),
#indi(ndrei), irbsor(kasor, 2, 2), nrbsor(2, 2), jwet(khor),
#llw(ndrei)


# Read the file; iwet points per line, each new line is a day
f = FortranFile( files_dir+'NN09401b', 'r' )
fdata=f.read_reals(dtype='float32')

# Turn 1D into 3D
#u(m, n, ilo, nday)
#ucomp(ntot)


# Preallocate
u=np.empty([m,n,ilo])
u[:]=np.nan

lwe = -1
nwet = -1
for j in range(0,n-1):
    lwa = lwe + 1
    lwe = indend[j] - 1
    for lw in range(lwa,lwe):
        i = iwet[lw] -1
        lump = lazc[lw] -1
        for k in range(0,lump-1):
            nwet = nwet + 1
            u[i, j, k] = fdata[nwet] -1



import numpy as np
import plotly.express as px
import plotly.graph_objects as go

draw_n=False
dx = 0.1
dy = 0.1
nx = 30
ny = 30
count = nx*ny
sigma = 0.2
nu=0.05

dt=sigma*dx*dy/nu

u=np.ones(nx*ny)
v=np.ones(nx*ny)

u[int(ny*nx/2)+int(nx/2)-2:int(ny*nx/2)+int(nx/2)+2]=2

pos = np.zeros((nx*ny,2))

neighbors = {}

maxT = 50
Frames=[]

def getds(a,b):
    return pos[a,:]-pos[b,:]

for y in np.arange(0,ny):
    for x in np.arange(0,nx):
        pos[x+y*ny,0]=x*dx+(y%2)*dx*0.5
        pos[x+y*ny,1]=y*dy
for y in np.arange(0,ny):
    for x in np.arange(0,nx):
        idx=x+nx*y
        neighbors[idx]=[]
        #Horizontal neighbors
        if x > 0:
            neighbors[idx].append(idx-1)
        if x < nx-1:
            neighbors[idx].append(idx+1)
        #Up neighbors
        if y < ny-1:
            neighbors[idx].append(idx+nx)
            if y%2==1:
                if x < nx-1:
                    neighbors[idx].append(idx+nx+1)
            else:
                if x > 0:
                    neighbors[idx].append(idx+nx-1)
        #down neighbors
        if y > 0:
            neighbors[idx].append(idx-nx)
            if y%2==1:
                if x < nx-1:
                    neighbors[idx].append(idx-nx+1)
            else:
                if x > 0:
                    neighbors[idx].append(idx-nx-1)


    
    
startData = go.Contour(z=u,x=pos[:,0],y=pos[:,1])
dudx=np.zeros(nx*ny)
dudy=np.zeros(nx*ny)

for t in np.arange(0,maxT):

    un=u.copy()
    vn=v.copy()
    #Bake the neighbors
    for p in np.arange(0,count):
        dxCount=0
        dyCount=0

        for n in neighbors[p]:
            ds=getds(p,n)
            if ds[0]!=0:
                dudx[p]+=(un[p]-un[n])/ds[0]
                dxCount+=1
            if ds[1]!=0:
                dudy[p]+=(un[p]-un[n])/ds[1]
                dyCount+=1
            if dxCount!=0:
                dudx[p]/=dxCount
            if dyCount != 0:
                dudy[p]/=dyCount

    for p in np.arange(0,count):
        dudx2=0
        dudy2=0
        dxCount=0
        dyCount=0
        for n in neighbors[p]:
            ds=getds(p,n)
            if ds[0]!=0:
                dudx2+=(dudx[p]-dudx[n])/ds[0]
                dxCount+=1
            if ds[1]!=0:
                dudy2+=(dudy[p]-dudy[n])/ds[1]
                dyCount+=1
        ncount=len(neighbors[p])
        dudx2/=ncount
        dudy2/=ncount

        un=u.copy()

        u[p]=un[p]+nu*dt*(dudx2+dudy2)

    
    
    Frames.append(go.Frame(data=go.Contour(z=u,x=pos[:,0],y=pos[:,1], 
                                           contours_coloring='heatmap', 
                                           line_width=0)))

    
fig = go.Figure(
    data=startData,
    layout=go.Layout(
        xaxis=dict(range=[0, 5], autorange=False),
        yaxis=dict(range=[0, 5], autorange=False),
        title="Pressure",
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Play",
                          method="animate",
                          args=[None])])]
    ),
    frames=Frames)
  
    
fig.show()
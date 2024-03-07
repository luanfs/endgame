import numpy as np
import matplotlib.pyplot as plt
from plotting_routines  import plot_scalarfield


# Python script to plot the outputs
# directory
graphdir ='../graphs/' # must exist
datadir  ='../dump/' # must exist
nbfaces = 6
figformat='png'

# some constants
N    = 192 # number of cells
tc   = 7 # test case
gtype=0
sec2day=86400

if tc==2: # steady flow
   hmin, hmax = 1000.0, 3000.0
   umin, umax = -30, -60
elif tc==5: #flow over a mountain
   hmin, hmax = 5000.0, 6000.0
   umin, umax = -10, 40
   vmin, vmax = -25, 25
elif tc==7: #barotropic instability
   hmin, hmax = 8800, 10500
   umin, umax = -50, 50
   vmin, vmax = -50, 50

map_projection='mercator'
dpi=100
figformat='png'
colormap='jet'

timedata = np.loadtxt(datadir+'TC'+str(tc)+"_reftimes.dat").astype(int)

#print(basename)

# Get scalar field
h = np.zeros((N,N,6,len(timedata))) # h at agrid
u = np.zeros((N,N,6,len(timedata))) # u at agrid
v = np.zeros((N,N,6,len(timedata))) # v at agrid


for t in range(0,len(timedata)):
   for p in range(0,6):
      
      # get h
      basename = "tc"+str(tc)+"_g"+str(gtype)+"_N"+str(N)+"_h"
      filename = basename+'_t'+str(timedata[t])+"_face"+str(p+1)+'.dat'
      z = open(datadir+filename, 'rb')
      z = np.fromfile(z, dtype=np.float64)
      z = np.reshape(z, (N,N))
      h[:,:,p,t] = z

      # get u
      basename = "tc"+str(tc)+"_g"+str(gtype)+"_N"+str(N)+"_u"
      filename = basename+'_t'+str(timedata[t])+"_face"+str(p+1)+'.dat'
      z = open(datadir+filename, 'rb')
      z = np.fromfile(z, dtype=np.float64)
      zz = z
      z = np.reshape(z, (N,N))
      u[:,:,p,t] = z

      # get v
      basename = "tc"+str(tc)+"_g"+str(gtype)+"_N"+str(N)+"_v"
      filename = basename+'_t'+str(timedata[t])+"_face"+str(p+1)+'.dat'
      z = open(datadir+filename, 'rb')
      z = np.fromfile(z, dtype=np.float64)
      z = np.reshape(z, (N,N))
      v[:,:,p,t] = z

   # plot h graph
   colormap = 'jet'
   title ="TC"+str(tc)+" - h - time (days) = "+str(timedata[t]/sec2day)
   output_name =  graphdir+"tc"+str(tc)+"_g"+str(gtype)+"_N"+str(N)+"_h_t"+str(timedata[t])
   plot_scalarfield(h[:,:,:,t], map_projection, title, output_name, colormap, hmin, hmax, dpi, figformat, N)

   # plot u graph
   colormap = 'jet'
   title ="TC"+str(tc)+" - u - time (days) = "+str(timedata[t]/sec2day)
   output_name =  graphdir+"tc"+str(tc)+"_g"+str(gtype)+"_N"+str(N)+"_u_t"+str(timedata[t])
   plot_scalarfield(u[:,:,:,t], map_projection, title, output_name, colormap, umin, umax, dpi, figformat, N)
   #print(np.amin(u[:,:,:,t]), np.amax(u[:,:,:,t]) )

   # plot v graph
   colormap = 'jet'
   title ="TC"+str(tc)+" - v - time (days) = "+str(timedata[t]/sec2day)
   output_name =  graphdir+"tc"+str(tc)+"_g"+str(gtype)+"_N"+str(N)+"_v_t"+str(timedata[t])
   plot_scalarfield(v[:,:,:,t], map_projection, title, output_name, colormap, vmin, vmax, dpi, figformat, N)
   #print(np.amin(v[:,:,:,t]), np.amax(v[:,:,:,t]) )


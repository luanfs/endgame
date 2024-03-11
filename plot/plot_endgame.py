import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib import ticker, cm, colors, colorbar

# Python script to plot the outputs
# directory
graphdir ='../graphs/' # must exist
datadir  ='../dump/' # must exist
nbfaces = 6
figformat='png'

# some constants
N = 128
M = N//2
tc = 5 # test case
sec2day=86400


map_projection='mercator'
dpi=100
figformat='png'
colormap='jet'

timedata = np.loadtxt(datadir+'TC'+str(tc)+"_reftimes.dat").astype(int)

#print(basename)

# Get scalar field
h = np.zeros((N,M,len(timedata))) # h
u = np.zeros((N,M,len(timedata))) # u
v = np.zeros((N,M,len(timedata))) # v
vort = np.zeros((N,M,len(timedata)))
pv   = np.zeros((N,M,len(timedata)))

lat = np.linspace(-90,90,M)
lon = np.linspace(0,360,N)
lat, lon = np.meshgrid(lat,lon)

if tc==5: #flow over a mountain
   hmin, hmax = 5000.0, 6000.0
   umin, umax = -10, 40
   vmin, vmax = -25, 25
   pvmin, pvmax = -3.1e-08, 3.1e-08
   vortmin, vortmax = -3.6e-05, 4.7e-05

elif tc==7: #barotropic instability
   hmin, hmax = 8400, 10500
   umin, umax = -20, 85
   vmin, vmax = -45, 45
   pvmin, pvmax = -1.5e-08, 2.4e-08
   vortmin, vortmax = -8.9e-05, 9.8e-05


fields = [h,u,v,vort,pv]
field_names = ('h','u','v','pv','vort')
for t in range(0,len(timedata)):
   for field, name in zip(fields, field_names):
      filename = "eg_swe_run_ic"+str(tc)+"_cor1_"+name+"_t"+str(timedata[t])+"_"+str(N)+"x"+str(M)+'.dat'
      z = open(datadir+filename, 'rb')
      z = np.fromfile(z, dtype=np.float64)
      z = np.reshape(z, (N,M))
      field[:,:,t] = z


#hmin, hmax = np.amin(fields[0]), np.amax(fields[0])
#umin, umax = np.amin(fields[1]), np.amax(fields[1])
#vmin, vmax = np.amin(fields[2]), np.amax(fields[2])
#pvmin, pvmax = np.amin(fields[3]), np.amax(fields[3])
#vortmin, vortmax = np.amin(fields[4]), np.amax(fields[4])
fmins = [hmin, umin, vmin, pvmin, vortmin]
fmaxs = [hmax, umax, vmax, pvmax, vortmax]

for t in range(0,len(timedata)):
   for field, name, fmin, fmax in zip(fields, field_names, fmins, fmaxs):
      # plot the graph
      # map projection
      if map_projection == "mercator":
          plt.figure(figsize=(1832/dpi, 977/dpi), dpi=dpi)
          plateCr = ccrs.PlateCarree()        
      elif map_projection == "sphere":
          plt.figure(figsize=(800/dpi, 800/dpi), dpi=dpi) 
          plateCr = ccrs.Orthographic(central_longitude=0.0, central_latitude=0.0)
          plateCr = ccrs.Orthographic(central_longitude=0.25*180, central_latitude=180/6.0)


      projection=ccrs.PlateCarree(central_longitude=0)
      plateCr._threshold = plateCr._threshold/10. 
      ax = plt.axes(projection=plateCr)
      ax.set_global()
      ax.stock_img()
      ax.gridlines(draw_labels=True)

      im=plt.contourf(lon, lat, field[:,:,t], cmap='jet',  transform=ccrs.PlateCarree(), levels=np.linspace(fmin,fmax,100))
      title ="TC"+str(tc)+" - "+name+" - time (days) = "+str(timedata[t]/sec2day)+" - "+str(N)+"x"+str(M) 
      plt.title(title)

      # Plot colorbar
      cax,kw = colorbar.make_axes(ax,orientation='vertical' , fraction=0.046, pad=0.04, shrink=0.8, format='%.1e')
      cb=plt.colorbar(im, cax=cax, extend='both',**kw)
      cb.ax.tick_params(labelsize=8)
      filename = "eg_swe_run_ic"+str(tc)+"_cor1_"+name+"_t"+str(timedata[t])+"_"+str(N)+"x"+str(M)
      plt.savefig(graphdir+filename+'.'+figformat, format=figformat)
      print('plotted ', filename)
      #plt.show()
      plt.close()

exit()

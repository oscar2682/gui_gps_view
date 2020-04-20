"""
Rutinas para procesar y visualizar
datos GPS
Oscar A. Castro-Artola, Instituto de Geofisica, marzo de 2015
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sys import exit

num_ticks = 10

def t_ticks(start,end,num_ticks):
    """
    t: time vector in seconds (float)
    num_ticks: number of ticks
    start: start time in seconds (float)
    end: end time in seconds (float)
    """
    from obspy.core import read, UTCDateTime
    from time import gmtime, strftime, strptime
    import datetime as dt

    t_ticks = np.linspace(start,end,num_ticks)
    t_labels = []
    for i in t_ticks:
        time,jaday = decimalYear(i)
        t_label = time.strftime('%d/%m/%Y')
        t_labels.append(t_label)

    return t_ticks,t_labels

def decimalYear(datein):
    from calendar import isleap
    from obspy.core import UTCDateTime
    from numpy import ceil,floor
    year = int(datein)
    if isleap(year) is True:
        jdays = 366
    else:
        jdays = 365
    jday_dec = datein % 1
    jday = ceil(jday_dec*jdays)
    hours = int(jday_dec*24)
    timeUTC = UTCDateTime(year=year, julday=jday, hour=hours)

    return timeUTC,jdays

def rem_mean(date,data,error):
    """
    Remove mean in time and data.
    Ready to plot.
    """
    data=data/100
    unos=np.ones((len(data),1))
    eln=1e4*unos/(error**2)
    dat=np.mean(eln*data)*unos/np.sum(eln)+data
    Tm=np.mean(date)
    date=date-Tm*unos
    dat=dat-np.mean(dat)
    date=date+Tm*unos

    return date,dat

def plot_one(file, formato, debuger=False):
    """
    Grafica un archivo GPS con el formato indicado en
    como entrada.
    """
    global num_ticks
    if formato == 'vladi':
        archivo=open(file,'r')
        datos=archivo.readlines()[3:]
        sta_name=file[-13:-9]
        comp=file[-1]
        comp_name=['']
        if (comp == '1'):
          comp_name='NS'
        elif (comp=='2'):
          comp_name='EW'
        elif (comp=='3'):
          comp_name='Z'
        date=np.zeros((len(datos),1))
        data=np.zeros((len(datos),1))
        dat=np.zeros((len(datos),1))
        error=np.zeros((len(datos),1))
        for i,lineas in enumerate(datos):
            date[i],data[i],error[i]=lineas.split()[0],lineas.split()[1],lineas.split()[2]
        a,b = rem_mean(date,data,error)
        ticks,labels = t_ticks(a[0],a[-1],num_ticks)
        b = b * 1e5
    elif formato == 'sara':
        archivo=open(file[0],'r')
        datos=archivo.readlines()
        sta_name=file[-8:-4]
        comp=file[-12:-9]
        comp_name=['']
        if (comp == 'lat'):
          comp_name='NS'
        elif (comp=='ong'):
          comp_name='EW'
        elif (comp=='ght'):
          comp_name='Z'
        date=np.zeros((len(datos),1))
        data=np.zeros((len(datos),1))
        dat=np.zeros((len(datos),1))
        error=np.zeros((len(datos),1))
        for i,lineas in enumerate(datos):
            date[i],data[i],error[i]=lineas.split()[0],lineas.split()[1],lineas.split()[2]
        a,b = rem_mean(date,data,error)
        ticks,labels = t_ticks(a[0],a[-1],num_ticks)
        b = b * 1e5
    elif formato == 'cabral':
        archivo=open(file,'r')
        datos=archivo.readlines()[1:]
        sta_name=file[-4:]
        comp=file[-9:-5]
        if (comp == 'orth'):
          comp_name='NS'
          date=np.zeros((len(datos),1))
          data=np.zeros((len(datos),1))
          dat=np.zeros((len(datos),1))
          error=np.zeros((len(datos),1))
          for i,lineas in enumerate(datos):
              date[i],data[i],error[i]=lineas.split()[0],lineas.split()[1],lineas.split()[8]
        elif (comp=='east'):
          comp_name='EW'
          date=np.zeros((len(datos),1))
          data=np.zeros((len(datos),1))
          dat=np.zeros((len(datos),1))
          error=np.zeros((len(datos),1))
          for i,lineas in enumerate(datos):
              date[i],data[i],error[i]=lineas.split()[0],lineas.split()[1],lineas.split()[8]
        elif (comp=='vert'):
          comp_name='Z'
          date=np.zeros((len(datos),1))
          data=np.zeros((len(datos),1))
          dat=np.zeros((len(datos),1))
          error=np.zeros((len(datos),1))
          for i,lineas in enumerate(datos):
              date[i],data[i],error[i]=lineas.split()[0],lineas.split()[1],lineas.split()[6]
#        a,b = rem_mean(date,data,error)
        ticks,labels = t_ticks(date[0],date[-1],num_ticks)
        a = date
        b = data
    else:
        exit('[ERROR] Unrecognized format')

    # Se leen todas las lineas del archivo y se asigna a las variables
    # Se quita la media de los datos y del tiempo
    #ind = np.where(a >= 2010)
    #a = a[ind[0]]
    #b = b[ind[0]]

    sta_name=str(sta_name).upper()
    plt.figure()
    plt.plot(a,b,'ro',ms=3.0,alpha=0.5)
    plt.xlabel('Years since %4.1f'% (date[0]))
    plt.ylabel('Milimeters')
    plt.xticks(ticks,labels,rotation=45)
    plt.grid()
    plt.xlim(a[0], a[-1])
    plt.title('%s - %s' % (sta_name,comp_name))
    plt.subplots_adjust(bottom=0.15)
    plt.show()

def plot_three(estacion,formato):
    """
    Grafica un archivo GPS con el formato indicado en
    como entrada.
    """
    global num_ticks

    if formato == 'vladi':
        ruta='/home/oscar/Doctorado/GPS/programas/python/datos_vladi/completos/'
        ns_file = ruta + 'mb_' + estacion.upper() + '_GP0.dat1'
        ew_file = ruta + 'mb_' + estacion.upper() + '_GP0.dat2'
        up_file = ruta + 'mb_' + estacion.upper() + '_GP0.dat3'
        ns_archivo=open(ns_file,'r')
        ew_archivo=open(ew_file,'r')
        up_archivo=open(up_file,'r')
        ns_datos=ns_archivo.readlines()[3:]
        ew_datos=ew_archivo.readlines()[3:]
        up_datos=up_archivo.readlines()[3:]
        ns_date=np.zeros((len(ns_datos),1))
        ns_data=np.zeros((len(ns_datos),1))
        ns_dat=np.zeros((len(ns_datos),1))
        ns_error=np.zeros((len(ns_datos),1))
        for i,lineas in enumerate(ns_datos):
            ns_date[i],ns_data[i],ns_error[i]=lineas.split()[0],lineas.split()[1],lineas.split()[2]
        ns_x,ns_y = rem_mean(ns_date,ns_data,ns_error)
        ns_ticks,ns_labels = t_ticks(ns_x[0],ns_x[-1],num_ticks)
        ns_y = ns_y *1e5
        ew_date=np.zeros((len(ew_datos),1))
        ew_data=np.zeros((len(ew_datos),1))
        ew_dat=np.zeros((len(ew_datos),1))
        ew_error=np.zeros((len(ew_datos),1))
        for i,lineas in enumerate(ew_datos):
            ew_date[i],ew_data[i],ew_error[i]=lineas.split()[0],lineas.split()[1],lineas.split()[2]
        ew_x,ew_y = rem_mean(ew_date,ew_data,ew_error)
        ew_ticks,ew_labels = t_ticks(ew_x[0],ew_x[-1],num_ticks)
        ew_y = ew_y *1e5
        up_date=np.zeros((len(up_datos),1))
        up_data=np.zeros((len(up_datos),1))
        up_dat=np.zeros((len(up_datos),1))
        up_error=np.zeros((len(up_datos),1))
        for i,lineas in enumerate(up_datos):
            up_date[i],up_data[i],up_error[i]=lineas.split()[0],lineas.split()[1],lineas.split()[2]
        up_x,up_y = rem_mean(up_date,up_data,up_error)
        up_ticks,up_labels = t_ticks(up_x[0],up_x[-1],num_ticks)
        up_y = up_y *1e5
    elif formato == 'sara':
        ruta = '/home/oscar/Doctorado/GPS/programas/python/datos_sara/'
        ns_file = ruta + estacion.upper() + '/lat.' + estacion.lower() + '.dat'
        ew_file = ruta + estacion.upper() + '/long.' + estacion.lower() + '.dat'
        up_file = ruta + estacion.upper() + '/height.' + estacion.lower() + '.dat'
        ns_archivo=open(ns_file,'r')
        ew_archivo=open(ew_file,'r')
        up_archivo=open(up_file,'r')
        ns_datos=ns_archivo.readlines()
        ew_datos=ew_archivo.readlines()
        up_datos=up_archivo.readlines()
        ns_date=np.zeros((len(ns_datos),1))
        ns_data=np.zeros((len(ns_datos),1))
        ns_dat=np.zeros((len(ns_datos),1))
        ns_error=np.zeros((len(ns_datos),1))
        for i,lineas in enumerate(ns_datos):
            ns_date[i],ns_data[i],ns_error[i]=lineas.split()[0],lineas.split()[1],lineas.split()[2]
        ns_x,ns_y = rem_mean(ns_date,ns_data,ns_error)
        ns_ticks,ns_labels = t_ticks(ns_x[0],ns_x[-1],num_ticks)
        ns_y = ns_y *1e5
        ew_date=np.zeros((len(ew_datos),1))
        ew_data=np.zeros((len(ew_datos),1))
        ew_dat=np.zeros((len(ew_datos),1))
        ew_error=np.zeros((len(ew_datos),1))
        for i,lineas in enumerate(ew_datos):
            ew_date[i],ew_data[i],ew_error[i]=lineas.split()[0],lineas.split()[1],lineas.split()[2]
        ew_x,ew_y = rem_mean(ew_date,ew_data,ew_error)
        ew_ticks,ew_labels = t_ticks(ew_x[0],ew_x[-1],num_ticks)
        ew_y = ew_y *1e5
        up_date=np.zeros((len(up_datos),1))
        up_data=np.zeros((len(up_datos),1))
        up_dat=np.zeros((len(up_datos),1))
        up_error=np.zeros((len(up_datos),1))
        for i,lineas in enumerate(up_datos):
            up_date[i],up_data[i],up_error[i]=lineas.split()[0],lineas.split()[1],lineas.split()[2]
        up_x,up_y = rem_mean(up_date,up_data,up_error)
        up_ticks,up_labels = t_ticks(up_x[0],up_x[-1],num_ticks)
        up_y = up_y *1e5
    elif formato == 'cabral':
        ruta = '/home/oscar/Doctorado/GPS/programas/python/datos_enrique_cabral/'
        ns_file = ruta + 'north_' + estacion.upper()
        ew_file = ruta + 'east_' + estacion.upper()
        up_file = ruta + 'vert_' + estacion.upper()
        ns_archivo=open(ns_file,'r')
        ew_archivo=open(ew_file,'r')
        up_archivo=open(up_file,'r')
        ns_datos=ns_archivo.readlines()[1:]
        ew_datos=ew_archivo.readlines()[1:]
        up_datos=up_archivo.readlines()[1:]
        ns_date=np.zeros((len(ns_datos),1))
        ns_data=np.zeros((len(ns_datos),1))
        ns_dat=np.zeros((len(ns_datos),1))
        ns_error=np.zeros((len(ns_datos),1))
        for i,lineas in enumerate(ns_datos):
            ns_date[i],ns_data[i],ns_error[i]=lineas.split()[0],lineas.split()[1],lineas.split()[8]
        ns_x = ns_date
        ns_y = ns_data
        ns_ticks,ns_labels = t_ticks(ns_x[0],ns_x[-1],num_ticks)
        ew_date=np.zeros((len(ew_datos),1))
        ew_data=np.zeros((len(ew_datos),1))
        ew_dat=np.zeros((len(ew_datos),1))
        ew_error=np.zeros((len(ew_datos),1))
        for i,lineas in enumerate(ew_datos):
            ew_date[i],ew_data[i],ew_error[i]=lineas.split()[0],lineas.split()[1],lineas.split()[8]
        ew_x = ew_date
        ew_y = ew_data
        ew_ticks,ew_labels = t_ticks(ew_x[0],ew_x[-1],num_ticks)
        up_date=np.zeros((len(up_datos),1))
        up_data=np.zeros((len(up_datos),1))
        up_dat=np.zeros((len(up_datos),1))
        up_error=np.zeros((len(up_datos),1))
        for i,lineas in enumerate(up_datos):
            up_date[i],up_data[i],up_error[i]=lineas.split()[0],lineas.split()[1],lineas.split()[6]
        up_x = up_date
        up_y = up_data
        up_ticks,up_labels = t_ticks(up_x[0],up_x[-1],num_ticks)
    else:
        exit('[ERROR] Unrecognized format')

    ind = np.where(ns_x >= 2000)
    ns_x = ns_x[ind[0]]
    ns_y = ns_y[ind[0]]
    ind = np.where(ew_x >= 2000)
    ew_x = ew_x[ind[0]]
    ew_y = ew_y[ind[0]]
    ind = np.where(up_x >= 2000)
    up_x = up_x[ind[0]]
    up_y = up_y[ind[0]]

    plt.figure(num=None, figsize=(7, 13))
    plt.subplots_adjust(wspace=.05)
    plt.subplot(3,1,1)
    plt.grid()
    plt.plot(ns_x,ns_y,'ro',mec='green',mfc='red',mew=.5,ms=3.0,alpha=0.5)
    plt.ylabel('Milimeters')
    plt.xticks(ns_ticks,ns_labels,rotation=30)
    plt.xlim(ns_x[0], ns_x[-1])
    plt.title('%s - %s' % (estacion.upper(),'NS'))
    plt.subplot(3,1,2)
    plt.grid()
    plt.plot(ew_x,ew_y,'ro',mec='blue',mfc='red',mew=.5,ms=3.0,alpha=0.5)
    plt.ylabel('Milimeters')
    plt.xticks(ew_ticks,ew_labels,rotation=30)
    plt.xlim(ns_x[0], ns_x[-1])
    plt.title('%s - %s' % (estacion.upper(),'EW'))
    plt.subplot(3,1,3)
    plt.grid()
    plt.plot(up_x,up_y,'ro',mec='blue',mfc='green',mew=.5,ms=3.0,alpha=0.5)
    plt.xlabel('Years since %4.1f'% (up_date[0]))
    plt.ylabel('Milimeters')
    plt.xticks(up_ticks,up_labels,rotation=30)
    plt.xlim(ns_x[0], ns_x[-1])
    plt.title('%s - %s' % (estacion.upper(),'UP'))
    plt.subplots_adjust(bottom=0.1, top=0.95, hspace=.43)
#   plt.savefig(estacion.upper()+'_'+formato+'.jpg',dpi=300)
    plt.show()

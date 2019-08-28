from multiprocessing import Pool
from functools import partial

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from .main import RadianceObj,AnalysisObj, _popen

Path.ls = lambda x: sorted(list(x.iterdir()))



metadata = {'Name': 'Chamberytown',
            'latitude': 45.637, 
            'longitude': 5.881, 
            'altitude': 235.0, 
            'State':'NZ', 
            'USAF':1, 
            'TZ':0}


def get_time_interval(inca, date):
    sl = inca.input_meteo.index.get_loc(date)
    if type(sl) is slice:
        return sl.start, sl.stop
    else: return (sl, sl+1)


def read_meteo_file(ines_meteo_file):
    meteo = pd.read_hdf(ines_meteo_file, key='df')
    return meteo.meteo[['ghi', 'dni', 'dhi']].rename(columns=str.upper)

def define_meteo(inca, ines_meteo_file):
    inca.input_meteo = read_meteo_file(ines_meteo_file)
    return inca.readInesMeteoFile(inca.input_meteo, metadata)

def define_scene(inca, monitor=5):
    mod1 = 'test'
    inca.makeModule(name=mod1,x=0.99,y=1.65,numpanels = 1,xgap=0.04,ygap=0.05)
    mod2 = 'prismSolar'
    inca.makeModule(name=mod2, x=0.99,y=1.65,numpanels = 2,xgap=0.04,ygap=0.05)
    sceneObjs = []
    sceneDict1 = {'tilt':30,'pitch': 9.5,'clearance_height':1.63,'azimuth':180, 'nMods': 1, 'nRows': 2, 'appendRadfile':True,'originx': -3.09, 'originy': 0.736} 
    sceneObjs += [inca.makeScene(moduletype=mod1,sceneDict=sceneDict1, hpc=True)]

    sceneDict2 = {'tilt':30,'pitch': 9.5,'clearance_height':0.9,'azimuth':180, 'nMods': 5, 'nRows': 2, 'appendRadfile':True,'originx': 0, 'originy': 0} 
    sceneObjs += [inca.makeScene(moduletype=mod2,sceneDict=sceneDict2, hpc=True)]

    sceneDict3 = {'tilt':30,'pitch': 9.5,'clearance_height':1.63,'azimuth':180, 'nMods': 1, 'nRows': 2, 'appendRadfile':True,'originx': 3.09, 'originy': 0.736} 
    sceneObjs += [inca.makeScene(moduletype=mod1,sceneDict=sceneDict3, hpc=True)]

    sceneDict4 = {'tilt':30,'pitch': 9.5,'clearance_height':0.9,'azimuth':180, 'nMods': 5, 'nRows': 2, 'appendRadfile':True,'originx': 6.17, 'originy': 0} 
    sceneObjs += [inca.makeScene(moduletype=mod2,sceneDict=sceneDict4, hpc=True)]

    sceneDict5 = {'tilt':30,'pitch': 9.5,'clearance_height':0.9,'azimuth':180, 'nMods': 5, 'nRows': 2, 'appendRadfile':True,'originx': -6.17, 'originy': 0} 
    sceneObjs += [inca.makeScene(moduletype=mod2,sceneDict=sceneDict5, hpc=True)]

    sceneDict6 = {'tilt':30,'pitch': 9.5,'clearance_height':0.9,'azimuth':180, 'nMods': 5, 'nRows': 2, 'appendRadfile':True,'originx': -12.36, 'originy': 0} 
    sceneObjs += [inca.makeScene(moduletype=mod2,sceneDict=sceneDict6, hpc=True)]

    sceneDict7 = {'tilt':30,'pitch': 9.5,'clearance_height':0.9,'azimuth':180, 'nMods': 5, 'nRows': 2, 'appendRadfile':True,'originx': 12.36, 'originy': 0} 
    sceneObjs += [inca.makeScene(moduletype=mod2,sceneDict=sceneDict7, hpc=True)]
    
    inca.monitored_obj = sceneObjs[monitor]
    return inca.monitored_obj


def genbox(inca, 
           name, 
           scene_name='customScene.rad', 
           material='Metal_Aluminum_Anodized',  
           dim=(1.0,1.0,1.0), 
           r=(0,0,0), 
           t=(0.0,0.0,0.0), 
           hpc=True):
    genbox_cmd = f'!genbox {material} {name} {dim[0]} {dim[1]} {dim[2]} '
    xform_cmd = f'| xform -rx {r[0]} -ry {r[1]} -rz {r[2]} -t {t[0]} {t[1]} {t[2]}'
    cmd = genbox_cmd + xform_cmd
    box = inca.makeCustomObject(name, cmd)
    inca.appendtoScene(scene_name, box,  hpc=hpc)
    return

def add_vert_posts(inca,    
                    scene_name='customScene.rad', 
                    material='Metal_Aluminum_Anodized',
                    hpc=True):
    genbox(inca,'vert_post1', scene_name, material, dim=(0.12, 0.24, 0.77), t=(-15.965, -1.45, 0), hpc=hpc)
    genbox(inca,'vert_post2', scene_name, material, dim=(0.12, 0.24, 0.77), t=(-12.8750, -1.45, 0), hpc=hpc)
    genbox(inca,'vert_post3', scene_name, material, dim=(0.12, 0.24, 0.77), t=(-9.785, -1.45, 0), hpc=hpc)
    genbox(inca,'vert_post4', scene_name, material, dim=(0.12, 0.24, 0.77), t=(-6.685, -1.45, 0), hpc=hpc)
    genbox(inca,'vert_post5', scene_name, material, dim=(0.12, 0.24, 0.77), t=(-3.595, -1.45, 0), hpc=hpc)
    genbox(inca,'vert_post6', scene_name, material, dim=(0.12, 0.24, 0.77), t=(5.655, -1.45, 0), hpc=hpc)
    genbox(inca,'vert_post7', scene_name, material, dim=(0.12, 0.24, 0.77), t=(8.745, -1.45, 0), hpc=hpc)
    return

def add_diag_posts(inca,    
                    scene_name='customScene.rad', 
                    material='Metal_Aluminum_Anodized',
                    hpc=True):
    genbox(inca,'diag_post1', scene_name, material, dim=(0.12, 0.24, 3.4), r=(-60,0,0), t=(-15.965, -1.45, 0.77), hpc=hpc)
    genbox(inca,'diag_post2', scene_name, material, dim=(0.12, 0.24, 3.4), r=(-60,0,0), t=(-12.8750, -1.45, 0.77), hpc=hpc)
    genbox(inca,'diag_post3', scene_name, material, dim=(0.12, 0.24, 3.4), r=(-60,0,0), t=(-9.785, -1.45, 0.77), hpc=hpc)
    genbox(inca,'diag_post4', scene_name, material, dim=(0.12, 0.24, 3.4), r=(-60,0,0), t=(-6.685, -1.45, 0.77), hpc=hpc)
    genbox(inca,'diag_post5', scene_name, material, dim=(0.12, 0.24, 3.4), r=(-60,0,0), t=(-3.595, -1.45, 0.77), hpc=hpc)
    genbox(inca,'diag_post6', scene_name, material, dim=(0.12, 0.24, 3.4), r=(-60,0,0), t=(5.655, -1.45, 0.77), hpc=hpc)
    genbox(inca,'diag_post7', scene_name, material, dim=(0.12, 0.24, 3.4), r=(-60,0,0), t=(8.745, -1.45, 0.77), hpc=hpc)
    return

    
def add_box(inca):
    name='Boite_electrique'
    text='! genbox beigeroof originMarker 0.12 0.20 0.24 | xform -t -12.875 0.35 1.30'
    customObject = inca.makeCustomObject(name,text)
    inca.appendtoScene(inca.scene.radfiles, customObject, '!xform -rz 0', hpc=True)

    name='cables'
    text='! genbox beigeroof originMarker 0.04 0.100 0.07 | xform -t -12.83 0.35 1.24'
    customObject = inca.makeCustomObject(name,text)
    inca.appendtoScene(inca.scene.radfiles, customObject, '!xform -rz 0', hpc=True)

    return

def add_ref_cell(inca):
    moduletype_refCell = 'celda_ref'
    inca.makeModule(name=moduletype_refCell,x=0.12,y=0.12,numpanels = 1)
    sceneRef_rCell = {'tilt':30,'pitch': 9.5,'clearance_height':1.25,'azimuth':180, 'nMods': 1, 'nRows': 1, 'appendRadfile':True,'originx': -12.815, 'originy': 0.15} 
    sceneObj_rCell = inca.makeScene(moduletype=moduletype_refCell, sceneDict=sceneRef_rCell, hpc=True)
    return sceneObj_rCell

def compute_radiance(timeindex, inca, sim_name='sim', sensorsy=9):
    if (((inca.metdata.ghi[timeindex] >= 10) or (inca.metdata.dni[timeindex]>10))
        and inca.metdata.dhi[timeindex]>10
        and inca.metdata.solpos.iloc[timeindex, 3]>1
        and inca.metdata.solpos.iloc[timeindex, 3]<89):
        skyname = inca.gendaylit(inca.metdata,timeindex) 
        filelist = inca.getfilelist()
        filelist[1] = skyname
        def _format_dt(dt):
            return f'{dt.day}-{dt.month}-{dt.year}_{dt.time()}'
        octfile = inca.makeOct(filelist, octname = sim_name + _format_dt(inca.metdata.datetime[timeindex]) )
        analysis = AnalysisObj(octfile, inca.basename) 
        # frontscan, backscan = analysis.moduleAnalysis(inca.monitored_obj, 2, 1)#(scene, modWanted = modWanted, rowWanted = rowWanted, sensorsy=sensorsy)
        frontscan, backscan = analysis.moduleAnalysis(inca.monitored_obj, sensorsy=sensorsy)
        front, back = analysis.analysis(octfile, 'output', frontscan, backscan) 
        return front['Wm2'] + back['Wm2']
    else:
        return [0]*(2*sensorsy)


def delete_oct_files(project_path):
    for f in project_path.glob('*.oct'):
        f.unlink()
    print(f'Deleted .oct files')
    return

def delete_rad_files(project_path):
    for f in (project_path).glob('*/*.rad'):
        f.unlink()
    print(f'Deleted .rad files')
    return

def view_timeindex(filename, view='box', program='rvu'):
    if program == 'rpict': output = ' > render.pic' 
    else: output = ''
    if view == 'diag':
        cmd = program + ' -vp -17 3 1 -vd 2 -1 -0.3 -vu 0 0 1 -av 0.2 0.2 0.2 '  + filename + output
    elif view == 'side':
        cmd = program + ' -vp -14.3 0.2 1.5 -vd 1 0 0 -vu 0 0 1 -av 0.2 0.2 0.2 '  + filename + output
    elif view == 'back':
        cmd = program + ' -vp -12.815 2 1 -vd 0 -1 0 -vu 0 0 1 -av 0.2 0.2 0.2 '  + filename + output
    elif view == 'front':
        cmd = program + ' -vp 0 -40 25 -vd 0 1 -0.5 -vu 0 0 1 -av 0.2 0.2 0.2 '  + filename + output
    return _popen(cmd, None)


if __name__ == '__main__':

    project_name = 'IncaFixed'
    # lspv_path = Path("C:/Users/tc256760/Documents/Modelisation Framework/lspv_analyseSoft")
    lspv_path = Path.home()/Path("Documents/lspv_analyseSoft")
    # ines_meteo_file = lspv_path/'Inca/tmy_INCA_bifi_1H.hdf'

    project_path = lspv_path/'RayTracing_simulations/dev_nbs'/project_name
    if not project_path.exists(): project_path.mkdir()
    sim_name = 'inca_period_test'
    ines_meteo_file = Path.home()/'DATA/INCA/chic_bi3p/tmy_INCA_bifi_1H.hdf'
    sensorsy=9
    inca = RadianceObj(sim_name, str(project_path.absolute())) # Radiance object named inca_first_test
    define_scene(inca)
    define_meteo(inca, ines_meteo_file)
    
    date = '18 July 2017'
    ti, tf = get_time_interval(inca, date)
    print(f'Timeindexes : {ti}, {tf}')
    
    f = partial(compute_radiance, inca=inca, sim_name=sim_name)
    p = Pool(6)
    res_list = p.map(f, range(ti,tf))
    p.close()
    p.join()

    res_df = pd.DataFrame(data=res_list, index = inca.input_meteo[date].index, 
                          columns = [f'g_{i}' for i in range(sensorsy)]+[f'gb_{i}' for i in range(sensorsy)])

    res_df.to_hdf(project_path/'sim_18jul.hdf', key='df')
    res_df.to_csv(project_path/'sim_18jul.csv')

    print("THE END")
from scipy.io import loadmat
import numpy
import pandas as pd

def load(num):
    '''
        Load battery data from mat file and return dataframe for training
    '''
    FILE_NAME = f'/home/jovyan/work/data/nasa/batteries/RW{num}.mat'
    matlab_structure = loadmat(FILE_NAME)
    mdata = matlab_structure['data']  # variable in mat file 
    ndata = {n: mdata[n][0,0] for n in mdata.dtype.names}
    step_data = ndata['step'][0]
    comment = [n[0][0]  for n in step_data ]
    time = [n[2][0]  for n in step_data]
    current = [n[5][0]  for n in step_data]
    temperature = [n[6][0]  for n in step_data ]
    step_dict = { "step": comment, "time": time,  "current": current}
    df = pd.DataFrame.from_dict(step_dict)
    df = df[df['step']=='reference discharge']
    df.insert(2, 'capacity', 0)
    df["capacity"] = df.apply(lambda df: numpy.trapz(df['current'], df['time']) / 3600, axis=1)
    df["time"] = df.apply(lambda df: df['time'][len(df['time'])//2]/3600, axis=1)
    df = df.drop(columns=['step', 'current'])
    df.insert(0, 'battery', num)
    return df

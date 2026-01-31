import numpy as np

def getStitchedFrame(frameDict):
    return np.concatenate([frameDict[f"{i}"] for i in range(len(frameDict))], axis=1)
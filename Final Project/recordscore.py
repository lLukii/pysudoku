# File used to record high score (Pretty small file but still made for the sake of organization.) Made by Lucas Yichen Jiao. 

from pathlib import Path
import pickle

def file_io(score):
    # load high score
    try:
        with open("score.dat", "rb") as f:
            hs = pickle.load(f)
        
    except: 
        hs = 2**63-1
    
    # evaluate user score
    with open("score.dat", "wb") as f:
        pickle.dump(min(hs, score), f)
    
    print(hs)
    print(score)
    # return current high score. 
    return min(hs, score)
        

from torch.utils.data import Dataset
import pandas as pd
import pymongo

def pack():
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['face']
    figure_meta = db['figure']
    #  path face times
    score_col = db['score']

    for x in score_col.find():



from torch.utils.data import Dataset
import pandas as pd
import pymongo

def pack():
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['face']
    figure_meta = db['figure']
    #  path face times width height x y
    score_col = db['score']
    # id path score 0 error 1 up 2 down 3 left 4 right

    score = dict()

    score_cnt = 0

    for x in score_col.find():
        print(x)
        score_cnt += 1
        if x['path'] not in score:
            score['path'] = [0, 0, 0, 0, 0]
        else:
            score['path'][x['score']] += 1

    print('Label times:', score_cnt)


if __name__ == '__main__':
    pack()
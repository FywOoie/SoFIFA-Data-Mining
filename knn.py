import numpy as np
import sqlite3
from sklearn.metrics import accuracy_score
import torch
import creepper as cre
import tqdm
import time

con = sqlite3.connect('players.db')
cursorObj = con.cursor()
select_sql = 'select * from players'
results = cursorObj.execute(select_sql)

trainData = []
testData = []
trainLabel = []
testLabel = []
count = 0
for info in results.fetchall():
    if count < 8000:
        trainData.append([int(info[3]), info[4], info[5]])
        trainLabel.append(info[6])
    else:
        testData.append([int(info[3]), info[4], info[5]])
        testLabel.append(info[6])
    count += 1

# 定义KNN函数
def KNN(train_x, train_y, test_x, test_y, k):
    since = time.time()
    test_y.append(0)
    m = test_x.size(0)
    n = train_x.size(0)

    xx = (test_x ** 2).sum(dim=1, keepdim=True).expand(m, n)
    yy = (train_x ** 2).sum(dim=1, keepdim=True).expand(n, m).transpose(0, 1)
    dist_mat = xx + yy - 2 * test_x.matmul(train_x.transpose(0, 1))
    mink_idxs = dist_mat.argsort(dim=-1)
    res = []
    for idxs in mink_idxs:
        res.append(np.bincount(np.array([train_y[idx] for idx in idxs[:k]])).argmax())

    assert len(res) == len(test_y)
    print("acc", accuracy_score(test_y, res))
    time_elapsed = time.time() - since
    print('KNN mat training complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))
    return res[-1]

def cal_distance(x, y):
    return torch.sum((x - y) ** 2) ** 0.5
def KNN_by_iter(train_x, train_y, test_x, test_y, k):
    since = time.time()
    res = []
    for x in tqdm(test_x):
        dists = []
        for y in train_x:
            dists.append(cal_distance(x, y).view(1))
        #torch.cat()用来拼接tensor
        idxs = torch.cat(dists).argsort()[:k]
        res.append(np.bincount(np.array([train_y[idx] for idx in idxs])).argmax())

    print("acc", accuracy_score(test_y, res))
    time_elapsed = time.time() - since
    print('KNN iter training complete in {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))

test = [26,78,89]
testData.append(test)
trainData = torch.tensor(trainData)
testData =  torch.tensor(testData)
re = KNN(trainData, trainLabel, testData, testLabel, 10)
print(cre.label2class.get(re))

# KNN_by_iter(trainData, trainLabel, testData, testLabel, 10)
# print(cre.label2class.get(re))

con.close()
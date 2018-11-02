#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 22:24:36 2018

@author: Phoebe
"""
import numpy as np

path = "/Users/Phoebe/Desktop/data/input/"
filename = "train.csv"
f = open(path+filename, 'r', encoding = 'UTF-8-sig')

feature = []
labels = []
maxlab = []
meanlab = []
for line in f:
    r = line.split(',')
    f = np.array(r[:600]).astype(float)
    feature.append(f)
    l = np.array(r[600:]).astype(int)
    labels.append(l)
    maxlab.append(int(r[600]))
    meanlab.append(int(r[601]))

print(len(feature),len(feature[0]),len(labels[0]))
print(labels[0], maxlab[0], meanlab[0])


filename2 = "combinedtest.csv"
f2 = open(path+filename2, 'r', encoding = 'UTF-8-sig')

tfeature = []
tlabels = []
tmaxlab = []
tmeanlab = []
for line in f2:
    r = line.split(',')
    f = np.array(r[:600]).astype(float)
    
    tfeature.append(f)
    l = np.array(r[600:]).astype(int)
    tlabels.append(l)
    tmaxlab.append(int(r[600]))
    tmeanlab.append(int(r[601]))

print(len(tfeature),len(tfeature[0]),len(tlabels[0]))
print(tlabels[0], tmaxlab[0], tmeanlab[0])


'''
random forest
'''
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

max_clf = RandomForestClassifier(n_estimators = 300, max_features = 600, 
                             max_depth = None, min_samples_split = 2, 
                             oob_score = False, n_jobs = -1)
#clf.fit(feature, labels)
#score = clf.score(tfeature, tlabels)
#print(score)
max_clf.fit(feature, maxlab)
max_score = max_clf.score(tfeature, tmaxlab)
print("accuracy for max drop rate:%s"%max_score)

mean_clf = max_clf
mean_clf.fit(feature, maxlab)
mean_score = mean_clf.score(tfeature, tmaxlab)
print("accuracy for mean drop rate:%s"%mean_score)
#scores = cross_val_score(clf, feature, labels, cv=5)
#print(scores.mean())


"""
Given a prediction compute the grading and a submission file
"""

import numpy as np
import string
import random,string,math,csv
from sklearn.naive_bayes import GaussianNB

def print_submission(testIDs, RankOrder, yLabels):
    """
    Creates the csv submission file
    ----------
    Inputs:
    ----------
        testIDs: np.array(int, size :Test DataSet Size)
        vecors of the IDs of the test examples

        RankOrder: np.array(int, size :Test DataSet Size)
        vecors of the ranks : the higher is the rank, the most likely the label is to be 's'

        yLabels: np.array(binary (1 or 0),size:Test DataSet Size)
        vecors of the labels of the test examples (1 for label 's', 0 for label 'b')

    ----------
    Outputs:
    ----------
        [0] : np.array(string, size:(Test DataSet Size, 3))
        np array in the submission format (includes the header : EventId,RankOrder,Class)

    """

    sub = np.array([[str(testIDs[i]), str(RankOrder[i]), 's' if yLabels[i] == 1 else 'b'] for i in range(len(testIDs))])
    sub = sub[sub[:,0].argsort()]
    sub = np.append([['EventID', 'RankOrder', 'Class']], sub, axis = 0)

    np.savetxt("submission.csv",sub,fmt='%s',delimiter=',')

    return sub


def get_yPredicted_s(xsTrain_s, yTrain_s, xsValidation_s):
    yPredicted_s = []
    yProba_s = []
    gnb = GaussianNB()
    #forest = RandomForestClassifier()
    for n in range(8):
        gnb.fit(xsTrain_s[n], yTrain_s[n])
        yPredicted_s.append(gnb.predict(xsValidation_s[n]))
        yProba_s.append(gnb.predict_proba(xsValidation_s[n]))
        #forestClassifier = forest.fit(xsTrain_s[n], yTrain_s[n])
        #yPredicted_s.append(forestClassifier.predict(xsValidation_s[n]))
    return yPredicted_s, yProba_s



def get_s_b(yPredicted, yValidation, weightsValidation):
    """
    takes in inpuy the vector of predicted label on the validation set,
    the vector of real label of the validation set and the vector of weights on the validation set,
    and returns the weighted sum of the real positive (s) and the the weighted sum of the real negative (b)
    """
    if yPredicted.shape != yValidation.shape or yValidation.shape != weightsValidation.shape:
        print "Bad inputs shapes. Inputs must be the same size"
        exit()

    s = np.dot(yPredicted*yValidation, weightsValidation)
    #yPredictedComp = np.ones(yPredicted.shape) - yPredicted #vector with label 0 for event and label 1 for non event
    yValidationComp = np.ones(yValidation.shape) - yValidation #vector with label 0 for event and label 1 for non event
    b = np.dot(yPredicted*yValidationComp, weightsValidation)

    return s, b


def get_s_b_8(yPredicted_s, yValidation_s, weightsValidation_s):
    final_s = 0.
    final_b =0.
    for n in range(8):
        s, b = get_s_b(yPredicted_s[n], yValidation_s[n], weightsValidation_s[n])
        final_s +=s
        final_b +=b

    return final_s, final_b
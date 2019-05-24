''' The functions in this module produce results related to the confusion matrix.
Functions are available to plot the confusion matrix including the kappa coefficient,
and calcuate error of commission, error of omission, producer's accuracy
and user's accuracy. '''

'''Note - documentation still needed for individual functions'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import cohen_kappa_score

def plot_conf_matrix(ytrue, ypred, cmap=plt.cm.Blues):
    cm = confusion_matrix(ytrue,ypred)
    print(cm)
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    print("")
    print("Accuracy score:", accuracy_score(ytrue, ypred))
    print("")
    print("Kappa coefficient: ", cohen_kappa_score(ytrue, ypred))
    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)

    ax.set(xticks=np.arange(4), xticklabels=['Predicted \n Shadow',
                                                       'Predicted \n Flood',
                                                       'Predicted \n Vegetation',
                                                       'Predicted \n Buildings'],
         yticks=np.arange(4), yticklabels=['True \n Shadow',
                                           'True \n Flood',
                                           'True \n Vegetation',
                                            'True \n Buildings'],
        title = "Normalized Confusion Matrix")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    plt.show()
    return ax

def oc_error_up_accuracy(cm, classes):
    row_sum_list = []
    false_neg_list = []
    omission_error_list = []
    producers_accuracy_list = []
    for i in range(4):
        row_sum=0
        for j in range(4):
            row_sum = cm[i,j]+row_sum
            if i == j:
                a = i
        row_sum_list.append(row_sum)
        false_neg = row_sum-cm[a,a]
        false_neg_list.append(false_neg)
        omission_error = false_neg/row_sum
        omission_error_list.append(omission_error)
        producers_accuracy = cm[a,a]/row_sum
        producers_accuracy_list.append(producers_accuracy)
    omission_error_df = pd.DataFrame(list(zip(classes,omission_error_list)), columns = ['Class','Error of Omission'])
    producers_accuracy_df = pd.DataFrame(list(zip(classes,producers_accuracy_list)), columns = ['Class','Producers Accuracy'])

    col_sum_list = []
    false_pos_list = []
    comission_error_list = []
    users_accuracy_list = []
    for j in range(4):
        col_sum=0
        for i in range(4):
            col_sum = cm[i,j]+col_sum
            if i == j:
                a = i
        col_sum_list.append(col_sum)
        false_pos = col_sum-cm[a,a]
        false_pos_list.append(false_pos)
        comission_error = false_pos/col_sum
        comission_error_list.append(comission_error)
        users_accuracy = cm[a,a]/col_sum
        users_accuracy_list.append(users_accuracy)
    users_accuracy_df = pd.DataFrame(list(zip(classes,users_accuracy_list)), columns = ['Class','Users Accuracy'])
    commission_error_df = pd.DataFrame(list(zip(classes,comission_error_list)), columns = ['Class','Error of Commission'])
    error_df = pd.merge(commission_error_df, omission_error_df, on='Class',how='left')
    accuracy_df = pd.merge(producers_accuracy_df, users_accuracy_df, on='Class',how='left')
    error_accuracy_df = pd.merge(error_df,accuracy_df,on='Class',how='left')
    return error_accuracy_df


def producers_accuracy(cm, classes):
    producers_accuracy_list = []
    for i in range(4):
        row_sum=0
        for j in range(4):
            row_sum = cm[i,j]+row_sum
            if i == j:
                a = i
        producers_accuracy = cm[a,a]/row_sum
        producers_accuracy_list.append(producers_accuracy)
    producers_accuracy_df = pd.DataFrame(list(zip(classes,producers_accuracy_list)), columns = ['Class','Producers Accuracy'])
    return producers_accuracy_df


def users_accuracy(cm, classes):
    users_accuracy_list = []
    for j in range(4):
        col_sum=0
        for i in range(4):
            col_sum = cm[i,j]+col_sum
            if i == j:
                a = i
        users_accuracy = cm[a,a]/col_sum
        users_accuracy_list.append(users_accuracy)
    commissionError_df = pd.DataFrame(list(zip(classes,users_accuracy_list)), columns = ['Class','Users Accuracy'])
    return commissionError_df

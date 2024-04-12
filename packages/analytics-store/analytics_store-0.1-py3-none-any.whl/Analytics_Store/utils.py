###################################
#
# THE ANALYTICS STORE
#
# Python Programming For Data Analytics
#
# Utility Functions
#
###################################


import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import export_graphviz


def data_viz(df):
    # Plot histograms for numeric columns
    for idx, col in enumerate(df.select_dtypes(include=[np.number]).keys()):
        df[col].plot.hist(title=col, rwidth=0.8)
        plt.show()

    # Plot bar plots  for categorical/boolean columns
    for idx, col in enumerate(df.select_dtypes(include=[object, bool]).keys()):
        # Only draw bar plots for variables with less than 30 levels
        if len(df[col].unique()) < 30:
            df[col].value_counts().plot.bar(title=col)
            plt.show()


def data_viz_target(df, target_feat):
    num_target_levels = len(df[target_feat].unique())

    for f in df.select_dtypes(include='number').columns:
        print(f)
        sns.displot(data=df,
                    x=f,
                    col=target_feat)
        plt.show()

    for f in df.select_dtypes(include='object').columns:
        print(f)
        sns.catplot(data=df,
                    x=f,
                    col=target_feat,
                    kind='count',
                    color='royalblue')
        plt.show()


# Method for calcualting Akaike's Information Criterion
def AIC(y_test, y_pred, k):
    """Calcualte Akaike's Information Criterion (AIC)
    Args
    ----
    y_test -- ground truth
    y_pred -- preedictions
    """
    resid = y_test - y_pred
    sse = sum(resid ** 2)
    aic = 2 * k - 2 * math.log(sse)
    return aic


def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


from IPython.display import display, HTML
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pandas_datareader import data #BB need: pip install pandas_datareader
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split, LeaveOneOut, KFold, cross_val_score

#from pandas.tools.plotting import table

#BB added 
# import numpy 
# import scipy 
# import scikit-learn //Machine Learning and Data Mining
# import tensorflow //machine learning 
'''

import json
import requests
import os
'''

import requests, json, fnmatch, os, os.path, sys, subprocess, glob, ntpath, copy, re, operator
from os import path
from pandas.io.json import json_normalize
from collections import Counter
from statistics import mean

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.preprocessing import StandardScaler #for PCA 

#to plot the graphs inline on jupyter notebook

import gen3
from gen3.auth import Gen3Auth
from gen3.submission import Gen3Submission
from gen3.file import Gen3File

class Gen3Error(Exception):
    pass


class Gen3Analysis(Gen3Submission):
    """Analysis functions for exploratory data analysis in a Gen3 Data Commons.

    A class for interacting with the Gen3 query and data export services.
    Supports generating tables and plots to explore data in a Gen3 Data Commons.

    Args:
        # endpoint (str): The URL of the data commons.
        # auth_provider (Gen3Auth): A Gen3Auth class instance.

    Examples:
        This generates the Gen3Analysis class pointed at the sandbox commons while
        using the credentials.json downloaded from the commons profile page.

        >>> endpoint = "https://nci-crdc-demo.datacommons.io"
        ... auth = Gen3Auth(endpoint, refresh_file="credentials.json")
        ... sub = Gen3Submission(endpoint, auth)
        ... analysis = Gen3Analysis(sub, auth)

    """

    def __init__(self, endpoint, auth_provider):
        self._auth_provider = auth_provider
        self._endpoint = endpoint

    def __export_file(self, filename, output):
        """Writes an API response to a file.
        """
        outfile = open(filename, "w")
        outfile.write(output)
        outfile.close
        print("\nOutput written to file: "+filename)


    def plot_categorical_property(self, df, property):
        #plot a bar graph of categorical variable counts in a dataframe
        df = df[df[property].notnull()]
        N = len(df)
        categories, counts = zip(*Counter(df[property]).items())
        y_pos = np.arange(len(categories))
        plt.bar(y_pos, counts, align='center', alpha=0.5)
        #plt.figtext(.8, .8, 'N = '+str(N))
        plt.xticks(y_pos, categories)
        plt.ylabel('Counts')
        plt.title(str('Counts by '+property+' (N = '+str(N)+')'))
        plt.xticks(rotation=90, horizontalalignment='center')
        #add N for each bar
        plt.show()


    def plot_categorical_property_by_order(self, df, property): 
        #plot a bar graph of categorical variable counts in a dataframe
        df = df[df[property].notnull()]
        N = len(df)
        categories, counts = zip(*df[property].value_counts().items())  #valuecounts orders it from largest to smallest 
        y_pos = np.arange(len(categories))
        plt.bar(y_pos, counts, align='center', alpha=0.5)
        #plt.figtext(.8, .8, 'N = '+str(N))
        plt.xticks(y_pos, categories)
        plt.ylabel('Counts')
        plt.title(str('Counts by '+property+' (N = '+str(N)+')'))
        plt.xticks(rotation=90, horizontalalignment='center')
        #add N for each bar
        plt.show()

    def pie_categorical_property_count(self, df, property): 
        #plot a bar graph of categorical variable counts in a dataframe
        df = df[df[property].notnull()]
        N = len(df)
        categories, counts = zip(*df[property].value_counts().items())  #valuecounts orders it from largest to smallest 
        labels = []
        for i in range(len(categories)):
            name = categories[i] + ' (' + str(counts[i]) + ')'
            labels.append(name)
        fig, ax = plt.subplots()
        ax.pie(counts, labels=labels, autopct='%1.1f%%')
        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis('equal')  
        plt.title(str('Counts by '+property+' (N = '+str(N)+')'), fontsize=15)
        plt.tight_layout()
        plt.show()


    def plot_numeric_property(self, df, property, by_project=False):
        #plot a histogram of numeric variable in a dataframe       #BB: columns with numeric and strings show up as object instead of float
        df[property] = pd.to_numeric(df[property],errors='coerce') #BB: this line changes object into float 
        df = df[df[property].notnull()]
        data = list(df[property])
        N = len(data)
        fig = sns.distplot(data, hist=False, kde=True,
                 bins=int(180/5), color = 'darkblue',
                 kde_kws={'linewidth': 2})
        plt.figtext(.8, .8, 'N = '+str(N))
        plt.xlabel(property)
        plt.ylabel("Probability")
        plt.title("PDF for all projects "+property+' (N = '+str(N)+')') # You can comment this line out if you don't need title
        plt.show(fig)

        if by_project is True:
            projects = list(set(df['project_id']))
            for project in projects:
                proj_df = df[df['project_id']==project]
                data = list(proj_df[property])
                N = len(data)
                fig = sns.distplot(data, hist=False, kde=True,
                         bins=int(180/5), color = 'darkblue',
                         kde_kws={'linewidth': 2})
                plt.figtext(.8, .8, 'N = '+str(N))
                plt.xlabel(property)
                plt.ylabel("Probability")
                plt.title("PDF for "+property+' in ' + project+' (N = '+str(N)+')') # You can comment this line out if you don't need title
                plt.show(fig)


    def plotviolin_numeric_property_by_categorical_property(self, df, numeric_property, categorical_property):
        #plot a histogram of numeric variable in a dataframe       #BB: columns with numeric and strings show up as object instead of float
        df[numeric_property] = pd.to_numeric(df[numeric_property],errors='coerce') #BB: this line changes object into float 
        df = df[df[numeric_property].notnull()]
        data = list(df[numeric_property])
        N = len(data)

        df[categorical_property].apply(str)
        df = df[df[categorical_property].notnull()]
        groups = df.groupby(categorical_property) 

        for name, group in groups: 
             plt.plot(group[numeric_property], marker="o", linestyle="", label=name) 
        sns.violinplot(x = categorical_property, y = numeric_property, data = df)
        plt.title("PDF for "+numeric_property+' by ' + categorical_property+' (N = '+str(N)+')', fontsize=15) 
        plt.show()


    def boxplot_numeric_property_by_categorical_property(self, df, numeric_property, categorical_property):
        #plot a histogram of numeric variable in a dataframe       #BB: columns with numeric and strings show up as object instead of float
        df[numeric_property] = pd.to_numeric(df[numeric_property],errors='coerce') #BB: this line changes object into float 
        df = df[df[numeric_property].notnull()]
        data = list(df[numeric_property])
        N = len(data)

        df[categorical_property].apply(str)
        df = df[df[categorical_property].notnull()]
        groups = df.groupby(categorical_property) 

        for name, group in groups: 
             plt.plot(group[numeric_property], marker="o", linestyle="", label=name) 
        sns.boxplot(x = categorical_property, y = numeric_property, data = df)
        plt.title("PDF for "+numeric_property+' by ' + categorical_property+' (N = '+str(N)+')', fontsize=15) 
        plt.show()


    def boxplot_numeric_property(self, df, numeric_property):
        #plot a histogram of numeric variable in a dataframe       #BB: columns with numeric and strings show up as object instead of float
        df[numeric_property] = pd.to_numeric(df[numeric_property],errors='coerce') #BB: this line changes object into float 
        df = df[df[numeric_property].notnull()]
        data = list(df[numeric_property])
        N = len(data)
        sns.boxplot(y = numeric_property, data = df, orient="h")
        plt.title("PDF for "+numeric_property+' (N = '+str(N)+')', fontsize=15) 
        plt.show()


    def scatter_numeric_by_numeric(self, df, numeric_property_a, numeric_property_b):
        #plot a histogram of numeric variable in a dataframe       #BB: columns with numeric and strings show up as object instead of float
        df[numeric_property_a] = pd.to_numeric(df[numeric_property_a],errors='coerce') #BB: this line changes object into float 
        df = df[df[numeric_property_a].notnull()]

        df[numeric_property_b] = pd.to_numeric(df[numeric_property_b],errors='coerce') #BB: this line changes object into float 
        df = df[df[numeric_property_b].notnull()]
        N = len(df)

        plt.scatter(df[numeric_property_a], df[numeric_property_b])
        plt.title('Scatter Plot Comparing ' + numeric_property_a + " vs " + numeric_property_b + ' (N = '+str(N)+')', fontsize=15)
        plt.xlabel(numeric_property_a)
        plt.ylabel(numeric_property_b)
        plt.show()


    def scatter_numeric_by_numeric_by_category(self, df, numeric_property_a, numeric_property_b, categorical_property):
        df[numeric_property_a] = pd.to_numeric(df[numeric_property_a],errors='coerce') #BB: this line changes object into float 
        df = df[df[numeric_property_a].notnull()]

        df[numeric_property_b] = pd.to_numeric(df[numeric_property_b],errors='coerce') #BB: this line changes object into float 
        df = df[df[numeric_property_b].notnull()]
        N = len(df)

        groups = df.groupby(categorical_property)

        for name, group in groups:
            plt.plot(group[numeric_property_a], group[numeric_property_b], marker="o", linestyle="", label=name, alpha=0.5)
        plt.legend(bbox_to_anchor=(1.1, 1.05))
        plt.title('Scatter Plot Comparing ' + numeric_property_a + " vs " + numeric_property_b + ' segmented by ' + categorical_property + ' (N = '+str(N)+')', fontsize=15)
        plt.xlabel(numeric_property_a)
        plt.ylabel(numeric_property_b)
        plt.show()


    def property_counts_table(self, prop, df):
        df = df[df[prop].notnull()]
        counts = Counter(df[prop])
        df1 = pd.DataFrame.from_dict(counts, orient='index').reset_index()
        df1 = df1.rename(columns={'index':prop, 0:'count'}).sort_values(by='count', ascending=False)
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            display(df1)


    def property_counts_by_project(self, prop, df):
        df = df[df[prop].notnull()]
        categories = list(set(df[prop]))
        projects = list(set(df['project_id']))

        project_table = pd.DataFrame(columns=['Project','Total']+categories)
        project_table

        proj_counts = {}
        for project in projects:
            cat_counts = {}
            cat_counts['Project'] = project
            df1 = df.loc[df['project_id']==project]
            total = 0
            for category in categories:
                cat_count = len(df1.loc[df1[prop]==category])
                total+=cat_count
                cat_counts[category] = cat_count

            cat_counts['Total'] = total
            index = len(project_table)
            for key in list(cat_counts.keys()):
                project_table.loc[index,key] = cat_counts[key]

            project_table = project_table.sort_values(by='Total', ascending=False, na_position='first')

        #display(project_table) #Displays two tables if uncommented out (this line and the return line)
        return project_table

#issue with query_txt
    def node_record_counts(self, project_id):
        query_txt = """{node (first:-1, project_id:"%s"){type}}""" % (project_id)
        res = Gen3Submission.query(query_txt)
        df = json_normalize(res['data']['node'])
        counts = Counter(df['type'])
        df = pd.DataFrame.from_dict(counts, orient='index').reset_index()
        df = df.rename(columns={'index':'node', 0:'count'})
        return df


#had issue with table 
    def save_table_image(self, df,filename='mytable.png'):
        """ Saves a pandas DataFrame as a PNG image file.
        """
        ax = plt.subplot(111, frame_on=False) # no visible frame
        ax.xaxis.set_visible(False)  # hide the x axis
        ax.yaxis.set_visible(False)  # hide the y axis
        table(ax, df)  # where df is your data frame
        plt.savefig(filename)



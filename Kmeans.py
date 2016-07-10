from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
import random

class Kmeans(object):
    """
    Creates a K-Means fitting object to find k-classes
    """
    def __init__(self):
        self.feature_names = None
        self.k = None
        self.centers = None
        self.distances = []
        self.predictions = None
        self.predictions_old = None
        self.plot_count = 0
        self.changes = 1

    def fit(self, data, k_value):
        self.k = k_value
        self.centers = np.array(random.sample(data, self.k))
        self.compute_euclidean(data)
        self.assign_class()
        self.plot_figure(data)
        while self.changes > 0:
            self.cluster_center(data)
            self.compute_euclidean(data)
            self.assign_class()
            self.plot_figure(data)
            self.changes = sum(self.predictions != self.predictions_old)
        print 'The K-means classifer has converged after {} trials'.format(self.plot_count)

    def compute_euclidean(self, data):
        self.predictions_old = self.predictions
        self.distances = []
        for point in data:
            c_distances = []
            for centroid in self.centers:
                d = (point - centroid)**2
                d = d.sum()
                d = np.sqrt(d)
                c_distances.append(d)
            self.distances.append(c_distances)

    def assign_class(self):
        self.predictions = np.ones((len(self.distances)), dtype=np.int64)
        for i in xrange(len(self.distances)):
            self.predictions[i] = np.argmin(self.distances[i])

    def cluster_center(self, data):
        c = []
        for i in xrange(self.k):
            idx = self.predictions == i
            c.append(data[idx].mean(axis=0))
        self.centers = np.array(c)

    def plot_figure(self, data):
        """
        Creates a png for every iteration of the kmeans fit
        """
        fname = str(self.k) + '_kmeans_plot_' + str(self.plot_count) + '.png'
        self.plot_count += 1
        col = self.assign_color(self.predictions)
        fig = plt.figure(figsize=(8,6))
        plt.scatter(data[:,1], data[:,2], c=col, edgecolors='w', s=75, alpha=0.4)
        plt.scatter(self.centers[:,1], self.centers[:,2], c=['r', 'b', 'g', 'darkorange', 'darkviolet'], edgecolors='w', s=200)
        title = 'Kmeans clustering with ' + str(self.k) + ' classes'
        plt.title(title)
        plt.savefig(fname)
        plt.close()

    def assign_color(self, predictions):
        """
        Assigns colors to the datapoints
        """
        colors = []
        for i in xrange(len(predictions)):
            if predictions[i] == 0:
                colors.append('r')
            elif predictions[i] == 1:
                colors.append('b')
            elif predictions[i] == 2:
                colors.append('g')
            elif predictions[i] == 3:
                colors.append('darkorange')
            else:
                colors.append('darkviolet')
        return colors


if __name__ == '__main__':
    iris = datasets.load_iris()
    features = iris['feature_names']
    data = iris['data']
    target = iris['target']
    kmeans = Kmeans()
    num = raw_input('How many clusters would you like to show? (1 - 5): ')
    kmeans.fit(data, int(num))

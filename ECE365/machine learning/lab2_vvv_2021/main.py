import numpy as np
import scipy.spatial.distance as dist
from scipy import stats
from sklearn import neighbors
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


class Question1(object):
    # lab1.ex5 (x^T)Ay = np.dot(np.dot(X, A), Y.T)
    # lab1.ex6 (x^T)Ax = np.sum(np.dot(X, A)*X, axis=1)
    def bayesClassifier(self, data, pi, means, cov):
        # labels = None
        invC = np.linalg.pinv(cov)
        objectiveFunction = np.log(pi) + np.dot(
            np.dot(means, invC), data.T).T - 0.5*np.sum(np.dot(means, invC)*means, axis=1).T
        labels = np.argmax(objectiveFunction, axis=1)
        return labels

    def classifierError(self, truelabels, estimatedlabels):
        boolean = truelabels != estimatedlabels
        # print(np.count_nonzero(boolean))
        error = (np.count_nonzero(boolean)) / len(truelabels)
        return error


class Question2(object):
    def trainLDA(self, trainfeat, trainlabel):
        # Assuming all labels up to nlabels exist.
        nlabels = int(trainlabel.max())+1
        pi = np.zeros(nlabels)            # Store your prior in here
        # Store the class means in here
        means = np.zeros((nlabels, trainfeat.shape[1]))
        # Store the covariance matrix in here
        cov = np.zeros((trainfeat.shape[1], trainfeat.shape[1]))
        # Put your code below
        for i in range(nlabels):
            boolean = i == trainlabel
            pi[i] = np.count_nonzero(boolean) / len(trainlabel)
            means[i] = np.sum(trainfeat[boolean], axis=0) / np.count_nonzero(boolean)
            # print(trainfeat[boolean])
            for j in trainfeat[boolean]:
                # print((j-pi[i]).shape)
                # print((j-pi[i]).T.shape)
                # print(np.dot((j-pi[i]), (j-pi[i]).T))
                cov += np.dot((j-means[i]).reshape((trainfeat.shape[1], 1)), (j-means[i]).reshape((trainfeat.shape[1], 1)).T)
        cov /= (len(trainlabel) - nlabels)

        # Don't change the output!
        return (pi, means, cov)

    def estTrainingLabelsAndError(self, trainingdata, traininglabels):
        q1 = Question1()
        # You can use results from Question 1 by calling q1.bayesClassifier(...), etc.
        # If you want to refer to functions under the same class, you need to use self.fun(...)
        pi, means, cov = self.trainLDA(trainingdata, traininglabels)
        esttrlabels = q1.bayesClassifier(trainingdata, pi, means, cov)
        trerror = q1.classifierError(traininglabels, esttrlabels)
        return (esttrlabels, trerror)

    def estValidationLabelsAndError(self, trainingdata, traininglabels, valdata, vallabels):
        q1 = Question1()
        # You can use results from Question 1 by calling q1.bayesClassifier(...), etc.
        # If you want to refer to functions under the same class, you need to use self.fun(...)
        pi, means, cov = self.trainLDA(trainingdata, traininglabels)
        estvallabels = q1.bayesClassifier(valdata, pi, means, cov)
        valerror = q1.classifierError(vallabels, estvallabels)
        # Don't change the output!
        return (estvallabels, valerror)



class Question3(object):
    def kNN(self, trainfeat, trainlabel, testfeat, k):
        distance = dist.cdist(testfeat, trainfeat, metric="euclidean")
        knn = np.argpartition(distance, k)[:, :k]
        labels = stats.mode(trainlabel[knn], axis=1)[0].reshape((testfeat.shape[0], ))
        # print(testfeat.shape)
        # print(labels.shape)
        return labels

    def kNN_errors(self, trainingdata, traininglabels, valdata, vallabels):
        q1 = Question1()
        trainingError = np.zeros(4)
        validationError = np.zeros(4)
        k_array = [1, 3, 4, 5]

        for i in range(len(k_array)):
            # Please store the two error arrays in increasing order with k
            # This function should call your previous self.kNN() function.
            # Put your code below
            esiTraLabels = self.kNN(trainingdata, traininglabels, trainingdata, k_array[i])
            esiValLabels = self.kNN(trainingdata, traininglabels, valdata, k_array[i])
            trainingError[i] = q1.classifierError(traininglabels, esiTraLabels)
            validationError[i] = q1.classifierError(vallabels, esiValLabels)
            
        # Don't change the output!
        return (trainingError, validationError)



class Question4(object):
    def sklearn_kNN(self, traindata, trainlabels, valdata, vallabels):
        classifier, valerror, fitTime, predTime = (None, None, None, None)
        q1 = Question1()
        import time
        classifier = neighbors.KNeighborsClassifier(n_neighbors=1, algorithm="ball_tree")
        fitTimeStart = time.time()
        classifier.fit(traindata, trainlabels)
        fitTimeEnd = time.time()
        predTimeStart = time.time()
        estimatedlabels = classifier.predict(valdata)
        predTimeEnd = time.time()
        valerror = q1.classifierError(vallabels, estimatedlabels)
        fitTime = fitTimeEnd - fitTimeStart
        predTime = predTimeEnd - predTimeStart
        # Don't change the output!
        return (classifier, valerror, fitTime, predTime)

    def sklearn_LDA(self, traindata, trainlabels, valdata, vallabels):
        classifier, valerror, fitTime, predTime = (None, None, None, None)
        q1 = Question1()
        import time
        classifier = LinearDiscriminantAnalysis()
        fitTimeStart = time.time()
        classifier.fit(traindata, trainlabels)
        fitTimeEnd = time.time()
        predTimeStart = time.time()
        estimatedlabels = classifier.predict(valdata)
        predTimeEnd = time.time()
        valerror = q1.classifierError(vallabels, estimatedlabels)
        fitTime = fitTimeEnd - fitTimeStart
        predTime = predTimeEnd - predTimeStart
        # Don't change the output!
        return (classifier, valerror, fitTime, predTime)

###
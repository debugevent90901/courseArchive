##################################################################################################################
##      Assignment 3.2 solution functions created for the course ECE449 at Zhejiang University / University of  ##
##      Illinois at Urbana-Champaign Institute (ZJU-UIUC Institute) in Spring 2021 semester.                      ##
##      This notebook refers to the following link.  ##
##      Reference links:                                                                                        ##
##           https://gtraskas.github.io/post/ex7/
##      For academic use only. No warranty guarenteed.                                                          ##
##      Licensing Information:  You are free to use or extend this project if:                                  ##
##          (1) You don't distribute or publish coding solutions for ECE449 Assignments in this project online. ##
##          (2) You retain this notice.                                                                         ##
##          (3) You provide clear attribution to ZJU-UIUC Institute.                                            ##
##--------------------------------------------------------------------------------------------------------------##
##          Written by Feiyu Zhang (feiyu.17@intl.zju.edu.cn), last edit: 2021-05-02                        ##
##--------------------------------------------------------------------------------------------------------------##
##      The solution functions in this file are just for reference, multiple solutions are accepted.            ##
##      It is okay if your implementations are slightly different from the provided solutions below.            ##
##################################################################################################################

def findClosestCentroids(X, centroids):
    """
    Returns the closest centroids in idx for a dataset X
    where each row is a single example. idx = m x 1 vector
    of centroid assignments (i.e. each entry in range [1..K])
    Args:
        X        : array(# training examples, n)
        centroids: array(K, n)
    Returns:
        idx      : array(# training examples, 1)
    """
    # Set K size.
    K = centroids.shape[0]

    # Initialise idx.
    idx = np.zeros((X.shape[0], 1), dtype=np.int8)

    # ====================== YOUR CODE HERE ======================
    # replace the following line with your implementation.
    for i in range(X.shape[0]):
        distances = np.linalg.norm(X[i] - centroids, axis=1)
        # argmin returns the indices of the minimum values along an axis,
        # replacing the need for a for-loop and if statement.
        min_dst = np.argmin(distances)
        idx[i] = min_dst

    # =============================================================    
    return idx

def computeCentroids(X, idx, K):
    """
    Returns the new centroids by computing the means
    of the data points assigned to each centroid. It is
    given a dataset X where each row is a single data point,
    a vector idx of centroid assignments (i.e. each entry
    in range [1..K]) for each example, and K, the number of
    centroids. A matrix centroids is returned, where each row
    of centroids is the mean of the data points assigned to it.
    Args:
        X        : array(# training examples, 2)
        idx      : array(# training examples, 1)
        K        : int, # of centroids
    Returns:
        centroids: array(# of centroids, 2)
    """

    # ====================== YOUR CODE HERE ======================
    # replace the following line with your implementation.
    # Create useful variables
    m, n = X.shape
    
    # Initialize centroids matrix.
    centroids = np.zeros((K, n))    
    for k in range(K):
        centroids[k, :] = np.mean(X[idx.ravel() == k, :], axis=0)

    # =============================================================

    
    return centroids

def kMeansInitCentroids(X, K):
    """
    Initializes K centroids that are to be 
    used in K-Means on the dataset X.
    Args:
        X                : array(# training examples, n)
        K                : int, # of centroids
    Returns:
        initial_centroids: array(# of centroids, n)
    """
    # Init centroids.
    centroids = np.zeros((K, X.shape[1]))

    # ====================== YOUR CODE HERE ======================
    # replace the following line with your implementation.

    # Randomly reorder the indices of examples.
    randidx = np.random.permutation(X.shape[0])
    # Take the first K examples as centroids.
    centroids = X[randidx[:K], :]

    # =============================================================
    return centroids

def projectData(X, U, K):
    """
    Computes the projection of the normalized inputs X
    into the reduced dimensional space spanned by the first
    K columns of U. It returns the projected examples in Z.
    Args:
        X: array(# of training examples, n)
        U: array(n, n)
        K: int, # of dimensions
    Returns:
        Z: array(# of training examples, K)
    """
    # ====================== YOUR CODE HERE ======================
    # replace the following line with your implementation.
    # Init Z.
    Z = np.zeros((X.shape[0], K)) # m * K
    
    # Compute the projection of the data using only
    # the top K eigenvectors in U (first K columns).
    U_reduce = U[:,:K]
    Z = np.dot(X, U_reduce)
    # =============================================================


    return Z
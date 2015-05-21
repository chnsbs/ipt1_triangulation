

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np



def get_test_dataX(delta=0.05):
    '''
    Return a tuple X, Y, Z with a test data set.
    '''

    from matplotlib.mlab import  bivariate_normal
    x = y = np.arange(-3.0, 3.0, delta)
    X, Y = np.meshgrid(x, y)

    Z1 = bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
    Z2 = bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
    Z = Z2 - Z1

    X = X * 10
    Y = Y * 10
    Z = Z * 100
    return X, Y, Z


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


X, Y, Z = get_test_dataX(0.05)
ax.plot_wireframe(X, Y, Z, rstride=3, cstride=3)

plt.show()


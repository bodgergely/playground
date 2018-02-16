import tensorflow as tf
import numpy as np
from sklearn.datasets import fetch_california_housing

housing = fetch_california_housing()
m,n = housing.data.shape
housing_data_plus_bias = np.c_[np.ones((m,1)), housing.data]

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaled_housing_data = scaler.fit_transform(housing.data)
scaled_housing_data_plus_bias = np.c_[np.ones((m,1)), scaled_housing_data]

target = housing.target.reshape(-1,1)
y = tf.constant(target, dtype=tf.float32, name='y')

def reset_graph(seed=42):
    tf.reset_default_graph()
    tf.set_random_seed(seed)
    np.random.seed(seed)

def lr_analitical():
    X = tf.constant(housing_data_plus_bias, dtype=tf.float32, name='X')

    XT = tf.transpose(X)
    theta = tf.matrix_inverse(XT @ X) @ XT @ y

    theta_val = None
    with tf.Session() as sess:
        theta_val = theta.eval()

    return housing_data_plus_bias @ theta_val

def lr_gd():
    n_epochs = 1000
    learning_rate = 0.01

    X = tf.constant(scaled_housing_data_plus_bias, dtype=tf.float32, name='X')
    theta = tf.Variable(tf.random_uniform([n+1,1], -1.0, 1.0), name='theta')
    y_pred = tf.matmul(X, theta, name='predictions')
    error = y_pred - y
    mse = tf.reduce_mean(tf.square(error), name='mse')
    gradients = 2/m * tf.matmul(tf.transpose(X), error)
    training_op = tf.assign(theta, theta - learning_rate * gradients)

    init = tf.global_variables_initializer()
    
    best_theta = None
    with tf.Session() as sess:
        sess.run(init)

        mse_list = []
        for epoch in range(n_epochs):
            if epoch % 100 == 0:
                mse_list.append(mse.eval())      
            sess.run(training_op)
        
        best_theta = theta.eval()

    return scaled_housing_data_plus_bias @ best_theta

def lr_gd2():
    n_epochs = 1000
    learning_rate = 0.01

    X = tf.constant(scaled_housing_data_plus_bias, dtype=tf.float32, name='X')
    theta = tf.Variable(tf.random_uniform([n+1,1], -1.0, 1.0), name='theta')
    y_pred = tf.matmul(X, theta, name='predictions')
    error = y_pred - y
    mse = tf.reduce_mean(tf.square(error), name='mse')

    optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
    training_op = optimizer.minimize(mse)

    init = tf.global_variables_initializer()
    
    best_theta = None
    with tf.Session() as sess:
        sess.run(init)

        mse_list = []
        for epoch in range(n_epochs):
            if epoch % 100 == 0:
                mse_list.append(mse.eval())      
            sess.run(training_op)
        
        best_theta = theta.eval()

    return scaled_housing_data_plus_bias @ best_theta


def lr_momentum():
    n_epochs = 1000
    learning_rate = 0.01

    X = tf.constant(scaled_housing_data_plus_bias, dtype=tf.float32, name='X')
    theta = tf.Variable(tf.random_uniform([n+1,1], -1.0, 1.0), name='theta')
    y_pred = tf.matmul(X, theta, name='predictions')
    error = y_pred - y
    mse = tf.reduce_mean(tf.square(error), name='mse')

    optimizer = tf.train.MomentumOptimizer(learning_rate=learning_rate, momentum=0.9)
    training_op = optimizer.minimize(mse)

    init = tf.global_variables_initializer()
    
    best_theta = None
    with tf.Session() as sess:
        sess.run(init)

        mse_list = []
        for epoch in range(n_epochs):
            if epoch % 100 == 0:
                mse_list.append(mse.eval())      
            sess.run(training_op)
        
        best_theta = theta.eval()

    return scaled_housing_data_plus_bias @ best_theta



def compare():
    pred_anal = lr_analitical()
    pred_grad = lr_gd()
    pred_gd2 = lr_gd2()
    pred_momentum = lr_momentum()

    print(target[:15])

    score =  np.sqrt(np.sum(np.square(target - pred_anal)) / len(target))
    print("Accuracy Analytical: ", score)

    score =  np.sqrt(np.sum(np.square(target - pred_grad)) / len(target))
    print("Accuracy Grad: ", score)

    score =  np.sqrt(np.sum(np.square(target - pred_gd2)) / len(target))
    print("Accuracy Gradient Descent: ", score)

    score =  np.sqrt(np.sum(np.square(target - pred_momentum)) / len(target))
    print("Accuracy Momentum: ", score)

if __name__ == "__main__":
    compare()
     







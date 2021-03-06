import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
from read_data import get_data
import tkinter
import matplotlib.pyplot as plt
train_x, train_y, test_x, test_y = get_data()
NUMBER_OF_ATTRIBUTES = 6
steps = 5000
GLOBAL_STEP = 0.01
n_nodes_hl1 = 50
n_nodes_hl2 = 10
n_nodes_hl3 = 500
n_nodes_hl4 = 500
n_nodes_hl5 = 500


n_classes = 2
batch_size = 20

x = tf.placeholder('float', [None, NUMBER_OF_ATTRIBUTES])
y = tf.placeholder('float')


def exp_decay(global_step):
    return tf.train.exponential_decay(
        learning_rate=0.01, global_step=global_step,
        decay_steps=steps, decay_rate=0.01)


def neural_network_model(data):
    hidden_1_layer = {'weights': tf.Variable(tf.random_normal([len(train_x[0]), n_nodes_hl1])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl1]))}

    hidden_2_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl1, n_nodes_hl2])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl2]))}

    hidden_3_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl2, n_nodes_hl3])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl3]))}

    hidden_4_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl3, n_nodes_hl4])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl4]))}

    hidden_5_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl4, n_nodes_hl5])),
                      'biases': tf.Variable(tf.random_normal([n_nodes_hl5]))}

    output_layer = {'weights': tf.Variable(tf.random_normal([n_nodes_hl2, n_classes])),
                    'biases': tf.Variable(tf.random_normal([n_classes]))}

    l1 = tf.add(tf.matmul(data, hidden_1_layer['weights']), hidden_1_layer['biases'])
    l1 = tf.nn.tanh(l1)

    l2 = tf.add(tf.matmul(l1, hidden_2_layer['weights']), hidden_2_layer['biases'])
    l2 = tf.nn.relu(l2)

    l3 = tf.add(tf.matmul(l2, hidden_3_layer['weights']), hidden_3_layer['biases'])
    l3 = tf.nn.relu(l3)

    l4 = tf.add(tf.matmul(l3, hidden_4_layer['weights']), hidden_4_layer['biases'])
    l4 = tf.nn.relu(l4)

    l5 = tf.add(tf.matmul(l4, hidden_5_layer['weights']), hidden_5_layer['biases'])
    l5 = tf.nn.relu(l5)

    output = tf.matmul(l2, output_layer['weights']) + output_layer['biases']

    return output


def train_neural_network(x):
    prediction = neural_network_model(x)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y))
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01).minimize(cost)
    hm_iterations = 100
    history_loss=[]
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        for iteration in range(hm_iterations):
            iteration_loss = 0
            batch_counter = 0
            while batch_counter < len(train_x):
                start = batch_counter
                end = batch_counter + batch_size
                if end > len(train_x):
                    end = len(train_x) - 1
                batch_x = np.array(train_x[start:end])
                batch_y = np.array(train_y[start:end])
                batch_counter += batch_size
                _, c= sess.run([optimizer, cost], feed_dict={x: batch_x, y: batch_y})
                iteration_loss += c
            print('Iteration ', iteration + 1, 'completed out of', hm_iterations, ' loss: ', iteration_loss)
            correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
            accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
            print('Train ', accuracy.eval({x: train_x, y: train_y}))
            print('Test: ', accuracy.eval({x: test_x, y: test_y}))
            history_loss.append(iteration_loss)
        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        #print('Test: ', accuracy.eval({x: test_x, y: test_y}))
        plt.figure()
        plt.xlabel("Iter")
        plt.ylabel("Blad")
        plt.plot(history_loss)
        plt.show()



def main():
    train_neural_network(x)

if __name__ == '__main__':
    main()
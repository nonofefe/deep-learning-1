# import os,sys
# sys.path.append(os.pardir)
# import numpy as np
# from common.functions import *
# from common.gradient import *
#
# class TwoLayerNet:
#     def __init__(self,input_size,hidden_size,output_size,weight_init_std=0.01):
#         self.params = {}
#         self.params['W1'] = weight_init_std * \
#             np.random.randn(input_size,hidden_size)
#         self.params['b1'] = np.zeros(hidden_size)
#         self.params['W2'] = weight_init_std * \
#             np.random.randn(hidden_size,output_size)
#         self.params['b2'] = np.zeros(output_size)
#
#     def predict(self,x):
#         W1,W2 = self.params['W1'],self.params['W2']
#         b1,b2 = self.params['b1'],self.params['b2']
#
#         a1 = np.dot(x,W1) + b1
#         z1 = sigmoid(a1)
#         a2 = np.dot(z1,W2) + b2
#         y = softmax(a2)
#
#         return y
#
#     #x:入力データ t:教師データ
#     def loss(self,x,t):
#         y = self.predict(x)
#
#         return cross_entropy_error(y,t)
#
#     def accuracy(self,x,t):
#         y = self.predict(x)
#         y = np.argmax(y,axis=1)
#         t = np.argmax(t,axis=1)
#
#         accuracy = np.sum(y == t) / float(x.shape[0])
#         return accuracy
#
#     #x:入力データ t:教師データ
#     def numerical_gradient(self,x,t):
#         loss_W = lambda W: self.loss(x,t)
#
#         grads = {}
#         grads['W1'] = numerical_gradient(loss_W,self.params['W1'])
#         grads['b1'] = numerical_gradient(loss_W,self.params['b1'])
#         grads['W2'] = numerical_gradient(loss_W,self.params['W2'])
#         grads['b2'] = numerical_gradient(loss_W,self.params['b2'])
#
#         return grads
#
# net = TwoLayerNet(input_size=784,hidden_size=100,output_size=10)
# print(net.params['W1'].shape)
# print(net.params['b1'].shape)
# print(net.params['W2'].shape)
# print(net.params['b2'].shape)
#
# x = np.random.rand(100,784)
# t = np.random.rand(100,10)
# # y = net.predict(x)
# # print(y.shape)
# # print(y)
# grads = net.numerical_gradient(x,t)
#
# print(grads['W1'].shape)
# print(grads['b1'].shape)
# print(grads['W2'].shape)
# print(grads['b2'].shape)
#

# coding: utf-8
import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
import matplotlib.pyplot as plt
from dataset.mnist import load_mnist
from ch04.two_layer_net import TwoLayerNet

(x_train,t_train),(x_test,t_test) = load_mnist(normalize=True)

train_size = x_train.shape[0]
batch_size = 100

train_loss_list = []
train_acc_list = []
test_acc_list = []
#1エポックあたりの繰り返し数
iter_per_epoch = max(train_size / batch_size,1)

#ハイパーパラメータ
iters_num = 10000
batch_size = 100
learning_rate = 0.1

network = TwoLayerNet(input_size=784, hidden_size=50, output_size=10)

for i in range(iters_num):
    #ミニバッチの取得
    batch_mask = np.random.choice(train_size,batch_size)
    x_batch = x_train[batch_mask]
    t_batch = t_train[batch_mask]

    #勾配の計算
    grad = network.numerical_gradient(x_batch, t_batch)
    #grad = network.gradient(x_batch,t_batch) # 高速版

    #パラメータの更新
    for key in ('W1', 'b1', 'W2', 'b2'):
        network.params[key] -= learning_rate * grad[key]

    loss = network.loss(x_batch, t_batch)
    train_loss_list.append(loss)

    #1エポックごとに認識精度を計算
    if i % iter_per_epoch == 0:
        train_acc = network.accuracy(x_train,t_train)
        test_acc = network.accuracy(x_test,t_test)
        train_acc_list.append(train_acc)
        test_acc_list.append(test_acc)
        print("train acc, test acc | " + str(train_acc) + ", " +str(test_acc))

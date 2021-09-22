##################################################################################################################
##      ECE449 assignment 2, task 3: LeNet in PyTorch.                                                          ##
##--------------------------------------------------------------------------------------------------------------##
##      Script solution created for the course ECE449 at Zhejiang University / University of                    ##
##      Illinois at Urbana-Champaign Institute (ZJU-UIUC Institute) in Fall 2020 semester.                      ##
##      Licensing Information:  You are free to use or extend this project if:                                  ##
##          (1) You don't distribute or publish coding solutions for ECE449 Assignments in this project online. ##
##          (2) You retain this notice.                                                                         ##
##          (3) You provide clear attribution to ZJU-UIUC Institute.                                            ##
##--------------------------------------------------------------------------------------------------------------##
##          Written by Jinghua Wang (jinghuawang@intl.zju.edu.cn), last edit: 2020-11-04                        ##
##################################################################################################################
#        This solution file is created based on D2L.AI dive into deep learning textbook at https://d2l.ai.       #

import torch
from torch import nn

##################################################################################################################
#                                             NN implementations                                                 #

class Reshape(torch.nn.Module):
    def forward(self, x):
        return x.view(-1, 1, 28, 28)

def get_lenet():
    # get a lenet model using torch.nn
    net = torch.nn.Sequential(
        Reshape(),
        nn.Conv2d(1, 6, kernel_size=5, padding=2), nn.Sigmoid(),
        nn.AvgPool2d(kernel_size=2, stride=2),
        nn.Conv2d(6, 16, kernel_size=5), nn.Sigmoid(),
        nn.AvgPool2d(kernel_size=2, stride=2),
        nn.Flatten(),
        nn.Linear(16 * 5 * 5, 120), nn.Sigmoid(),
        nn.Linear(120, 84), nn.Sigmoid(),
        nn.Linear(84, 10)
    )
    return net

##################################################################################################################

##################################################################################################################
#                      You may write other helper functions and/or classes here, if you need                     #

def try_gpu(i=0):
    #Return gpu(i) if detected, otherwise return cpu() for device
    if torch.cuda.device_count() >= i + 1:
        return torch.device(f'cuda:{i}')
    return torch.device('cpu')

class Accumulator:
    # Class for accumulating sums over n variables.
    def __init__(self, n):
        self.data = [0.0] * n
    def add(self, *args):
        self.data = [a + float(b) for a, b in zip(self.data, args)]
    def reset(self):
        self.data = [0.0] * len(self.data)
    def __getitem__(self, idx):
        return self.data[idx]

def accuracy(y_hat, y):
    # Compute the number of correct predictions."""
    if len(y_hat.shape) > 1 and y_hat.shape[1] > 1:
        y_hat = y_hat.argmax(axis=1)        
    cmp = y_hat.type(y.dtype) == y
    return float((cmp.type(y.dtype)).sum())

def evaluate_accuracy_try_gpu(net, data_iter, device=None):
    # Evaluate the accuracy for a model on a dataset from data_iter.
    # If GPU exists then use GPU, otherwise use CPU.
    # returns None if net has not been constructed properly.
    if len(net) <= 1:
        return None
    net.eval()  # Set the model to evaluation mode to disable gradient update
    if not device:
        device = next(iter(net.parameters())).device
    # metric contains: (1) No. of correct predictions, (2) no. of predictions
    metric = Accumulator(2)
    for X, y in data_iter:
        X, y = X.to(device), y.to(device)
        metric.add(accuracy(net(X), y), y.numel())
    return metric[0] / metric[1]

##################################################################################################################

##################################################################################################################
#                 The training function (and its helper functions and/or classes, if you need)                   #

class Timer:
    """Record multiple running times."""
    import time
    def __init__(self):
        self.times = []
        self.start()
    def start(self):
        """Start the timer."""
        self.tik = self.time.time()
    def stop(self):
        """Stop the timer and record the time in a list."""
        self.times.append(self.time.time() - self.tik)
        return self.times[-1]
    def avg(self):
        """Return the average time."""
        return sum(self.times) / len(self.times)
    def sum(self):
        """Return the sum of time."""
        return sum(self.times)
    def cumsum(self):
        """Return the accumulated time."""
        return np.array(self.times).cumsum().tolist()

def train_cnn(net, train_iter, test_iter, num_epochs, lr, device=try_gpu()):
    def init_weights(m):
        if type(m) == nn.Linear or type(m) == nn.Conv2d:
            torch.nn.init.xavier_uniform_(m.weight)
    net.apply(init_weights)
    print('training on', device)
    net.to(device)
    optimizer = torch.optim.SGD(net.parameters(), lr=lr)
    loss = nn.CrossEntropyLoss()
    timer, num_batches = Timer(), len(train_iter)
    for epoch in range(num_epochs):
        # Sum of training loss, sum of training accuracy, no. of examples
        metric = Accumulator(3)
        for i, (X, y) in enumerate(train_iter):
            timer.start()
            net.train()
            optimizer.zero_grad()
            X, y = X.to(device), y.to(device)
            y_hat = net(X)
            l = loss(y_hat, y)
            l.backward()
            optimizer.step()
            with torch.no_grad():
                metric.add(l * X.shape[0], accuracy(y_hat, y), X.shape[0])
            timer.stop()
            train_l = metric[0]/metric[2]
            train_acc = metric[1]/metric[2]
        test_acc = evaluate_accuracy_try_gpu(net, test_iter)
        print(f'loss {train_l:.3f}, train acc {train_acc:.3f}, 'f'test acc {test_acc:.3f}, '
              f'{metric[2] * num_epochs / timer.sum():.1f} examples/sec 'f'on {str(device)}')

##################################################################################################################

##################################################################################################################
#                                          Other utility functions                                               #

def load_data_fashion_mnist(batch_size, resize=None):
    # Load the Fashion-MNIST dataset from hard drive into memory.
    # Download the Fashion-MNIST dataset if needed.
    import torchvision
    from torchvision import transforms
    from torch.utils import data
    trans = [transforms.ToTensor()]
    if resize:
        trans.insert(0, transforms.Resize(resize))
    trans = transforms.Compose(trans)
    fashion_mnist_train = torchvision.datasets.FashionMNIST(
        root="./data", train=True, transform=trans, download=True)
    fashion_mnist_test = torchvision.datasets.FashionMNIST(
        root="./data", train=False, transform=trans, download=True)
    return (data.DataLoader(fashion_mnist_train, batch_size, shuffle=True, num_workers=0),
            data.DataLoader(fashion_mnist_test, batch_size, shuffle=False, num_workers=0))

def get_correct_lenet_shape_str():
    return """Reshape output shape: 	 torch.Size([1, 1, 28, 28])
Conv2d output shape: 	 torch.Size([1, 6, 28, 28])
Sigmoid output shape: 	 torch.Size([1, 6, 28, 28])
AvgPool2d output shape: 	 torch.Size([1, 6, 14, 14])
Conv2d output shape: 	 torch.Size([1, 16, 10, 10])
Sigmoid output shape: 	 torch.Size([1, 16, 10, 10])
AvgPool2d output shape: 	 torch.Size([1, 16, 5, 5])
Flatten output shape: 	 torch.Size([1, 400])
Linear output shape: 	 torch.Size([1, 120])
Sigmoid output shape: 	 torch.Size([1, 120])
Linear output shape: 	 torch.Size([1, 84])
Sigmoid output shape: 	 torch.Size([1, 84])
Linear output shape: 	 torch.Size([1, 10])"""

##################################################################################################################
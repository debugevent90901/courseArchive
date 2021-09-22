##################################################################################################################
##      ECE449 assignment 2, task 4: ResNet in PyTorch.                                                         ##
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
from torch.nn import functional as F

##################################################################################################################
#                                             NN implementations                                                 #

class Residual(nn.Module):
    #The Residual block for ResNet.
    def __init__(self, input_channels, num_channels, use_1x1conv=False, strides=1):
        super().__init__()
        self.conv1 = nn.Conv2d(input_channels, num_channels, kernel_size=3, padding=1, stride=strides)
        self.conv2 = nn.Conv2d(num_channels, num_channels, kernel_size=3, padding=1)
        if use_1x1conv:
            self.conv3 = nn.Conv2d(input_channels, num_channels, kernel_size=1, stride=strides)
        else:
            self.conv3 = None
        self.bn1 = nn.BatchNorm2d(num_channels)
        self.bn2 = nn.BatchNorm2d(num_channels)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, X):
        Y = F.relu(self.bn1(self.conv1(X)))
        Y = self.bn2(self.conv2(Y))
        if self.conv3:
            X = self.conv3(X)
        Y += X
        return F.relu(Y)


def resnet_block(input_channels, num_channels, num_residuals, first_block=False):
    # return a sequence of Residual modules for building the complete resnet-18 model
    blk = []
    for i in range(num_residuals):
        if i == 0 and not first_block:
            blk.append(Residual(input_channels, num_channels, use_1x1conv=True, strides=2))
        else:
            blk.append(Residual(num_channels, num_channels))
    return blk


def get_resnet():
    # get a resnet model using PyTorch
    b1 = nn.Sequential(nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3),
                   nn.BatchNorm2d(64), nn.ReLU(),
                   nn.MaxPool2d(kernel_size=3, stride=2, padding=1))
    b2 = nn.Sequential(*resnet_block(64, 64, 2, first_block=True))
    b3 = nn.Sequential(*resnet_block(64, 128, 2))
    b4 = nn.Sequential(*resnet_block(128, 256, 2))
    b5 = nn.Sequential(*resnet_block(256, 512, 2))
    net = nn.Sequential(b1, b2, b3, b4, b5,
                    nn.AdaptiveAvgPool2d((1,1)),
                    nn.Flatten(), nn.Linear(512, 10))
    return net

##################################################################################################################

##################################################################################################################
#                      You may write other helper functions and/or classes here, if you need                     #


##################################################################################################################


##################################################################################################################
#                                          Other utility functions                                               #

def get_correct_resnet_shape_str():
    return """Sequential output shape:	 torch.Size([1, 64, 56, 56])
Sequential output shape:	 torch.Size([1, 64, 56, 56])
Sequential output shape:	 torch.Size([1, 128, 28, 28])
Sequential output shape:	 torch.Size([1, 256, 14, 14])
Sequential output shape:	 torch.Size([1, 512, 7, 7])
AdaptiveAvgPool2d output shape:	 torch.Size([1, 512, 1, 1])
Flatten output shape:	 torch.Size([1, 512])
Linear output shape:	 torch.Size([1, 10])"""

##################################################################################################################
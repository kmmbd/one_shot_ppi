import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from scipy.spatial import distance


# class ContrastiveLoss(nn.Module):
#
#     def __init__(self, margin=1.0):
#         super(ContrastiveLoss, self).__init__()
#         self.margin = margin
#
#     def forward(self, output1, output2, label):
#         # Find the pairwise distance or eucledian distance of two output feature vectors
#         euclidean_distance = F.pairwise_distance(output1, output2)
#         # perform contrastive loss calculation with the distance
#         loss_contrastive = torch.mean((1 - label) * torch.pow(euclidean_distance, 2) +
#                                       (label) * torch.pow(torch.clamp(self.margin - euclidean_distance, min=0.0), 2))
#
#         return loss_contrastive

class ContrastiveLoss(nn.Module):
    """
    Contrastive loss
    Takes embeddings of two samples and a target label == 1 if samples are from the same class and label == 0 otherwise
    """

    def __init__(self, margin):
        super(ContrastiveLoss, self).__init__()
        self.margin = margin
        self.eps = 1e-9

    def forward(self, output1, output2, target, size_average=True):

        # o1 = output1.cpu().numpy()
        # o1 = o1.detach().numpy()
        #
        # o2 = output2.detach().numpy()
        # X = np.vstack([o1, o2])
        # V = np.cov(X.T)
        # IV = np.linalg.inv(V)
        # distances = distance.mahalanobis(output1, output2, IV)
        distances = (output2 - output1).pow(2).sum(1)  # squared distances
        losses = 0.5 * (target.float() * distances +
                        (1 + -1 * target).float() * F.relu(self.margin - (distances + self.eps).sqrt()).pow(2))
        # losses = torch.from_numpy(losses).float().cuda()
        return losses.mean() if size_average else losses.sum()
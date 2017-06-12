import train
import test
import argparse
import os
import numpy as np
import random

from config import get_params

# parse arguments
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--mode', dest='mode', type=int, default=0)
parser.add_argument('--nlayers', dest='nlayers', type=int, default=3)
parser.add_argument('--dataset', dest='dataset', type=str, default='wdw')
parser.add_argument('--seed', dest='seed', type=int, default=1)
parser.add_argument('--gating_fn', dest='gating_fn', type=str, default='T.mul')
args = parser.parse_args()
cmd = vars(args)
params = get_params(cmd['dataset'])
params.update(cmd)

np.random.seed(params['seed'])
random.seed(params['seed'])

# save directory
w2v_filename = params['word2vec'].split('/')[-1].split('.')[0] if params['word2vec'] else 'None'
save_path = ('experiments/ex1/')
if not os.path.exists(save_path): os.makedirs(save_path)

# train
train.main(save_path, params)


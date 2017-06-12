from common import *

if 'datadir' in os.environ:
    cbt_datadir = os.environ['datadir']
else:
    cbt_datadir = '../data/CBTest/data/'

cbt_ne_train = os.path.join(cbt_datadir, 'train.txt')
cbt_ne_test = os.path.join(cbt_datadir, 'test.txt')
cbt_ne_val = os.path.join(cbt_datadir, 'train.txt')


from algo import sliding_window, run_nonlearning
from dataset import *
from config import *

task = os.environ['task']
test_path = globals()['cbt_' + task + '_test']

exs = read_cbt(test_path)
pprint(exs[:1])
print run_nonlearning(sliding_window, exs)

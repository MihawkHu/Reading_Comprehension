from algo import maximum_frequency, run_nonlearning
from dataset import *
from config import *

task = os.environ['task']
test_path = globals()['cbt_' + task + '_test']

exs = read_cbt(test_path)
pprint(exs[:1])
print run_nonlearning(maximum_frequency, exs)

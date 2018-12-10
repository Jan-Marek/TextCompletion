import sys

import numpy
import h5py
import theano
from collections import Counter
import re

from theanolm import Vocabulary, Architecture, Network, TextSampler
from theanolm.backend import TextFileType, get_default_device

modelPath = 'catModelNew14epochs.h5'
def restoreModel(path):
    with h5py.File(path, 'r') as state:
        print("Reading vocabulary from network state.")
        sys.stdout.flush()
        vocabulary = Vocabulary.from_state(state)
        print("Number of words in vocabulary:", vocabulary.num_words())
        print("Number of words in shortlist:", vocabulary.num_shortlist_words())
        print("Number of word classes:", vocabulary.num_classes())
        print("Building neural network.")
        sys.stdout.flush()
        architecture = Architecture.from_state(state)
        network = Network(architecture, vocabulary, mode=Network.Mode(minibatch=False))
        print("Restoring neural network state.")
        network.set_state(state)
        return network




#model = tlm.Network.from_file('kalevalaV100.h5')
model = restoreModel(modelPath)
sampler = TextSampler(model)
print(model.vocabulary)
seed = "i admire your dedication to helping all those"
correct = 'kittens'
wordN = 1
seedN = len(seed.split(' '))
seqN = 1500
samp = sampler.generate(wordN + 1, num_sequences=seqN, seed_sequence=seed)
allwords = ''
for sequence in samp:
    pstr = ''
    for i,s in enumerate(sequence):
        if i > 0:
            pstr = pstr + s + ' '
    allwords += sequence[-1] + ' '

c = Counter(re.findall('\w+', allwords))
print(100*c[correct]/seqN)
print(c.most_common(10))
for i,obj in enumerate(c.most_common(10)):
    print('{:d}. {:s} {:20s}    ({:.2f}%)'.format(i+1,seed,obj[0], 100*obj[1]/seqN))
try:
    print('   {:s} {:20s}    ({:.2f}%)'.format(seed,correct, 100*c[correct]/seqN))
except:
    print('Not found')


'''
try:
    eos_pos = sequence.index('</s>')
    sequence = sequence[:eos_pos+1]
except ValueError:
    pass
printstring + ' '.join(sequence) + '\n'
'''



'''
scorer = tlm.TextScorer(model)
#Now you can score the text string utterance using:

score = scorer.score_line('seppo', model.vocabulary)
print(score)
'''
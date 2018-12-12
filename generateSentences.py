import sys

import numpy
import h5py
import theano
from collections import Counter
import re

from theanolm import Vocabulary, Architecture, Network, TextSampler
from theanolm.backend import TextFileType, get_default_device

modelPath = 'catModelNew14epochs.h5'
modelPath = 'catsOrig.h5'
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
#samp = sampler.generate(15, num_sequences=30)



def printSample(samp):
    allwords = ''
    for sequence in samp:
        pstr = ''
        for i,s in enumerate(sequence):
            if i > 0:
                pstr = pstr + s + ' '
        #print(pstr)
        allwords += sequence[-1] + ' '
    return allwords

#printSample(samp)

def scoreTest(path):
    with open('catsTestOrig.txt') as infile, open('output.txt', 'w') as outfile:
        scoreN = 2000
        scored = scoreN
        count = 0
        successes = 0
        allsucc = 0
        for line in infile:
            count += 1
            if count > scoreN: break
            words = line.split()
            correct = words[-1]
            N = len(words)
            seed = ' '.join(words[0:-1])
            try:
                samp = sampler.generate(2, num_sequences=300, seed_sequence= seed)
            except:
                print('FAILL')
                scored -= 1
                continue
            allwords = printSample(samp)
            print(seed)
            print(correct)
            c = Counter(re.findall(r'\w+', allwords))
            print(c.most_common(3))
            print(c[correct])
            if c[correct]>=1: successes += 1
            allsucc += c[correct]
            outfile.write(line)
            outfile.write('CORRECT: ' + correct +  '  with prob.: ' + '{:.3f}'.format(c[correct]/300) + '%' + '    (Most probable word: ' + c.most_common(1)[0][0] + ' {:.3f}'.format(c.most_common(1)[0][1]/300)+ '%)' +'\n')
            outfile.write('\n')
        print('Word suggested: ',100*successes/scored, '%')
        print('Total mass: ',100*allsucc/(scored*300), '%')
        print('Scored: ', scored)
    return successes/scored


score = scoreTest('catsTrain10k.txt')


assert(False)



seed = "i admire your dedication to helping all those"
correct = 'kittens'
wordN = 1
seedN = len(seed.split(' '))
seqN = 1500
#samp = sampler.generate(wordN + 1, num_sequences=seqN, seed_sequence=seed)
samp = sampler.generate(15, num_sequences=30)#, seed_sequence=seed)

allwords = ''
for sequence in samp:
    pstr = ''
    for i,s in enumerate(sequence):
        if i > 0:
            pstr = pstr + s + ' '
    print(pstr)
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

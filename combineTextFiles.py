#  This concatenates all files that scraper has produces
#  Run when command line in TextCompletion folder

import numpy as np
import matplotlib.pyplot as plt
import glob
import os
files = glob.glob('./scraper/threads/*.txt') # Assumes that in TextCompletion folder

linesRead = 0 
words = []
with open('concatenatedCats.txt', 'w') as outfile:
    for f in files:
        with open(f) as infile:
            for line in infile:
                outfile.write(line)
                if line[0]==' ':  # Remove the space if there is one in the start
                    line = line[1:]
                words.append( len(line.split()) )
                linesRead += 1

print('There are ', linesRead, 'lines (Individual comments)')
print('There are ', np.sum(words), 'words in total')
plt.figure()
plt.hist(words, bins=300)

plt.xlabel('Message length (words)')
plt.ylabel('Amount of messages')
plt.title('Distribution of message lenghts')
plt.show()
assert(False)

np.random.seed(None)
order = np.random.choice(2,size=linesRead, replace=True, p=np.array([0.7, 0.3]))

with open('catsTrain.txt', 'w') as train, open('catsTest.txt', 'w') as test:  #,open(catsValidate.txt, 'w') as valid
    i = 0
    with open('concatenatedCats.txt', 'r') as file:
        for line in file:
            if order[i]==0:
                train.write(line)
            elif order[i]==1:
                test.write(line)
            #elif order[i]==2:
                #valid.write(line)
            i += 1

trainbytes = os.path.getsize('catsTrain.txt')
testbytes = os.path.getsize('catsTest.txt')

print('The test set size is: ', 100*testbytes/(testbytes+trainbytes), ' %')
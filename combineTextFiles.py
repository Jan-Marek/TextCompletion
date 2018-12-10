#  This concatenates all files that scraper has produces
#  Run when command line in TextCompletion folder

import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import re
files = glob.glob('./scraper/threads/*.txt') # Assumes that in TextCompletion folder

def tsplit(string, delimiters):
    """Behaves str.split but supports multiple delimiters."""
    delimiters = tuple(delimiters)
    stack = [string,]
    
    for delimiter in delimiters:
        for i, substring in enumerate(stack):
            substack = substring.split(delimiter)
            stack.pop(i)
            for j, _substring in enumerate(substack):
                stack.insert(i+j, _substring)
    return stack


linesRead = 0 
words = []
with open('concatenatedCats.txt', 'w') as outfile:
    for f in files:
        with open(f) as infile:
            for line in infile:
                if line[0]==' ':  # Remove the space if there is one in the start
                    line = line[1:]
                line = re.sub('®', ' ', line)
                line = re.sub(r'^https?:\/\/.*[\r\n]*', '', line)

                line = line.replace('<', ' ')
                line = line.replace('>', ' ')
                line = line.replace('*', ' ')
                line = line.replace('~', ' ')
                line = line.replace('+', ' ')
                line = line.replace('€', ' ')
                line = line.replace('$', ' ')
                line = line.replace('}', ' ')
                line = line.replace('{', ' ')
                line = line.replace('+', ' ')

                #Removing the - could be argued? profit?
                line = line.replace('-', ' ')
                line = re.sub(r'@\w+', r' <name> ',line)   # @ symbol with word substituted with tag <name>

                # Remove multiple occurences of . ? and !
                line = re.sub(r'\.+', ".", line)
                line = re.sub(r'\!+', "!", line)
                line = re.sub(r'\?+', "?", line)
                #line = line.replace('.', ' .')
                line = line.replace(',', ' ')

                # Just replace / with word or
                line = line.replace(r'/', ' or ')

                # Replace numbers with number tag
                line = re.sub(r"\d+", ' <num> ', line)

                line = line.replace(':', ' ')
                line = line.replace('"', ' ')
                line = line.replace('(', ' ')
                line = line.replace(')', ' ')
                line = line.replace('[', ' ')
                line = line.replace(']', ' ')

                # lastly substitute multiple spaces with one
                line = re.sub(' +', ' ', line)
                words.append( len(line.split()) )
                for i in tsplit(line, ('?', '!', '.')):  # split by ! . and ?
                    if len(line)>0:
                        linesRead += 1
                        outfile.write( i )

printAnalysis = False
if printAnalysis:
    print('There are ', linesRead, 'lines (Individual comments)')
    print('There are ', np.sum(words), 'words in total')
    plt.figure()
    plt.hist(words, bins=300)

    plt.xlabel('Message length (words)')
    plt.ylabel('Amount of messages')
    plt.title('Distribution of message lenghts')
    plt.show()
else:
    np.random.seed(1111)
    print(linesRead)
    order = np.random.choice(2,size=linesRead+1, replace=True, p=np.array([0.9, 0.1]))

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
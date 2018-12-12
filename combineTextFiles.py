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
messages = 0
words = []
takeFiles = 0 # tells how many files to take
filesN = 1000000 # files taken at maximum
with open('concatenatedCats.txt', 'w') as outfile:
    for f in files:
        takeFiles = takeFiles + 1
        if takeFiles > filesN: # only max amount of files
            break

        with open(f) as infile:
            for line in infile:
                line = re.sub(r'^https?:\/\/.*[\r\n]*', '', line) # remove links
                line = line.replace('®', ' ')
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
                line = line.replace(';', ' ')
                line = line.replace('"', ' ')
                line = line.replace('(', ' ')
                line = line.replace(')', ' ')
                line = line.replace('[', ' ')
                line = line.replace(']', ' ')

                # limit only to some characters
                line = re.sub(r"[^a-z.!?'<>]+", ' ', line)

                # lastly substitute multiple spaces with one
                line = re.sub(' +', ' ', line)
                senList = tsplit(line, ('?', '!', '.'))
                used = False
                for ind, utter in enumerate(senList):  # split by ! . and ?
                    if len(utter)>=6 and len(utter.split())>=4 and len(utter.split())<=200:  #require at least 6 characters and 4 words for utterance to pass
                        if utter[0]==' ':  # Remove the space if there is one in the start
                            utter = utter[1:]
                        linesRead += 1
                        words.append( len(utter.split()) )
                        if ind+1 == len(senList): 
                            outfile.write( utter )
                        else:
                            outfile.write( utter + "\n")    
                        used = True
                if used: messages += 1

printAnalysis = True
if printAnalysis:
    print('There are ', linesRead, 'lines (Individual sentences)')
    print('There are ', np.sum(words), 'words in total')
    print(messages, 'messages were used in total')
    print("words shorter than 40", np.sum(np.array(words)<=40)/len(words)) 
    plt.figure()
    plt.hist(words, bins=200)
    print(np.median(words))
    print(np.mean(words))
    plt.xlabel('Sentence length (words)')
    plt.ylabel('Amount of sentences')
    plt.title('Distribution of sentence lenghts')
    plt.show()
if True:
    np.random.seed(1111)
    print(linesRead)
    order = np.random.choice(2,size=linesRead+1, replace=True, p=np.array([0.9, 0.1]))

    with open('catsTrain.txt', 'w') as train, open('catsTest.txt', 'w') as test:  #,open(catsValidate.txt, 'w') as valid
        i = 0
        with open('concatenatedCats.txt', 'r') as file:
            for l in file:
                if len(l) > 3:
                    if order[i]==0:
                        train.write(l)
                    if order[i]==1:
                        test.write(l)
                    i += 1

    trainbytes = os.path.getsize('catsTrain.txt')
    testbytes = os.path.getsize('catsTest.txt')

    print('The test set size is: ', 100*testbytes/(testbytes+trainbytes), ' %')
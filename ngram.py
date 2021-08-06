# simple example of using simpletext files
#
# All this does is count words (ngrams - with n=1) and write a CSV file with the top 100 as the columns
#
# this uses the standard python tokenization tools
import sklearn.feature_extraction.text as SFT

# we use a token pattern that duplicates what we did in the VEP tokenizer
# this was created by Erin to be as close as possible to the hand-coded one
# but it works in the standard way
# this is probably the most magical bit
simple_word_pat = r'\w+(?:[\-\'\^\*]?\w)*'
erin_word_pat = r'[0-9]+(?:[\,\.][0-9]+)+|[\w\^]+(?:[\-\'\*][\w\^]+)*'

# simple way to get a list of files
import glob

# the word counts are in a matrix - so we need to use the math tools
import numpy

# for dealing with filenames
import os.path

# write a CSV file - the old fashioned way
import csv

# other useful things
import time


def ngram(dir, *, ext="txt", topN=20):
    # get rid of leading . in extension since the search pattern takes care of it
    if (ext[0]=="."):
        ext = ext[1:]
    # get a list of files to process
    files = glob.glob(dir + "/**/*[.]" + ext, recursive=True)
    print("Files to Process: ",len(files))

    # this actually loads in the files - the vectorizer is the data structure
    startT = time.time()
    countVectorizer = SFT.CountVectorizer("filename", token_pattern=erin_word_pat)
    wordMatrix = countVectorizer.fit_transform(files)
    endT = time.time()
    print("Reading produced a {} matrix with {} non-zeros in {:.2f} seconds".format(wordMatrix.shape,
                                                                            wordMatrix.getnnz(),
                                                                            endT - startT))

    # now we have a massive matrix, with a column for every word and a row for every document
    # this is the word for each column
    terms =countVectorizer.get_feature_names()

    # we want to just get the top-N words
    # first, get the word frequencies by summing across the documents
    totals = wordMatrix.sum(axis=0)
    # sort in order (this makes a list of column numbers
    # unfortunately, this is a tensor - which is inconvenient, so change it to a 1D array
    topWords = numpy.array(numpy.flip(numpy.argsort(totals)).flat)

    # print out the top 5 words...
    print("The top 5 words are: ",[terms[idx] for idx in topWords[:5]])

    # get the length of each document - again, need to get rid of the weird tensor thing
    docLengths=numpy.array(wordMatrix.sum(axis=1).flat)

    # get a matrix of the top N words
    topGrams = wordMatrix[:,topWords[:topN]].toarray()

    # now to write it out
    with open("ngrams.csv","w",newline='') as fo:
        w = csv.writer(fo)
        # make the header...
        w.writerow(["Document","Total Length"] + [terms[idx] for idx in topWords[:topN]])

        # now write out each row...
        for i,doc in enumerate(files):
            doclen = docLengths[i]
            row = [os.path.basename(doc),doclen]
            for v in topGrams[i]:
                row.append(0 if doclen==0 or v==0 else float(v)/float(doclen))
            w.writerow(row)

    return countVectorizer,wordMatrix
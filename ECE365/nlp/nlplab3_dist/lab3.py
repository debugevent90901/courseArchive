import numpy as np
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import defaultdict, Counter
from nltk.lm import Laplace
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm.preprocessing import pad_both_ends
import copy


# deliverable 1.1
def tokenize_corpus(corpus):
    '''
    Returns the tokenized version of the nltk corpus string.

    :param corpus: str, corpus
    :returns: tokenized version of corpus
    :rtype: list of list of strings

    Hint: use nltk.tokenize.sent_tokenize, and nltk.tokenize.word_tokenize
    '''
    return [word_tokenize(i) for i in sent_tokenize(corpus)]
    # raise NotImplementedError


# deliverable 1.2
def pad_corpus(corpus):
    '''
    Returns a padded version of the tokenized corpus.

    :param corpus: list of list of str, tokenized corpus.
    :returns: padded version of the tokenized corpus.
    :rtype: list of list of strings
    '''

    start_symbol = '<s>'
    end_symbol = '</s>'

    a_copy = copy.deepcopy(corpus)
    for i in a_copy:
        i.insert(0, start_symbol)
        i.append(end_symbol)
    return a_copy
    # raise NotImplementedError


# deliverable 1.3
def split_corpus(corpus):
    '''
    Splits the input corpus into a train and test corpus based on a 80-20 split.

    :param corpus: list of list of str, padded tokenized corpus.
    :returns: train subset of the corpus.
    :returns: test subset of the corpus.
    :rtype: list of list of strings, list of list of strings
    '''
    coeffi = int(np.floor(len(corpus) * 0.8))
    return corpus[0: coeffi], corpus[coeffi:]
    # raise NotImplementedError


# deliverable 1.4
def count_ngrams(corpus, n=3):
    '''
    Takes in a corpus and counts the frequency of all unique n-grams (1-grams, 2-grams, ..., up to length n), and stores them in a dictionary. It also returns a list of all unique words (vocab).

    :param corpus: list of list of str, padded tokenized training corpus.
    :param n: maximum order of n-grams considered.
    :returns: dictionary of count of n-grams. Keys are n-grams (tuples), and values are their frequency in the corpus.
    :returns: list of vocab words
    :rtype: dictionary (key: tuple, value: int), list of strings
    '''
    freq_dict = defaultdict()
    word_list = []
    for i in corpus:
        word_list.extend(i)

    n_gram_list = []
    for i in range(n+1):
        for j in corpus:
            n_gram_list.extend(nltk.ngrams(j, i))

    freq_dict = defaultdict(int, Counter(n_gram_list))

    return freq_dict, list(set(word_list))
    # raise NotImplementedError


# deliverable 1.5
def estimate(counts, word, context):
    '''
    Estimates the n-gram probability of a word [w_i] following a context of size n-1.

    :param counts: a dictionary of n-gram counts.
    :param word: a list of one word, [w_i]
    :param context: a list of preceding n-1 words in order
    :returns: probability of the n-gram.
    :rtype: float.
    '''
    count_two, count_three = 0, 0
    order = len(context) + 1
    for i in counts.keys():
        if len(i) == order:
            gram_list = list(i)
            if gram_list[: order-1] == context:
                count_two += counts[i]
                if gram_list[order-1: ] == word:
                    count_three = counts[i]
    return count_three / count_two



# deliverable 2.1
def get_perplexity(lm, test_data):
    '''
    Evaluate perplexity of language model lm on test corpus test_data

    :param lm: NLTK Language Model object.
    :param test_data: list of str, test corpus as a sequence of words.
    :returns: perplexity of language model lm when tested on test_data.
    :rtype: float

    Hint: use NLTK LM's method 'perplexity'.
    '''
    return lm.perplexity(test_data)
    # raise NotImplementedError


# deliverable 3.1
def vary_ngram(train_corpus, test_corpus, n_gram_orders):
    '''
    Use the nltk.lm.Laplace for training.
    Returns a dictionary of perplexity values at different order n-gram LMs

    :param train_corpus: list of list of str, corpus to train language model on.
    :param test_corpus: list of list of str, corpus to test language model on.
    :n_gram_orders: list of ints, orders of n-grams desired.
    :returns: a dictionary of perplexities at different orders, key=order, value=perplexity.
    :rtype: dict.

    Hint: Follow the same LM training procedure as in the notebook in the end of Exercise 1.
    '''
    perplexity_dict = defaultdict()
    test = sum([['<s>'] + x + ['</s>'] for x in test_corpus], [])
    for order in n_gram_orders:
        train, vocab = padded_everygram_pipeline(order, train_corpus)
        lm = Laplace(order)
        lm.fit(train, vocab)
        perplexity_dict[order] = get_perplexity(lm, test)
    return perplexity_dict
    # raise NotImplementedError

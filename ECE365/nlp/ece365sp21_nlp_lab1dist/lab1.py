from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import matplotlib.pyplot as plt
from nltk.corpus import udhr


def get_freqs(corpus, puncts):
    freqs = {}
    # BEGIN SOLUTION
    puncts = ['.', '!', '?', ',', ';', ':',
            '[', ']', '{', '}', '(', ')', '\'', '\"']
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in puncts:
        corpus = corpus.replace(i, ' ')
    for i in digits:
        corpus = corpus.replace(i, ' ')
    word_list = corpus.lower().split()
    for word in word_list:
        if word in freqs:
            freqs[word] += 1
        else:
            freqs[word] = 1
    # END SOLUTION
    return freqs


def get_top_10(freqs):
    top_10 = []
    # BEGIN SOLUTION
    sorted_freqs = sorted(freqs.items(), key=lambda item: item[1], reverse=True)
    top_10 = [word[0] for word in sorted_freqs[: 10]]
    # END SOLUTION
    return top_10


def get_bottom_10(freqs):
    bottom_10 = []
    # BEGIN SOLUTION
    sorted_freqs = sorted(freqs.items(), key=lambda item: item[1], reverse=False)
    bottom_10 = [word[0] for word in sorted_freqs[: 10]]
    # END SOLUTION
    return bottom_10


def get_percentage_singletons(freqs):
    # BEGIN SOLUTION
    return (sum(i == 1 for i in freqs.values())) * 100 / len(freqs)
    # END SOLUTION


def get_freqs_stemming(corpus, puncts):
    # BEGIN SOLUTION
    freqs = {}
    porter = PorterStemmer()
    puncts = ['.', '!', '?', ',', ';', ':',
            '[', ']', '{', '}', '(', ')', '\'', '\"']
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in puncts:
        corpus = corpus.replace(i, ' ')
    for i in digits:
        corpus = corpus.replace(i, ' ')
    word_list = corpus.lower().split()
    word_list = [porter.stem(word) for word in word_list]
    for word in word_list:
        if word in freqs:
            freqs[word] += 1
        else:
            freqs[word] = 1
    return freqs
    # END SOLUTION


def get_freqs_lemmatized(corpus, puncts):
    # BEGIN SOLUTION
    freqs = {}
    wordnet_lemmatizer = WordNetLemmatizer()
    puncts = ['.', '!', '?', ',', ';', ':',
            '[', ']', '{', '}', '(', ')', '\'', '\"']
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in puncts:
        corpus = corpus.replace(i, ' ')
    for i in digits:
        corpus = corpus.replace(i, ' ')
    word_list = corpus.lower().split()
    word_list = [wordnet_lemmatizer.lemmatize(word, pos="v") for word in word_list]
    for word in word_list:
        if word in freqs:
            freqs[word] += 1
        else:
            freqs[word] = 1
    return freqs
    # END SOLUTION


def size_of_raw_corpus(freqs):
    # BEGIN SOLUTION
    return len(freqs)
    # END SOLUTION


def size_of_stemmed_raw_corpus(freqs_stemming):
    # BEGIN SOLUTION
    return len(freqs_stemming)
    # END SOLUTION


def size_of_lemmatized_raw_corpus(freqs_lemmatized):
    # BEGIN SOLUTION
    return len(freqs_lemmatized)
    # END SOLUTION


def percentage_of_unseen_vocab(a, b, length_i):
    # BEGIN SOLUTION
    return len(set(a)-set(b)) / length_i
    # END SOLUTION


def frac_80_perc(freqs):
    # BEGIN SOLUTION
    word_num = sum(freqs.values())
    sorted_freqs = sorted(freqs.values(), reverse=True)
    count = 0
    for i in range(len(sorted_freqs)):
        count += sorted_freqs[i]
        if(count > word_num * 0.8):
            return i/len(freqs)
    # END SOLUTION

def plot_zipf(freqs):
    # BEGIN SOLUTION
    plt.plot(list(range(1, len(freqs)+1)), sorted(freqs.values(), reverse=True))
    plt.xlabel('rank of words')
    plt.ylabel('frequency of words')
    # END SOLUTION
    plt.show()  # put this line at the end to display the figure.


def get_TTRs(languages):
    TTRs = {}
    for lang in languages:
        words = udhr.words(lang)
        # BEGIN SOLUTION
        words, count =[word.lower() for word in words], []
        for i in range(100, 1301, 100):
            _type = set(words[: i])
            count.append(len(_type))
        TTRs[lang] = count   
        # END SOLUTION
    return TTRs


def plot_TTRs(TTRs):
    # BEGIN SOLUTION
    tokens = list(range(100, 1301, 100))
    for lang in TTRs:
        plt.plot(tokens, TTRs[lang], label=lang)
    plt.xlabel('amount of tokens')
    plt.ylabel('count of types')
    plt.legend()
    # END SOLUTION
    plt.show()  # put this line at the end to display the figure.

from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import matplotlib.pyplot as plt
from nltk.corpus import udhr

def get_freqs(corpus, puncts):
    freqs = {}
    ### BEGIN SOLUTION
    puncts = ['.','!','?',',',';',':','[', ']', '{', '}', '(', ')', '\'', '\"']
    digits = ['0','1','2','3','4','5','6','7','8','9']
    for i in puncts+digits:
        corpus = corpus.replace(i, ' ')
    words = corpus.lower().split()
    for w in words:
        if w in freqs:
            freqs[w] += 1
        else:
            freqs[w] = 1
    ### END SOLUTION
    return freqs

def get_top_10(freqs):
    top_10 = []
    ### BEGIN SOLUTION
    sorted_freqs = sorted(freqs.items(), key = lambda x:x[1], reverse = True)
    for w in sorted_freqs[:10]:
        top_10.append(w[0])
    ### END SOLUTION
    return top_10

def get_bottom_10(freqs):
    bottom_10 = []
    ### BEGIN SOLUTION
    sorted_freqs = sorted(freqs.items(), key = lambda x:x[1])
    for w in sorted_freqs[:10]:
        bottom_10.append(w[0])
    ### END SOLUTION
    return bottom_10

def get_percentage_singletons(freqs):
    ### BEGIN SOLUTION
    return list(freqs.values()).count(1)/len(freqs)*100
    ### END SOLUTION
    pass

def get_freqs_stemming(corpus, puncts):
    ### BEGIN SOLUTION
    freqs_stemming = {}
    puncts = ['.','!','?',',',';',':','[', ']', '{', '}', '(', ')', '\'', '\"']
    digits = ['0','1','2','3','4','5','6','7','8','9']
    for i in puncts+digits:
        corpus = corpus.replace(i, ' ')
    words = corpus.lower().split()
    porter = PorterStemmer()
    words = [porter.stem(w) for w in words]
    for w in words:
        if w in freqs_stemming:
            freqs_stemming[w] += 1
        else:
            freqs_stemming[w] = 1
    return freqs_stemming
    ### END SOLUTION
    pass

def get_freqs_lemmatized(corpus, puncts):
    ### BEGIN SOLUTION
    freqs_lemmatized = {}
    puncts = ['.','!','?',',',';',':','[', ']', '{', '}', '(', ')', '\'', '\"']
    digits = ['0','1','2','3','4','5','6','7','8','9']
    for i in puncts+digits:
        corpus = corpus.replace(i, ' ')
    words = corpus.lower().split()
    wordnet_lemmatizer = WordNetLemmatizer()
    words = [wordnet_lemmatizer.lemmatize(w, pos="v") for w in words]
    for w in words:
        if w in freqs_lemmatized:
            freqs_lemmatized[w] += 1
        else:
            freqs_lemmatized[w] = 1
    return freqs_lemmatized
    ### END SOLUTION
    pass

def size_of_raw_corpus(freqs):
    ### BEGIN SOLUTION
    return len(freqs.values())
    ### END SOLUTION
    pass

def size_of_stemmed_raw_corpus(freqs_stemming):
    ### BEGIN SOLUTION
    return len(freqs_stemming.values())
    ### END SOLUTION
    pass

def size_of_lemmatized_raw_corpus(freqs_lemmatized):
    ### BEGIN SOLUTION
    return len(freqs_lemmatized.values())
    ### END SOLUTION
    pass

def percentage_of_unseen_vocab(a, b, length_i):
    ### BEGIN SOLUTION
    set_a = set(a)
    set_b = set(b)
    return len(set_a-set_b)/length_i
    ### END SOLUTION
    pass

def frac_80_perc(freqs):
    ### BEGIN SOLUTION
    sorted_freqs = sorted(freqs.values(), reverse = True)
    num_80 = sum(sorted_freqs)*0.8
    cnt = 0
    for i in range(len(sorted_freqs)):
        cnt += sorted_freqs[i]
        if(cnt > num_80):
            return i/len(sorted_freqs)
    ### END SOLUTION
    pass

def plot_zipf(freqs):
    ### BEGIN SOLUTION
    rank = list(range(1, len(freqs)+1))
    sorted_freqs = sorted(freqs.values(), reverse = True)
    plt.plot(rank, sorted_freqs)
    plt.xlabel('rank of words')
    plt.ylabel('frequency of words')
    ### END SOLUTION
    plt.show()  # put this line at the end to display the figure.

def get_TTRs(languages):
    TTRs = {}
    for lang in languages:
        words = udhr.words(lang)
        ### BEGIN SOLUTION
        TTRs[lang] = []
        for t in range(100, 1301, 100):
            lower_words = [w.lower() for w in words[:t]]
            TTRs[lang].append(len(set(lower_words)))
        ### END SOLUTION
    return TTRs

def plot_TTRs(TTRs):
    ### BEGIN SOLUTION
    tokens = list(range(100,1301,100))
    for lang in TTRs:
        plt.plot(tokens, TTRs[lang], label = lang)
    plt.xlabel('amount of tokens')
    plt.ylabel('count of types')
    plt.legend()
    ### END SOLUTION
    plt.show()  # put this line at the end to display the figure.

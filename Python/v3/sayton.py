import tensorflow as tf
import tflearn

import random
import numpy as np

'''
NOTE:
This attempts SkipGram/Word2Vec model. It doesn't have negative sampling so it's garbage. Don't run this on anything except small sets. 

https://towardsdatascience.com/learn-word2vec-by-implementing-it-in-tensorflow-45641adaf2ac
'''


print("Pulling in data...")
path = "../../Data/new.txt"
f = open(path, encoding="utf-8")
f = f.read()
f = f.split("\n\n")

# NOTE: Comment this out to attempt to run with the full dataset
f = ['The quick brown fox jumps over the lazy dog', 'There is a snake in my boot', 'I sell propane and propane accessories']

corpus_raw = f
raw_sentences = f

print("Parsing data...")

max_len_seq = 0
for seq in f:
    if len(seq) > max_len_seq:
        max_len_seq = len(seq)

# convert to lower case
# corpus_raw = corpus_raw.lower()

words = []
for message in corpus_raw:
    for word in message.split():
        if word != '.':  # because we don't want to treat . as a word
            words.append(word)

words = set(words)  # so that all duplicate words are removed
word2int = {}
int2word = {}
vocab_size = len(words)  # gives the total number of unique words

for i, word in enumerate(words):
    word2int[word] = i
    int2word[i] = word

# raw sentences is a list of sentences.
sentences = []
for sentence in raw_sentences:
    sentences.append(sentence.split())

WINDOW_SIZE = 2

print("REALLY parsing data...")

data = []
for sentence in sentences:
    for word_index, word in enumerate(sentence):
        for nb_word in sentence[max(word_index - WINDOW_SIZE, 0): min(word_index + WINDOW_SIZE, len(sentence)) + 1]:
            if nb_word != word:
                data.append([word, nb_word])

# function to convert numbers to one hot vectors


# def to_one_hot(data_point_index, vocab_size):
#     temp = np.zeros(vocab_size)
#     temp[data_point_index] = 1
#     return temp


x_train = []  # input word
y_train = []  # output word

for data_word in data:
    tempx = np.zeros(vocab_size)
    tempy = tempx
    tempx[word2int[data_word[0]]] = 1
    tempx[word2int[data_word[1]]] = 1
    x_train.append(tempx)
    y_train.append(tempy)

# x_train = tf.one_hot(x_train, vocab_size)
# y_train = tf.one_hot(y_train, vocab_size)


    # tempx = np.zeros(vocab_size)
    # tempy = tempx
    # tempx[word2int[data_word[0]]] = 1
    # tempx[word2int[data_word[1]]] = 1
    # x_train.append(tempx)
    # y_train.append(tempy)

    # x_train.append(to_one_hot(word2int[data_word[0]], vocab_size))
    # y_train.append(to_one_hot(word2int[data_word[1]], vocab_size))

# convert them to numpy arrays
# x_train = np.asarray(x_train)
# y_train = np.asarray(y_train)

print("Setting up network...")

x = tf.placeholder(tf.float32, shape=(None, vocab_size))
y_label = tf.placeholder(tf.float32, shape=(None, vocab_size))

EMBEDDING_DIM = 5 # you can choose your own number
W1 = tf.Variable(tf.random_normal([vocab_size, EMBEDDING_DIM]))
b1 = tf.Variable(tf.random_normal([EMBEDDING_DIM])) #bias
hidden_representation = tf.add(tf.matmul(x,W1), b1)

W2 = tf.Variable(tf.random_normal([EMBEDDING_DIM, vocab_size]))
b2 = tf.Variable(tf.random_normal([vocab_size]))
prediction = tf.nn.softmax(tf.add( tf.matmul(hidden_representation, W2), b2))


sess = tf.Session()
init = tf.global_variables_initializer()
sess.run(init) #make sure you do this!

# define the loss function:
cross_entropy_loss = tf.reduce_mean(-tf.reduce_sum(y_label * tf.log(prediction), reduction_indices=[1]))

# define the training step:
train_step = tf.train.GradientDescentOptimizer(0.1).minimize(cross_entropy_loss)

n_iters = 10000
# train for n_iter iterations

for _ in range(n_iters):
    sess.run(train_step, feed_dict={x: x_train, y_label: y_train})
    print('loss is : ', sess.run(cross_entropy_loss, feed_dict={x: x_train, y_label: y_train}))

vectors = sess.run(W1 + b1)

def euclidean_dist(vec1, vec2):
    return np.sqrt(np.sum((vec1-vec2)**2))

def find_closest(word_index, vectors):
    min_dist = 10000 # to act like positive infinity
    min_index = -1
    query_vector = vectors[word_index]
    for index, vector in enumerate(vectors):
        if euclidean_dist(vector, query_vector) < min_dist and not np.array_equal(vector, query_vector):
            min_dist = euclidean_dist(vector, query_vector)
            min_index = index
    return min_index


from sklearn.manifold import TSNE

model = TSNE(n_components=2, random_state=0)
np.set_printoptions(suppress=True)
vectors = model.fit_transform(vectors) 

from sklearn import preprocessing

normalizer = preprocessing.Normalizer()
vectors =  normalizer.fit_transform(vectors, 'l2')

print(vectors)

import matplotlib.pyplot as plt


fig, ax = plt.subplots()
print(words)
for word in words:
    print(word, vectors[word2int[word]][1])
    ax.annotate(word, (vectors[word2int[word]][0],vectors[word2int[word]][1] ))
plt.show()

import tensorflow
import tflearn

import random
import numpy as np


'''
NOTE:
This was an attempt at implementing word2vec/skip-gram model with tflearn. 
tflearn currently isn't suited to do word model networks and only works on character model networks. Lame. 
Currently left in a broken state as the lines: 
    print(m.generate(600, temperature=1.0, seq_seed=seed))
Is the part setup for character models. I've looked into changing the tflearn code but that doesn't seem like the best idea. 
'''

path = "../../Data/new.txt"
f = open(path, encoding="utf-8")
f = f.read()
f = f.split("\n\n")

max_len_seq = 0
for seq in f:
    if len(seq) > max_len_seq:
        max_len_seq = len(seq)

print(max_len_seq)


# Creating our word dictionary and training/testing data
vp = tflearn.data_utils.VocabularyProcessor(max_len_seq, min_frequency=0)
vp = vp.fit(f)

trainingData = np.array(list(vp.transform(f)))

word_dict = vp.vocabulary_._mapping
vp.save('word_dict')

word2int = word_dict
int2word = {v: k for k, v in word2int.items()}


words = f
words = set(words)


word2int = {}
int2word = {}
vocab_size = len(word_dict)  # gives the total number of unique words
for i, word in enumerate(words):
    word2int[word] = i
    int2word[i] = word

sentences = []
for sentence in f:
    sentences.append(sentence.split())

data = []
WINDOW_SIZE = 2
for sentence in sentences:
    for word_index, word in enumerate(sentence):
        for nb_word in sentence[max(word_index - WINDOW_SIZE, 0): min(word_index + WINDOW_SIZE, len(sentence)) + 1]:
            if nb_word != word:
                data.append([word, nb_word])


def to_one_hot(data_point_index, vocab_size):
    temp = np.zeros(vocab_size)
    temp[data_point_index] = 1
    return temp

vocab_size = len(word_dict)

Xtrain = []  # input word
Ytrain = []  # output word
for data_word in data:
    tempx = to_one_hot(word_dict[data_word[0]], vocab_size)
    tempy = to_one_hot(word_dict[data_word[1]], vocab_size)
    Xtrain.append(tempx)
    Ytrain.append(tempy)
# convert them to numpy arrays
Xtrain = np.asarray(Xtrain)
Ytrain = np.asarray(Ytrain)

g = tflearn.input_data(shape=[None, max_len_seq])
g = tflearn.embedding(g, input_dim=len(word_dict), output_dim=128)
g = tflearn.lstm(g, 512, return_seq=True)
g = tflearn.dropout(g, 0.5)
g = tflearn.lstm(g, 512)
g = tflearn.dropout(g, 0.5)
g = tflearn.fully_connected(g, len(word_dict), activation='softmax')
g = tflearn.regression(g, optimizer='adam', loss='categorical_crossentropy',
                       learning_rate=0.001)

m = tflearn.SequenceGenerator(g, dictionary=word_dict,
                              seq_maxlen=max_len_seq,
                              clip_gradients=5.0,
                              checkpoint_path='./checkpoints/sayton_model')

for i in range(50):
    seed = random.choice(f)
    m.fit(X, Y, validation_set=0.1, batch_size=128,
          n_epoch=1, run_id='sayton')
    print("-- TESTING...")
    print("-- Test with temperature of 1.0 --")
    print(m.generate(600, temperature=1.0, seq_seed=seed))
    print("-- Test with temperature of 0.5 --")
    print(m.generate(600, temperature=0.5, seq_seed=seed))

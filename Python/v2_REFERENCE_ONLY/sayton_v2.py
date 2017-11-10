from __future__ import absolute_import, division, print_function

import os
import pickle
from six.moves import urllib
import past 

import tflearn
from tflearn.data_utils import *

'''
NOTES: 
I forget what I was doing here, I think this was the start of getting word model working and I was jsut trying to understand tflearn. 
Probaly doesn't work for anything. Don't run it. 
'''

# TODO - Read the data in as chunks of 10,000 lines or something. 
# path = "../../Data/new.txt"
path = "./shakespeare_input.txt"
char_idx_file = 'char_idx_v2.pickle'

maxlen = 25

# Load the data in and create a character index (a dictionary of the words and the number of times they are repeated)
char_idx = None
if os.path.isfile(char_idx_file):
    print('Loading previous char_idx')
    char_idx = pickle.load(open(char_idx_file, 'rb'))

# This is actually just calling string_to_semi_redudant_sequences for everything in our textfile for us. 
# so if you wanna see the docs for it look at the source code or string_to_semi_redudant_sequences
# X are the inputs, Y are the outputs
# X, Y, char_idx = \
#     textfile_to_semi_redundant_sequences(path, seq_maxlen=maxlen, redun_step=3)

# TODO - What do these look like?
# print(X)
# print(Y)


# Saves our dictionary for later use
pickle.dump(char_idx, open(char_idx_file, 'wb'))


# New
g = tflearn.input_data([None, maxlen, len(char_idx)])
# g = tflearn.fully_connected(g, len(char_idx), activation='softmax')
# g = tflearn.embedding(g, 10000, 342)
g = tflearn.bidirectional_rnn(g, tflearn.BasicLSTMCell(342), tflearn.BasicLSTMCell(342), dynamic=True)
g = tflearn.dropout(g, 0.5)
g = tflearn.fully_connected(g, len(char_idx), activation='softmax')
g = tflearn.regression(g, optimizer='adam', loss='categorical_crossentropy',learning_rate=0.001)


# Old
# g = tflearn.input_data([None, maxlen, len(char_idx)])
# g = tflearn.lstm(g, 512, return_seq=True)
# g = tflearn.dropout(g, 0.5)
# g = tflearn.lstm(g, 512, return_seq=True)
# g = tflearn.dropout(g, 0.5)
# g = tflearn.lstm(g, 512)
# g = tflearn.dropout(g, 0.5)
# g = tflearn.fully_connected(g, len(char_idx), activation='softmax')
# g = tflearn.regression(g, optimizer='adam', loss='categorical_crossentropy',
#                        learning_rate=0.001)

m = tflearn.SequenceGenerator(g, dictionary=char_idx,
                              seq_maxlen=maxlen,
                              clip_gradients=5.0,
                              checkpoint_path='./checkpoints/sayton_model')

for i in range(50):
    seed = random_sequence_from_textfile(path, maxlen)
    m.fit(X, Y, validation_set=0.1, batch_size=128,
          n_epoch=1, run_id='shakespeare')
    print("-- TESTING...")
    print("-- Test with temperature of 1.0 --")
    print(m.generate(600, temperature=1.0, seq_seed=seed))
    print("-- Test with temperature of 0.5 --")
    print(m.generate(600, temperature=0.5, seq_seed=seed))

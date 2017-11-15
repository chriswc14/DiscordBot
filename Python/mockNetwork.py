import random
import sys
import pickle
import tflearn
from tflearn.data_utils import *


def createNetwork(max_len, char_dict, save_load_point):
    g = tflearn.input_data([None, max_len, len(char_dict)])
    g = tflearn.lstm(g, 512, return_seq=True)
    g = tflearn.dropout(g, 0.5)
    g = tflearn.lstm(g, 512, return_seq=True)
    g = tflearn.dropout(g, 0.5)
    g = tflearn.lstm(g, 512)
    g = tflearn.dropout(g, 0.5)
    g = tflearn.fully_connected(g, len(char_dict), activation='softmax')
    g = tflearn.regression(
        g, optimizer='adam', loss='categorical_crossentropy', learning_rate=0.001)

    m = tflearn.SequenceGenerator(g, dictionary=char_dict, seq_maxlen=max_len,
                                  clip_gradients=5.0, max_checkpoints=5, checkpoint_path=save_load_point)

    return m

# Data must have each message on a newline


def getData(path, max_len=30, char_dict=None):
    X, Y, char_dict = \
        textfile_to_semi_redundant_sequences(
            path, seq_maxlen=max_len, redun_step=3, pre_defined_char_idx=char_dict)
    return X, Y, char_dict

# Returns the trained network


def trainNetwork(network, X, Y, epochs, run_id="sayton"):
    network.fit(X, Y, validation_set=0.1, batch_size=128,
                n_epoch=epochs, run_id=run_id)
    return network


def runNetwork(seed, network):
    # responses = ['hello', 'whats up', 'sup', 'yayaya',
    #              'happy birthday', 'im a real person i swear']
    print(seed)
    seed = " ".join(seed)
    print(seed)
    output = network.generate(len(seed), temperature=0.1, seq_seed=seed)

    return output


def main():
    data_path = "../Data/Parsed/anon_discord.txt"
    char_dict_path = "./char_dict.pkl"
    save_load_point = "./Sayton_Checkpoints/sayton.model"
    max_len = 30

    char_dict = pickle.load(open(char_dict_path, 'rb'))

    X, Y, char_dict = getData(data_path, max_len, char_dict=char_dict)

    network = createNetwork(max_len, char_dict, save_load_point)
    network.load(save_load_point)



    run = True
    while run == True:
        call = sys.stdin.readline().split()
        if call[0] == 'runNetwork':
            res = runNetwork(call[1:max_len], network)
        # elif call[0] == 'saveNetwork':
        #     res = saveNetwork(call[1], call[2])
        # elif call[0] == 'loadNetwork':
        #     res = loadNetwork(call[1])
        # elif call[0] == 'trainNetwork':
        #     res = trainNetwork(call[1], call[2], call[3])
        else:
            res = "nothing workd ;_;"
        print(res)


def test():
    data_path = "../Data/Parsed/anon_discord.txt"
    char_dict_path = "./char_dict.pkl"
    save_load_point = "./Sayton_Checkpoints/sayton.model"
    max_len = 30

    char_dict = pickle.load(open(char_dict_path, 'rb'))

    X, Y, char_dict = getData(data_path, max_len, char_dict=char_dict)

    network = createNetwork(max_len, char_dict, save_load_point)

    for i in range(50):
        network.load(save_load_point)
        # network = trainNetwork(network, X, Y, epochs=1)
        # network.save(save_load_point)

        seed = sys.stdin.readline()
        # seed = random_sequence_from_textfile(data_path, max_len)
        print("-- TESTING...")
        print("-- Test with temperature of 1.0 --")
        print(network.generate(len(seed), temperature=1.0, seq_seed=seed))
        print("-- Test with temperature of 0.5 --")
        print(network.generate(len(seed), temperature=0.5, seq_seed=seed))
        print("-- Test with temperature of 0.1 --")
        print(network.generate(len(seed), temperature=0.1, seq_seed=seed))


main()

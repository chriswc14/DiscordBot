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


def runNetwork(seed, network, max_len):
    seed = " ".join(seed)
    msg = prepMsg(seed, max_len)
    output = network.generate(len(msg) * 5, temperature=0.25, seq_seed=msg)

    '''
    So to make this look good we need to pull some tricks. 
    Make it generate a lot of messages, hope there are atlesat 3 newlines. (aka messages)
    Generally what happens is that the first message will be a continuation of
    the seed and make no sense. The second message will be a full sentence written by the NN.
    Finally the last sentence will almost always be cut short. 
    All the middle messages are what's good. 
    '''

    output = output.split("\n")
    try:
        # output = output[1:-1]
        # output = random.choice(output)
        # The first after the initial sentence seems to be best
        output = output[1]
    except IndexError:
        return "\"This error shouldnt ever happen maybe \"- Dakota"

    return output


def prepMsg(msg, max_len):
    # Weird stupid workaround for the time being
    # buffFile = open("./buffFile.txt", mode="w", encoding="utf-8")
    # buffFile.write(msg)
    # buffFile.close()
    # msg = random_sequence_from_textfile("./buffFile.txt", max_len)

    if(len(msg) < max_len):
        msg = msg.rjust(max_len)
    else:
        # msg = random_sequence_from_string(msg, max_len)
        msg = msg[-50:]

    return msg


def main():
    data_path = "../Data/Parsed/anon_discord.txt"
    char_dict_path = "./char_dict.pkl"
    save_load_point = "./Sayton_Checkpoints/sayton.model"
    max_len = 50

    char_dict = pickle.load(open(char_dict_path, 'rb'))

    X, Y, char_dict = getData(data_path, max_len, char_dict=char_dict)

    network = createNetwork(max_len, char_dict, save_load_point)
    network.load(save_load_point)

    run = True
    while run == True:
        call = sys.stdin.readline().split()
        print(runNetwork(call, network, max_len))
        # if call[0] == 'runNetwork':
        #     res = runNetwork(call[1:], network, max_len)
        # elif call[0] == 'saveNetwork':
        #     res = saveNetwork(call[1], call[2])
        # elif call[0] == 'loadNetwork':
        #     res = loadNetwork(call[1])
        # elif call[0] == 'trainNetwork':
        #     res = trainNetwork(call[1], call[2], call[3])
        # else:
        #     res = "nothing workd ;_;"
        # print(res)


def test():
    data_path = "../Data/Parsed/anon_discord.txt"
    char_dict_path = "./char_dict.pkl"
    save_load_point = "./Sayton_Checkpoints/sayton.model"
    max_len = 50

    char_dict = pickle.load(open(char_dict_path, 'rb'))

    X, Y, char_dict = getData(data_path, max_len, char_dict=char_dict)

    network = createNetwork(max_len, char_dict, save_load_point)

    network.load(save_load_point)

    for i in range(3500):
        network = trainNetwork(network, X, Y, epochs=1)
        network.save(save_load_point)

        with open("sayton_speaks.txt", "a") as myfile:
            seed = random_sequence_from_textfile(data_path, max_len)
            myfile.write("-- TESTING WITH SEED: ")
            myfile.write(seed)
            myfile.write("-- Test with temperature of 1.0 --")
            myfile.write(network.generate(
                len(seed), temperature=1.0, seq_seed=seed))
            myfile.write("-- Test with temperature of 0.5 --")
            myfile.write(network.generate(
                len(seed), temperature=0.5, seq_seed=seed))
            myfile.write("-- Test with temperature of 0.1 --")
            myfile.write(network.generate(
                len(seed), temperature=0.1, seq_seed=seed))

        '''
        NOTE: STDIN WORKAROUND
        
        buffFile = open("./buffFile.txt", mode="w", encoding="utf-8")
        seed = sys.stdin.readline()
        buffFile.write(seed)
        buffFile.close()
        seed = random_sequence_from_textfile("./buffFile.txt", max_len)
        print(seed)

        print("-- TESTING...")
        print("-- Test with temperature of 0.5 --")
        print(network.generate(len(seed), temperature=0.5, seq_seed=seed))

        seed = random_sequence_from_textfile(data_path, max_len)
        print(seed)

        print("-- TESTING...")
        print("-- Test with temperature of 0.5 --")
        print(network.generate(len(seed), temperature=0.5, seq_seed=seed))
        '''


main()

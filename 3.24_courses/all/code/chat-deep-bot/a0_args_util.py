import argparse  # Command line parsing
import configparser  # Saving the models parameters
from chatbot.textdata import TextData

class ArgsUtil:
    
    # def __init__(self):
    #     # Model/dataset parameters
    #     #self.argsT = None

    class TestMode:
        """ Simple structure representing the different testing modes
        """
        ALL = 'all'
        INTERACTIVE = 'interactive'  # The user can write his own questions
        DAEMON = 'daemon'  # The chatbot runs on background and can regularly be called to predict something

    @staticmethod
    def parseArgs(self, args):
        """
        Parse the arguments from the given command line
        Args:
            args (list<str>): List of arguments to parse. If None, the default sys.argv will be parsed
        """

        parser = argparse.ArgumentParser()

        # Global options
        globalArgs = parser.add_argument_group('Global options')
        globalArgs.add_argument('--test',
                                nargs='?',
                                choices=[ArgsUtil.TestMode.ALL, ArgsUtil.TestMode.INTERACTIVE, ArgsUtil.TestMode.DAEMON],
                                const=ArgsUtil.TestMode.ALL, default=None,
                                help='if present, launch the program try to answer all sentences from data/test/ with'
                                     ' the defined model(s), in interactive mode, the user can wrote his own sentences,'
                                     ' use daemon mode to integrate the chatbot in another program')
        globalArgs.add_argument('--createDataset', action='store_true', help='if present, the program will only generate the dataset from the corpus (no training/testing)')
        globalArgs.add_argument('--playDataset', type=int, nargs='?', const=10, default=None,  help='if set, the program  will randomly play some samples(can be use conjointly with createDataset if this is the only action you want to perform)')
        globalArgs.add_argument('--reset', action='store_true', help='use this if you want to ignore the previous model present on the model directory (Warning: the model will be destroyed with all the folder content)')
        globalArgs.add_argument('--verbose', action='store_true', help='When testing, will plot the outputs at the same time they are computed')
        globalArgs.add_argument('--debug', action='store_true', help='run DeepQA with Tensorflow debug mode. Read TF documentation for more details on this.')
        globalArgs.add_argument('--keepAll', action='store_true', help='If this option is set, all saved model will be kept (Warning: make sure you have enough free disk space or increase saveEvery)')  # TODO: Add an option to delimit the max size
        globalArgs.add_argument('--modelTag', type=str, default= None, help='tag to differentiate which model to store/load')
        globalArgs.add_argument('--rootDir', type=str, default=None, help='folder where to look for the models and data')
        globalArgs.add_argument('--watsonMode', action='store_true', help='Inverse the questions and answer when training (the network try to guess the question)')
        globalArgs.add_argument('--autoEncode', action='store_true', help='Randomly pick the question or the answer and use it both as input and output')
        globalArgs.add_argument('--device', type=str, default='gpu', help='\'gpu\' or \'cpu\' (Warning: make sure you have enough free RAM), allow to choose on which hardware run the model')
        globalArgs.add_argument('--seed', type=int, default=None, help='random seed for replication')

        # Dataset options
        datasetArgs = parser.add_argument_group('Dataset options')
        datasetArgs.add_argument('--corpus', choices=TextData.corpusChoices(), default=TextData.corpusChoices()[0], help='corpus on which extract the dataset.')
        datasetArgs.add_argument('--datasetTag', type=str, default='', help='add a tag to the dataset (file where to load the vocabulary and the precomputed samples, not the original corpus). Useful to manage multiple versions. Also used to define the file used for the lightweight format.')  # The samples are computed from the corpus if it does not exist already. There are saved in \'data/samples/\'
        datasetArgs.add_argument('--ratioDataset', type=float, default=1.0, help='ratio of dataset used to avoid using the whole dataset')  # Not implemented, useless ?
        datasetArgs.add_argument('--maxLength', type=int, default=100, help='maximum length of the sentence (for input and output), define number of maximum step of the RNN')
        datasetArgs.add_argument('--filterVocab', type=int, default=0, help='remove rarelly used words (by default words used only once). 0 to keep all words.')
        datasetArgs.add_argument('--skipLines', action='store_true', help='Generate training samples by only using even conversation lines as questions (and odd lines as answer). Useful to train the network on a particular person.')
        #datasetArgs.add_argument('--vocabularySize', type=int, default=40000, help='Limit the number of words in the vocabulary (0 for unlimited)')
        datasetArgs.add_argument('--vocabularySize', type=int, default=5000, help='Limit the number of words in the vocabulary (0 for unlimited)')

        # Network options (Warning: if modifying something here, also make the change on save/loadParams() )
        nnArgs = parser.add_argument_group('Network options', 'architecture related option')
        nnArgs.add_argument('--hiddenSize', type=int, default=512, help='number of hidden units in each RNN cell')
        nnArgs.add_argument('--numLayers', type=int, default=2, help='number of rnn layers')
        nnArgs.add_argument('--softmaxSamples', type=int, default=0, help='Number of samples in the sampled softmax loss function. A value of 0 deactivates sampled softmax')
        #nnArgs.add_argument('--initEmbeddings', action='store_true', help='if present, the program will initialize the embeddings with pre-trained word2vec vectors')
        nnArgs.add_argument('--embeddingSize', type=int, default=64, help='embedding size of the word representation')
        #nnArgs.add_argument('--embeddingSource', type=str, default="GoogleNews-vectors-negative300.bin", help='embedding file to use for the word representation')

        # Training options
        trainingArgs = parser.add_argument_group('Training options')
        trainingArgs.add_argument('--numEpochs', type=int, default=30, help='maximum number of epochs to run')
        trainingArgs.add_argument('--saveEvery', type=int, default=2000, help='nb of mini-batch step before creating a model checkpoint')
        trainingArgs.add_argument('--batchSize', type=int, default=50, help='mini-batch size')
        trainingArgs.add_argument('--learningRate', type=float, default=0.002, help='Learning rate')
        trainingArgs.add_argument('--dropout', type=float, default=0.9, help='Dropout rate (keep probabilities)')

        
        self.args = parser.parse_args(args)

        self.args.maxLengthEnco = self.args.maxLength
        self.args.maxLengthDeco = self.args.maxLength + 2


# argsUtil = ArgsUtil()
# argsUtil.parseArgs(argsUtil, ['--test', 'daemon', '--modelTag', 'xh'])

# print(argsUtil.args.modelTag)


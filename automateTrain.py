import os
import cPickle
import numpy as np
from sklearn.mixture import GMM
from scipy.io.wavfile import read
from feature_extraction import extract_features
import warnings

warnings.simplefilter('ignore')


def addUser(username):
    try:
        curdir = os.getcwd()
        source = os.path.join(curdir, 'train_data/{}/'.format(username))
        destination = os.path.join(curdir, 'speaker_models/')
        list_file = os.path.join(curdir, "train_data/{}/list.txt".format(username))
        file_paths = open(list_file, 'r').readlines()

        features = np.asarray(())

        for path in file_paths:
            path = path.strip()
            # print path

            # Read the audio
            sr, audio = read(os.path.join(source, path))

            # Extract 40 dimesnional MFCC & Delta features
            vector = extract_features(audio, sr)

            if features.size == 0:
                features = vector
            else:
                features = np.vstack((features, vector))

        gmm = GMM(n_components=16, n_iter=200, covariance_type='diag', n_init=3)
        gmm.fit(features)

        pklFile = os.path.join(destination, "{}.gmm".format(username))
        cPickle.dump(gmm, open(pklFile, "w"))
        print "+ modelling completed for speaker: ", pklFile, " with data point = ", features.shape

        return 1
    except:
        return 0

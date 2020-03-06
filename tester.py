import os
import time
import cPickle
import numpy as np
from scipy.io.wavfile import read
from feature_extraction import extract_features
import warnings
import sys
warnings.filterwarnings("ignore")


curdir = os.getcwd()
test_dir = os.path.join(curdir, "test_data/")
speakers = os.path.join(curdir, "speaker_models/")

gmm_files = [os.path.join(speakers, fname) for fname in os.listdir(speakers) if fname.endswith('.gmm')]

models = [cPickle.load(open(fname, 'r')) for fname in gmm_files]
speakers_names = [fname.split("/")[-1].split(".gmm")[0] for fname in gmm_files]

error = 0
total_sample = 0.0

error_dict = {}
if len(sys.argv) < 2:

    print("Do you want to Test a Single Audio: Press '1' or The complete Test Audio Sample: Press '0' ?")
    take = int(raw_input().strip())

    if take == 1:
        print("Enter the File name from Test Audio Sample Collection :")
        path = raw_input().strip()
        print("Testing Audio : ", path)
        sr, audio = read(os.path.join(test_dir + path))
        vector = extract_features(audio, sr)

        log_likelihood = np.zeros(len(models))

        for i in range(len(models)):
            gmm = models[i]  # checking with each model one by one
            scores = np.array(gmm.score(vector))
            log_likelihood[i] = scores.sum()
        print(log_likelihood)
        winner = np.argmax(log_likelihood)
        print("\tdetected as - ", speakers[winner])

        time.sleep(1.0)

    elif take == 0:

        for root, subdirs, files in os.walk(test_dir):
            if files:
                speaker = root.split("/")[-1].strip()
                error_dict[speaker] = {}
                error_dict[speaker]['e_count'] = 0
                error_dict[speaker]['misclassifications'] = []
                for file in files:
                    if ".wav" in file:
                        file = file.strip()

                        total_sample += 1.0
                        print("Testing Audio : ", file)
                        sr, audio = read(os.path.join(test_dir, "{}/".format(speaker) + file))
                        vector = extract_features(audio, sr)

                        log_likelihood = np.zeros(len(models))

                        for i in range(len(models)):
                            gmm = models[i]  # checking with each model one by one
                            scores = np.array(gmm.score(vector))
                            log_likelihood[i] = scores.sum()
                        winner = np.argmax(log_likelihood)
                        print("\tDetected as - ", speakers_names[winner])

                        checker_name = speaker  # path.split("/")[0]
                        if speakers_names[winner] != checker_name:
                            error += 1
                            error_dict[speaker]['e_count'] += 1
                            error_dict[speaker]['misclassifications'].append(speakers_names[winner])
                            print("Speaker {} detected as {}".format(checker_name, speakers_names[winner]))
                        time.sleep(1.0)

        # print error, total_sample
        accuracy = ((total_sample - error) / total_sample) * 100
        print("Errors : ", error)
        print("Total Samples : ", total_sample)
        print("Error Dictionary")
        print(error_dict)
        print("The Accuracy Percentage for the current testing Performance with MFCC + GMM is : ", accuracy, "%")

    print("Hurray ! Speaker identified. Mission Accomplished Successfully. ")
elif len(sys.argv) == 2:
    file_path = sys.argv[1]
    sr, audio = read(file_path)
    vector = extract_features(audio, sr)

    log_likelihood = np.zeros(len(models))

    for i in range(len(models)):
        gmm = models[i]  # checking with each model one by one
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores.sum()
    # print(log_likelihood)
    winner = np.argmax(log_likelihood)
    print(speakers_names[winner])

else:
    print("Extra Arguments Passed.")

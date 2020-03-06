from automateTrain import addUser
from preprocessAudio import split_into_5
import os

train_dir = "train_data/"

for file in os.listdir(train_dir):
    username = file
    print(username)
    split_into_5(username)
    addUser(username)

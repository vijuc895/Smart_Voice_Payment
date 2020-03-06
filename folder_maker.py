import os
import subprocess

path = "train_data/compress"
print(os.listdir(path))

files = os.listdir(path)
cur_dir = os.getcwd()
for file in files:
    if ".wav" in file:
        print(file)
        file_dir = os.path.join(os.path.join(cur_dir, path), file.split(".")[0])
        os.mkdir(file_dir, 755)
        subprocess.call(["mv", os.path.join(path, file), file_dir])
        subprocess.call(["mv", os.path.join(file_dir, file), os.path.join(file_dir, "audio.wav")])
        # os.path.join(path, file), ])
        # subprocess.call(["rm", file])
print("Completed.")

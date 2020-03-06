import os
import subprocess


def get_file_paths(username):

    curdir = os.getcwd()

    train_folder = os.path.join(curdir, "train_data/{}/".format(username))
    # test_folder = os.path.join(curdir, "test_data/{}/".format(username))

    train_list_txt = os.path.join(train_folder, "list.txt")
    # test_list_txt = os.path.join(test_folder, "list.txt")

    in_path = os.path.join(train_folder, username+".wav")
    out_path = os.path.join(train_folder, "out%03d.wav")

    return curdir, train_folder, train_list_txt, in_path, out_path  # test_folder, test_list_txt,


def remove_noise_silence(username):

    subprocess.call([
        "sox",
        username,
        "-n",
        "noise.prof"
    ])
    subprocess.call([
        "sox",
        username,
        "filtered.wav",
        "noisered",
        "noise.prof",
        "0.21",
        "silence",
        "-l",
        "1",
        "0.3",
        "5%",
        "-1",
        "2.0",
        "5%"
    ])


def split_into_5(username, test=False):

    try:
        if not test:
            curdir, train_folder, train_list_txt, in_path, out_path = get_file_paths(username)

            subprocess.call([
                'ffmpeg',
                '-i',
                in_path,
                '-f',
                'segment',
                '-segment_time',
                '15',
                '-c',
                'copy',
                out_path]
            )
            subprocess.call(["rm", "{}audio.wav".format(train_folder)])

            with open(train_list_txt, "w") as file:
                train_list = os.listdir(train_folder)
                for item in train_list:
                    if ".wav" in item:
                        file.write(item + "\n")
                file.close()

            # with open(test_list_txt, "w") as file:
            #     test_list = os.listdir(test_folder)
            #     for item in test_list:
            #         if ".wav" in item:
            #             file.write(item)
            #     file.close()
            return 1
        # elif test:
        #
    except:
        return 0


if __name__ == "__main__":
    split_into_5()
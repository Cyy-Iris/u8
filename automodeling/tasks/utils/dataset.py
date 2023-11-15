import os


def load_data(dir):
    data = []
    for fname in os.listdir(dir):
        if fname.endswith("_input.txt"):
            key = fname.replace("_input.txt", "")
            ref_fname = key + "_label.txt"

            with open(os.path.join(dir, fname), "r") as f:
                input_txt = f.read()

            with open(os.path.join(dir, ref_fname), "r") as f:
                ref_txt = f.read()

            data.append((input_txt, ref_txt))

    return data

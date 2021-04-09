import json


def read_json(file):
    with open(file) as f:
        data = json.load(f)
    return data


def find_meaning(key, data):
    if key in data.keys():
        return data[key]
    else:
        return "Word not found"


if __name__ == "__main__":
    inp_file = "data.json"
    raw_data = read_json(inp_file)
    while True:
        word = input("Enter the word: ")
        if word.lower() != 'quit':
            meaning = find_meaning(word, raw_data)
            print(meaning)

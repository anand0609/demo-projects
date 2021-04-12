import json
from difflib import get_close_matches


def read_json(file):
    with open(file) as f:
        data = json.load(f)
    return data


def find_meaning(key, data):
    if key.lower() in data:
        return data[key.lower()]
    elif key.lower().capitalize() in data:  # Searching Nouns
        return data[key.lower().capitalize()]
    elif key.upper() in data:  # Searching upper case Acronyms
        return data[key.upper()]
    elif len(get_close_matches(key, data.keys())) > 0:
        response = input("Did you mean {} instead? Enter Y if yes, or N if no: ".format(get_close_matches(key, data.keys())[0]))
        if response.upper() == "Y":
            return data[get_close_matches(key, data.keys())[0]]
        elif response.upper() == "N":
            return "The word doesn't exist. Please double check it."
        else:
            return "We didn't understand your entry."
    else:
        return "Word not found"


if __name__ == "__main__":
    inp_file = "data.json"
    raw_data = read_json(inp_file)
    while True:
        word = input("Enter the word: ")
        if word.lower() != 'quit':
            meaning = find_meaning(word, raw_data)
            if type(meaning) == list:
                for m in meaning:
                    print(m)
            else:
                print(meaning)
        else:
            break

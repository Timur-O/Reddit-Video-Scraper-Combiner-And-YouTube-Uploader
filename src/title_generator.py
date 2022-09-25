import random


class TitleGenerator:
    def __init__(self):
        self.adjective = ['crispy', 'spicy', 'cursed', 'dank', 'flavorful', 'salty', 'hot', 'juicy', 'funny', 'haha',
                          'surprising', 'corny', 'cracked', 'feisty', 'unusual', 'fried', 'delicious', 'succulent',
                          'curried', 'exceptional', 'marvelous', 'satisfying', 'valuable', 'deluxe', 'tiptop',
                          'stupendous', 'precious', 'sizzling', 'musty', 'sticky', 'moist', 'well seasoned', 'seasoned',
                          'frosty', 'suspicious', 'saucy']
        self.video_words = ['videos', 'tiktoks', 'vines', 'memes', 'tik toks']
        self.person = ['i', 'I', 'my wife\'s boyfriend', 'my dog', 'my cat', 'my crocodile', 'my boyfriend',
                       'my girlfriend', 'my son', 'my dog\'s uncle', 'my iguana', 'my frog', 'my friend']
        self.verbs = ['found', 'discovered', 'tripped over', 'cooked up', 'unearthed', 'acquired', 'manifested',
                      'encountered', 'lost', 'misplaced', 'snorted', 'airdropped', 'collected', 'threw', 'ate',
                      'munched on', 'feasted upon']
        self.location = ['the basement', 'the closet', 'the pool', 'bed', 'the wardrobe', 'a motel', 'school',
                         'my dog house']

    def generate(self):
        title = ""
        title += self.adjective[int(random.uniform(0, 1) * len(self.adjective))] + " "
        title += self.video_words[int(random.uniform(0, 1) * len(self.video_words))] + " "
        title += self.person[int(random.uniform(0, 1) * len(self.person))] + " "
        title += self.verbs[int(random.uniform(0, 1) * len(self.verbs))] + " in "
        title += self.location[int(random.uniform(0, 1) * len(self.location))] + " "
        return title

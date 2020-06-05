import markovify
import logging

log = logging.getLogger("markov")
log.setLevel(logging.DEBUG)

def generate_genre(total):
    with open("./corpus/nouns.txt") as f:
        text = f.read()
    
    # build model
    text_model = markovify.NewlineText(text)

    # make a new genre:
    genre = text_model.make_short_sentence(total)
    print(f'markov - bullshit genre: {genre}\ngenre len: {len(genre)}')
    return genre.lower()
    
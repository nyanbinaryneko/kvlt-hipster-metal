import markovify

def generate_genre(total):
    with open("./corpus/genres.txt") as f:
        text = f.read()
    
    # build model
    text_model = markovify.NewlineText(text)

    # make a new genre:
    genre = text_model.make_short_sentence(total)
    print(f'bullshit genre: {genre}')
    return genre
    
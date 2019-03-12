import markovify

if __name__ == "__main__":
    with open("./corpus/genres.txt") as f:
        text = f.read()
    
    # build model
    text_model = markovify.NewlineText(text)

    for i in range(10):
        print(f'bullshit genre: {text_model.make_short_sentence(100)}')
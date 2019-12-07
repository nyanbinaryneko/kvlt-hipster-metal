from markov import generate_genre
import random

def generate_poser_take():
    genre_long = [ generate_genre(140) ]
    genre_short = [ generate_genre(100) ]
    STEMS = [
            { 
                "sentence": f"Oh, you think you are kvlt, I only listen to {genre_long[0]}.",
                "genres": genre_long
            }, 
            {
                "sentence": f"if you were really into metal you would know {genre_long[0]}.",
                "genres": genre_long
            }, 
            {
                "sentence": f"Hey, poser, I'm the founder of {genre_long[0]}.",
                "genres": genre_long
            }, 
            {
                "sentence": f"These fuckin' kids never heard of {genre_long[0]}.",
                "genres": genre_long
            }, 
            {
                "sentence": f"I remember the days before hipsters and posers infecting {genre_long[0]}.",
                "genres": genre_long
            }, 
            {
                "sentence": f"{genre_long[0]} IS FOR REAL METALHEADS ONLY!!!!",
                "genres": genre_long
            }, 
            {
                "sentence":f'I was listening to {genre_long[0]} before you were born.', 
                "genres": genre_long
            }, 
            {
                "sentence": f"you like {genre_long[0]}? ugh. that's for posers.",
                "genres": genre_long
            },
            {
                "sentence": f'Tool is just Radiohead for rape apologists.',
                "genres": []
            },
            {
                "sentence": f'Geez, who the fuck invented post-{genre_long[0]}core? It fuckin\' sucks.',
                "genres": genre_long
            },
            {
                "sentence": f'Can anyone actually name a band that is {genre_short[0]}? Spotify says they are a thing...but I don\'t believe them..',
                "genres": genre_short
            },
            ]
    tweet = random.choice(STEMS)
    if random.randint(0, 10) == 1:
        tweet["sentence"] = f'{tweet["sentence"]}'.upper()

    if "rac" in tweet["sentence"].lower() or "oi!" in tweet["sentence"].lower():
        genres = [genre for genre in tweet["genres"] if "rac" in genre.lower() or "oi!" in genre.lower()]
        if(len(genres) > 1):
            genre = " and ".join(genres)
        else:
            genre = genres[0]
        tweet["sentence"] = f'{genre}. LISTEN TO REAL METAL YOU PANDA COSPLAYERS!'.upper()
    return  tweet["sentence"]
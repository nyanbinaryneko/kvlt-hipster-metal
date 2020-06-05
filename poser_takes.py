from markov import generate_genre
import random

def generate_poser_take():
    genre = generate_genre(140)

    STEMS = [
            { 
                "sentence": f"Oh, you think you are kvlt, I only listen to {genre}.",
                "genres": genre
            }, 
            {
                "sentence": f"if you were really into metal you would know {genre}.",
                "genres": genre
            }, 
            {
                "sentence": f"Hey, poser, I'm the founder of {genre}.",
                "genres": genre
            }, 
            {
                "sentence": f"These fuckin' kids never heard of {genre}.",
                "genres": genre
            }, 
            {
                "sentence": f"I remember the days before hipsters and posers infecting {genre}.",
                "genres": genre
            }, 
            {
                "sentence": f"{genre} IS FOR REAL METALHEADS ONLY!!!!",
                "genres": genre
            }, 
            {
                "sentence":f'I was listening to {genre} before you were born.', 
                "genres": genre
            }, 
            {
                "sentence": f"you like {genre}? ugh. that's for posers.",
                "genres": genre
            },
            {
                "sentence": f'Tool is just Radiohead for rape apologists.',
                "genres": []
            },
            {
                "sentence": f'Geez, who the fuck invented post-{genre}core? It fuckin\' sucks.',
                "genres": genre
            },
            {
                "sentence": f'Can anyone actually name a band that is {genre}? Spotify says they are a thing...but I don\'t believe them..',
                "genres": genre
            },
            {
                "sentence": f'{genre} was better in the 80s.',
                "genres": genre
            }
            ]
    tweet = random.choice(STEMS)
    if random.randint(0, 10) == 1:
        tweet["sentence"] = f'{tweet["sentence"]}'.upper()

    if "rac" in tweet["sentence"].lower() or "oi!" in tweet["sentence"].lower():
        genres = [genre for genre in tweet["genres"] if "rac" in genre.lower() or "oi!" in genre.lower()]
        if(len(genres) > 1):
            genre = " and ".join(genres)
        else:
            genre = genres
        tweet["sentence"] = f'{genre}. IS FOR FUCKING POSERS! LISTEN TO REAL METAL YOU PANDA COSPLAYING COWARDS!'.upper()
    return  tweet["sentence"]

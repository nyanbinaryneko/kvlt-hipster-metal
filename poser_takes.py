from markov import generate_genre
import random

def generate_poser_take():
    genre = generate_genre(140)

    STEMS = [
            { 
                "sentence": f"Oh, you think you are kvlt, I only listen to {genre.capitalize()}.",
                "genres": genre.split()
            }, 
            {
                "sentence": f"if you were really into metal you would know {genre.capitalize()}.",
                "genres": genre.split()
            }, 
            {
                "sentence": f"Hey, poser, I'm the founder of {genre.capitalize()}.",
                "genres": genre.split()
            }, 
            {
                "sentence": f"These fuckin' kids never heard of {genre.capitalize()}.",
                "genres": genre.split()
            }, 
            {
                "sentence": f"I remember the days before hipsters and posers infecting {genre.capitalize()}.",
                "genres": genre.split()
            }, 
            {
                "sentence": f"{genre.capitalize()} IS FOR REAL METALHEADS ONLY!!!!",
                "genres": genre.split()
            }, 
            {
                "sentence":f'I was listening to {genre.capitalize()} before you were born.', 
                "genres": genre.split()
            }, 
            {
                "sentence": f"you like {genre.capitalize()}? ugh. that's for posers.",
                "genres": genre.split()
            },
            {
                "sentence": f'Tool is just Radiohead for rape apologists.',
                "genres": []
            },
            {
                "sentence": f'Why listen to Tool when Soen, Katatonia, and Rivers of Nihil exist?',
                "genres": []
            },
            {
                "sentence": f'Blood Incantation is just Incantation for people who aren\'t racist.',
                "genres": []
            },
            
            {
                "sentence": f'What if Devin Townsend was Weird Al this whole time?',
                "genres": []
            },
            {
                "sentence": f'Geez, who the fuck invented post-{genre.capitalize()}core? It fuckin\' sucks.',
                "genres": genre.split()
            },
            {
                "sentence": f'Can anyone actually name a band that is {genre.capitalize()}? Spotify says they are a thing...but I don\'t believe them..',
                "genres": genre.split()
            },
            {
                "sentence": f'{genre.capitalize()} was better in the 80s.',
                "genres": genre.split()
            }
            ]
    tweet = random.choice(STEMS)
    print(tweet["genres"])
    if random.randint(0, 10) == 1:
        tweet["sentence"] = f'{tweet["sentence"]}'.upper()

    if "rac" in tweet["sentence"].lower() or "oi!" in tweet["sentence"].lower():
        genres = [genre for genre in tweet["genres"] if "rac" in genre.lower() or "oi!" in genre.lower()]
        if(len(genres) > 1):
            genre = " and ".join(genres)
        else:
            genre = genres
        tweet["sentence"] = f'{genre.upper()}. IS FOR FUCKING POSERS! LISTEN TO REAL METAL YOU PANDA COSPLAYING COWARDS!'.upper()
    return  tweet["sentence"]

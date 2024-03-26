from openai import OpenAI
import os
import json
import sys
import logging
import typer

logger = logging.getLogger("CSM")

def lookup_movie_age(movie_name:str) -> dict[str,str|int|bool]:
    logger.info("Looking up %s recommended age", movie_name)
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a research assistant, sharing information about movies as provided by the common sense media website.  You return the information in JSON format"},
            {"role": "user", "content": f"What is the age recommendation and MPAA rating for the movie named 'Captain America Civil War'?"},
            {"role": "assistant", "content": '{ "movie_title": "Captain America Civil War",  "age_recommendation": 13, "mpaa_rating": "PG-13"}'},
            {"role": "user", "content": f"What is the age recommendation and MPAA rating for the movie named '{movie_name}'"},
        ]
    )

    return json.loads(completion.choices[0].message.content)

def lookup_movie_violence(movie_name:str) -> dict[str,str|int|bool]:
    logger.info("Looking up %s violence score", movie_name)
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a research assistant, sharing information about movies as provided by the common sense media website.  You return the information in JSON format"},
            {"role": "user", "content": f"How much 'Violence and Scariness' is in the movie named 'Captain America Civil War'?"},
            {"role": "assistant", "content": '{ "movie_title": "Captain America Civil War",  "violence": "a lot", "violence_score": 4}'},
            {"role": "user", "content": f"How much 'Violence and Scariness' is in the movie called 'The Blind Side'?"},
            {"role": "assistant", "content": '{ "movie_title": "The Blind Side",  "violence": "some", "violence_score": 3}'},
            {"role": "user", "content": f"How much 'Violence and Scariness' is in the movie 'Finding Dory'?"},
            {"role": "assistant", "content": '{ "movie_title": "Finding Dory",  "violence": "some", "violence_score": 3}'},
            {"role": "user", "content": f"How much 'Violence and Scariness' is in 'The Hunger Games: The Ballad of Songbirds and Snakes'?"},
            {"role": "assistant", "content": '{ "movie_title": "The Hunger Games: The Ballad of Songbirds and Snakes",  "violence": "a lot", "violence_score": 4}'},
            {"role": "user", "content": f"How much 'Violence and Scariness' is in '{movie_name}'"},
        ]
    )

    return json.loads(completion.choices[0].message.content)

def move_movie(source: str, target_base_dir: str, dry_run: bool=False):
    movie_name = os.path.splitext(os.path.basename(source))[0]
    movie_info = lookup_movie_age(movie_name)
    print(movie_info)
    target_dir = os.path.join(target_base_dir, str(movie_info['age_recommendation']))
    print(target_dir)
    #print(lookup_movie_violence(movie_name))

app = typer.Typer()

@app.command()
def move(movie_path: str, dest_dir: str, dry_run: bool=False):
    if movie_path.endswith('.mkv'):
        move_movie(movie_path, dest_dir)
    else:
        print("Provided filename didn't end in mkv")

if __name__ == '__main__':
    app()


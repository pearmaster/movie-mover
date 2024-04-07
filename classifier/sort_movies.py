from openai import OpenAI
import os
import json
import sys
import logging
import typer
import shutil

logger = logging.getLogger("CSM")

def parse_nfo(file_path) -> str:
    with open(file_path, 'r') as nfo_file:
        nfo_content = nfo_file.read()
    year_start = nfo_content.find("<year>") + len("<year>")
    year_end = nfo_content.find("</year>")
    year = nfo_content[year_start:year_end].strip()
    return year

def lookup_movie_age(movie_name:str, publish_year:None|str=None) -> dict[str,str|int|bool]:
    logger.info("Looking up %s recommended age", movie_name)
    client = OpenAI()

    msgs = [
        {"role": "system", "content": "You are a research assistant, sharing information about movies as provided by the common sense media website.  You return the information in JSON format"},
        {"role": "user", "content": f"What is the age recommendation and MPAA rating for the movie named 'Captain America Civil War'?"},
        {"role": "assistant", "content": '{ "movie_title": "Captain America Civil War",  "age_recommendation": 13, "mpaa_rating": "PG-13"}'},
    ]

    if publish_year is None:
        msgs.append({"role": "user", "content": f"What is the age recommendation and MPAA rating for the movie named '{movie_name}'"})
    else:
        msgs.append({"role": "user", "content": f"What is the age recommendation and MPAA rating for the movie named '{movie_name}' which was released in {publish_year}"})

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=msgs
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

def move_movie(source: str, target_base_dir: str, prompt:None|bool=None):
    movie_name = os.path.splitext(os.path.basename(source))[0]
    if 'part0' in movie_name.lower():
        movie_name = os.path.splitext(os.path.basename(movie_name))[0]
    src_dir = os.path.dirname(source)
    print(source)
    nfo_path = os.path.join(src_dir, f"{movie_name}.nfo")
    if os.path.exists(nfo_path):
        year = parse_nfo(nfo_path)
        movie_info = lookup_movie_age(movie_name, year)
    else:
        movie_info = lookup_movie_age(movie_name)
    print(movie_info)
    target_dir = os.path.join(target_base_dir, movie_info['mpaa_rating'], str(movie_info['age_recommendation']))
    #print(lookup_movie_violence(movie_name))
    files_to_move = [ f for f in os.listdir(src_dir) if f.startswith(movie_name) ]
    print(files_to_move)
    if prompt is None:
        prompt = typer.confirm(f"Move file to from {src_dir} to {target_dir}?")
    if prompt:
        print(f"Moving to {target_dir}")
        os.makedirs(target_dir, exist_ok=True)
        for f in files_to_move:
            shutil.move(os.path.join(src_dir, f), target_dir)

app = typer.Typer()

@app.command()
def move(movie_path: str, dest_dir: str):
    print(f"Moving {movie_path} to {dest_dir}")
    if os.path.isdir(movie_path):
        print("Moving a directory")
        for fname in os.listdir(movie_path):
            if fname.endswith('.mkv') or fname.endswith('.m4v') or fname.endswith('.webm'):
                filepath = os.path.join(movie_path, os.fsdecode(fname))
                if os.path.isfile(filepath):
                    move_movie(filepath, dest_dir, prompt=True)
    elif os.path.isfile(movie_path):
        print("Moving a file")
        if movie_path.endswith('.mkv') or movie_path.endswith('.m4v') or fname.endswith('.webm'):
            move_movie(movie_path, dest_dir)
        else:
            print("Provided filename didn't end in mkv or m4v")
    else:
        print(f"'{movie_path}' is neither a file nor a directory")

if __name__ == '__main__':
    print("Running")
    app()


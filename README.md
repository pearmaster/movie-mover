# sort_movies

Python script that asks GPT-4 about a movie's parental ratings and then moves the movie file into a folder that is named based on those ratings.

## Running via docker

```sh
docker run -it --rm --env OPENAI_API_KEY=sk-... -v /mnt/mountpoint:/mnt/mountpoint movie_mover '/mnt/mountpoint/movies/moviename.mkv' /mnt/mountpoint/by-age
```

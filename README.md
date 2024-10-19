# sort_movies

Python script that asks GPT-4 about a movie's parental ratings and then moves the movie file into a folder that is named based on those ratings.

## Running via docker

```sh
docker run -it --rm --env OPENAI_API_KEY=sk-... \
-v /mnt/mountpoint:/mnt/mountpoint \
ghcr.io/pearmaster/movie-mover:latest \
/mnt/mountpoint/movies/unsorted/ /mnt/mountpoint/movies/
```

This will find MKV movies under /mnt/mountpoint/movies/unsorted/ and then put them in ratings and age subfolders under mnt/mountpoint/movies/

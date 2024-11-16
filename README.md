# Recipes Offline

A database of recipes from the top recipe sites, with all the junk removed, organized and searchable.
Inspired by: [https://www.justtherecipe.com/](https://www.justtherecipe.com/)

This project would not be possible without [Recipe Scrapers](https://github.com/hhursev/recipe-scrapers) Python library.

## Quickstart

### Linux

```shell
sh ./download_files.sh
docker compose up
```

### Windows

```shell
./download_files.ps1
```

Windows does not support unzipping .gz files from the command line. You will need
to use a third-party GUI tool like [7zip](https://7-zip.org/download.html) (consider this your punishment for using Windows)  

Manually unzip `./data/recipes.sqlite.gz`

```shell
docker compose build
```

## Developer Tools

This project has only been tested for 3.12.7

#### Crawler

```shell
python -m src.tools.crawler.main
```

#### Scraper

```shell
python -m src.tools.scraper.main
```

#### Cleanup

```shell
# Make sure all recipes conform to the Pydantic RecipeData model
python -m src.tools.validate_recipes
```

#### CLI Search

```shell 
python -m src.service.search
```

# Performance

To get this project to run on smaller VMs, we need to conserve memory usage. The first memory-saving feature is to put our recipe data into a SQLite file that can live on-disk. Query speed with batching is slower than reading from a list in-memory, but negligible compared to the time taken up by the similarity search.

The second thing we can do is decrease the precision of our vector embeddings. The embeddings are `float32` by default. We can quantize these to binary without [losing much accuracy](https://emschwartz.me/binary-vector-embeddings-are-so-cool/). This also gives us a 100x speedup in search. However, keeping the full-sized embeddings in memory for rescoring takes up about 500MB. We can skip the rescoring step, but this affects our accuracy quite a bit. The most relevant search result wont always be at the top now. Increasing the number of search results can help, but it's not as convenient for users. However, my goal for deployment is to get this to fit on a $5 Digital Ocean droplet, so the user will have to suffer.  

|                 | Memory Usage |
|-----------------|--------------|
| In-Memory       | 4.4GB        |
| SQLite float32  | 0.84GB       |
| SQLite binary   | 0.36GB       |

### Why Hari?

"JustRecipes" was taken on Squarespace. I liked the idea of making a reference to Hari Seldon from Foundation, who works to preserve human knowledge in a big-ass encyclopedia.
Looking into it though, the word hari had serendipitous meanings in other languages.

[Hari Seldon](https://en.wikipedia.org/wiki/Hari_Seldon) Is an important character in the Foundation series by Isaac Asimov.  

[Hari in Japanese 針 means "needle".](https://www.tanoshiijapanese.com/dictionary/entry_details.cfm?entry_id=35150) Hari Recipes allows you to search for a needle in a haystack.  

[Hari (Sanskrit: हरि) is among the primary epithets of the Hindu preserver deity Vishnu, meaning 'the one who takes away' (sins).[1] It refers to the one who removes darkness and illusion, the one who removes all obstacles to spiritual progress.](https://en.wikipedia.org/wiki/Hari) 
Ok maybe this one is a bit of a stretch, but Hari Recipes removes all of the obstacles (SEO blogspam and LLM spam) to spiritual progress (finding a recipe for Szechuan Pork Ribs).

Hari also sounds like "Hurry" which describes what I want from a recipe search experience. I don't want to scroll through 54 paragraphs about grandma's southern porch swing. I want to know how much sugar goes into sweet tea, dammit.

But really, I just like the way it sounds.



#### TODO
- [x] fastapi 
- [ ] search api working
- [ ] add templates for routes
- [ ] get this working
- [ ] add basic configuration with .env file
- [ ] cleanup + docs

- [ ] dockerized api
    - [ ] upgrade distro to WSL2
    - [ ] get working
- [ ] load tests with locust

- [ ] host on digitalocean
- [ ] get working
- [ ] configure SSL
- [ ] test
- [ ] release
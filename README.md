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

Manually unzip `./src/data/recipes_validated.json.gz`

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
python -m src.tools.search.search
```

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
- [ ] fastapi wrapper
- [ ] dockerized api
- [ ] search api working
- [ ] add templates for routes
- [ ] get this working
- [ ] add basic configuration with .env file
- [ ] cleanup + docs
- [ ] load tests with locust

- [ ] push to digitalocean
- [ ] get working
- [ ] configure SSL
- [ ] release
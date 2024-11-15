# Recipes Offline

A database of recipes from the top recipe sites, with all the junk removed, organized and searchable.
Inspired by: [https://www.justtherecipe.com/](https://www.justtherecipe.com/)

This project would not be possible without [Recipe Scrapers](https://github.com/hhursev/recipe-scrapers) Python library.

## Quickstart

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


#### Organization
- [ ] finish refactoring
    - [ ] data collection module
        - [ ] test that it runs
    - [ ] common/utils
        - [ ] test that it runs
- [ ] add info about unzipping gzipped file
- [ ] fastapi wrapper
- [ ] dockerized api
- [ ] search api working
- [ ] add templates for routes
- [ ] get this working
- [ ] download embeddings and recipes from S3 and unzip in docker build step
- [ ] cleanup + docs
- [ ] release v1

pip install sentence-transformers torch recipe-scrapers beautifulsoup4 tldextract tqdm pydantic faiss-cpu

python -m src.tools.search.search
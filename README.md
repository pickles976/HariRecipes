# Recipes Offline

https://www.justtherecipe.com/

[Recipe Scrapers](https://github.com/hhursev/recipe-scrapers)
[Semantic Search](https://subirverma.medium.com/semantic-search-with-s-bert-is-all-you-need-951bc710e160)

- [x] come up with a recipe scraping strategy
- [x] cap at 100 recipes and play around with different strategies
- [x] generalize recipe walker algorithm
- [x] switch from dict for visited to set() for visited
- [x] switch from json to csv for recipes

- [ ] find schemas for the websites in websites.json

- [ ] get all recipe links for allrecipes.com
- [ ] figure out how long it will take to scrape
- [ ] scrape recipes
- [ ] come up with a filesystem schema with checkpoints
- [ ] put documents in sqlite
- [ ] try to make sqlite searchable? How about a tokenizer and similarity searches?

- [ ] [tf-idf](https://github.com/gautamdasika/Document-Search-Engine/blob/master/finalsearch.py)

### Recipe Scraping basics

There are two ways I know that you can tell if a url is a valid recipe:

1. The url prefix is known to correspond to a recipe. For example if a url has the prefix https://www.allrecipes.com/recipe/ 
2. Look for script tags with type "application/ld+json". These script tags should have a schema in the class that matches a commonly-used recipe schema like "yoast-schema-graph" or a proprietary one like "allrecipes-schema"




# Recipes Offline

A database of recipes from the top recipe sites, with all the junk removed, organized and searchable.
Inspired by: [https://www.justtherecipe.com/](https://www.justtherecipe.com/)

### Libraries and Helpful documents

[Recipe Scrapers](https://github.com/hhursev/recipe-scrapers)

### Recipe Scraping basics

There are two ways I know that you can tell if a url is a valid recipe:

1. The url prefix is known to correspond to a recipe. For example if a url has the prefix https://www.allrecipes.com/recipe/ 
2. Look for script tags with type "application/ld+json". These script tags should have a schema in the class that matches a commonly-used recipe schema like "allrecipes-schema"

Scraping by prefix-url is much faster, because you don't actually need to visit the link to know that it is a recipe. However for most websites, just a link prefix is not enough. In this case we need to rely on the metadata, which looks like this:

```html
<script id="allrecipes-schema_1-0" class="comp allrecipes-schema mntl-schema-unified" type="application/ld+json">[
{
"@context": "http://schema.org",
"@type": ["Recipe"]
,"headline": "One Pan Chicken Gnocchi"
,"datePublished": "2024-05-29T13:44:45.890-04:00"
,"dateModified": "2024-05-29T13:44:45.890-04:00"
,"author": [
{"@type": "Person"
,"name": "TheDailyGourmet"
,"url": "https://www.allrecipes.com/thedailygourmet-7113600"
}
]</script>
```

This script will have a recipe metadata class, and the inner text will be a list of ld+json, typically the first of which has `"@type"` of `["Recipe"]`, as well as some other tags sometimes.


# Info

1. Run crawler on all whitelisted recipe websites
2. Combine all recipe lists into a mega list
3. Run scraper on all_recipes.csv
4. Run validate_recipes.py to convert all recipes to a somewhat consistent representation
5. Run test_parse.py to make sure that all recipes can parse to Pydantic models
6. Generate embeddings for all recipes
7. (Optional) binarize embeddings
8. Vectorize queries and measure cosine distance (or hamming distance for binary vectors)

## TODO:

#### Scraping
- [x] figure out how long it will take to scrape (~4hrs)
- [x] scrape all recipes

#### Validation
- [x] clean up data
- [x] make pydantic model

https://emschwartz.me/binary-vector-embeddings-are-so-cool/

#### Organization
- [x] Semantic Search
 - [x] https://sbert.net/examples/applications/semantic-search/README.html
- [x] create embedding pickle file for recipes (~4.2 hrs)
- [ ] test out binary embedding queries
- [ ] create sqlite file from recipes json
- [ ] Load recipes from sqlite with queries
- [ ] repl demo

- [ ] fastapi wrapper
- [ ] dockerized api
- [ ] html page
- [ ] html served from fastapi
- [ ] cleanup + docs
- [ ] release v1
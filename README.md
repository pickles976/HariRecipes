# Recipes Offline

A database of recipes from the top recipe sites, with all the junk removed, organized and searchable.
Inspired by: [https://www.justtherecipe.com/](https://www.justtherecipe.com/)

### Libraries and Helpful documents

[Recipe Scrapers](https://github.com/hhursev/recipe-scrapers)
[Semantic Search](https://subirverma.medium.com/semantic-search-with-s-bert-is-all-you-need-951bc710e160)
[nltk example](https://github.com/gautamdasika/Document-Search-Engine/blob/master/finalsearch.py)


### Recipe Scraping basics

There are two ways I know that you can tell if a url is a valid recipe:

1. The url prefix is known to correspond to a recipe. For example if a url has the prefix https://www.allrecipes.com/recipe/ 
2. Look for script tags with type "application/ld+json". These script tags should have a schema in the class that matches a commonly-used recipe schema like "yoast-schema-graph" or a proprietary one like "allrecipes-schema"

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

### TODO:

allrecipes.com:
```commandline
Elapsed: 0:56:05.523423
Found: 53107 links!
Found: 36719 recipes!
```

#### Crawling
- [x] come up with a recipe scraping strategy
- [x] cap at 100 recipes and play around with different strategies
- [x] generalize recipe walker algorithm
- [x] switch from dict for visited to set() for visited
- [x] switch from json to csv for recipes
- [x] Pickle spider object at checkpoints so we can resume scraping if something happens and the scraping does not complete
- [ ] How could we trampoline a recursive search like this? (yield the params of the next call?)

#### Scraping
- [ ] get all recipe links
- [ ] figure out how long it will take to scrape
- [ ] scrape all recipes
- [ ] come up with a filesystem schema with checkpoints
- [ ] searchable sqlite

#### Collection
- [x] find schemas for the websites in websites.json
    - [ ] goodhousekeeping
    - [ ] greatbritishchefs
    - [ ] grouprecipes
    - [x] hassanchef
    - [x] hreshey land
    - [x] im-worthy
    - [x] indianhealthyrecipes
    - [x] jimcooksfood
    - [x] joshuaweissman
    - [x] kennymgovern.com
    - [ ] kinarthurbaking
    - [ ] kristines kitchen blog
    - [x] lovin it vegan
    - [ ] martha stewart
    - [ ] mccormick



 - [ ] populate websites.json with field necessary for scraping

Scrape cookpade
```
        // {
        //     "url": "https://cookpad.com/",
        //     "root_url": "https://cookpad.com/us/search/rice",
        //     "recipe_prefix": "https://cookpad.com/us/recipes/",
        //     "ignore": ["download", "navigation", "auth"]
        // },
```

```
tf-idf for every lemma in all 100 recipes
store the top n% of those lemmas as your keywords (n can be 100 if you like)
treat those as tags: store a table of (lemma, relevance, recipe_id)
when you query, search every word/lemma in the query. every recipe that shows up in the query results is a search result, ordered by the sum of relevances.
```
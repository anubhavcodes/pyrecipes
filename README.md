### pyrecipes

A tool to scrape recipes from popular websites and convert them into usable formats like json, yaml etc. 

### Motivation

I use [paprika](https://paprikaapp.com) and it only supports importing of recipes via yaml. I was tired of manually 
downloading recipes and pasting in paprika from Hello Fresh. After writing a scraper for Hello Fresh I would like it
to be extensible for other recipe sites.

### Usage
```bash
docker pull anubhavcodes/pyrecipes
docker container run --rm -v $PWD:/srv pyrecips:latest "hello_fresh_recipe_url"
```

The above docker run command will generate a `recipe.yml` in the current directory that you can import directly in your 
paprikaapp.

TODO 

- [] Add difficulty and preparation to hellofresh
- [] Add images support for hellofresh
- [] Add ability to export to multiple formats
- [] Add ability to set name as recipe as the name of export file
- [] Add ability to export multiple recipes in one go
- [] More??

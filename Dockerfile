FROM python:3.12.7-slim-bullseye

# Download files
RUN mkdir ./data
RUN apt-get -y update; apt-get -y install curl
RUN if [ "$FLOAT32_SEARCH" = "1" ] ; \
    then curl -L "https://github.com/pickles976/HariRecipes/releases/download/data/recipe_embeddings.pickle" > ./data/recipe_embeddings.pickle ; \
    else echo "Ignoring Float32 Embeddings..." ; \
    fi
RUN curl -L  "https://github.com/pickles976/HariRecipes/releases/download/data/recipe_embeddings_binary.pickle" > ./data/recipe_embeddings_binary.pickle
RUN curl -L "https://github.com/pickles976/HariRecipes/releases/download/data/recipes.sqlite.gz" > ./data/recipes.sqlite.gz
RUN gzip -d ./data/recipes.sqlite.gz 

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY ./src ./src

EXPOSE 8000

CMD ["fastapi", "run", "./src/service/app.py"]
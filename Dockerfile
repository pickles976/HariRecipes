FROM python:3.12.7-slim-bullseye

COPY ./data/recipe_embeddings_binary.pickle ./data/recipe_embeddings_binary.pickle
COPY ./data/recipes.sqlite ./data/recipes.sqlite
COPY ./src ./src
COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

CMD ["fastapi", "run", "./src/service/app.py"]
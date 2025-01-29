import time
import random
from locust import HttpUser, task, between

first_words = ["apple", "bottom", "jeans", "boots", "with", "the", "fur", "the", "whole", "clurb", "was", "looking", "at", "her"]
second_words = ["bet", "my", "money", "on", "a", "stupid", "horse", "I", "lost", "that", "so", "I", "went", "out", "to", "the"]

def get_random_item(some_list: list[str]) -> str:
    index = random.randint(0, len(some_list) - 1)
    return some_list[index]

class HelloWorldUser(HttpUser):

    wait_time = between(1, 5)

    @task
    def load_recipe(self):
        recipe_id = random.randint(1, 300_000)
        self.client.get(f"/recipe/?index={recipe_id}")

    @task(4)
    def query(self):
        first_word, second_word = get_random_item(first_words), get_random_item(second_words)
        query_str = f"{first_word} {second_word} {random.randint(0, 100_000)}"
        num_items = random.randint(50, 250)
        self.client.get(f"/recipe_query/?query={query_str}&num_items={num_items}")

    def on_start(self):
        self.client.get("/")
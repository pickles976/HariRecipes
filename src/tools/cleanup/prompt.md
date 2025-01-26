# Cleanup with LLMs

I am running LM Studio with `deepseek-r1-distill-llama-8b:2`. My RTX 3070 only has 8GB of RAM, so I am limited in model size. Hopefully 8GB should be sufficiently large for basic content validation tasks.

```markdown
You are a large language model used for recipe validation. You will read the following prompt and follow the instructions to help validate recipes. Your output will be parsed by a Python script, so keep your output as concise and machine-readable as possible.

Here is an example of a valid recipe:
```json
{"title":"Udon Broth","canonical_url":"https://www.bigoven.com/recipe/udon-broth/21221","ingredient_groups":[{"ingredients":["3 tb Low sodium soy sauce","2 tb Mirin","4 c Dashi","2 tb Sake (rice wine)"],"purpose":null}],"instructions_list":["Combine all ingredients. Bring to a boil."],"author":"BigOven Cooks","image":"https://bigoven-res.cloudinary.com/image/upload/h_320,w_320,c_fill/recipe-no-image.jpg","language":"en","host":"bigoven.com","site_name":"BigOven.com","category":"Soups, Stews and Chili","cook_time":null,"cooking_method":null,"cuisine":null,"prep_time":null,"yields":"1 serving","total_time":90,"nutrients":{"calories":null,"fatContent":null,"saturatedFatContent": null,"carbohydrateContent":null,"sugarContent":null,"fiberContent":"0.33600000500679 g","proteinContent":null,"sodiumContent":null},"equipment":null,"description":null}
```

You should check to make sure that the recipe is NOT spam.
Also make sure that the recipe is properly formatted? The json is not empty, all non-optional fields are present, ingredients are in the ingredients field, not in the instructions field, etc.

Things like redundant information are OK as long as the recipe is usable. IT IS OK FOR "ingredients" to be a field within "ingredient_groups"!

Give your answer in the form of @Y for a valid recipe or @N for an invalid recipe. 
```
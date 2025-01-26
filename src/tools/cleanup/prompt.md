# Cleanup with LLMs

I am running LM Studio with `hermes-3-llama-3.1-8b`. My RTX 3070 only has 8GB of RAM, so I am limited in model size. Hopefully 8GB should be sufficiently large for basic content validation tasks.

```markdown
You are a large language model used for recipe validation. You will read the following prompt and follow the instructions to help validate recipes. 

Here is an example of a valid recipe:

```json
{"title":"Udon Broth","canonical_url":"https://www.bigoven.com/recipe/udon-broth/21221","ingredient_groups":[{"ingredients":["3 tb Low sodium soy sauce","2 tb Mirin","4 c Dashi","2 tb Sake (rice wine)"],"purpose":null}],"instructions_list":["Combine all ingredients. Bring to a boil."],"author":"BigOven Cooks","image":"https://bigoven-res.cloudinary.com/image/upload/h_320,w_320,c_fill/recipe-no-image.jpg","language":"en","host":"bigoven.com","site_name":"BigOven.com","category":"Soups, Stews and Chili","cook_time":null,"cooking_method":null,"cuisine":null,"prep_time":null,"yields":"1 serving","total_time":90,"nutrients":{"calories":null,"fatContent":null,"saturatedFatContent": null,"carbohydrateContent":null,"sugarContent":null,"fiberContent":"0.33600000500679 g","proteinContent":null,"sodiumContent":null},"equipment":null,"description":null}
```

Make sure that the recipe is NOT spam.
Make sure that the ingredient list is not empty.
Make sure that the instructions list is not empty.
Make sure that the recipe is actually useful and not just garbage.
Make sure that the recipe is properly formatted.
Make sure ingredients are in the ingredients field.
Make sure instructions are in the instructions field.

Give your answer in the form of @Y for a valid recipe or @N for an invalid recipe. 
```
#!/usr/bin/env python3
from itertools import count

from flask import (
    Flask,
    abort,
    redirect,
    render_template,
    request,
    url_for,
)

from model import (
    ALL_RECIPE_CATEGORY_OPTION,
    RECIPE_CATEGORY_OPTIONS,
    RECIPE_SORT_OPTIONS,
    SORT_RULES,
    Ingredient,
    IngredientUnit,
    Recipe,
    RecipeCategory,
    RecipeStep,
)


app = Flask(__name__)


recipes = [
    Recipe(
        id=1,
        title="Яйцо пашот в микроволновке",
        category=RecipeCategory.BREAKFAST,
        cook_time=3,
        ingredients=[
            Ingredient(
                name="Куриное яйцо",
                amount=60,
                unit=IngredientUnit.GRAM,
            ),
            Ingredient(
                name="Вода",
                amount=100,
                unit=IngredientUnit.MILLILITER,
            ),
        ],
        steps=[
            RecipeStep(
                desc="Налейте холодную воду в небольшую кружку. Добавьте соль и перемешайте до растворения.",
                image_url="https://i.ibb.co/zq0cM0t/recipe-1-step-1.png",
            ),
            RecipeStep(
                desc="Аккуратно разбейте в кружку яйцо, чтобы не повредить желток. Поставьте емкость в микроволновку на максимальную мощность на 2 минуты.",
                image_url="https://i.ibb.co/SDFDvQvr/recipe-1-step-2.png",
            ),
            RecipeStep(
                desc="На тарелку выложите лист салата, а сверху положите готовое яйцо, приготовленное в микроволновке в кружке, пашот.",
                image_url="https://i.ibb.co/67bB38GS/recipe-1-step-3.png",
            ),
        ],
    ),
    Recipe(
        id=2,
        title="Овощной салат с зерненым творогом и песто",
        category=RecipeCategory.LUNCH,
        cook_time=5,
        ingredients=[
            Ingredient(
                name="Помидор",
                amount=2,
                unit=IngredientUnit.PIECE,
            ),
            Ingredient(
                name="Зерненый творог в сливках",
                amount=60,
                unit=IngredientUnit.GRAM,
            ),
            Ingredient(
                name="Соус песто",
                amount=15,
                unit=IngredientUnit.MILLILITER,
            ),
            Ingredient(
                name="Кинза",
                amount=0.5,
                unit=IngredientUnit.PIECE,
            ),
            Ingredient(
                name="Красный лук",
                amount=0.25,
                unit=IngredientUnit.PIECE,
            ),
        ],
        steps=[
            RecipeStep(
                desc="Нарежьте помидоры на 6–8 частей, удалив плодоножку. Нарежьте лук тонкими кольцами, разделите их пальцами.",
                image_url="https://i.ibb.co/ZpGLmBPT/recipe-2-step-1.png",
            ),
            RecipeStep(
                desc="Смешайте в большой миске помидоры, лук и творог без сливок. Мелко порубите кинзу и добавьте в салат.",
                image_url="https://i.ibb.co/vvhpxJwb/recipe-2-step-2.png",
            ),
            RecipeStep(
                desc="Заправьте соусом песто и добавьте немного соли.",
                image_url="https://i.ibb.co/rGh4mMB5/recipe-2-step-3.png",
            ),
        ],
    ),
    Recipe(
        id=3,
        title="Говяжий язык с миксом из салатной зелени",
        category=RecipeCategory.DINNER,
        cook_time=5,
        ingredients=[
            Ingredient(
                name="Говяжий язык",
                amount=40,
                unit=IngredientUnit.GRAM,
            ),
            Ingredient(
                name="Салатная смесь",
                amount=40,
                unit=IngredientUnit.GRAM,
            ),
            Ingredient(
                name="Оливковое масло",
                amount=5,
                unit=IngredientUnit.MILLILITER,
            ),
            Ingredient(
                name="Лимонный сок",
                amount=5,
                unit=IngredientUnit.MILLILITER,
            ),
        ],
        steps=[
            RecipeStep(
                desc="Нарежьте отварной говяжий язык тонкими ломтиками. Выложите на тарелку.",
                image_url="https://i.ibb.co/ymm2TW8z/recipe-3-step-1.png",
            ),
            RecipeStep(
                desc="Выложите микс салатов в миску, посыпьте солью. Смешайте в небольшой пиале масло с лимонным соком и перцем.",
                image_url="https://i.ibb.co/twKbQ1J2/recipe-3-step-2.png",
            ),
            RecipeStep(
                desc="Полейте салатный микс заправкой. Перемешайте и положите на тарелку рядом с нарезанным языком.",
                image_url="https://i.ibb.co/DHtyLJSW/recipe-3-step-3.png",
            ),
        ],
    ),
]
recipe_ids = count(4)


@app.route("/")
def index():
    search_query = request.args.get("search_query", "").strip()
    raw_category = request.args.get(
        "category",
        ALL_RECIPE_CATEGORY_OPTION,
    ).strip()
    raw_sort = request.args.get(
        "sort",
        "Новые",
    ).strip()

    if raw_category not in RECIPE_CATEGORY_OPTIONS:
        abort(400)
    
    category = raw_category

    if raw_sort not in RECIPE_SORT_OPTIONS:
        abort(400)

    sort = raw_sort

    filtered_recipes = [
        recipe
        for recipe in recipes
        if search_query.lower() in recipe.title.lower() and \
           (category == ALL_RECIPE_CATEGORY_OPTION or recipe.category == category)
    ]
    filtered_recipes.sort(key=SORT_RULES[sort])

    return render_template(
        "index.html",
        category_lst=RECIPE_CATEGORY_OPTIONS,
        sort_lst=RECIPE_SORT_OPTIONS,
        search_query=search_query,
        category=category,
        sort=sort,
        recipes=filtered_recipes,
    )


def find_recipe(recipe_id):
    return next((r for r in recipes if r.id == recipe_id), None)


@app.route("/recipe/<int:recipe_id>")
def recipe_detail(recipe_id):
    recipe = find_recipe(recipe_id)

    if recipe is None:
        abort(404)
    
    return render_template("recipe_detail.html", recipe=recipe)


def parse_recipe_form(recipe_form):
    raw_title = recipe_form.get("title", "").strip()
    raw_category = recipe_form.get("category", "").strip()
    raw_cook_time = recipe_form.get("cook_time", "").strip()
    raw_ingredients = [
        {
            "name": name,
            "amount": amount,
            "unit": unit,
        } for name, amount, unit in zip(
            recipe_form.getlist("ingredient_name[]"),
            recipe_form.getlist("ingredient_amount[]"),
            recipe_form.getlist("ingredient_unit[]"),
        )
    ]
    raw_steps = [
        {
            "desc": desc,
            "image_url": image_url,
        } for desc, image_url in zip(
            recipe_form.getlist("step_desc[]"),
            recipe_form.getlist("step_image_url[]"),
        )
    ]
    recipe_form_data =  {
        "title": raw_title,
        "category": raw_category,
        "cook_time": raw_cook_time,
        "ingredients": raw_ingredients,
        "steps": raw_steps,
    }
    return recipe_form_data


def validate_recipe_form(recipe_form_data):
    errors = []
    
    if not recipe_form_data["title"]:
        errors.append(
            "Название блюда обязательно для заполнения"
        )

    try:
        recipe_form_data["category"] = RecipeCategory(
            recipe_form_data["category"]
        )
    except ValueError:
        errors.append(
            "Категория (строка из выпадающего списка) обязательна для заполнения"
        )

    try:
        recipe_form_data["cook_time"] = int(recipe_form_data["cook_time"])

        if recipe_form_data["cook_time"] < 1:
            raise ValueError
    except ValueError:
        errors.append(
            "Время готовки (натуральное число) обязательно для заполнения"
        )

    if not recipe_form_data["ingredients"]:
        errors.append(
            "В рецепте должен быть хотя бы один ингредиент"
        )

    for raw_ingredient in recipe_form_data["ingredients"]:
        raw_ingredient["name"] = raw_ingredient["name"].strip()

        if not raw_ingredient["name"]:
            errors.append(
                "Название ингредиента обязательно для заполнения"
            )

        try:
            raw_ingredient["amount"] = float(raw_ingredient["amount"])

            if raw_ingredient["amount"] <= 0:
                raise ValueError
        except ValueError:
            errors.append(
                "Кол-во ингредиента (положительное число) обязательно для заполнения"
            )

        try:
            raw_ingredient["unit"] = IngredientUnit(raw_ingredient["unit"])
        except ValueError:
            errors.append(
                "Единица измерения ингредиента (строка из выпадающего списка) обязательна для заполнения"
            )

    if not recipe_form_data["steps"]:
        errors.append(
            "В рецепте должен быть хотя бы один шаг приготовления"
        )

    for raw_step in recipe_form_data["steps"]:
        raw_step["desc"] = raw_step["desc"].strip()

        if not raw_step["desc"]:
            errors.append(
                "Описание шага приготовления обязательно для заполнения"
            )

        raw_step["image_url"] = raw_step["image_url"].strip()

        if not raw_step["image_url"]:
            raw_step["image_url"] = None

    return errors


@app.route("/add", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        recipe_form_data = parse_recipe_form(request.form)
        errors = validate_recipe_form(recipe_form_data)

        if errors:
            return render_template(
                "add_recipe.html",
                errors=errors,
                recipe_form_data=recipe_form_data,
                category_lst=RecipeCategory,
                unit_lst=IngredientUnit,
            )

        ingredients = [
            Ingredient(
                name=ingredient["name"],
                amount=ingredient["amount"],
                unit=ingredient["unit"],
            ) for ingredient in recipe_form_data["ingredients"]
        ]
        steps = [
            RecipeStep(
                desc=step["desc"],
                image_url=step["image_url"],
            ) for step in recipe_form_data["steps"]
        ]

        recipes.append(
            Recipe(
                id=next(recipe_ids),
                title=recipe_form_data["title"],
                category=recipe_form_data["category"],
                cook_time=recipe_form_data["cook_time"],
                ingredients=ingredients,
                steps=steps,
            )
        )

        return redirect(url_for('index'))

    return render_template(
        "add_recipe.html",
        recipe_form_data={},
        category_lst=RecipeCategory,
        unit_lst=IngredientUnit,
    )


@app.route("/edit/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    recipe = find_recipe(recipe_id)

    if recipe is None:
        abort(404)

    if request.method == "POST":
        recipe_form_data = parse_recipe_form(request.form)
        errors = validate_recipe_form(recipe_form_data)

        if errors:
            return render_template(
                "edit_recipe.html",
                recipe_id=recipe_id,
                errors=errors,
                recipe_form_data=recipe_form_data,
                category_lst=RecipeCategory,
                unit_lst=IngredientUnit,
            )

        ingredients = [
            Ingredient(
                name=ingredient["name"],
                amount=ingredient["amount"],
                unit=ingredient["unit"],
            ) for ingredient in recipe_form_data["ingredients"]
        ]
        steps = [
            RecipeStep(
                desc=step["desc"],
                image_url=step["image_url"],
            ) for step in recipe_form_data["steps"]
        ]

        recipe.title = recipe_form_data["title"]
        recipe.category = recipe_form_data["category"]
        recipe.cook_time = recipe_form_data["cook_time"]
        recipe.ingredients = ingredients
        recipe.steps = steps

        return redirect(url_for('recipe_detail', recipe_id=recipe_id))

    ingredients = [
        {
            "name": ingredient.name,
            "amount": ingredient.amount,
            "unit": ingredient.unit,
        } for ingredient in recipe.ingredients
    ]
    steps = [
        {
            "desc": step.desc,
            "image_url": "" if step.image_url is None else step.image_url,
        } for step in recipe.steps
    ]

    recipe_form_data = {
        "title": recipe.title,
        "category": recipe.category,
        "cook_time": recipe.cook_time,
        "ingredients": ingredients,
        "steps": steps,
    }

    return render_template(
        "edit_recipe.html",
        recipe_id=recipe_id,
        recipe_form_data=recipe_form_data,
        category_lst=RecipeCategory,
        unit_lst=IngredientUnit,
    )

@app.post("/delete/<int:recipe_id>")
def delete_recipe(recipe_id):
    recipe = find_recipe(recipe_id)

    if recipe is None:
        abort(404)

    recipes.remove(recipe)
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(error):
    return render_template("not_found.html"), 404


@app.errorhandler(400)
def bad_request(error):
    return render_template("bad_request.html"), 400


if __name__ == "__main__":
    app.run(debug=True)
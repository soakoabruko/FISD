from dataclasses import dataclass
from enum import StrEnum


class RecipeCategory(StrEnum):
    BREAKFAST = "Завтрак"
    LUNCH = "Обед"
    DINNER = "Ужин"

    SNACK = "Перекус"
    DESSERT = "Десерт"
    DRINK = "Напиток"


ALL_RECIPE_CATEGORY_OPTION = "Все"


class IngredientUnit(StrEnum):
    GRAM = "г"
    KILOGRAM = "кг"
    MILLILITER = "мл"
    LITER = "л"
    PIECE = "шт."


@dataclass(frozen=True, slots=True)
class Ingredient:
    name: str
    amount: float
    unit: IngredientUnit


@dataclass(frozen=True, slots=True)
class RecipeStep:
    desc: str
    image_url: str | None = None


@dataclass(slots=True)
class Recipe:
    id: int
    title: str
    category: RecipeCategory
    cook_time: int
    ingredients: list[Ingredient]
    steps: list[RecipeStep]


RECIPE_CATEGORY_OPTIONS = (ALL_RECIPE_CATEGORY_OPTION, *RecipeCategory)
RECIPE_SORT_OPTIONS = ("Новые", "Старые", "Быстрые", "Долгие")
SORT_RULES = {
    "Новые": (lambda recipe: -recipe.id),
    "Старые": (lambda recipe: recipe.id),
    "Быстрые": (lambda recipe: recipe.cook_time),
    "Долгие": (lambda recipe: -recipe.cook_time),
}
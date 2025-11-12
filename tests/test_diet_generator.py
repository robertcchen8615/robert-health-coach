from skills.skill_4_diet_generator.scripts import diet_generator


def test_generate_default():
    """Test generate_diet with empty profile (default calories = 2000)."""
    plan = diet_generator.generate_diet({})
    assert isinstance(plan, dict)
    assert isinstance(plan["calories_total"], int)
    assert plan["calories_total"] == 2000
    assert len(plan["meals"]) == 3
    assert all("calories" in meal for meal in plan["meals"])


def test_generate_custom_calories():
    """Test generate_diet with custom calories and name."""
    profile = {"calories": 1500, "name": "Alice"}
    plan = diet_generator.generate_diet(profile)
    assert plan["calories_total"] == 1500
    assert plan["name"] == "Alice"
    total = sum(m["calories"] for m in plan["meals"])
    assert total == 1500


def test_generate_with_preferences():
    """Test generate_diet with dietary preferences."""
    profile = {"calories": 2200, "preferences": ["vegetarian", "gluten-free"]}
    plan = diet_generator.generate_diet(profile)
    assert plan["calories_total"] == 2200
    assert "vegetarian" in plan["notes"]
    assert "gluten-free" in plan["notes"]


def test_generate_high_calories():
    """Test with high calorie intake (e.g., athlete)."""
    profile = {"calories": 4000, "name": "Athlete"}
    plan = diet_generator.generate_diet(profile)
    assert plan["calories_total"] == 4000
    total = sum(m["calories"] for m in plan["meals"])
    assert total == 4000
    # breakfast: 30% of 4000 = 1200, lunch: 40% = 1600, dinner: 30% = 1200
    assert plan["meals"][0]["calories"] == 1200
    assert plan["meals"][1]["calories"] == 1600
    assert plan["meals"][2]["calories"] == 1200


def test_generate_low_calories():
    """Test with low calorie intake (e.g., restricted diet)."""
    profile = {"calories": 1000}
    plan = diet_generator.generate_diet(profile)
    assert plan["calories_total"] == 1000
    total = sum(m["calories"] for m in plan["meals"])
    assert total == 1000
    # breakfast: 30% of 1000 = 300, lunch: 40% = 400, dinner: 30% = 300
    assert plan["meals"][0]["calories"] == 300
    assert plan["meals"][1]["calories"] == 400
    assert plan["meals"][2]["calories"] == 300


def test_generate_empty_preferences():
    """Test that empty preferences list is handled gracefully."""
    profile = {"calories": 2000, "preferences": []}
    plan = diet_generator.generate_diet(profile)
    assert "preferences: " in plan["notes"]


def test_generate_string_calories_conversion():
    """Test that string calories are converted to int."""
    # In real use, this might come from JSON/form inputs
    profile = {"calories": "2500"}
    plan = diet_generator.generate_diet(profile)
    assert plan["calories_total"] == 2500
    total = sum(m["calories"] for m in plan["meals"])
    assert total == 2500


def test_generate_meals_have_items():
    """Verify each meal has food items."""
    profile = {"calories": 2000}
    plan = diet_generator.generate_diet(profile)
    for meal in plan["meals"]:
        assert "items" in meal
        assert isinstance(meal["items"], list)
        assert len(meal["items"]) > 0


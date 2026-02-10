"""
Health calculation formulas - BMI, BMR (Mifflin-St Jeor), calories, macros, water.
All formulas use metric: weight (kg), height (cm).
"""

from decimal import Decimal


def calculate_bmi(weight_kg: float, height_cm: float) -> Decimal:
    """
    BMI = weight (kg) / height (m)^2
    Height is converted from cm to m.
    """
    if not height_cm or height_cm <= 0:
        return Decimal('0')
    height_m = height_cm / 100
    bmi = float(weight_kg) / (height_m ** 2)
    return Decimal(str(round(bmi, 2)))


def get_bmi_category(bmi: Decimal) -> str:
    """Returns category: Underweight, Normal, Overweight, Obese."""
    b = float(bmi)
    if b < 18.5:
        return 'Underweight'
    if b < 25:
        return 'Normal'
    if b < 30:
        return 'Overweight'
    return 'Obese'


def calculate_bmr_mifflin_st_jeor(weight_kg: float, height_cm: float, age: int, gender: str) -> Decimal:
    """
    Mifflin-St Jeor equation (1990):
    Men:   BMR = 10*weight(kg) + 6.25*height(cm) - 5*age + 5
    Women: BMR = 10*weight(kg) + 6.25*height(cm) - 5*age - 161
    """
    base = 10 * weight_kg + 6.25 * height_cm - 5 * age
    if gender == 'M':
        bmr = base + 5
    else:
        bmr = base - 161
    return Decimal(str(round(max(0, bmr), 2)))


def get_activity_multiplier(goal: str) -> float:
    """
    Approximate daily activity multiplier for TDEE.
    maintain: 1.55 (moderately active), lose: 1.375, gain: 1.725
    """
    multipliers = {'lose': 1.375, 'maintain': 1.55, 'gain': 1.725}
    return multipliers.get(goal, 1.55)


def calculate_daily_calories(bmr: Decimal, goal: str) -> Decimal:
    """
    TDEE = BMR * activity multiplier.
    For lose: subtract ~500 kcal; for gain: add ~300 kcal (simplified).
    """
    mult = get_activity_multiplier(goal)
    tdee = float(bmr) * mult
    if goal == 'lose':
        tdee = max(1200, tdee - 500)
    elif goal == 'gain':
        tdee = tdee + 300
    return Decimal(str(round(tdee, 2)))


def calculate_daily_protein(weight_kg: float, goal: str) -> Decimal:
    """Protein: 1.6-2.2 g per kg body weight. Lose/gain use higher end."""
    if goal == 'lose':
        g_per_kg = 2.0
    elif goal == 'gain':
        g_per_kg = 2.0
    else:
        g_per_kg = 1.6
    return Decimal(str(round(weight_kg * g_per_kg, 2)))


def calculate_daily_fat(daily_calories: Decimal) -> Decimal:
    """Fat: 25% of calories from fat. 1 g fat = 9 kcal."""
    fat_kcal = float(daily_calories) * 0.25
    return Decimal(str(round(fat_kcal / 9, 2)))


def calculate_daily_carbs(daily_calories: Decimal, protein_g: Decimal, fat_g: Decimal) -> Decimal:
    """Remaining calories from carbs. 1 g carb = 4 kcal."""
    protein_kcal = float(protein_g) * 4
    fat_kcal = float(fat_g) * 9
    carb_kcal = max(0, float(daily_calories) - protein_kcal - fat_kcal)
    return Decimal(str(round(carb_kcal / 4, 2)))


def calculate_daily_water(weight_kg: float) -> Decimal:
    """Water: ~35 ml per kg body weight, result in liters."""
    liters = (weight_kg * 35) / 1000
    return Decimal(str(round(liters, 2)))


def compute_all_health_metrics(weight_kg: float, height_cm: float, age: int, gender: str, goal: str) -> dict:
    """
    Runs all health calculations and returns a dictionary of results.
    Used by views to display and save HealthData.
    """
    bmi = calculate_bmi(weight_kg, height_cm)
    bmi_category = get_bmi_category(bmi)
    bmr = calculate_bmr_mifflin_st_jeor(weight_kg, height_cm, age, gender)
    daily_calories = calculate_daily_calories(bmr, goal)
    daily_protein = calculate_daily_protein(weight_kg, goal)
    daily_fat = calculate_daily_fat(daily_calories)
    daily_carbs = calculate_daily_carbs(daily_calories, daily_protein, daily_fat)
    daily_water = calculate_daily_water(weight_kg)

    return {
        'bmi': bmi,
        'bmi_category': bmi_category,
        'bmr': bmr,
        'daily_calories': daily_calories,
        'daily_protein_g': daily_protein,
        'daily_fat_g': daily_fat,
        'daily_carbs_g': daily_carbs,
        'daily_water_liters': daily_water,
    }

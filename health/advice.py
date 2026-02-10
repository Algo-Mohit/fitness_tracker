"""
Smart advice system: BMI-based, protein, water, and personalized daily advice.
"""

from decimal import Decimal


def get_bmi_advice(bmi: Decimal, bmi_category: str) -> list:
    """
    If BMI < 18.5 → weight gain advice.
    If BMI > 25 → fat loss advice.
    Normal: maintenance tips.
    """
    advice = []
    b = float(bmi)
    if bmi_category == 'Underweight':
        advice.append('Your BMI suggests you are underweight. Focus on a calorie surplus with nutrient-dense foods.')
        advice.append('Eat regular meals and include healthy fats (nuts, avocado) and protein in each meal.')
        advice.append('Consider strength training to build muscle rather than only fat.')
    elif bmi_category in ('Overweight', 'Obese'):
        advice.append('Your BMI suggests excess body fat. A moderate calorie deficit with exercise is recommended.')
        advice.append('Prioritize protein to preserve muscle while losing fat.')
        advice.append('Add more vegetables and fiber, and reduce added sugars and refined carbs.')
    else:
        advice.append('Your BMI is in the normal range. Keep up your current habits and stay active.')
    return advice


def get_protein_advice(consumed_protein: float, required_protein: float) -> list:
    """If protein intake < required → show protein tips."""
    advice = []
    consumed_protein = float(consumed_protein)
    required_protein = float(required_protein)
    if required_protein <= 0:
        return advice
    if consumed_protein < required_protein * 0.9:
        shortfall = required_protein - consumed_protein
        advice.append(f'You are under your daily protein target by about {shortfall:.0f}g. Protein supports muscle and satiety.')
        advice.append('Add lean meat, eggs, Greek yogurt, lentils, or a protein shake to meet your goal.')
    return advice


def get_water_advice(consumed_water_liters: float, required_water_liters: float) -> list:
    """If water intake < required → hydration warning."""
    advice = []
    consumed_water_liters = float(consumed_water_liters)
    required_water_liters = float(required_water_liters)
    if required_water_liters <= 0:
        return advice
    if consumed_water_liters < required_water_liters * 0.8:
        advice.append('Your water intake is below the recommended amount. Dehydration can affect performance and recovery.')
        advice.append('Keep a bottle nearby and sip throughout the day.')
    return advice


def get_daily_fitness_advice(bmi_category: str, goal: str) -> list:
    """Personalized daily fitness advice based on BMI category and goal."""
    advice = []
    if goal == 'lose':
        advice.append('Stick to your calorie target and prioritize protein to preserve muscle.')
    elif goal == 'gain':
        advice.append('Eat in a surplus and train with progressive overload for muscle gain.')
    else:
        advice.append('Balance your intake with activity to maintain weight.')

    if bmi_category == 'Underweight':
        advice.append('Consider 3 main meals plus 1–2 snacks to hit your calorie goal.')
    elif bmi_category in ('Overweight', 'Obese'):
        advice.append('Aim for 150+ minutes of moderate activity per week.')
    return advice


def collect_all_advice(
    bmi: Decimal,
    bmi_category: str,
    goal: str,
    consumed_protein: float = 0,
    required_protein: float = 0,
    consumed_water: float = 0,
    required_water: float = 0,
) -> list:
    """
    Combines BMI advice, protein tips, water warning, and daily advice
    into one list for the dashboard.
    """
    all_advice = []
    all_advice.extend(get_bmi_advice(bmi, bmi_category))
    all_advice.extend(get_protein_advice(consumed_protein, required_protein))
    all_advice.extend(get_water_advice(consumed_water, required_water))
    all_advice.extend(get_daily_fitness_advice(bmi_category, goal))
    return all_advice

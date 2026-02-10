# Fitness Tracker – Full-Stack Web Application

A **complete, professional fitness tracking web application** built with Django (Python), HTML, CSS, JavaScript, and Bootstrap. It supports user authentication, health calculations (BMI, BMR, calories, macros), workout and nutrition logging, and a **smart advice system** with a clean dashboard.

---

## Tech Stack

| Layer        | Technology                          |
|-------------|--------------------------------------|
| Backend     | Django (Python)                      |
| Frontend    | HTML, CSS, JavaScript, Bootstrap 5   |
| Database    | SQLite (Django ORM)                  |
| Auth        | Django Auth System                   |
| Architecture| MVC (Models, Views, Templates)       |

---

## Project Structure

```
group project/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3                 # Created after migrate
├── fitness_tracker/           # Project config
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── users/                     # Authentication & profile
│   ├── models.py             # UserProfile
│   ├── views.py              # Register, Login, Logout, Profile
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── health/                    # Health calculations & dashboard
│   ├── models.py             # HealthData
│   ├── views.py              # Dashboard
│   ├── calculations.py       # BMI, BMR, calories, macros, water
│   ├── advice.py             # Smart advice logic
│   ├── urls.py
│   └── admin.py
├── workouts/                  # Workout tracking
│   ├── models.py             # WorkoutLog
│   ├── views.py              # List, Add, Edit, Delete
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── nutrition/                 # Nutrition tracking
│   ├── models.py             # NutritionLog
│   ├── views.py              # List, Add, Edit, Delete
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── templates/                 # Reusable HTML templates
│   ├── base.html             # Base layout, nav, Bootstrap
│   ├── users/
│   │   ├── login.html
│   │   ├── register.html
│   │   └── profile.html
│   ├── health/
│   │   └── dashboard.html
│   ├── workouts/
│   │   ├── workout_list.html
│   │   ├── workout_form.html
│   │   └── workout_confirm_delete.html
│   └── nutrition/
│       ├── nutrition_list.html
│       ├── nutrition_form.html
│       └── nutrition_confirm_delete.html
└── static/                    # CSS, JS, images
    └── .gitkeep
```

---

## Database Models

- **UserProfile** (users): One-to-one with Django `User`. Fields: `age`, `gender`, `height`, `weight`, `goal` (lose/maintain/gain). Used for all health calculations.
- **HealthData** (health): Snapshot of calculated metrics per user (BMI, BMR, daily calories, protein, fat, carbs, water). One record per user per day.
- **WorkoutLog** (workouts): Per-user workout entries. Fields: `date`, `exercise_name`, `sets`, `reps`, `duration_minutes`, `location` (home/gym), `notes`.
- **NutritionLog** (nutrition): Per-user food entries. Fields: `date`, `meal_name`, `protein_g`, `fat_g`, `carbs_g`, `total_calories`, `water_ml`. Calories auto-calculated from macros if not provided (4 cal/g protein, 4 cal/g carb, 9 cal/g fat).

---

## Views & URLs

- **users**: `/register/`, `/login/`, `/logout/`, `/profile/` (profile is login-required).
- **health**: `/health/dashboard/` (login-required; redirects to profile if incomplete).
- **workouts**: `/workouts/` (list), `/workouts/add/`, `/workouts/<id>/edit/`, `/workouts/<id>/delete/`.
- **nutrition**: `/nutrition/` (list), `/nutrition/add/`, `/nutrition/<id>/edit/`, `/nutrition/<id>/delete/`.
- Root `/` redirects to `/health/dashboard/` (login required sends anonymous users to login).

---

## Calculation Formulas

All inputs in **metric**: weight in **kg**, height in **cm**.

1. **BMI**  
   `BMI = weight (kg) / height (m)²`  
   Categories: Underweight (<18.5), Normal (18.5–24.9), Overweight (25–29.9), Obese (≥30).

2. **BMR (Mifflin–St Jeor)**  
   - Men: `BMR = 10×weight + 6.25×height − 5×age + 5`  
   - Women: `BMR = 10×weight + 6.25×height − 5×age − 161`  
   (height in cm, weight in kg, age in years.)

3. **Daily calories (TDEE-based)**  
   `TDEE = BMR × activity_multiplier`  
   Multipliers: lose ≈ 1.375, maintain ≈ 1.55, gain ≈ 1.725.  
   For “lose”: TDEE − 500 kcal (floor 1200). For “gain”: TDEE + 300 kcal.

4. **Daily protein (g)**  
   `protein = weight (kg) × 1.6–2.0` (higher for lose/gain).

5. **Daily fat (g)**  
   Fat = 25% of daily calories; `fat_g = (0.25 × daily_calories) / 9`.

6. **Daily carbs (g)**  
   Remaining calories after protein and fat:  
   `carb_kcal = daily_calories − protein_kcal − fat_kcal`, then `carbs_g = carb_kcal / 4`.

7. **Daily water (L)**  
   `water_liters = (weight_kg × 35) / 1000` (≈35 ml per kg).

---

## Smart Advice Logic

- **BMI &lt; 18.5 (Underweight):** Weight-gain advice (calorie surplus, nutrient-dense foods, strength training).
- **BMI &gt; 25 (Overweight/Obese):** Fat-loss advice (moderate deficit, protein priority, more vegetables, less sugar).
- **Protein:** If consumed protein &lt; 90% of required → show tips to add protein (meat, eggs, yogurt, lentils).
- **Water:** If consumed water &lt; 80% of required → hydration warning and tip to sip throughout the day.
- **Daily fitness:** Goal-based (lose/maintain/gain) and BMI-category tips (e.g. meals + snacks for underweight, 150+ min activity for overweight).

All advice is combined and shown on the **Dashboard** in a single “Personalized Advice” section.

---

## How to Run the Project

1. **Clone/navigate to project folder**
   ```bash
   cd "/home/mohitpareek/coding/workspace/group project"
   ```

2. **Create and activate a virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/macOS
   # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Open in browser**
   - App: **http://127.0.0.1:8000/**
   - Admin: **http://127.0.0.1:8000/admin/**

8. **Use the app**
   - Register → complete profile (age, gender, height, weight, goal) → use Dashboard, Workouts, and Nutrition. All calculation and advice use profile data and daily logs.

---


**Fitness Tracker Web Application**  
Full-stack Django application for tracking fitness and nutrition. Implemented **user authentication** (register, login, logout) and **user profiles** (age, gender, height, weight, goal). Built a **health calculations module** using **BMI**, **BMR (Mifflin–St Jeor)**, and derived **daily calorie and macro targets** (protein, fat, carbs) and **water intake**. Added **workout logging** (exercise, sets, reps, duration, home/gym) and **nutrition logging** (meals, macros, water) with **required vs consumed** comparison on the dashboard. Implemented a **rule-based advice system** (BMI categories, protein and water shortfalls, goal-based tips). Designed a **Bootstrap-based UI** with a central **dashboard** showing metrics, progress bars, recent workouts, and today’s nutrition. Used **Django ORM**, **model–view–template (MVC)** structure, **form validation**, and **login-required** decorators for protected pages. Suitable for placement projects, resumes, and viva discussions on full-stack development and fitness/health logic.

---

## Summary

- **Complete:** Auth, profile, health calculations, workout and nutrition logs, advice, dashboard.  
- **Clean:** Reusable base template, Bootstrap 5, organized apps and URLs.  
- **Placement-ready:** Clear structure, formulas and advice logic documented, README with setup and resume-style description.

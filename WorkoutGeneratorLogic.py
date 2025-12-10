import streamlit as st
import json
import random

st.set_page_config(
    page_title="Exercise Planner",
    page_icon="🏋️"
)

with open("data/exercises.json", "r") as f:
    exercises_db = json.load(f)

def generate_workout(workout_type, difficulty='Beginner', equipment=None, muscles_selected=None):
    exercises = exercises_db[workout_type]

    # Equipment filtering (multi-select)
    if equipment:  # equipment is now a list
        exercises = [
            ex for ex in exercises
            if ex["equipment"] in equipment or ex["equipment"] == "Bodyweight"
        ]

    # Difficulty filtering (Beginner can see all)
    if difficulty != "Beginner":
        exercises = [ex for ex in exercises if ex["difficulty"] == difficulty]

    # Muscle groups present in this filtered list
    muscle_groups = sorted(set(ex["muscle_group"] for ex in exercises))

    # If user selected specific muscles
    if muscles_selected:
        muscle_groups = [m for m in muscle_groups if m in muscles_selected]

    # Build workout
    workout_plan = {}
    for muscle in muscle_groups:
        muscle_exercises = [ex for ex in exercises if ex["muscle_group"] == muscle]
        selected = random.sample(muscle_exercises, k=min(2, len(muscle_exercises)))
        workout_plan[muscle] = selected

    return workout_plan


# ---------------- UI ---------------- #

st.title("Workout Generator")
st.write("Generate personalized workouts based on your preference.")

# Workout type
workout_type = st.selectbox(
    "Choose a workout type:",
    list(exercises_db.keys())
)

# Difficulty
difficulty = st.selectbox(
    "Choose difficulty:",
    ["Beginner", "Intermediate", "Advanced"]
)

# EQUIPMENT → MULTISELECT (same list as before)
all_equipment = sorted(
    set(ex["equipment"] for ex in exercises_db[workout_type])
)

equipment = st.multiselect(
    "Available equipment:",
    all_equipment
)

# Auto-detect muscle groups for this workout type
all_muscles = sorted(
    set(ex["muscle_group"] for ex in exercises_db[workout_type])
)

muscles_selected = st.multiselect(
    "Choose specific muscles (optional):",
    all_muscles
)

# Generate Button
if st.button("Generate Workout"):
    workout = generate_workout(
        workout_type,
        difficulty,
        equipment if len(equipment) > 0 else None,
        muscles_selected if len(muscles_selected) > 0 else None
    )

    st.subheader("Workout Plan:")

    if len(workout) == 0:
        st.error("No exercises match your filters. Try changing difficulty or equipment.")
    else:
        for muscle, exercises in workout.items():
            st.markdown(f"### **{muscle}**")
            for ex in exercises:
                st.write(f"**{ex['name']}** — {ex['sets']} sets × {ex['reps']} reps")
            st.write("---")

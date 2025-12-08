import streamlit as st
import json
import random


with open("data/exercises.json", "r") as f:
    exercises_db = json.load(f)

def generate_workout(workout_type, difficulty='Beginner', equipment='Any', muscles_selected=None):
    exercises = exercises_db[workout_type]


    if equipment != "Any":
        exercises = [
            ex for ex in exercises
            if ex["equipment"] == equipment or ex["equipment"] == "Bodyweight"
        ]


    exercises = [
        ex for ex in exercises
        if ex["difficulty"] == difficulty or difficulty == "Beginner"
    ]


    muscle_groups = sorted(set(ex["muscle_group"] for ex in exercises))


    if muscles_selected:
        muscle_groups = [m for m in muscle_groups if m in muscles_selected]

    workout_plan = {}

    for muscle in muscle_groups:
        muscle_exercises = [ex for ex in exercises if ex["muscle_group"] == muscle]
        selected = random.sample(muscle_exercises, k=min(2, len(muscle_exercises)))
        workout_plan[muscle] = selected

    return workout_plan




st.title("💪 Workout Generator")

st.write("Generate personalized workouts based on your preference.")



workout_type = st.selectbox(
    "Choose a workout type:",
    list(exercises_db.keys())
)

difficulty = st.selectbox(
    "Choose difficulty:",
    ["Beginner", "Intermediate", "Advanced"]
)

equipment = st.selectbox(
    "Available equipment:",
    ["Any", "Bodyweight", "Dumbbells", "Gym"]
)



all_muscles = sorted(
    set(ex["muscle_group"] for ex in exercises_db[workout_type])
)

muscles_selected = st.multiselect(
    "Choose specific muscles (optional):",
    all_muscles
)



if st.button("Generate Workout"):
    workout = generate_workout(
        workout_type,
        difficulty,
        equipment,
        muscles_selected if len(muscles_selected) > 0 else None
    )

    st.subheader("🔥 Your Workout Plan")

    if len(workout) == 0:
        st.error("No exercises match your filters. Try changing difficulty/equipment.")
    else:
        for muscle, exercises in workout.items():
            st.markdown(f"### **{muscle}**")
            for ex in exercises:
                st.write(f"**{ex['name']}** — {ex['sets']} sets × {ex['reps']} reps")


st.write("---")


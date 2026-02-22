import streamlit as st
import pandas as pd
import os
from datetime import date

# Set up the CSV file to store your data locally for now
DATA_FILE = "mission_60kg_data.csv"

# Function to load existing data
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        # Create an empty dataframe with our columns if the file doesn't exist
        columns = ["Date", "Weight", "Eggs", "Sattu", "Soya", "Banana", "Potatoes", "Workout_Type"]
        return pd.DataFrame(columns=columns)

# Function to save new data
def save_data(new_row):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

# --- APP UI START ---
st.set_page_config(page_title="Mission 60KG Tracker", page_icon="💪", layout="centered")

st.title("🚀 Mission 60KG Tracker")
st.markdown("Track your ₹1000/month hostel diet and 5:30 AM workouts.")

# Create tabs for logging and viewing progress
tab1, tab2 = st.tabs(["📝 Daily Log", "📊 My Progress"])

with tab1:
    st.header("Log Today's Progress")
    
    # 1. Date & Weight
    col1, col2 = st.columns(2)
    with col1:
        log_date = st.date_input("Date", date.today())
    with col2:
        weight = st.number_input("Current Weight (kg)", min_value=40.0, max_value=80.0, value=50.0, step=0.1)
    
    # 2. The ₹1000 Diet Checklist
    st.subheader("🟢 Daily Diet Non-Negotiables")
    ate_eggs = st.checkbox("2 Boiled Eggs 🥚")
    ate_sattu = st.checkbox("Heavy Sattu Drink 🥤")
    ate_soya = st.checkbox("30g Soya Chunks 🍲")
    ate_banana = st.checkbox("1 Banana 🍌")
    ate_potatoes = st.checkbox("2 Boiled Potatoes 🥔")
    
    # 3. Workout Tracker
    st.subheader("💪 Workout Log")
    workout_type = st.selectbox("What did you train today at 5:30 AM?", 
                                ["Rest Day", "Push (Chest/Triceps/Shoulders)", "Legs & Core", "Pull (Back/Biceps)", "Full Body Density"])
    
    # Save Button
    if st.button("💾 Save Daily Log"):
        new_entry = {
            "Date": str(log_date),
            "Weight": weight,
            "Eggs": ate_eggs,
            "Sattu": ate_sattu,
            "Soya": ate_soya,
            "Banana": ate_banana,
            "Potatoes": ate_potatoes,
            "Workout_Type": workout_type
        }
        save_data(new_entry)
        st.success("Log saved successfully! Keep pushing for that 60kg.")

with tab2:
    st.header("📈 Weight Gain Dashboard")
    
    df = load_data()
    
    if not df.empty:
        # Plot the weight curve
        st.subheader("Weight Trend")
        # Ensure data is sorted by date for the chart
        df_chart = df.sort_values(by="Date")
        st.line_chart(df_chart.set_index("Date")["Weight"])
        
        # Show raw data
        st.subheader("Raw Data Log")
        st.dataframe(df)
    else:
        st.info("No data yet. Save your first log in the 'Daily Log' tab!")

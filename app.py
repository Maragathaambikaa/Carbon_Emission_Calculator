import streamlit as st

# Initialize the session state if not already initialized
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Define the login function
def login(username, password):
    # Simulate login check (you can replace this with real authentication)
    if password == "pass":  # Assume "pass" is the correct password for simplicity
        st.session_state.logged_in = True
        st.session_state.username = username
        st.experimental_rerun()  # Refresh the app to load the main content
    else:
        st.error("Incorrect password")

# Define the logout function
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.experimental_rerun()  # Refresh the app to load the login page

# Login page
def login_page():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        login(username, password)

# Main content
def main_page():
    EMISSION_FACTORS = {
        "India": {
            "Transportation": 0.14,  # kgCO2/km
            "Electricity": 0.82,  # kgCO2/kWh
            "Diet": 1.25,  # kgCO2/meal, 2.5kgco2/kg
            "Waste": 0.1  # kgCO2/kg
        }
    }

    # Set wide layout and page name
    st.set_page_config(layout="wide", page_title="Personal Carbon Calculator")

    # Streamlit app code
    st.title("Personal Carbon Calculator App ⚠️")
    st.subheader(f"Welcome, {st.session_state.username}!")

    # User inputs
    st.subheader("🌍 Your Country")
    country = st.selectbox("Select", ["India"])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🚗 Daily commute distance (in km)")
        distance = st.slider("Distance", 0.0, 100.0, key="distance_input")

        st.subheader("💡 Monthly electricity consumption (in kWh)")
        electricity = st.slider("Electricity", 0.0, 1000.0, key="electricity_input")

    with col2:
        st.subheader("🍽️ Waste generated per week (in kg)")
        waste = st.number_input("Waste", 0.0, 100.0, key="waste_input")

        st.subheader("🍽️ Number of meals per day")
        meals = st.number_input("Meals", 0, key="meals_input")

    # Normalize inputs
    if distance > 0:
        distance = distance * 365  # Convert daily distance to yearly
    if electricity > 0:
        electricity = electricity * 12  # Convert monthly electricity to yearly
    if meals > 0:
        meals = meals * 365  # Convert daily meals to yearly
    if waste > 0:
        waste = waste * 52  # Convert weekly waste to yearly

    # Calculate carbon emissions
    transportation_emissions = EMISSION_FACTORS[country]["Transportation"] * distance
    electricity_emissions = EMISSION_FACTORS[country]["Electricity"] * electricity
    diet_emissions = EMISSION_FACTORS[country]["Diet"] * meals
    waste_emissions = EMISSION_FACTORS[country]["Waste"] * waste

    # Convert emissions to tonnes and round off to 2 decimal points
    transportation_emissions = round(transportation_emissions / 1000, 2)
    electricity_emissions = round(electricity_emissions / 1000, 2)
    diet_emissions = round(diet_emissions / 1000, 2)
    waste_emissions = round(waste_emissions / 1000, 2)

    # Calculate total emissions
    total_emissions = round(
        transportation_emissions + electricity_emissions + diet_emissions + waste_emissions, 2
    )

    if st.button("Calculate CO2 Emissions"):
        # Display results
        st.header("Results")

        col3, col4 = st.columns(2)

        with col3:
            st.subheader("Your Carbon Emissions in each Category")
            st.info(f"🚗 Transportation: {transportation_emissions} tonnes CO2 per year")
            st.info(f"💡 Electricity: {electricity_emissions} tonnes CO2 per year")
            st.info(f"🍽️ Diet: {diet_emissions} tonnes CO2 per year")
            st.info(f"🗑️ Waste: {waste_emissions} tonnes CO2 per year")

        with col4:
            st.subheader("Total Carbon Footprint")
            st.success(f"🌍 Your total carbon footprint is: {total_emissions} tonnes CO2 per year")
            st.write(f"India's Carbon Emission- as per 2021 data")
            st.warning("In 2021, CO2 emissions per capita for India was 1.9 tons of CO2 per capita. Between 1972 and 2021, CO2 emissions per capita of India grew substantially from 0.39 to 1.9 tons of CO2 per capita rising at an increasing annual rate that reached a maximum of 9.41% in 2021")
        st.write("Click to see Official datasets")
        url='https://data.worldbank.org'

        st.markdown(f'''
    <a href={url}><button style="background-color:red;">World Bank Data</button></a>
    ''',
       unsafe_allow_html=True)
    
    if st.button("Logout"):
        logout()

# Display the appropriate page based on login status
if st.session_state.logged_in:
    main_page()
else:
    login_page()

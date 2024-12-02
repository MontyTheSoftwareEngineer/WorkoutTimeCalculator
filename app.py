import streamlit as st

# Function to parse time in minutes and seconds into total seconds
def parse_time(minutes, seconds):
    minutes = int(minutes) if minutes is not None else 0
    seconds = int(seconds) if seconds is not None else 0
    return minutes * 60 + seconds

# Function to format seconds back into MM:SS format
def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes}:{seconds:02d}"

st.title("CrossFit Workout Timer 🏋️‍♂️")

# Input Type Selection
input_type = st.selectbox("Select Input Type", ["Start & End Times", "End Times & Rest Time"])

# Rest Time Options for "End Times & Rest Time" mode
if input_type == "End Times & Rest Time":
    st.subheader("Rest Time Options")
    same_rest = st.checkbox("Use the same rest time for all rounds", value=True)

    if same_rest:
        # Single rest time input
        st.subheader("Rest Time Between Rounds")
        rest_col1, rest_col2 = st.columns([1, 1])
        rest_min = rest_col1.number_input("Minutes (Rest)", min_value=0, step=1, value=0, key="rest_min")
        rest_sec = rest_col2.number_input("Seconds (Rest)", min_value=0, max_value=59, step=1, value=0, key="rest_sec")
        global_rest_time = parse_time(rest_min, rest_sec)
    else:
        global_rest_time = None

# Initialize session state for round data
if "rounds" not in st.session_state:
    st.session_state.rounds = []

# Add a round card
def add_round():
    st.session_state.rounds.append({"start_min": 0, "start_sec": 0, "end_min": 0, "end_sec": 0, "rest_min": 0, "rest_sec": 0})

# Remove the last round card
def remove_round():
    if st.session_state.rounds:
        st.session_state.rounds.pop()

# Add the first round by default
if not st.session_state.rounds:
    add_round()

# Render round cards
st.subheader("Rounds")
for idx, round_data in enumerate(st.session_state.rounds):
    with st.expander(f"Round {idx + 1}", expanded=True):
        if input_type == "Start & End Times":
            # Start Time Inputs
            st.write("Start Time")
            col1, col2 = st.columns([1, 1])
            round_data["start_min"] = col1.number_input(
                f"Start Minutes (Round {idx + 1})", min_value=0, step=1, value=round_data["start_min"], key=f"start_min_{idx}"
            )
            round_data["start_sec"] = col2.number_input(
                f"Start Seconds (Round {idx + 1})", min_value=0, max_value=59, step=1, value=round_data["start_sec"], key=f"start_sec_{idx}"
            )

            # End Time Inputs
            st.write("End Time")
            col3, col4 = st.columns([1, 1])
            round_data["end_min"] = col3.number_input(
                f"End Minutes (Round {idx + 1})", min_value=0, step=1, value=round_data["end_min"], key=f"end_min_{idx}"
            )
            round_data["end_sec"] = col4.number_input(
                f"End Seconds (Round {idx + 1})", min_value=0, max_value=59, step=1, value=round_data["end_sec"], key=f"end_sec_{idx}"
            )
        elif input_type == "End Times & Rest Time":
            # End Time Inputs
            st.write("End Time")
            col1, col2 = st.columns([1, 1])
            round_data["end_min"] = col1.number_input(
                f"End Minutes (Round {idx + 1})", min_value=0, step=1, value=round_data["end_min"], key=f"end_min_{idx}"
            )
            round_data["end_sec"] = col2.number_input(
                f"End Seconds (Round {idx + 1})", min_value=0, max_value=59, step=1, value=round_data["end_sec"], key=f"end_sec_{idx}"
            )

            # Rest Time Inputs (if not using global rest time)
            if not same_rest:
                st.write("Rest Time for This Round")
                col3, col4 = st.columns([1, 1])
                round_data["rest_min"] = col3.number_input(
                    f"Rest Minutes (Round {idx + 1})", min_value=0, step=1, value=round_data["rest_min"], key=f"rest_min_{idx}"
                )
                round_data["rest_sec"] = col4.number_input(
                    f"Rest Seconds (Round {idx + 1})", min_value=0, max_value=59, step=1, value=round_data["rest_sec"], key=f"rest_sec_{idx}"
                )

# Buttons to add or remove rounds
st.button("+ Add Round", on_click=add_round)
st.button("- Remove Last Round", on_click=remove_round)

# Calculate Button
if st.button("Calculate"):
    results = []
    previous_end_time = 0

    for idx, round_data in enumerate(st.session_state.rounds):
        if input_type == "Start & End Times":
            start_time = parse_time(round_data["start_min"], round_data["start_sec"])
            end_time = parse_time(round_data["end_min"], round_data["end_sec"])
            round_time = end_time - start_time
        elif input_type == "End Times & Rest Time":
            end_time = parse_time(round_data["end_min"], round_data["end_sec"])
            if idx == 0:
                start_time = 0  # First round starts at 0:00
            else:
                if same_rest:
                    rest_time = global_rest_time
                else:
                    rest_time = parse_time(round_data["rest_min"], round_data["rest_sec"])

                start_time = previous_end_time + rest_time

            round_time = end_time - start_time
            previous_end_time = end_time

        results.append((f"Round {idx + 1}", format_time(start_time), format_time(end_time), format_time(round_time)))

    # Display Results
    st.subheader("Results")
    st.table(
        {
            "Round": [r[0] for r in results],
            "Start Time (MM:SS)": [r[1] for r in results],
            "End Time (MM:SS)": [r[2] for r in results],
            "Round Time (MM:SS)": [r[3] for r in results],
        }
    )

import functions
import time
import streamlit as st
import pandas as pd
import altair as alt

URL = "https://programmer100.pythonanywhere.com/"
DATA_STORE = 'data-temp.txt'


def create_chart(df):
    # Modified chart configuration for better visibility
    chart = alt.Chart(df).mark_line(
        color='#00ff00',  # Make line green for better visibility on dark background
        strokeWidth=2
    ).encode(
        x=alt.X('time:O', title='Time'),  # Changed to ordinal type for discrete time points
        y=alt.Y('temperature:Q',
                title='Temperature (°C)',
                scale=alt.Scale(domain=[15, 23])),  # Fixed y-axis range
        tooltip=['time', 'temperature']
    ).properties(
        width=600,
        height=400
    ).configure_axis(
        labelColor='white',
        titleColor='white',
        grid=True,
        gridColor='#444444'
    ).configure_view(
        strokeWidth=0,
        fill='#0E1117'  # Match Streamlit's dark theme
    )
    return chart


def main():
    st.set_page_config(layout="wide")

    # Title and header
    st.title("Average World Temperature Monitor")
    st.subheader("By Ahmad Fauzan")
    st.divider()

    # Create columns for layout
    col1, col2 = st.columns([7, 3])

    # Display current date in left column
    with col1:
        current_date = time.strftime('Date: %A, %d-%b-%y')
        st.write(f"**{current_date}**")

    # Initialize session state for data storage
    if 'temp_data' not in st.session_state:
        st.session_state.temp_data = []
        st.session_state.times = []

    # Get new temperature data
    scraped = functions.scrape(URL)
    extracted = functions.extract(scraped, file_store='extract-temp.yaml', data='temperature')
    current_time = time.strftime('%H:%M:%S')

    # Store data
    functions.store(extracted, DATA_STORE)
    st.session_state.temp_data.append(float(extracted))
    st.session_state.times.append(current_time)

    # Keep only last 30 data points for better visualization
    if len(st.session_state.temp_data) > 30:
        st.session_state.temp_data = st.session_state.temp_data[-30:]
        st.session_state.times = st.session_state.times[-30:]

    # Create dataframe for chart
    df = pd.DataFrame({
        'time': st.session_state.times,
        'temperature': st.session_state.temp_data
    })

    # Display chart in left column
    with col1:
        chart = create_chart(df)
        st.altair_chart(chart, use_container_width=True)

    # Display temperature list in right column
    with col2:
        st.write("**Temperature Records**")
        for time_str, temp in zip(reversed(st.session_state.times[-10:]),
                                  reversed(st.session_state.temp_data[-10:])):
            st.write(f"{time_str} - {temp}°C")

    # Auto-refresh every second
    time.sleep(1)
    st.rerun()


if __name__ == "__main__":
    main()
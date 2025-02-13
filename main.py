import functions
import time
import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

URL = "https://programmer100.pythonanywhere.com/"
DATA_STORE = 'data-temp.txt'


def create_chart(df):
    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('time:T', title='Time'),
        y=alt.Y('temperature:Q', title='Temperature (°C)'),
        tooltip=['time:T', 'temperature:Q']
    ).properties(
        width=600,
        height=400
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
        current_date = datetime.now().strftime('%A, %d-%b-%y')
        st.write(f"**Date:** {current_date}")

    # Initialize session state for data storage
    if 'temp_data' not in st.session_state:
        st.session_state.temp_data = []
        st.session_state.times = []

    # Get new temperature data
    scraped = functions.scrape(URL)
    extracted = functions.extract(scraped, file_store='extract-temp.yaml', data='temperature')
    current_time = datetime.now()

    # Store data
    functions.store(extracted, DATA_STORE)
    st.session_state.temp_data.append(float(extracted))
    st.session_state.times.append(current_time)

    # Create dataframe for chart
    df = pd.DataFrame({
        'time': st.session_state.times,
        'temperature': st.session_state.temp_data
    })

    # Display chart in left column
    with col1:
        st.altair_chart(create_chart(df), use_container_width=True)

    # Display temperature list in right column
    with col2:
        st.write("**Temperature Records**")
        for time, temp in zip(reversed(st.session_state.times[-10:]),
                              reversed(st.session_state.temp_data[-10:])):
            st.write(f"{time.strftime('%H:%M:%S')} - {temp}°C")

    # Auto-refresh every minute
    time.sleep(60)
    st.experimental_rerun()


if __name__ == "__main__":
    main()
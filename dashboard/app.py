from shiny import reactive, render
from shiny.express import ui
import random
from datetime import datetime
from collections import deque
import pandas as pd
import plotly.express as px
from ipyleaflet import Map
from shinywidgets import render_plotly, render_widget
from shinyswatch import theme
from scipy import stats
from faicons import icon_svg # https://fontawesome.com/v4/cheatsheet/

# First, set a constant UPDATE INTERVAL for all live data

UPDATE_INTERVAL_SECS: int = 1

# Initialize a REACTIVE VALUE with a common data structure
# This reactive value is a wrapper around a DEQUE of readings

DEQUE_SIZE: int = 10
reactive_value_wrapper = reactive.value(deque(maxlen=DEQUE_SIZE))

# Initialize a REACTIVE CALC that all display components can call
# to get the latest data and display it.

@reactive.calc()
def reactive_calc_combined():
    # Invalidate this calculation every UPDATE_INTERVAL_SECS to trigger updates
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)

    # Data generation logic
    temp = round(random.uniform(20, 21), 1)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_deque_info = {"temp":temp, "timestamp":timestamp}

    # get the deque and append the new entry
    reactive_value_wrapper.get().append(new_deque_info)

    # Get a snapshot of the current deque for any further processing
    deque_snapshot = reactive_value_wrapper.get()

    # For Display: Convert deque to DataFrame for display
    deque_df = pd.DataFrame(deque_snapshot)

    # For Display: Get the latest dictionary entry
    latest_deque_entry = new_deque_info

    # Return a tuple with everything we need
    # Every time we call this function, we'll get all these values
    return deque_snapshot, deque_df, latest_deque_entry

# Define the Shiny UI Page layout
# Call the ui.page_opts() function
ui.page_opts(title="PyShiny Express: Live Random Data", fillable=True)
theme.superhero()

with ui.sidebar(open="open"):

    ui.h2("Oklahoma City Explorer", class_="text-center")
    ui.p(
        "A demonstration of real-time temperature readings in Oklahoma City.",
        class_="text-center",
    )
    
    @render_widget(width="200%", height="200px")
    def my_map():
        return Map(center=(35.36, -97.38), zoom=10)
        
    ui.hr()
    ui.h6("Links:")
    ui.a(
        "GitHub Source",
        href="https://github.com/adriacv17/cintel-05-cintel",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://adriacv17.github.io/cintel-05-cintel/",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    

# In Shiny Express, everything not in the sidebar is in the main panel

with ui.layout_columns():
    with ui.value_box(
        showcase=icon_svg("fire"),
        theme="bg-gradient-red-yellow",
    ):

        "Current Temperature"

        @render.text
        def display_temp():
            """Get the latest reading and return a temperature string"""
            deque_snapshot, deque_df, latest_deque_entry = reactive_calc_combined()
            return f"{latest_deque_entry['temp']} C"

        "warm as normal"

  

    with ui.value_box(
        showcase=icon_svg("clock"),
        theme="bg-gradient-orange-yellow",
    ):
        "Current Date and Time"
        @render.text
        def display_time():
            """Get the latest reading and return a timestamp string"""
            deque_snapshot, deque_df, latest_deque_entry = reactive_calc_combined()
            return f"{latest_deque_entry['timestamp']}"


with ui.layout_columns():
    with ui.card(full_screen=True,width="200%", height="300px"):
        ui.card_header("Most Recent Readings")

        @render.data_frame
        def display_deque_df():
            """Get the latest reading and return a dataframe with current readings"""
            deque_snapshot, deque_df, latest_deque_entry = reactive_calc_combined()
            pd.set_option('display.width', None)        # Use maximum width
            return render.DataGrid( deque_df,width="100%")

    with ui.card(full_screen=True):
        ui.card_header("Chart with Current Trend")

        @render_plotly
        def display_plot():
            # Fetch from the reactive calc function
            deque_snapshot, deque_df, latest_deque_entry = reactive_calc_combined()

            # Ensure the DataFrame is not empty before plotting
            if not deque_df.empty:
                # Convert the 'timestamp' column to datetime for better plotting
                deque_df["timestamp"] = pd.to_datetime(deque_df["timestamp"])

                # Create scatter plot for readings
                # pass in the deque_df, the name of the x column, the name of the y column,
                # and more
        
                fig = px.scatter(deque_df,
                x="timestamp",
                y="temp",
                title="Temperature Readings with Regression Line",
                labels={"temp": "Temperature (°C)", "timestamp": "Time"},
                color="temp",
                color_continuous_scale=px.colors.sequential.Peach)
                fig.update_layout(coloraxis_colorbar=dict(yanchor="top", y=0.9, x=1, ticks="outside"))
                fig.update_layout(paper_bgcolor="yellow")
                # Linear regression - we need to get a list of the
                # Independent variable x values (time) and the
                # Dependent variable y values (temp)
                # then, it's pretty easy using scipy.stats.linregress()

                # For x let's generate a sequence of integers from 0 to len(deque_df)
                sequence = range(len(deque_df))
                x_vals = list(sequence)
                y_vals = deque_df["temp"]

                slope, intercept, r_value, p_value, std_err = stats.linregress(x_vals, y_vals)
                deque_df['best_fit_line'] = [slope * x + intercept for x in x_vals]

                # Add the regression line to the figure
                fig.add_scatter(x=deque_df["timestamp"], y=deque_df['best_fit_line'], mode='lines', name='Regression Line')
 
                # Update layout as needed to customize further
                fig.update_layout(xaxis_title="Time",yaxis_title="Temperature (°C)")
            return fig
# %%
import time
import pandas as pd
from utils.crypto_data_download import CryptoDataDownload
from strategies import strategy
from strategies.drunk_monkey import DrunkMonkey
import datetime
import streamlit as st
import matplotlib.pyplot as plt

# --- Value Choice Dicts --- #
strategies = {"Drunk Monkey": DrunkMonkey}
data_sources = {
    "Binance BTCUSDT 1h": {
        "path": "data/Binance_BTCUSDT_1h.csv",
        "data_type": CryptoDataDownload,
    }
}

# --- Streamlit --- #
st.title("QuantSim Backtester")
# Empty placeholders
strategy_header = st.empty()
strategy_name = st.empty()
progress_bar_placeholder = st.empty()
net_worth_placeholder = st.empty()
chart_placeholder = st.empty()

# --- SIDE BAR --- #
st.sidebar.title("Strategy Parameters")
st.sidebar.markdown("### Capital")
capital = st.sidebar.number_input("Initial Capital (USDT)", value=100000.0)
strategy_choice = st.sidebar.selectbox("Strategy", ["Drunk Monkey"])
data_choice = st.sidebar.selectbox("Data", ["Binance BTCUSDT 1h"])
start = st.sidebar.button("Start")


def calculate_change(current_value: float, initial_value: float):
    """
    Calculates the gain/loss as a percentage.

    Args:
        current_value (float): The current value.
        initial_value (float): The initial value.

    Returns:
        float: The gain/loss as a percentage.
    """
    return (current_value - initial_value) / initial_value


def run_simulation():
    """
    Runs the simulation, updating the UI as it goes.
    """
    global net_worth_placeholder, chart_placeholder

    # Create the strategy generator
    strategy = strategies[strategy_choice](
        data_source=data_sources[data_choice]["path"],
        data_type=data_sources[data_choice]["data_type"],
        capital=capital,
    )
    gen = strategy.execute()

    strategy_name.markdown(f"### Strategy: {strategy_choice}")
    # Set up chart
    data = {
        "x": [],
        "y": [],
    }
    fig, ax = plt.subplots(figsize=(7, 4))

    # Iterate through the strategy
    idx = 0
    for _, n in gen:
        # Update the progress bar
        progress_bar_placeholder.progress(idx / n)

        net_worth: float = strategy.calculate_net_worth()
        # Update the chart
        data["x"].append(idx)
        data["y"].append(net_worth)
        print(f"progress: {idx:,}/{n:,} =  {idx / n:,.2f}")

        # Update the metric
        net_worth_placeholder.metric(
            "Net Worth",
            f"${net_worth:,.2f}",
            delta=f"{calculate_change(net_worth, strategy.initial_capital)*100:,.2f}",
        )

        # Update plot at every 1000th iteration
        if idx % 1000 != 0:
            idx += 1
            continue

        # Update the chart
        with chart_placeholder.container():
            ax.set_title("Net Worth")
            ax.set_xlabel("Time")
            ax.set_ylabel("USDT")
            ax.grid("on")
            ax.plot(data["x"], data["y"], color="blue")
            plt.tight_layout()
            st.pyplot(fig, clear_figure=False)

        idx += 1

    st.success("Simulation Complete")


if start:
    run_simulation()


# %%

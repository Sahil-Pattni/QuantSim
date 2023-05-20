# %%
import time
from typing import List
import pandas as pd
from utils.crypto_data_download import CryptoDataDownload
from strategies import strategy
from strategies.drunk_monkey import DrunkMonkey
import datetime
import streamlit as st
import matplotlib.pyplot as plt

from utils.trade import Trade

# --- Value Choice Dicts --- #
strategies = {"Drunk Monkey": DrunkMonkey}
data_sources = {
    "Binance BTCUSDT 1h": {
        "path": "data/Binance_BTCUSDT_1h.csv",
        "data_type": CryptoDataDownload,
    }
}

# Plotting Figure
fig, ax = plt.subplots(figsize=(7, 4))

# --- Streamlit --- #
st.title("QuantSim Backtester")
# Empty placeholders
strategy_desc = st.container()
progress_bar_placeholder = st.empty()
metrics_placeholder = st.empty()
chart_placeholder = st.empty()
trade_history_placeholder = st.container()
# --- SIDE BAR --- #
st.sidebar.title("Strategy Parameters")
st.sidebar.markdown("### Capital")
capital = st.sidebar.number_input("Initial Capital (USDT)", value=100000.0)
strategy_choice = st.sidebar.selectbox("Strategy", ["Drunk Monkey"])
data_choice = st.sidebar.selectbox("Data", ["Binance BTCUSDT 1h"])
step = st.sidebar.number_input("Chart Update Frequency", value=500)
start = st.sidebar.button("Start")


def clear_all():
    """
    Clears all placeholders.
    """
    global trade_history_placeholder, strategy_desc
    progress_bar_placeholder.empty()
    chart_placeholder.empty()
    strategy_desc = st.container()
    metrics_placeholder = st.empty()
    trade_history_placeholder = st.container()


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


def update_chart(data: dict):
    """
    Updates the chart with the given data.

    Args:
        data (dict): The data to update the chart with.
                      Must have keys "x" and "y".
    """
    global chart_placeholder, fig, ax
    # Clear previous chart
    ax.clear()
    with chart_placeholder.container():
        ax.set_title("Net Worth")
        ax.set_xlabel("Time")
        ax.set_ylabel("USDT")
        plt.setp(ax.get_xticklabels(), rotation=45)
        ax.grid("on")
        ax.plot(data["x"], data["y"], color="blue")
        plt.tight_layout()
        st.pyplot(fig, clear_figure=False)


def update_metrics(net_worth: float, num_sells: int, num_buys: int):
    # Update the metric
    with metrics_placeholder.container():
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Net Worth",
            f"${net_worth:,.2f}",
            delta=f"{calculate_change(net_worth, capital)*100:,.2f}%",
        )
        col2.metric("Number of Buys", f"{num_buys:,}")
        col3.metric("Number of Sells", f"{num_sells:,}")


def run_simulation(step=1000):
    """
    Runs the simulation, updating the UI as it goes.
    """
    global net_worth_placeholder

    # Create the strategy generator
    strategy = strategies[strategy_choice](
        data_source=data_sources[data_choice]["path"],
        data_type=data_sources[data_choice]["data_type"],
        capital=capital,
    )
    gen = strategy.execute()

    with strategy_desc:
        st.markdown(f"### Strategy: {strategy_choice}")
        st.markdown(strategy.description)
    # Set up chart
    data = {
        "x": [],
        "y": [],
    }

    trades: List[Trade] = []
    num_buys, num_sells = 0, 0

    # Iterate through the strategy
    for idx, n, trade, date in gen:
        # Update the trade history
        for t in trade:
            trades.append(t)
            if t.action == "BUY":
                num_buys += 1
            else:
                num_sells += 1

        # Update data
        net_worth: float = strategy.calculate_net_worth()
        data["x"].append(date)
        data["y"].append(net_worth)

        # Update plot at every 1000th iteration
        if idx % step != 0:
            continue

        # Update the chart
        update_chart(data)

        # Update metrics
        update_metrics(net_worth, num_sells, num_buys)

        # Update the progress bar
        with progress_bar_placeholder:
            st.progress(idx / n)

    st.success("Simulation Complete")

    with trade_history_placeholder:
        st.header("Trade History")
        trades = pd.DataFrame([t.__dict__ for t in trades])
        st.dataframe(trades, use_container_width=True)


if start:
    run_simulation(step=step)


# %%

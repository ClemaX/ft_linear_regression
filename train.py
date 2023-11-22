#!/usr/bin/env python
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import to_rgba
import seaborn as sns
import pandas as pd

from utils import *

DATA_FILEPATH = "data.csv"
THETAS_FILEPATH = "thetas.csv"

LEARNING_RATE = 0.01
ITERATION_COUNT = 1000


def data_load_standardized(filepath):
    df = pd.read_csv(filepath)
    standardized_df = (df - df.mean()) / df.std()

    return standardized_df


def lerp_color(color_a, color_b, factor):
    rgba_a = to_rgba(color_a)
    rgba_b = to_rgba(color_b)

    rgb_lerped = tuple((1 - factor) * a + factor * b for a, b in zip(rgba_a, rgba_b))

    return (rgb_lerped[0][0], rgb_lerped[1][0], rgb_lerped[2][0], rgb_lerped[3][0])


def model_error():
    # Get approximation delta
    error = data.apply(lambda row: model(row["km"]) - row["price"], axis="columns")

    # Calculate thetas error
    return pd.DataFrame(
        data={
            "theta_0": [error.mean()],
            "theta_1": [(error * data["km"]).mean()]
        }
    )


def model_learn():
    global thetas

    error = model_error()

    # Calculate deltas
    delta_thetas = -error * LEARNING_RATE

    thetas += delta_thetas

    cost = (error["theta_0"] ** 2 + error["theta_1"] ** 2)**0.5

    return cost

line = None

def model_plot(color=None):
    global line

    # Draw linear approximation
    if line is not None:
        line.remove()
        del line

    line = ax_data.axline(
        (0, thetas["theta_0"][0]), slope=thetas["theta_1"][0],
        color=color)


def train_step(epoch):
    global cost_history

    cost = model_learn()
    cost_history = pd.concat([
        cost_history,
        pd.DataFrame({"epoch": epoch, "cost": cost})
    ])

    model_plot(lerp_color("#50fa7b", "#ff5555", cost))

    ax_cost.clear()
    sns.lineplot(ax=ax_cost, data=cost_history, x="epoch", y="cost")


# Apply theme
sns.set_theme(
    style="dark",
    rc={
        "figure.facecolor": "#1E1F28",
        "axes.facecolor": "#282a36",
        "axes.edgecolor": "#bd93f9",
        "axes.titlecolor": "#50fa7b",
        "axes.labelcolor": "#ff79c6",
        "xtick.color": "#f8f8f2",
        "ytick.color": "#f8f8f2",
        "text.color": "#f8f8f2",
    }
)

# Load standardized CSV dataset
data = data_load_standardized(DATA_FILEPATH)

# Initialize cost history
cost_history = pd.DataFrame({"epoch": [], "cost": []})

# Create pyplot figure
fig, (ax_data, ax_cost) = plt.subplots(2, 1)

# Plot dataset
ax_data.set(title="Standardized Car Price by Kilometers")
sns.scatterplot(
    ax=ax_data,
    data=data, x="km", y="price", palette="blend:#ff79c6,#8be9fd",
    edgecolor="face", hue="price")

ax_cost.set(title="Cost")

ani = FuncAnimation(fig, train_step, frames=ITERATION_COUNT, interval=100)

plt.show()

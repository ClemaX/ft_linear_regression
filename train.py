#!/usr/bin/env python
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import to_rgba
import seaborn as sns
import pandas as pd

from common import *


DATA_FILEPATH = "data.csv"

LEARNING_RATE = 0.05
MAX_ITERATIONS = 1000
COST_TARGET = 0.005

PARAMS_INITIAL = {'theta': [0, 0]}


def data_load_standardized(filepath=DATA_FILEPATH):
    df = pd.read_csv(filepath)
    standardized_df = (df - df.mean()) / df.std()

    return standardized_df


def lerp_color(color_a, color_b, factor):
    rgba_a = to_rgba(color_a)
    rgba_b = to_rgba(color_b)

    rgb_lerped = tuple((1 - factor) * a + factor * b for a, b in zip(rgba_a, rgba_b))

    return (rgb_lerped[0], rgb_lerped[1], rgb_lerped[2], rgb_lerped[3])


def model_error():
    # Get approximation delta
    error = data.apply(lambda row: model(params, row['km']) - row['price'], axis='columns')

    # Calculate params error
    return pd.DataFrame(
        data={
            'theta': [
                error.mean(),
                (error * data['km']).mean()],
        }
    )


def model_learn():
    global params

    error = model_error()

    # Calculate deltas
    delta_params = -error * LEARNING_RATE

    params += delta_params

    cost = (error['theta'][0] ** 2 + error['theta'][1] ** 2)**0.5

    return cost

line = None

def model_plot(color=None):
    global line

    if line is not None:
        line.remove()
        del line

    line = ax_data.axline(
        (0, params['theta'][0]), slope=params['theta'][1],
        color=color)


def model_plot_cost():
    cost_line.set_data(epoch_history, cost_history)
    ax_cost.set_xlim(0, max(1, max(epoch_history)))


def train_step(epoch):
    global cost_history

    cost = model_learn()

    epoch_history.append(epoch)
    cost_history.append(cost)

    model_plot(lerp_color("#50fa7b", "#ff5555", cost))

    model_plot_cost()

    if cost <= COST_TARGET:
        print("Stopping animation...")
        ani.pause()

        print("Saving params...")
        params_save(params)


# Apply theme
sns.set_theme(
    style="dark",
    rc={
        'figure.facecolor': "#1E1F28",
        'axes.facecolor': "#282a36",
        'axes.edgecolor': "#bd93f9",
        'axes.titlecolor': "#50fa7b",
        'axes.labelcolor': "#ff79c6",
        'xtick.color': "#f8f8f2",
        'ytick.color': "#f8f8f2",
        'text.color': "#f8f8f2",
    }
)

# Load standardized CSV dataset
data = data_load_standardized()

# Initialize params
params = pd.DataFrame(data=PARAMS_INITIAL)

# Initialize cost history
epoch_history = []
cost_history = []

# Create pyplot figure
fig, (ax_data, ax_cost) = plt.subplots(2, 1)

# Plot dataset
ax_data.set(title="Standardized Car Price by Kilometers")
sns.scatterplot(
    ax=ax_data,
    data=data, x='km', y='price', palette="blend:#ff79c6,#8be9fd",
    edgecolor='face', hue='price')

# Plot cost
cost_line, = ax_cost.plot(epoch_history, cost_history, label="Cost")
ax_cost.legend()
ax_cost.set_ylim(0, 1)

# Animate training
ani = FuncAnimation(fig, train_step, frames=MAX_ITERATIONS, interval=30)

plt.show()

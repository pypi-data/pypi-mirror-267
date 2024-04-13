"""Tests for converter.py."""
# %% Imports
# Standard Library Imports
from copy import deepcopy

# Third Party Imports
from matplotlib import pyplot as plt
from numpy import arange, array, cos, max, min, sin

# Econoplots Imports
from econoplots.converter import convert2Econo

# %% Make data
x = arange(-1, 1, 0.2)
y = array([3.1 * sin(x), 2 * cos(x), sin(x + 0.2)]).T
print(f"min(x) = {min(x)}")
print(f"max(x) = {max(x)}")
print(f"min(y) = {min(y)}")
print(f"max(y) = {max(y)}")

# %% Test line converter function
fig, ax_line = plt.subplots()
# ax_line.plot(x, y, color="red")
ax_line.plot(x, y, color="red", label=["a", "b", "c"])
ax_line.set_xlabel(r"X label $\epsilon, \varepsilon \kappa$ ")
ax_line.set_ylabel("Y label")
ax_line.legend()

ax_new = convert2Econo(deepcopy(ax_line))
# %% Test line convert with 0,0 dot
ax_new = convert2Econo(deepcopy(ax_line), zero_dot=True)


# %% Test line fill converter
fig, ax_fill = plt.subplots()
ax_fill.fill_between(x, y[:, 0], label="der", color="green")
# ax_line.plot(x, y, color="red", label=["a", "b", "c"])
ax_fill.set_xlabel("X label")
ax_fill.set_ylabel("Y label")
ax_fill.legend(loc="center")

ax_new = convert2Econo(deepcopy(ax_fill), "fill")

# %% Test box plot converter
# test with and without fliers
fig, ax_box = plt.subplots()
ax_box.boxplot(
    y,
    vert=False,
    labels=["seriesA", "sB", "Another Series"],
    patch_artist=True,
    showfliers=True,
)
ax_box.set_xlabel("X Label, showfliers=True")

ax_new = convert2Econo(ax_box, ax_type="hbox")

fig, ax_box = plt.subplots()
ax_box.boxplot(
    y,
    vert=False,
    labels=["seriesA", "sB", "Another Series"],
    patch_artist=True,
    showfliers=False,
)
ax_box.set_xlabel("X Label, showfliers=False")

ax_new = convert2Econo(ax_box, ax_type="hbox")
# %% Test bar converter (vertical)
x_bar = [1, 2, 3, 4]
y_bar = [3, 5, 7, 1.1]
fig, ax_bar = plt.subplots()
ax_bar.bar(x_bar, y_bar, label="series A")
ax_bar.legend(loc="center")
ax_new = convert2Econo(ax_bar, ax_type="bar")
# %% Test bar converter (horizontal)
x_bar = [1, 2, 3, 4]
y_bar = [3, 5, 7, 1.1]
fig, ax_hbar = plt.subplots()
ax_hbar.barh(x_bar, y_bar)
ax_new = convert2Econo(ax_hbar, ax_type="bar", orientation="horizontal")
# %% done
plt.show()
print("done")

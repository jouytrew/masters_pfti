import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def plot_grade_recovery_curve(ax: plt.Axes, df: pd.DataFrame, element: str, s=3, alpha=0.2):
    s = 3
    
    ax_sec = ax.twinx()

    x = df['cml_weight_pct']
    ax.set_xlabel("Cumulative Mass %")
    ax.set_xlim(0, 1)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    y = df['cml_grade']
    
    ax.plot(x, y, color='blue', alpha=0.2, ls='--')
    ax.scatter(x, y, color='blue', s=s)
    
    ax.set_ylim([0, None])
    ax.set_ylabel(f"Cumulative {element} Grade", c="blue")

    y = df['cml_recovery']
    ax_sec.set_ylabel(f"Cumulative {element} Recovery", c="red") 
    ax_sec.set_ylim(0, 1)
    ax_sec.set_yticks([0, 0.25, 0.5, 0.75, 1])
    ax_sec.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    ax_sec.plot([0, 1], [0, 1], color='grey', alpha=0.2, ls='-.')

    ax_sec.plot(x, y, color='red', alpha=0.2, ls='--')
    ax_sec.scatter(x, y, color='red', s=s)
    
def plot_g_r(ax: plt.Axes, ax_sec: plt.Axes, df: pd.DataFrame, color_g='blue', color_r='red', *args, **kwargs):
    x = df['cml_weight_pct']
    y = df['cml_grade']
    ax.plot(x, y, color=color_g, **kwargs)
    
    y = df['cml_recovery']
    ax_sec.plot(x, y, color=color_r, **kwargs)
    
def scatter_g_r(ax: plt.Axes, ax_sec: plt.Axes, df: pd.DataFrame, color_g='blue', color_r='red', *args, **kwargs):
    x = df['cml_weight_pct']
    y = df['cml_grade']
    ax.scatter(x, y, color=color_g, **kwargs)
    
    y = df['cml_recovery']
    ax_sec.scatter(x, y, color=color_r, **kwargs)
    
def set_g_r_labels(ax: plt.Axes, ax_sec: plt.Axes, element: str):
    ax.set_xlabel("Cumulative Mass %")
    ax.set_xlim(0, 1)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1])
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    
    ax.set_ylabel(f"Cumulative {element} Grade", c="blue")
    
    ax_sec.set_ylabel(f"Cumulative {element} Recovery", c="red") 
    ax_sec.set_ylim(0, 1)
    ax_sec.set_yticks([0, 0.25, 0.5, 0.75, 1])
    ax_sec.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
            
    ax.set_ylim([0, None])



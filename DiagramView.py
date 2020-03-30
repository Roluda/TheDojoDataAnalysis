import matplotlib.pyplot as mpl
import numpy as np

def displayTotalMoves(dictionary):
    x = np.arange(len(dictionary))
    width = 0.35

    fig, ax = mpl.subplots()
    rects = ax.bar(x, dictionary.values(), width, label = dictionary.keys())
    ax.set_ylabel('Amount')
    ax.set_title('Moves used in Data')
    ax.set_xticks(x)
    ax.set_xticklabels(dictionary.keys(), rotation=35, ha ="right")

    fig.tight_layout()
    mpl.show()



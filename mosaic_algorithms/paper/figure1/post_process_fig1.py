import matplotlib.pyplot as plt
import sys
sys.path.append('C:\\Users\kekka\Documents\pythonProjects\pySPICElib')

def post_process_fig1():
    # Zoom in
    plt.xlim([-30, 60])
    plt.ylim([-15, 35])
    xtick = range(-30, 61, 15)
    ytick = range(-15, 36, 10)

    # x tick label
    xtickstr = []
    for i in xtick:
        if i < 0 and i > -180:
            xtickstr.append(f"{-i}ºW")
        elif i > 0 and i < 180:
            xtickstr.append(f"{i}ºE")
        else:
            xtickstr.append(f"{abs(i)}º")

    # y tick label
    ytickstr = []
    for i in ytick:
        if i < 0:
            ytickstr.append(f"{-i}ºS")
        elif i > 0:
            ytickstr.append(f"{i}ºN")
        else:
            ytickstr.append(f"{i}º")

    plt.gca().set_xticks(xtick)
    plt.gca().set_yticks(ytick)
    plt.gca().set_xticklabels(xtickstr)
    plt.gca().set_yticklabels(ytickstr)
    plt.gca().tick_params(which='both', direction='in', top=True, right=True)
    plt.grid(True, which='both', color='w', linestyle=':', linewidth=1, alpha=1)

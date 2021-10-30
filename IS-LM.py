import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
plt.style.use('seaborn-dark')

def IS():
    return (A - y*(1 - c*(1 - t)))/b

def LM():
    return (1/h)*(k*y - Ms/P)

def MD():
    M = np.arange(0, 50000)
    return (1/h)*(k*y_eq() - M)

def AE():
    return A + c*(1-t)*y - b*i_eq()

def y_eq():
    return np.argwhere(np.diff(np.sign(IS() - LM()))).flatten()

def i_eq():
    return (1/h)*(k*y_eq() - Ms/P)

def AD():
    return b/h*Ms/(y*(1-c*(1-t)+b/h*k) - A)

def labelBars(ax, ba):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for child in ax.get_children():
        if isinstance(child, plt.Annotation):
            child.remove()
    height = np.round(ba.get_height(), 3)
    str_height = str(height)
    if height < 1:
        str_height = str(height*100)+'%'
    ax.annotate(str_height.replace('[', '').replace(']', ''),
                xy=(ba.get_x() + ba.get_width()/2, 0),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha='center', va='bottom')

# Create figure and axes
fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(nrows=3, ncols=2)
y = np.arange(100000)

# Initial values
A = 27000
b = 180000
c = 0.8
t = 0.2

h = 180000
k = 0.34
Ms = 8000
P = 1

# Draw initial lines
lIS, = ax3.plot(IS(), color='cornflowerblue')
lLM, = ax3.plot(LM(), color='mediumseagreen')

lAE, = ax1.plot(AE(), color='cornflowerblue')
ax1.plot(y, y, color='gray')

lMD, = ax4.plot(MD(), color='mediumseagreen')
lineMs = ax4.axvline(Ms/P, color='orange')

filt = (AD() < 5) & (AD() > 0)
lAD, = ax5.plot(y[filt], AD()[filt], color='tomato')
lP = ax5.axhline(P, color='orange')

# Draw initial bars
bi, = ax6.bar(0, i_eq(), color='mediumseagreen')

ax7 = ax6.twinx()
by, = ax7.bar(1, y_eq(), color='cornflowerblue')

# Horizontal and vertical equilibrium  lines
liney1 = ax1.axvline(y_eq(), linestyle='--', color='dimgray')
liney3 = ax3.axvline(y_eq(), linestyle='--', color='dimgray')
liney5 = ax5.axvline(y_eq(), linestyle='--', color='dimgray')
linei3 = ax3.axhline(i_eq(), linestyle='-.', color='dimgray')
linei4 = ax4.axhline(i_eq(), linestyle='-.', color='dimgray')
linei6 = ax6.axhline(i_eq(), linestyle='-', color='firebrick', xmin=0.047, xmax=0.447)
liney7 = ax7.axhline(y_eq(), linestyle='-', color='firebrick', xmin=0.554, xmax=0.952)

lines = [liney1, liney3, liney5, linei3, linei4]

# Add sliders axes
sliders_axes = []
for i in range(8):
    sliders_axes.append(plt.axes([0.55, 0.85 - i*0.24/8, 0.32, 0.25/8]))

# Function to update graph every time a slider is changed
def update(val):
    global A, b, c, t, h, k, Ms, P
    A  = sA.val
    b  = sb.val
    c  = sc.val
    t  = st.val
    h  = sh.val
    k  = sk.val
    Ms = sM.val
    P  = sP.val

    lIS.set_ydata(IS())
    lLM.set_ydata(LM())

    lMD.set_ydata(MD())
    lineMs.set_xdata(Ms/P)

    lAE.set_ydata(AE())

    fil = (AD() < 5) & (AD() > 0)
    lAD.set_data(y[fil], AD()[fil])
    lP.set_ydata(P)

    liney1.set_xdata(y_eq())
    liney3.set_xdata(y_eq())
    liney5.set_xdata(y_eq())
    linei4.set_ydata(i_eq())
    linei3.set_ydata(i_eq())

    bi.set_height(i_eq())
    by.set_height(y_eq())

    labelBars(ax6, bi)
    labelBars(ax7, by)

    fig.canvas.draw_idle()


# Create sliders, set min & max values. Whenever they are changed, run function "update".
sA = Slider(sliders_axes[0], 'A', A/1.333, A*1.5, valinit=A ); sA.on_changed(update)
sb = Slider(sliders_axes[1], 'b', b/2,     b*2,   valinit=b ); sb.on_changed(update)
sc = Slider(sliders_axes[2], 'c', 0.5,     0.9,   valinit=c ); sc.on_changed(update)
st = Slider(sliders_axes[3], 't', t/2,     t*2,   valinit=t ); st.on_changed(update)
sh = Slider(sliders_axes[4], 'h', h/2,     h*2,   valinit=h ); sh.on_changed(update)
sk = Slider(sliders_axes[5], 'k', k/2,     k*2,   valinit=k ); sk.on_changed(update)
sM = Slider(sliders_axes[6], 'M', Ms/2,    Ms*2,  valinit=Ms); sM.on_changed(update)
sP = Slider(sliders_axes[7], 'P', P/2,     P*2,   valinit=P ); sP.on_changed(update)
sliders = [sA, sb, sc, st, sh, sk, sM, sP]

# Reset function and button
def reset(event):
    for slider in sliders:
        slider.reset()
resetax = plt.axes([0.67, 0.91, 0.1, 0.04])
button = Button(resetax, 'Reset', hovercolor='0.9')
button.on_clicked(reset)

# Toggle Equilibrium Lines button
def toggleLines(event):
    for line in lines:
        line.set_visible(not line.get_visible())
    plt.show()
toggleLines_ax = plt.axes([0.15, 0.91, 0.3, 0.04])
toggleLinesButton = Button(toggleLines_ax, 'On/Off Equilibrium Lines')
toggleLinesButton.on_clicked(toggleLines)

# Formatting
plt.subplots_adjust(hspace=0.05, wspace=0.05, left=0.1, bottom=0.1)
ymax = 100000
imax = 0.1

# ax1
ax1.set_ylabel('AE')
ax1.set_xticks([])
ax1.set_yticks([1/5*ymax, 2/5*ymax, 3/5*ymax, 4/5*ymax, 5/5*ymax])
ax1.set_yticks([1/5*ymax, 2/5*ymax, 3/5*ymax, 4/5*ymax, 5/5*ymax])
ax1.set_xlim(0, ymax)
ax1.set_ylim(0, ymax)

# ax2
ax2.axis('off')

# ax3
ax3.set_ylabel('i')
ax3.set_xticks([])
ax3.set_yticks(np.arange(0, imax+0.02, 0.025))
ax3.set_yticklabels(['{:,.1%}'.format(x) for x in ax3.get_yticks()])
ax3.set_xlim(0, ymax)
ax3.set_ylim(-0.01, imax+0.01)

# ax4
ax4.set_xlabel('M')
ax4.set_xlim(0, Ms*3)
ax4.set_ylim(-0.01, imax+0.01)
ax4.set_yticks(ax3.get_yticks())
ax4.set_yticklabels(ax3.get_yticklabels())
ax4.yaxis.tick_right()

# ax5
ax5.set_xlabel('y')
ax5.set_ylabel('P')
ax5.set_xlim(0, ymax)
ax5.set_ylim(0.4, 2.2)
ax7.set_yticks(np.arange(0, ymax, 10000))

# ax6
ax6.set_ylim(0, imax)
ax6.set_yticks([])
ax6.set_xticks([0, 1])
ax6.set_xticklabels(['i', 'y'])
ax6.set(frame_on=False, anchor='S')
bounds = ax6.get_position().bounds
newpos = [bounds[0], bounds[1], bounds[2], bounds[3]-0.05]
ax6.set_position(newpos)
# ax6.axis('off')

# ax7
ax7.set_ylim(0, ymax)
ax7.axis('off')

labelBars(ax6, bi)
labelBars(ax7, by)

figman = plt.get_current_fig_manager()
figman.resize(1200, 650)
figman.set_window_title('IS-LM: Aggregate Demand')
plt.show()


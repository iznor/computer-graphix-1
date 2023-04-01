# Submitted by:
# Dan Omid - 208787689
# Ido Dor - 204558241

import math
import tkinter as tk

curveLines = 4

# Set up colors
black = "#000000"
white = "#FFFFFF"
yellow = "#EEEE3B"
red = "#F52526"
green = "#35B050"
brown = "#8B4513"
blue = "#425D96"
orange = "#E67E37"

# Set up the input for curve lines:
def get_input():
    global curveLines
    user_input = entry.get()
    try:
        curveLines = int(user_input)
        #root.destroy()
    except ValueError:
        label.config(text="Please enter a valid integer value")
# create the GUI window
root = tk.Tk()
root.geometry("300x100")
root.title("User Input")
# create a label to display instructions
label = tk.Label(root, text="Input number of lines for 'Curve':")
label.pack()

# create an entry widget for the user input
entry = tk.Entry(root)
entry.pack()

# create a button to submit the input
button = tk.Button(root, text="Submit", command=get_input)
button.pack()

# Set up the window to be a fullscreen
window = tk.Tk()
window.title("Shapes by Ido and Dan")
screen_width = window.winfo_screenwidth() / 2
screen_height = window.winfo_screenheight()

# Set up the canvas
canvas = tk.Canvas(window, width=screen_width, height=screen_height, bg="white")
canvas.pack(fill="both", expand=True)

# Set up variables for the mouse press
count = 0

# init control points
control_x1 = 0
control_y1 = 0
control_x2 = 0
control_y2 = 0

# Short diagonal end points
end_point_short_x_1 = 0
end_point_short_y_1 = 0
end_point_short_x_2 = 0
end_point_short_y_2 = 0

# Middle points
mid_point_long_x = 0
mid_point_long_y = 0

# init curve points
curve_x1 = 0
curve_y1 = 0
curve_x2 = 0
curve_y2 = 0

# curve points to be calculated as the middle of each of the 4 rhombus outlines (4 points total)
curve_points = [(control_x1, control_y1), (curve_x1, curve_y1), (curve_x2, curve_y2), (control_x1, control_y2)]

def line_length(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    distance = math.sqrt(dx * dx + dy * dy)
    return distance


def calculateMiddle(x1, y1, x2, y2):
    x3 = (x1 + x2) / 2
    y3 = (y1 + y2) / 2
    return x3, y3


def plotCirclePoints(x, y, color):
    global mid_point_long_x, mid_point_long_y

    canvas.create_rectangle(mid_point_long_x + x, mid_point_long_y + y, mid_point_long_x + x + 1,
                            mid_point_long_y + y + 1, fill=color, outline=color)

    canvas.create_rectangle(mid_point_long_x - x, mid_point_long_y + y, mid_point_long_x - x + 1,
                            mid_point_long_y + y + 1, fill=color, outline=color)

    canvas.create_rectangle(mid_point_long_x + x, mid_point_long_y - y, mid_point_long_x + x + 1,
                            mid_point_long_y - y + 1, fill=color, outline=color)

    canvas.create_rectangle(mid_point_long_x - x, mid_point_long_y - y, mid_point_long_x - x + 1,
                            mid_point_long_y - y + 1, fill=color, outline=color)

    canvas.create_rectangle(mid_point_long_x + y, mid_point_long_y + x, mid_point_long_x + y + 1,
                            mid_point_long_y + x + 1, fill=color, outline=color)

    canvas.create_rectangle(mid_point_long_x - y, mid_point_long_y + x, mid_point_long_x - y + 1,
                            mid_point_long_y + x + 1, fill=color, outline=color)

    canvas.create_rectangle(mid_point_long_x + y, mid_point_long_y - x, mid_point_long_x + y + 1,
                            mid_point_long_y - x + 1, fill=color, outline=color)

    canvas.create_rectangle(mid_point_long_x - y, mid_point_long_y - x, mid_point_long_x - y + 1,
                            mid_point_long_y - x + 1, fill=color, outline=color)


# Define the DDA algorithm function for creating a line by using 2 points
def dda(x1, y1, x2, y2, color):
    # Calculate the differences in x and y
    dx = x2 - x1
    dy = y2 - y1

    # Determine the number of steps needed for the line
    steps = abs(dx) if abs(dx) > abs(dy) else abs(dy)

    # Calculate the x and y increments for each step
    if steps == 0: steps += 1
    x_inc = dx / steps
    y_inc = dy / steps

    # Draw each pixel in the line using a loop
    x, y = x1, y1
    for i in range(int(steps)):
        canvas.create_rectangle(x, y, x + 1, y + 1, fill=color, outline=color)
        x += x_inc
        y += y_inc


# Calculate Bersenheim's value
def GetBersenheimVal(x1, x2, x3, x4, t):
    ax = -x1 + 3 * x2 - 3 * x3 + x4
    bx = 3 * x1 - 6 * x2 + 3 * x3
    cx = -3 * x1 + 3 * x2
    dx = x1
    res = ax * t ** 3 + bx * t ** 2 + cx * t + dx
    return round(res)


# Use the calculated curve points to draw the curve
def MyCurve(color):
    global control_x1, control_y1, end_point_short_x_1, end_point_short_y_1, end_point_short_x_2, end_point_short_y_2, \
        control_x2, control_y2, curveLines

    xt1 = control_x1
    yt1 = control_y1
    curve = curveLines

    for t in range(0, curve + 1):
        pointx = GetBersenheimVal(control_x1, end_point_short_x_1, end_point_short_x_2, control_x2, t / curve)
        pointy = GetBersenheimVal(control_y1, end_point_short_y_1, end_point_short_y_2, control_y2, t / curve)
        dda(xt1, yt1, pointx, pointy, color)
        xt1 = pointx
        yt1 = pointy
    return


# Function for drawing a polygon and other lines
def MyLine(distance, rhombus_color, diagonals_color):
    global control_x1, control_y1, control_x2, control_y2, mid_point_long_x, mid_point_long_y, end_point_short_x_1, \
        end_point_short_y_1, end_point_short_x_2, end_point_short_y_2

    # Calculate the length of the long / short diagonal
    long_diagonal = distance
    short_diagonal = (long_diagonal / 3) * 2

    # Calculate the coordinates of the middle point of the long diagonal
    mid_point_long_x, mid_point_long_y = calculateMiddle(control_x1, control_y1, control_x2, control_y2)


    # Calculate the angle between the two diagonals
    dx = control_x2 - control_x1
    dy = control_y2 - control_y1
    angle = math.atan2(dy, dx)
    angle_short = angle + math.pi / 2

    # Calculate the coordinates of the endpoints of the short diagonal
    dx_short = math.cos(angle_short) * short_diagonal / 2
    dy_short = math.sin(angle_short) * short_diagonal / 2
    end_point_short_x_1 = mid_point_long_x + dx_short
    end_point_short_y_1 = mid_point_long_y + dy_short
    end_point_short_x_2 = mid_point_long_x - dx_short
    end_point_short_y_2 = mid_point_long_y - dy_short


    # Drawing the long diagonal line
    dda(control_x1, control_y1, control_x2, control_y2, diagonals_color)

    # Drawing the short diagonal line by 2 dda calls
    dda(end_point_short_x_1, end_point_short_y_1, mid_point_long_x, mid_point_long_y, diagonals_color)
    dda(end_point_short_x_2, end_point_short_y_2, mid_point_long_x, mid_point_long_y, diagonals_color)

    # Drawing the full rhombus by 4 dda calls
    dda(end_point_short_x_1, end_point_short_y_1, control_x1, control_y1, rhombus_color)
    dda(end_point_short_x_2, end_point_short_y_2, control_x1, control_y1, rhombus_color)
    dda(end_point_short_x_1, end_point_short_y_1, control_x2, control_y2, rhombus_color)
    dda(end_point_short_x_2, end_point_short_y_2, control_x2, control_y2, rhombus_color)


def inner_circle(m_x, m_y, x_a, y, color):
    x = 0
    radius = line_length(m_x, m_y, x_a, y)
    y = radius
    p = 3 - (2 * radius)
    while x <= y:
        plotCirclePoints(x, y, color)
        if p < 0:
            p = p + 4 * x + 6
        else:
            plotCirclePoints(x + 1, y, color)
            p = p + 4 * (x - y) + 10
            y -= 1
        x = x + 1


def outer_circle(m_x, m_y, x_a, y, color):
    x = 0
    radius = line_length(m_x, m_y, x_a, y)
    y = radius
    p = 3 - (2 * radius)
    while x <= y:
        plotCirclePoints(x, y, color)
        if p < 0:
            p = p + 4 * x + 6
        else:
            plotCirclePoints(x + 1, y, color)
            p = p + 4 * (x - y) + 10
            y -= 1
        x = x + 1


# A function for drawing 2 braes circles
def MyCircle(inner_color, outer_color):
    global end_point_short_x_1, end_point_short_y_1, mid_point_long_x, mid_point_long_y, control_x1, control_y1
    inner_circle(mid_point_long_x, mid_point_long_y, end_point_short_x_1, end_point_short_y_1, inner_color)
    outer_circle(mid_point_long_x, mid_point_long_y, control_x1, control_y1, outer_color)


# Event handler for pressing a mouse and activate function
def mouse_pressed(event):
    global control_x1, control_y1, control_x2, control_y2, count
    if count == 0:
        control_x1 = event.x
        control_y1 = event.y
        count += 1
    else:
        control_x2 = event.x
        control_y2 = event.y
        count = 0
        distance = line_length(control_x1, control_y1, control_x2, control_y2)

        # Create the rhombus and diagonals
        MyLine(distance, blue, orange)

        # Create the circle
        MyCircle(green, red)

        # Create the curve
        MyCurve(black)


# Binding the mouse key to the program
canvas.bind("<Button-1>", mouse_pressed)

# Run the window
window.mainloop()

# run the GUI window
root.mainloop()

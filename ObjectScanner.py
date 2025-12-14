#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
brain_inertial = Inertial()
motor_5 = Motor(Ports.PORT5, False)
distance_6 = Distance(Ports.PORT6)
optical_1 = Optical(Ports.PORT1)



# generating and setting random seed
def initializeRandomSeed():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    systemTime = brain.timer.system() * 100
    urandom.seed(int(xaxis + yaxis + zaxis + systemTime)) 
    
# Initialize random seed 
initializeRandomSeed()


# Color to String Helper
def convert_color_to_string(col):
    if col == Color.RED:
        return "red"
    if col == Color.GREEN:
        return "green"
    if col == Color.BLUE:
        return "blue"
    if col == Color.WHITE:
        return "white"
    if col == Color.YELLOW:
        return "yellow"
    if col == Color.ORANGE:
        return "orange"
    if col == Color.PURPLE:
        return "purple"
    if col == Color.CYAN:
        return "cyan"
    if col == Color.RED_VIOLET:
        return "red_violet"
    if col == Color.VIOLET:
        return "violet"
    if col == Color.BLUE_VIOLET:
        return "blue_violet"
    if col == Color.BLUE_GREEN:
        return "blue_green"
    if col == Color.YELLOW_GREEN:
        return "yellow_green"
    if col == Color.YELLOW_ORANGE:
        return "yellow_orange"
    if col == Color.RED_ORANGE:
        return "red_orange"
    if col == Color.BLACK:
        return "black"
    if col == Color.TRANSPARENT:
        return "transparent"
    return ""

#endregion VEXcode Generated Robot Configuration

screen_precision = 0
console_precision = 0
screen_width = 160 #x-y units
screen_height = 108
theta = 18 # number in degrees
arm_radius = 127 # mm
myVariable = 0
i = 0
distance_vals = [0 for x in range(20)]
angle_dist_record = [0 for x in range(20)] # in rads for trig funcs
lens = [0 for x in range(20)]
color_vals = [0 for x in range(20)]
rect_coords = [0 for x in range(20)]
corrected_coords = [0 for x in range(20)]
scaled_coords = []
old_min_x, old_max_x, old_min_y, old_max_y = (1000, -1000, 1000, -1000)

def avg(vals):
    retSum = 0
    for i in vals:
        retSum += i
    return retSum/len(vals)

def convert_hue_to_color():
    global avg_color, color_vals
    avg_color = avg(color_vals)
    # hue_normal = avg_color / 60 # convert to color parts
    if (avg_color > 300 or avg_color < 30):
        return Color.RED
    if (avg_color > 30 and avg_color < 75):
        return Color.YELLOW
    if (avg_color > 75 and avg_color < 140):
        return Color.GREEN
    if (avg_color > 140 and avg_color < 210):
        return Color.CYAN
    if (avg_color > 210 and avg_color < 300):
        return Color.BLUE

def subtractive_coords():
    global lens, distance_vals, arm_radius
    for x in range(len(distance_vals)):
        lens[x] = arm_radius - distance_vals[x]

def polar_rect_coord_conv():
    global lens, theta, rect_coords, angle_dist_record, corrected_coords, scaled_coords, old_min_x, old_max_x, old_min_y, old_max_y
    # polar to rectangular conversion
    for i in range(len(lens)):
        rect_coords[i] = ((lens[i] * math.cos(angle_dist_record[i])), (lens[i] * math.sin(angle_dist_record[i])))
    # calculate centroid
    x_avg = 0
    y_avg = 0
    for i in range(len(rect_coords)):
        x_avg = x_avg + rect_coords[i][0]
        y_avg = y_avg + rect_coords[i][1]
    x_avg = x_avg / len(rect_coords)
    y_avg = y_avg / len(rect_coords)
    # data_print([x_avg, y_avg], 5)

    # align centroid with screen center
    for i in range(len(corrected_coords)):
        corrected_coords[i] = (rect_coords[i][0] - x_avg + (screen_width/2), rect_coords[i][1] - y_avg + (screen_height/2))
    
    old_min_x, old_max_x, old_min_y, old_max_y = (1000, -1000, 1000, -1000)
    for j in range(len(corrected_coords)):
        if corrected_coords[j][0] < old_min_x:
            old_min_x = corrected_coords[j][0]
        if corrected_coords[j][0] > old_max_x:
            old_max_x = corrected_coords[j][0]
        if corrected_coords[j][1] < old_min_y:
            old_min_y = corrected_coords[j][1]
        if corrected_coords[j][1] > old_max_y:
            old_max_y = corrected_coords[j][1]
    new_min_x = 0
    new_max_x = 160
    new_min_y = 0
    new_max_y = 108

    old_range_x = old_max_x - old_min_x
    old_range_y = old_max_y - old_min_y
    new_range_x = 160
    new_range_y = 108

    scale_factor_x = new_range_x / old_range_x
    scale_factor_y = new_range_y / old_range_y
    # data_print([scale_factor_x, scale_factor_y], 5)
    uniform_scale = min(scale_factor_x, scale_factor_y)

    for x, y in corrected_coords:
        # new_x = 0
        # new_y = 0
        if old_range_x == 0 or old_range_y == 0:
            new_x = (new_min_x + new_max_x)/2
            new_y = (new_min_y + new_max_y)/2
        else:
            new_x = ((x - old_min_x) * uniform_scale) + new_min_x
            new_y = ((y - old_min_y) * uniform_scale) + new_min_y
            # data_print(scaled_coords)
        scaled_coords.append((new_x, new_y))
    # data_print(scaled_coords, 5)
    
def print_shape():
    global scaled_coords
    # data_print(scaled_coords, 5)
    avg_color = avg(color_vals)
    obj_color = convert_hue_to_color()
    brain.screen.set_pen_width(3)
    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.clear_screen()
    for x in range(len(scaled_coords)):
        if x == len(scaled_coords) - 1:
            brain.screen.draw_line(scaled_coords[x][0], scaled_coords[x][1], scaled_coords[0][0], scaled_coords[0][1])
        else:
            brain.screen.draw_line(scaled_coords[x][0], scaled_coords[x][1], scaled_coords[x+1][0], scaled_coords[x+1][1])
    scanline_poly_fill(scaled_coords, obj_color)
    timer(5)
    brain.screen.set_pen_width(1)
    blank_screen()

def blank_screen():
    brain.screen.set_pen_color(Color.BLACK)
    for i in range(screen_width):
        for j in range(screen_height):
            brain.screen.draw_pixel(i, j)
    brain.screen.set_pen_color(Color.WHITE)

def scanline_poly_fill(points, color):
    if not points:
        return
    min_y = int(min(p[1] for p in points))
    max_y = int(max(p[1] for p in points))
    closed_points = points + [points[0]]
    for y in range(min_y, max_y + 1):
        intersections = []
        for i in range(len(points)):
            p1 = closed_points[i]
            p2 = closed_points[i+1]
            y1, y2 = p1[1], p2[1]
            x1, x2 = p1[0], p2[0]
            if (y1 <= y < y2) or (y2 <= y < y1):
                if y1 != y2:
                    x_intersect = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                    intersections.append(int(round(x_intersect)))
        intersections.sort()
        brain.screen.set_pen_color(color)
        for i in range(0, len(intersections) - 1, 2):
            x_start = intersections[i]
            x_end = intersections[i+1]
            brain.screen.draw_line(x_start, y, x_end, y)
    brain.screen.set_pen_color(Color.WHITE)

def data_print(list_of_data, timer_len):
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    if any(isinstance(item, tuple) for item in list_of_data):
        for tuple_item in list_of_data:
            if brain.screen.row() == 5:
                timer(timer_len)
                brain.screen.clear_screen()
                brain.screen.set_cursor(1,1)
            brain.screen.print(tuple_item)
            brain.screen.next_row()
    else:
        brain.screen.print(list_of_data)
        brain.screen.next_row()
        timer(timer_len)
    brain.screen.print("Please wait...")
    brain.screen.next_row()
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)

def timer(timer_len):
    brain.timer.clear()
    for count in range(timer_len):
        brain.screen.clear_row(5)
        brain.screen.set_cursor(5,1)
        brain.screen.print(str(math.ceil(timer_len - brain.timer.time(SECONDS))) + "(s)")
        brain.screen.set_cursor(5, 8)
        brain.screen.print("(>) Exit")
        wait(1, SECONDS)
        brain.screen.set_cursor(5, 1)
        if (brain.buttonRight.pressing()):
            break

def menu():
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    brain.screen.print("(<) Return Arm Pos")
    brain.screen.next_row()
    brain.screen.print("(>) Run Program")

def wait_screen():
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    brain.screen.print("Scanning...")
    brain.screen.next_row()
    brain.screen.print("Please wait")

def test():
    global screen_precision, console_precision, screen_width, screen_height, theta, arm_radius, myVariable, i, distance_vals, angle_dist_record, lens, color_vals, rect_coords, corrected_coords, scaled_coords
    init_arm_pos = motor_5.position(DEGREES)
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    menu()
    while True:
        if brain.buttonLeft.pressing():
            if motor_5.position(DEGREES) != init_arm_pos:
                motor_5.spin_to_position(init_arm_pos, DEGREES)
            menu()
        if brain.buttonRight.pressing():
            wait_screen()
            if motor_5.position(DEGREES) != init_arm_pos:
                motor_5.spin_to_position(init_arm_pos, DEGREES)
            distance_vals = [0 for x in range(20)]
            angle_dist_record = [0 for x in range(20)] # in rads for trig funcs
            lens = [0 for x in range(20)]
            color_vals = [0 for x in range(20)]
            rect_coords = [0 for x in range(20)]
            corrected_coords = [0 for x in range(20)]
            scaled_coords = []
            distance_vals = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            angle_dist_record = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            color_vals = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            lens = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


            avg_color = optical_1.hue()
            i = 0
            for repeat_count in range(int(len(color_vals))):
                optical_1.set_light_power(150,PERCENT)
                optical_1.set_light(LedStateType.ON)
                motor_5.spin_for(FORWARD, theta, DEGREES)
                distance_vals[i] = distance_6.object_distance(MM)
                color_vals[i] = optical_1.hue()
                angle_dist_record[i] = motor_5.position(DEGREES) * (math.pi / 180) # radian conversion
                i += 1
                wait(20, MSEC)
            i = 0
            subtractive_coords()
            polar_rect_coord_conv()
            print_shape()
            menu()
            
        wait(20, MSEC)

def spin_program():
    pass

def when_started1():
    test()

when_started1()

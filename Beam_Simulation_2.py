import math
import turtle
from copy import deepcopy




#Swaps two values with each other
def swap(a, b):
    temp = b
    b = a
    a = temp

    return a, b

#Checks if the values in the passed list fall within the length
def check_within_bound(loc, length):
    for l in loc:
        if (l < 0) or (l > length):
            print("Locations should be within beam length")
            return True

    return False

#Checks if the values in the passed list are equal to each other
def check_equal(loc):
    if len(loc) > 1:
        if loc[0] == loc[1]:
            print("Location values can't be equal")
            return True

    return False

#Checks the inputs to the beam list. Returns False in case the inputs are wrong
def verify_beam(beam):
    if beam[0] != 's' and beam[0] != 'o' and beam[0] != 'c':
        print("Please enter the correct type")
        return beam, False
    
    if check_number(beam[1]) or check_number(beam[2][0]) or check_number(beam[2][1]):
        return beam, False

    beam[1] = float(beam[1])
    beam[2][0] = float(beam[2][0])
    beam[2][1] = float(beam[2][1])

    if beam[1] <= 0:
        print("Beam length should be greater than 0")
        return beam, False

    if check_within_bound(beam[2], beam[1]):
        return beam, False

    if check_equal(beam[2]):
        return beam, False

    if beam[2][0] > beam[2][1]:
        beam[2][0], beam[2][1] = swap(beam[2][0], beam[2][1])

    return beam, True

#Function for taking inputs for beam from the user
def input_beam():
    valid = False

    while not valid:
        beam = []
        beam.append(input("Enter beam type (s = Simply Supported, o = Overhanging, c = Cantilever): "))

        beam.append(input("Enter beam length in m: "))

        if (beam[0] == "s"):
            beam.append([0, beam[1]])

        elif (beam[0] == "o"):
            beam.append([])
            beam[2].append(input("Enter support location 1 in m: "))
            beam[2].append(input("Enter support location 2 in m: "))

        if (beam[0] == "c"):
            beam.append([0, beam[1]])

        beam, valid = verify_beam(beam)
        print("\n")

    return beam

#Verifies the values in the load list. Returns False in case the values are not valid
def verify_load(load, length):
    if load[0] != 'p' and load[0] != 'd' and load[0] != 'm':
        print("Please enter the correct type")
        return load, False

    for j in range(len(load[1:])):
        for i in range(len(load[j+1])):
            if check_number(load[j+1][i]):
                return load, False
            load[j+1][i] = float(load[j+1][i])

    if check_within_bound(load[1], length):
        return load, False

    if check_equal(load[1]):
        return load, False

    if len(load[1]) == 2:
        if load[1][0] > load[1][1]:
            print("Force start location can't be greater than end location")
            return load, False

        if (load[2][0] > 0 and load[2][1] < 0) or (load[2][0] < 0 and load[2][1] > 0):
            print("Force values should same sign")
            return load, False

    return load, True

#Function for allowing user to input parameters for the load the list
def input_load(beam):
    valid = False
    load = []

    while not valid:
        load.append([])

        load[-1].append(input("Enter load type (p = Point Load, d = distributed, m = Moment): "))

        if (load[-1][0] == "p"):
            load[-1].append([input("Enter force location in m: ")])
            load[-1].append([input("Enter force value in kN (+ for upwards and - for downwards): ")])

        elif (load[-1][0] == "d"):
            load[-1].append([input("Enter force start location in m: "), input("Enter force end location in m: ")])
            load[-1].append([input("Enter force start value in kN/m (+ for upwards and - for downwards): "), input("Enter force end value in kN/m (+ for upwards and - for downwards): ")])

        if (load[-1][0] == "m"):
            load[-1].append([input("Enter force location in m: ")])
            load[-1].append([input("Enter force value in kN.m (+ for anticlockwise and - for clockwise): ")])

        #valid = True
        load[-1], valid = verify_load(load[-1], beam[1])

        choice = ""
        while choice != "y" and choice != "n":
            choice = input("Enter anoher load?(y/n): ")

        if not valid:
            load.pop()

        if choice == "y":
            valid = False
        print("\n")

    return load

#Checks if the passed string is a number or not
def check_number(string):
    try:
        float(str(string).lstrip("+-"))
        return False
    except ValueError:
        print("Input values should be numbers")
        return True

#Generates the beam list from input file
def generate_beam_from_file(file):
    lines = file.readlines()

    for i in lines:
        if i[:3] == "_B_":
            beam = i[3:].split("_")
            break

    beam[-1] = beam[-1][:len(beam[-1])-1]

    if beam[0] != "o":
        beam.append([0, beam[1]])

    elif beam[0] == "o":
        beam[2] = [beam[2], beam[3]]
        beam.pop()
    
    beam, valid = verify_beam(beam)

    return beam, valid

#Generates load list from imput file
def generate_load_from_file(file, beam):
    lines = file.readlines()
    load = []
    
    for i in lines:
        if i[:3] == "_L_":
            load.append(i[3:].split("_"))
            load[-1][-1] = load[-1][-1][:len(load[-1][-1])-1]
            
            if load[-1][0] != "d":
                load[-1][1] = [load[-1][1]]
                load[-1][2] = [load[-1][2]]

            elif load[-1][0] == "d":
                load[-1][1] = [load[-1][1], load[-1][2]]
                load[-1][2] = [load[-1][3], load[-1][4]]
                load[-1].pop()
                load[-1].pop()

            load[-1], valid = verify_load(load[-1], beam[1])
                
            if not valid:
                break

    return load, valid

#Function for reading the file and selecting lines that contain beam and load data.
def read_file(filename):
    file = open(filename, "r")
    beam, valid1 = generate_beam_from_file(file)
    file.close()

    file = open(filename, "r")
    load, valid2 = generate_load_from_file(file, beam)
    file.close()

    return beam, load, (valid1 and valid2)

#Saves user input to a file Output.txt
def save(beam, load):
    file = open("Output.txt", "w")
    file.write("Line should start with _x_ where x is either B for Beam and L for Load. This must be followed by parameters each separated by _.\n")
    file.write("For what parameters are required, run the program in realtime mode. All of the required parameters are requested by the program.\n")
    file.write("The order of the parameters must be the same as that required by the program for that particular beam type of load type!")

    s = "\n_B"
    for i in range(len(beam)):
        if i != 2:
            s = s + "_" + str(beam[i])

        elif beam[0] != "o":
            break

        else:
            for j in range(len(beam[i])):
                s = s + "_" + str(beam[i][j])

    file.write(s)

    for i in range(len(load)):
        s = "\n_L"
        for j in range(len(load[i])):
            if j == 0:
                s = s + "_" + str(load[i][j])

            else:
                for k in range(len(load[i][j])):
                    s = s + "_" + str(load[i][j][k])

        file.write(s)

    file.close()

#Checks which loads are being applied for being considered to be x m long. Converts the distributed loads into point forces.
#Returns a list containing of only point loads and moments acting within x m span of the beam
def evaluate_loading(x, load):
    loading = []

    for l in load:
        if l[1][0] <= x:
            if l[0] != "d":
                loading.append(deepcopy(l))

            elif l[0] == "d":
                dist = deepcopy(l)
                max_x = dist[1][1]

                if dist[1][1] > x:
                    max_x = x
                    dist[2][1] = dist[2][0] + ((dist[2][1] - dist[2][0]) * (x - dist[1][0]) / (dist[1][1] - dist[1][0]))
                    dist[1][1] = x

                if dist[2][0] != 0 and dist[2][1] != 0:
                    if dist[2][1] < dist[2][0]:
                        loading.append(["p", [dist[1][0] + (max_x - dist[1][0])/2], [(dist[2][0]) * (max_x - dist[1][0])]])
                        loading.append(["p", [dist[1][0] + (max_x - dist[1][0])*2/3], [(dist[2][1] - dist[2][0]) * (max_x - dist[1][0]) / 2]])

                    elif dist[2][1] > dist[2][0]:
                        loading.append(["p", [dist[1][0] + (max_x - dist[1][0])/2], [(dist[2][1]) * (max_x - dist[1][0])]])
                        loading.append(["p", [dist[1][0] + (max_x - dist[1][0])/3], [(dist[2][0] - dist[2][1]) * (max_x - dist[1][0]) / 2]])

                    else:
                        loading.append(["p", [dist[1][0] + (max_x - dist[1][0])/2], [(dist[2][1]) * (max_x - dist[1][0])]])

                else:
                    if dist[2][1] < dist[2][0]:
                        loading.append(["p", [dist[1][0] + (max_x - dist[1][0])*2/3], [(dist[2][1] - dist[2][0]) * (max_x - dist[1][0]) / 2]])

                    elif dist[2][1] > dist[2][0]:
                        loading.append(["p", [dist[1][0] + (max_x - dist[1][0])/3], [(dist[2][0] - dist[2][1]) * (max_x - dist[1][0]) / 2]])

                    else:
                        loading.append(["p", [dist[1][0] + (max_x - dist[1][0])/2], [(dist[2][1]) * (max_x - dist[1][0])]])

    return loading

#Calculates the reactions of the supports for the loading case. 
def calc_reactions(beam, load):
    loading = evaluate_loading(beam[1], load)

    sum_force = 0
    sum_force_dist = 0
    sum_moment = 0

    for l in loading:
        if l[0] != "m":
            sum_force += l[2][0]
            sum_force_dist += (l[2][0] * (l[1][0] - beam[2][0]))

        elif l[0] == "m":
            sum_moment += l[2][0]

    if beam[0] != "c":
        B = - (sum_force_dist + sum_moment)/(beam[2][1] - beam[2][0])
        A = - (sum_force + B)

        reactions = [["p", [beam[2][0]], [A]], ["p", [beam[2][1]], [B]]]

    elif beam[0] == "c":
        B = - (sum_force)
        A = - (sum_force_dist + sum_moment + B*(beam[2][1] - beam[2][0]))

        reactions = [["m", [beam[2][1]], [A]], ["p", [beam[2][1]], [B]]]

    return reactions

#Calculates the shear force and bending moment for x m span of the beam
def calculate(x, beam, load, reactions):
    loading = deepcopy(load)

    for i in reactions:
        loading.append(i)

    loading = evaluate_loading(x, loading)

    sum_force = 0
    sum_force_dist = 0
    sum_moment = 0

    for l in loading:
        if l[0] != "m":
            sum_force += l[2][0]
            sum_force_dist += (l[2][0] * (x - l[1][0]))

        elif l[0] == "m":
            sum_moment += l[2][0]

    shear = sum_force
    bending = sum_force_dist - sum_moment

    return shear, bending

#Generates the x, shear force and bending moment lists for plotting
def generate_shear_bending(beam, load, reactions, steps):
    x = []
    shear = []
    bending = []
    n = math.floor(beam[1]/steps)

    for i in range(n+1):
        x.append(i*steps)
    
        s, b = calculate(x[-1], beam, load, reactions)
    
        shear.append(round(s,5))
        bending.append(round(b,5))

    return x, shear, bending

#Sets up the turtle window and Turtle. Also creates two horizontal lines to separate the screen.
def setup_turtle(window_size, pen_width):
    turtle.TurtleScreen._RUNNING=True
    wn = turtle.Screen()
    wn.setup(window_size[0], window_size[1])
    wn.bgcolor("white")
    wn.title("Shear and Bending Simulation")

    pen = turtle.Turtle()
    wn.tracer(0,0)
    pen.width(pen_width)

    draw_line(pen, [-window_size[0]/2, window_size[1]/6], [window_size[0]/2, window_size[1]/6])
    draw_line(pen, [-window_size[0]/2, -window_size[1]/6], [window_size[0]/2, -window_size[1]/6])

    pen.penup()
    pen.goto(-window_size[0]/2, window_size[1]/2)

    return pen, wn

#Draws a line between start and end point
def draw_line(pen, start, end):
    pen.penup()
    pen.goto(start[0], start[1])

    pen.pendown()
    pen.goto(end[0], end[1])

#Draws a rectangle for given top left and bottom right points
def draw_rect(pen, top_left, bot_right):
    top_right = [bot_right[0], top_left[1]]
    bot_left = [top_left[0], bot_right[1]]

    pen.penup()
    pen.goto(top_left[0], top_left[1])

    pen.pendown()
    draw_line(pen, top_left, top_right)
    draw_line(pen, top_right, bot_right)
    draw_line(pen, bot_right, bot_left)
    draw_line(pen, bot_left, top_left)

#Draws the circular symbol for moment
def draw_moment(pen, point, radius, dir, arrow_dim):
    angle = 45

    pen.penup()
    pen.goto(point[0], point[1])
    
    pen.pendown()
    pen.circle(radius, 180)

    pen.penup()
    pen.circle(radius, 180)

    if dir == 1:
        ref = [point[0], point[1] + (2 * radius)]
    else:
        ref = [point[0], point[1]]

    arrow_end = [ref[0] + ((arrow_dim[0]/2)*math.tan(angle*math.pi/180)), ref[1] + arrow_dim[0]/2]
    draw_line(pen, ref, arrow_end)

    arrow_end = [ref[0] + ((arrow_dim[0]/2)*math.tan(angle*math.pi/180)), ref[1] - arrow_dim[0]/2]
    draw_line(pen, ref, arrow_end)

#Draws an arrow to denote application of a force
def draw_arrow(pen, start, arrow_dim, dir, surf):
    angle = 45

    if surf == "top":
        end = [start[0], start[1] + (arrow_dim[1])]

    elif surf == "bot":
        end = [start[0], start[1] - (arrow_dim[1])]

    draw_line(pen, start, end)

    if surf == "top":
        if dir > 0:
            ref = end
            
        elif dir < 0:
            ref = start

    elif surf == "bot":
        if dir > 0:
            ref = start
            
        elif dir < 0:
            ref = end

    arrow_end = [ref[0] + (arrow_dim[0]/2), ref[1] - dir*((arrow_dim[0]/2)*math.tan(angle*math.pi/180))]
    draw_line(pen, ref, arrow_end)

    arrow_end = [ref[0] - (arrow_dim[0]/2), ref[1] - dir*((arrow_dim[0]/2)*math.tan(angle*math.pi/180))]
    draw_line(pen, ref, arrow_end)

#Wrties text for the select point. Also has some offset depending on if we want the text to be above the point or below
def write_text(pen, text, point, dir, text_size):
    offset = text_size

    if dir == 1:
        offset += 0
    else:
        offset = -offset - 1.5 * text_size

    pen.penup()
    pen.goto(point[0], point[1] + offset)

    pen.pendown()
    pen.write(text, align = "center", font=("Verdana", text_size, "normal"))

#Draws the complete schematic diagram of the beam along with loading
def draw_schem(pen, beam, load, reactions, max, beam_dim, arrow_dim, text_size):
    beam_top = - max[1] + (beam_dim[1]/2)
    beam_bot = - max[1] - (beam_dim[1]/2)

    #Draws the rectangle for showing beam
    draw_rect(pen, [-beam_dim[0]/2, beam_top], [beam_dim[0]/2, beam_bot])

    #Loop iterates through each load, draws its representation and value
    for l in load:
        if l[2][0] > 0:
            dir = 1
        
        else:
            dir = -1

        x = (l[1][0]*beam_dim[0]/beam[1]) + (-beam_dim[0]/2)
        y = beam_top
        
        if l[0] == "p":
            draw_arrow(pen, [x, y], arrow_dim, dir, "top")
            write_text(pen, str(abs(round(l[2][0],3))) + " kN", [x, y + arrow_dim[1]], 1, text_size)

        elif l[0] == "d":
            n = math.floor((((l[1][1] - l[1][0]) / beam[1]) * beam_dim[0]) / (1.25*arrow_dim[0]))
            d_x = math.floor((((l[1][1] - l[1][0]) / beam[1]) * beam_dim[0]) / n)

            if abs(l[2][1]) > abs(l[2][0]):
                d_size = ((((d_x /(beam_dim[0]*(l[1][1] - l[1][0])/beam[1])) * (l[2][1] - l[2][0])) + l[2][0]))
                d_size = arrow_dim[1] * ((d_size - l[2][0])/(l[2][1]))
                y_size = arrow_dim[1] * (l[2][0])/(l[2][1])

            else:
                d_size = ((((d_x /(beam_dim[0]*(l[1][1] - l[1][0])/beam[1])) * (l[2][1] - l[2][0])) + l[2][0]))
                d_size = arrow_dim[1] * ((d_size - l[2][0])/(l[2][0]))
                y_size = arrow_dim[1]
            
            for i in range(n+1):
                draw_arrow(pen, [x + (i*d_x), y], [arrow_dim[0], y_size + (i*d_size)], dir, "top")

            if l[2][0] != 0 :
                write_text(pen, str(abs(round(l[2][0],3))) + " kN/m", [x, y + y_size], 1, text_size)
            if l[2][1] != 0 :
                write_text(pen, str(abs(round(l[2][1],3))) + " kN/m", [x + (n*d_x), y + y_size + (n*d_size)], 1, text_size)

        elif l[0] == "m":
            offset = beam_dim[1]*0.15
            draw_moment(pen, [x, beam_bot - offset], (beam_dim[1]/2) + (offset), dir, arrow_dim)

            offset *= 2
            if dir == 1:
                offset *= 1
                write_text(pen, str(abs(round(l[2][0],3))) + " kN.m", [x, beam_top + offset], 1, text_size)

            else:
                offset *= -1
                write_text(pen, str(abs(round(l[2][0],3))) + " kN.m", [x, beam_bot + offset], -1, text_size)

    #Loop iterates through each reaction, draws its representation and value
    for l in reactions:
        if l[2][0] > 0:
            dir = 1
        
        else:
            dir = -1

        x = (l[1][0]*beam_dim[0]/beam[1]) + (-beam_dim[0]/2)
        y = beam_bot
        
        if l[0] == "p":
            draw_arrow(pen, [x, y], arrow_dim, dir, "bot")
            write_text(pen, str(abs(round(l[2][0],3))) + " kN", [x, y - arrow_dim[1]], -1, text_size)

        elif l[0] == "m":
            offset = beam_dim[1]*0.15
            draw_moment(pen, [x, beam_bot - offset], (beam_dim[1]/2) + (offset), dir, arrow_dim)

            offset *= 2
            if dir == 1:
                offset *= 1
                write_text(pen, str(abs(round(l[2][0],3))) + " kN.m", [x + 4*offset, beam_top + offset], 1, text_size)

            else:
                offset *= -1
                write_text(pen, str(abs(round(l[2][0],3))) + " kN.m", [x - 4*offset, beam_bot + offset], -1, text_size)

    pen.penup()
    pen.goto(graph_dim[0]*1.4/2, - max[1] + graph_dim[1]/2)
    pen.write("Schematic", align = "right", font=("Verdana", 15, "normal"))

#Draws the tick marks on the graph. Also labels the tick marks with values
def draw_ticks(pen, start, end, max, n, tick_dim):
    delta = [(end[0] - start[0])/n, (end[1] - start[1])/n]
    
    if delta[0] == 0:
        tick_delta = [[-tick_dim/2, 0], [tick_dim/2, 0]]
    
    elif delta[1] == 0:
        tick_delta = [[0, tick_dim/2], [0, -tick_dim/2]]

    for i in range(n+1):
        point = deepcopy(start)

        point[0] += i*delta[0]
        point[1] += i*delta[1]

        draw_line(pen, [point[0] + tick_delta[0][0], point[1] + tick_delta[0][1]], [point[0] + tick_delta[1][0], point[1] + tick_delta[1][1]])

        pen.penup()
        pen.goto([point[0] + 1.5*tick_delta[0][0], point[1] + tick_delta[0][1]])

        if delta[0] == 0:
            pen.write(round((i-(n/2))*max*2/n,3), align = "right", font=("Verdana", 8, "normal"))
    
        elif delta[1] == 0 and i != 0:
            pen.write(round(i*max/n, 3), align = "center", font=("Verdana", 8, "normal"))

#Generates a list containing the locations of force application
def generate_loc(load, reactions):
    loc = []

    for i in load:
        for j in i[1]:
            loc.append(j)

    for i in reactions:
        for j in i[1]:
            loc.append(j)

    return loc

#Draws the graphs of the x and y lists
def draw_graph(x, y, pen, graph_dim, plot_width, offset, tick_dim, load, reactions):
    pen.color(0,0,0)

    draw_line(pen, [-graph_dim[0]/2, offset], [graph_dim[0]/2, offset])
    draw_line(pen, [-graph_dim[0]/2, offset + graph_dim[1]/2], [-graph_dim[0]/2, offset - graph_dim[1]/2])

    #Calculation of max values in x and y to set scale of the graph
    max_x = 0
    max_y = 0
    for i in range(len(x)):
        if abs(x[i]) > max_x:
            max_x = abs(x[i])

        if abs(y[i]) > max_y:
            max_y = abs(y[i])

    #Drawing of ticks on the graph
    n = 10
    draw_ticks(pen, [-graph_dim[0]/2, offset - graph_dim[1]/2], [-graph_dim[0]/2, offset + graph_dim[1]/2], max_y, n, tick_dim)

    n = 10
    draw_ticks(pen, [-graph_dim[0]/2, offset], [graph_dim[0]/2, offset], max_x, n, tick_dim)

    #Labeling of plots and axis
    if offset == 0:
        text = "Shear"
        y_title = "Shear (kN)"
    else:
        text = "Bending"
        y_title = "Bending (kN.m)"

    pen.penup()
    pen.goto(graph_dim[0]*1.4/2, offset + graph_dim[1]/2)
    pen.write(text, align = "right", font=("Verdana", 15, "normal"))

    pen.penup()
    pen.goto(-graph_dim[0]*1.175/2, offset)
    pen.write(y_title, align = "right", font=("Verdana", 10, "normal"))

    pen.penup()
    pen.goto(graph_dim[0]*1.45/2, offset)
    pen.write("Distance (m)", align = "right", font=("Verdana", 10, "normal"))

    #Calculation of pixel/val ratios and starting pixels for easy placement of datapoints
    x_r = graph_dim[0] / max_x
    y_r = graph_dim[1] / (2 * max_y)

    x_start = - graph_dim[0]/2
    y_start = offset

    pen.penup()
    pen.goto([x_start, y_start])
    pen.pendown()

    pen.width(plot_width)

    loc = generate_loc(load, reactions)

    #Loop for plotting each datapoints, important value pairs and maxima & minima
    for i in range(len(x)):
        pen.color(1,0,0)
        pen.pendown()
        pen.goto([x_start + (x_r * x[i]), y_start + (y_r * y[i])])

        #Plotting of important datapoints where either new load is added or old load ceases to act
        if x[i] in loc:
            if y[i] > 0:
                dir = 1
            else:
                dir = -1
            
            pen.penup()
            pen.color(0,0,1)
            write_text(pen, "[" + str(round(x[i],3)) + "," + str(round(y[i],3)) + "]", [x_start + (x_r * x[i]), y_start + (y_r * y[i])], dir, 8)

            pen.penup()
            pen.goto([x_start + (x_r * x[i]), y_start + (y_r * y[i])])
            pen.pendown()
            pen.dot(plot_width*4, (0,0,1))

        #Marking of maxima and minima
        if i > 0 and i < (len(x)-1):
            if (y[i] >= y[i-1] and y[i] > y[i+1]) or (y[i] > y[i-1] and y[i] >= y[i+1]) or (y[i] <= y[i-1] and y[i] < y[i+1]) or (y[i] < y[i-1] and y[i] <= y[i+1]):
                pen.penup()
                pen.goto([x_start + (x_r * x[i]), y_start + (y_r * y[i])])
                pen.pendown()
                pen.dot(plot_width*4, (0,1,0))

#High level function that calls all functions for graphics
def draw_graphics(x, shear, bending, pen, beam, load, reactions, max, beam_dim, arrow_dim, text_size, graph_dim, plot_width, tick_dim):
    draw_schem(pen, beam,load, reactions, max, beam_dim, arrow_dim, text_size)
    draw_graph(x, shear, pen, graph_dim, plot_width, 0, tick_dim, load, reactions)
    draw_graph(x, bending, pen, graph_dim, plot_width, max[1], tick_dim, load, reactions)
    

######################################################################################################################################################33

#Main body of the program

window_size = [800, 800]   #Sets the size of the window [width, height]
pen_width = 2   #Size of the pen for schematic and axis
plot_width = 2 #Size of the pen for lines of the graph
steps = 0.001    #Defines the step size

max = [window_size[0], window_size[1]/3] 

beam_dim = [max[0]*5/8, max[1]*1/8] #Size of the beam in schematic
arrow_dim = [beam_dim[0]/30, max[1]*1/5]    #Size of the arrow in schematic
graph_dim = [beam_dim[0], max[1]*3/4]   #Size of the graph
tick_dim = graph_dim[1]/10  #Size of the tick marks on the graph

text_size = 8   #Text size for schematic and data labels

quit = False

#Main loop that ensures continuous running unless user wants to quit
while not quit:
    #Selection of input mode
    input_mode = ""
    while input_mode != "r" and input_mode != "f":
        input_mode = input("Enter input mode: (r)ealtime or (f)ile: ")
    
    #Generation of beam and load matrices from either user input or file input
    if input_mode == "r":
        beam = input_beam()
        load = input_load(beam)
    
    elif input_mode == "f":
        valid = False
        while not valid:
            beam, load, valid = read_file("Sim_File.txt")
    
    #Option to save the input parameters
    choice = ""
    while choice != "y" and choice != "n":
        choice = input("Save beam parameters? (y/n): ")
    
    if choice == "y":
        save(beam, load)
    
    #Calculation of the reaction forces
    reactions = calc_reactions(beam, load)
    
    #Priniting of the three main lists
    print(beam)
    print(load)
    print(reactions)
    
    #Generation of x, shear and bending lists for plotting
    x, shear, bending = generate_shear_bending(beam, load, reactions, steps)

    #Setup of turtle elements
    pen, wn = setup_turtle(window_size, pen_width)

    #Drawing of graphics on turtle window
    draw_graphics(x, shear, bending, pen, beam, load, reactions, max, beam_dim, arrow_dim, text_size, graph_dim, plot_width, tick_dim)

    turtle.update()

    turtle.exitonclick()

    print("\n")

    #Option to quit program or continue
    choice = ""
    while choice != "y" and choice != "n":
        choice = input("Quit program? (y/n): ")

    if choice == "y":
        quit = True

    print("\n")
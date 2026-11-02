import random
import expyriment as xpy

#config dicttionary to eliminate magic numbers 
CONFIG = {
    "experiment_name": "Ternus Experiment",
    "screen_size": (600, 300),
    "bg_color": (0, 0, 0),
    "fg_color": (255, 255, 255),
    "circle_radius": 20,
    "shape_size": 35,
    "polygon_radius": 54,
    "frame_duration_ms": 250,
    "isi_values": [0, 50, 500, 1000],
    "trials_per_isi": 5,
    "fixation_duration_ms": 200,
    "iti_duration_ms": 500,
}

# Experiment initialization
e = xpy.design.Experiment(name=CONFIG["experiment_name"], background_colour=CONFIG["bg_color"], foreground_colour=CONFIG["fg_color"])
e.data_variable_names = ["condition", "trial", "isi_ms", "frame_ms", "response", "group_response", "key", "rt_ms"]
xpy.control.initialize(e)

def create_blank_canvas():
    """Creates a blank canvas with the specified background color."""
    return xpy.stimuli.Canvas(size=CONFIG["screen_size"], colour=CONFIG["bg_color"])

def create_fixation_cross():
    """Creates a fixation cross stimulus."""
    return xpy.stimuli.FixCross(size=(20, 20), line_width=4, colour=CONFIG["fg_color"])


# DOTS stimuli
#iteratively create the two frames of the DOTS condition using a loop to avoid repetition
canvas_dots_frame1 = create_blank_canvas()
for x_pos in (-120, -40, 40):
    xpy.stimuli.Circle(radius=CONFIG["circle_radius"], position=(x_pos, -50), colour=CONFIG["fg_color"]).plot(canvas_dots_frame1)

canvas_dots_frame2 = create_blank_canvas()
for x_pos in (-40, 40, 120):
    xpy.stimuli.Circle(radius=CONFIG["circle_radius"], position=(x_pos, -50), colour=CONFIG["fg_color"]).plot(canvas_dots_frame2)

# SHAPES stimuli
canvas_shapes_frame1 = create_blank_canvas()
xpy.stimuli.Circle(radius=CONFIG["circle_radius"], position=(-120, -50), colour=CONFIG["fg_color"]).plot(canvas_shapes_frame1)
xpy.stimuli.Shape(vertex_list=xpy.misc.geometry.vertices_regular_polygon(3, CONFIG["polygon_radius"]), position=(-40, -50), colour=CONFIG["fg_color"]).plot(canvas_shapes_frame1)
xpy.stimuli.Rectangle(size=(CONFIG["shape_size"], CONFIG["shape_size"]), position=(40, -50), colour=CONFIG["fg_color"]).plot(canvas_shapes_frame1)

canvas_shapes_frame2 = create_blank_canvas()
xpy.stimuli.Shape(vertex_list=xpy.misc.geometry.vertices_regular_polygon(3, CONFIG["polygon_radius"]), position=(-40, -50), colour=CONFIG["fg_color"]).plot(canvas_shapes_frame2)
xpy.stimuli.Rectangle(size=(CONFIG["shape_size"], CONFIG["shape_size"]), position=(40, -50), colour=CONFIG["fg_color"]).plot(canvas_shapes_frame2)
xpy.stimuli.Circle(radius=CONFIG["circle_radius"], position=(120, -50), colour=CONFIG["fg_color"]).plot(canvas_shapes_frame2)

# Fixation cross and text screens
thing1 = xpy.stimuli.FixCross(size=(20, 20), line_width=4, colour=CONFIG["fg_color"])
screen5 = xpy.stimuli.BlankScreen(colour=CONFIG["bg_color"])
thing1.plot(screen5)
text1 = xpy.stimuli.TextScreen(heading="Ternus experiment", text="Keep your eyes on the central cross.\n\nLEFT = element motion\nRIGHT = group motion\n\nPress SPACE to start.")
text2 = xpy.stimuli.TextScreen(heading="What did you see?", text="LEFT = element motion\nRIGHT = group motion")
screen6 = xpy.stimuli.BlankScreen(colour=CONFIG["bg_color"])

# Fixation on stimulus and text screens
thing1.plot(canvas_dots_frame1)
thing1.plot(canvas_dots_frame2)
thing1.plot(canvas_shapes_frame1)
thing1.plot(canvas_shapes_frame2)
thing1.plot(text1)
thing1.plot(text2)

# Preloading
canvas_dots_frame1.preload()
canvas_dots_frame2.preload()
canvas_shapes_frame1.preload()
canvas_shapes_frame2.preload()
screen5.preload()
text1.preload()
text2.preload()
screen6.preload()

# DOTS block and trial construction
b1 = xpy.design.Block(name="DOTS")
b1.set_factor("condition", "DOTS")
for v in [0, 0, 0, 0, 0, 50, 50, 50, 50, 50, 500, 500, 500, 500, 500, 1000, 1000, 1000, 1000, 1000]:
    t = xpy.design.Trial()
    t.set_factor("isi_ms", v)
    b1.add_trial(t)

# Randomization of DOTS trials
for i in range(len(b1.trials) - 1, 0, -1):
    j = random.randint(0, i)
    b1.trials[i], b1.trials[j] = b1.trials[j], b1.trials[i]

# SHAPES block and trial construction
b2 = xpy.design.Block(name="SHAPES")
b2.set_factor("condition", "SHAPES")
for v in [0, 0, 0, 0, 0, 50, 50, 50, 50, 50, 500, 500, 500, 500, 500, 1000, 1000, 1000, 1000, 1000]:
    t = xpy.design.Trial()
    t.set_factor("isi_ms", v)
    b2.add_trial(t)

# Randomization of SHAPES trials
for i in range(len(b2.trials) - 1, 0, -1):
    j = random.randint(0, i)
    b2.trials[i], b2.trials[j] = b2.trials[j], b2.trials[i]

# Stimuli for DOTS trials
for t in b1.trials:
    t.add_stimulus(canvas_dots_frame1)
    t.add_stimulus(canvas_dots_frame2)
    t.add_stimulus(screen5)
    t.add_stimulus(text2)
    t.add_stimulus(screen5)
    t.add_stimulus(screen6)

# Stimuli for SHAPES trials
for t in b2.trials:
    t.add_stimulus(canvas_shapes_frame1)
    t.add_stimulus(canvas_shapes_frame2)
    t.add_stimulus(screen5)
    t.add_stimulus(text2)
    t.add_stimulus(screen5)
    t.add_stimulus(screen6)

# Experiment start
e.add_block(b1)
e.add_block(b2)
xpy.control.start(skip_ready_screen=True)

# Counterbalancing
if e.subject % 2 == 0:
    e.blocks.reverse()

# Instructions
text1.present()
e.keyboard.wait(keys=[xpy.misc.constants.K_SPACE])

# Trial presentation
for b in e.blocks:
    for t in b.trials:
        v = t.get_factor("isi_ms")
        t.stimuli[2].present()
        e.clock.wait(200)

        for i in range(3):
            t.stimuli[0].present()
            e.clock.wait(250)
            if v > 0:
                t.stimuli[4].present()
                e.clock.wait(v)

            t.stimuli[1].present()
            e.clock.wait(250)
            if v > 0:
                t.stimuli[4].present()
                e.clock.wait(v)

        # Response collection
        t.stimuli[3].present()
        k, r = e.keyboard.wait(keys=[xpy.misc.constants.K_LEFT, xpy.misc.constants.K_RIGHT])

        if k == xpy.misc.constants.K_LEFT:
            a = "element"
            g = 0
        else:
            a = "group"
            g = 1

        # Intertrial interval
        t.stimuli[5].present()
        e.clock.wait(500)
        # Data saving
        e.data.add([b.get_factor("condition"), t.id, v, 250, a, g, k, r])
        e.data.save()

# Experiment end
xpy.control.end()
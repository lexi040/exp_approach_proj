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

#experiment initialization
#changed name of experiment variable from e to experiment
experiment = xpy.design.Experiment(name=CONFIG["experiment_name"], background_colour=CONFIG["bg_color"], foreground_colour=CONFIG["fg_color"])
experiment.data_variable_names = ["condition", "trial", "isi_ms", "frame_ms", "response", "group_response", "key", "rt_ms"]
xpy.control.initialize(experiment)

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
""" changed variable names to actually name what they represent and added a blank screen with fixation cross to be used in the trials """
fixation_cross = create_fixation_cross()
blank_screen_w_fixation_cross = create_blank_canvas()
fixation_cross.plot(blank_screen_w_fixation_cross)
blank_screen_clean = create_blank_canvas()

instructions_screen = xpy.stimuli.TextScreen(heading="Ternus experiment", text="Keep your eyes on the central cross.\n\nLEFT = element motion\nRIGHT = group motion\n\nPress SPACE to start.")
response_screen = xpy.stimuli.TextScreen(heading="What did you see?", text="LEFT = element motion\nRIGHT = group motion")

fixation_cross.plot(instructions_screen)
fixation_cross.plot(response_screen)

# Fixation on stimulus and text screens
for canvas in [canvas_dots_frame1, canvas_dots_frame2, canvas_shapes_frame1, canvas_shapes_frame2]:
    fixation_cross.plot(canvas)

# Preloading
#loop through all stimuli to preload them
for stimulus in [canvas_dots_frame1, canvas_dots_frame2, canvas_shapes_frame1, canvas_shapes_frame2, blank_screen_w_fixation_cross, blank_screen_clean, instructions_screen, response_screen]:
    stimulus.preload()  

#function that creates a trial block (follows DRY principle)
def create_trial_block(condition_name: str, frame1, frame2) -> xpy.design.Block:
    """Creates a radomized trial block with the specified conditione."""
    block = xpy.design.Block(name=condition_name)
    block.set_factor("condition", condition_name)
    #generate trials for each ISI value and add them to the block
    #20 trials total 4 isi values * 5 trials per isi value
    isi_factor_list = CONFIG["isi_values"] * CONFIG["trials_per_isi"]
    #randomize the order of the trials
    random.shuffle(isi_factor_list)

    for v in isi_factor_list:
        t = xpy.design.Trial()
        t.set_factor("isi_ms", v)
        t.add_stimulus(frame1)
        t.add_stimulus(frame2)
        t.add_stimulus(blank_screen_w_fixation_cross)
        t.add_stimulus(response_screen)
        t.add_stimulus(blank_screen_clean)
        block.add_trial(t)

    return block

dots_block = create_trial_block("DOTS", canvas_dots_frame1, canvas_dots_frame2)
shapes_block = create_trial_block("SHAPES", canvas_shapes_frame1, canvas_shapes_frame2)

experiment.add_block(dots_block)
experiment.add_block(shapes_block)

#start experiment
xpy.control.start(skip_ready_screen=True)
instructions_screen.present()
experiment.keyboard.wait(keys=[xpy.misc.constants.K_SPACE])

#kept coounterbalancig logic
if experiment.subject % 2 == 0:
    experiment.blocks.reverse()

for block in experiment.blocks:
    for trial in block.trials:
        isi = trial.get_factor("isi_ms")

        #present initial fixation
        trial.stimuli[2].present()  
        experiment.clock.wait(CONFIG["fixation_duration_ms"])

        #present the 3 alternating frames 
        for i in range(3):
            trial.stimuli[0].present()  #frame 1
            experiment.clock.wait(CONFIG["frame_duration_ms"])
            if isi > 0:
                trial.stimuli[2].present()  #blank with fixation cross
                experiment.clock.wait(isi)

            trial.stimuli[1].present()  #frame 2
            experiment.clock.wait(CONFIG["frame_duration_ms"])
            if isi > 0:
                trial.stimuli[2].present()  #lank with fixation cross
                experiment.clock.wait(isi)

        #response collection
        trial.stimuli[3].present(clear = False)  #response screen
        key, rt = experiment.keyboard.wait(keys=[xpy.misc.constants.K_LEFT, xpy.misc.constants.K_RIGHT])

        response = "element" if key == xpy.misc.constants.K_LEFT else "group"
        group_response = 0 if key == xpy.misc.constants.K_LEFT else 1

        #interval between trials
        trial.stimuli[4].present()  #blank clean screen
        experiment.clock.wait(CONFIG["iti_duration_ms"])

        #save data
        experiment.data.add([block.get_factor("condition"), trial.id, isi, CONFIG["frame_duration_ms"], response, group_response, key, rt])
        experiment.data.save()

xpy.control.end()


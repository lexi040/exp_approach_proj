import pytest
import expyriment as xpy
from scripts.Ternus import CONFIG, create_blank_canvas, create_fixation_cross, create_trial_block

def test_config_params():
    """Test that the CONFIG dictionary contains the expected parameters."""
    expected_keys = [
        "experiment_name", "screen_size", "bg_color", "fg_color",
        "circle_radius", "shape_size", "polygon_radius",
        "frame_duration_ms", "isi_values", "trials_per_isi",
        "fixation_duration_ms", "iti_duration_ms"
    ]
    for key in expected_keys:
        assert key in CONFIG, f"Missing config parameter: {key}"

def test_create_blank_canvas():
    """Test that create_blank_canvas returns a Canvas with the correct properties."""
    canvas = create_blank_canvas()
    assert isinstance(canvas, xpy.stimuli.Canvas)
    assert canvas.size == CONFIG["screen_size"]
   
def test_create_fixation_cross():
    """Test that create_fixation_cross returns a FixCross with the correct properties."""
    fixation_cross = create_fixation_cross()
    assert isinstance(fixation_cross, xpy.stimuli.FixCross) 

def test_create_trial_block_structure():
    """Test that create_trial_block returns a Block with the correct structure."""
    #create dummy frames for testing
    frame1 = create_blank_canvas()
    frame2 = create_blank_canvas()

    blank_w_cross = create_blank_canvas()
    resp_screen = create_blank_canvas() #mock response screen for testing because i couldnt figure out how to bypass the runtime error that screen size couldnt be accesses in the pytest env without initializing the experiment which also threw an error so dummy screen it is because i only care that the blocks are well created for this test, which as it turns out they are
    blank_clean = create_blank_canvas()
    
    block = create_trial_block("DOTS", frame1, frame2, blank_w_cross, resp_screen, blank_clean)

    expected_trial_count = len(CONFIG["isi_values"]) * CONFIG["trials_per_isi"]
    assert len(block.trials) == expected_trial_count 
    assert block.get_factor("condition") == "DOTS"

    isi_counts = {isi: 0 for isi in CONFIG["isi_values"]}
    for trial in block.trials:
        isi = trial.get_factor("isi_ms")
        assert isi in CONFIG["isi_values"]
        isi_counts[isi] += 1
        assert len(trial.stimuli) == 5

    for isi, count in isi_counts.items():
        assert count == CONFIG["trials_per_isi"]

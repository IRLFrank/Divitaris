from Animace.animace import AnimationManager

def setup_animations():
    manager = AnimationManager()
    manager.add_animation(
        name="run",
        spritesheet_path="Animace/spritesheets/test_sheet.png",
        row=0,
        frame_count=2,
        frame_width=16,
        frame_height=16
    )
    # Add more animations here as needed
    return manager
import argparse
import numpy as np
import genesis as gs


def add_house_part(scene, path, color, rho=500, use_elastoplastic=False, offset=(0.0, 0.0, 0.0)):
    """
    Add a house part with the appropriate material type.
    
    Args:
        scene: Genesis scene
        path: Path to mesh file
        color: RGBA color tuple
        rho: Density (kg/m³)
        use_elastoplastic: If True, use ElastoPlastic material (can break/yield)
                          If False, use Elastic material (won't break)
        offset: Position offset (x, y, z) for placing multiple houses
    """
    # Choose material based on whether we want breakable behavior
    if use_elastoplastic:
        material = gs.materials.MPM.ElastoPlastic(rho=rho)
    else:
        material = gs.materials.MPM.Elastic(rho=rho)
    
    return scene.add_entity(
        morph=gs.morphs.Mesh(
            file=path,
            pos=(offset[0], offset[1], offset[2]),
            euler=(90, 0, 0),
            scale=0.08,
            fixed=False,
        ),
        surface=gs.surfaces.Rough(color=color),
        material=material,
    )


def add_complete_house(scene, offset=(0.0, 0.0, 0.0)):
    """
    Add a complete house at the specified offset position.
    
    Args:
        scene: Genesis scene
        offset: Position offset (x, y, z) tuple
    
    Returns:
        Dictionary of house parts
    """
    house_parts = {}
    
    # FOUNDATION - Heavy and resistant (Elastic = won't break easily)
    house_parts['foundation'] = add_house_part(
        scene, "house_parts/house_foundation.obj",
        color=(0.50, 0.50, 0.50, 1.0),
        rho=2500,           # Very heavy concrete
        use_elastoplastic=False,  # Use elastic so it stays stable
        offset=offset
    )
    
    # FLOOR - ElastoPlastic so it can crack under pressure
    house_parts['floor'] = add_house_part(
        scene, "house_parts/house_floor.obj",
        color=(0.60, 0.45, 0.30, 1.0),
        rho=800,            # Wood density
        use_elastoplastic=True,  # Can break
        offset=offset
    )
    
    # WALLS - ElastoPlastic and lighter to break more easily
    house_parts['walls'] = add_house_part(
        scene, "house_parts/house_walls.obj",
        color=(0.90, 0.85, 0.75, 1.0),
        rho=400,            # Lighter construction material
        use_elastoplastic=True,  # WILL BREAK
        offset=offset
    )
    
    # ROOF - ElastoPlastic and very light
    house_parts['roof'] = add_house_part(
        scene, "house_parts/house_roof.obj",
        color=(0.60, 0.20, 0.20, 1.0),
        rho=300,            # Very light roofing
        use_elastoplastic=True,  # Will break easily
        offset=offset
    )
    
    # DOOR - ElastoPlastic
    house_parts['door'] = add_house_part(
        scene, "house_parts/house_door.obj",
        color=(0.40, 0.25, 0.10, 1.0),
        rho=450,
        use_elastoplastic=True,
        offset=offset
    )
    
    # DOOR FRAME - ElastoPlastic
    house_parts['door_frame'] = add_house_part(
        scene, "house_parts/house_door_frame.obj",
        color=(0.35, 0.20, 0.08, 1.0),
        rho=450,
        use_elastoplastic=True,
        offset=offset
    )
    
    # WINDOWS (GLASS) - Very fragile, ElastoPlastic with very low density
    house_parts['w_glass_L'] = add_house_part(
        scene, "house_parts/house_window_left_glass.obj",
        color=(0.70, 0.90, 1.00, 0.5),
        rho=200,            # Much lighter than actual glass to break easily
        use_elastoplastic=True,  # VERY FRAGILE
        offset=offset
    )
    
    house_parts['w_glass_R'] = add_house_part(
        scene, "house_parts/house_window_right_glass.obj",
        color=(0.70, 0.90, 1.00, 0.5),
        rho=200,
        use_elastoplastic=True,
        offset=offset
    )
    
    house_parts['w_glass_B'] = add_house_part(
        scene, "house_parts/house_window_back_glass.obj",
        color=(0.70, 0.90, 1.00, 0.5),
        rho=200,
        use_elastoplastic=True,
        offset=offset
    )
    
    # WINDOW FRAMES - ElastoPlastic, lighter than walls
    house_parts['w_frame_L'] = add_house_part(
        scene, "house_parts/house_window_left_frame.obj",
        color=(0.30, 0.20, 0.10, 1.0),
        rho=400,
        use_elastoplastic=True,
        offset=offset
    )
    
    house_parts['w_frame_R'] = add_house_part(
        scene, "house_parts/house_window_right_frame.obj",
        color=(0.30, 0.20, 0.10, 1.0),
        rho=400,
        use_elastoplastic=True,
        offset=offset
    )
    
    house_parts['w_frame_B'] = add_house_part(
        scene, "house_parts/house_window_back_frame.obj",
        color=(0.30, 0.20, 0.10, 1.0),
        rho=400,
        use_elastoplastic=True,
        offset=offset
    )
    
    return house_parts
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--vis", action="store_true", default=False)
    args = parser.parse_args()
    
    ########################## init ##########################
    gs.init(precision="32", logging_level="info")
    
    ########################## create a scene ##########################
    # DOUBLED ENVIRONMENT SIZE
    # Original: X(-1 to 3)=4, Y(-1 to 1)=2, Z(-0.2 to 1.5)=1.7
    # New:      X(-2 to 6)=8, Y(-2 to 2)=4, Z(-0.2 to 3.0)=3.2
    scene = gs.Scene(
        sim_options=gs.options.SimOptions(
            dt=4e-3,
            substeps=10,
        ),
        mpm_options = gs.options.MPMOptions(
            lower_bound=(-2.0, -2.0, -0.20),  # Doubled bounds
            upper_bound=( 6.0,  2.0,  3.0),   # Doubled bounds
            grid_density=40,
        ),
        viewer_options=gs.options.ViewerOptions(
            camera_pos=(1.5, -4.0, 2.2),  # Cinematic angle - closer and more realistic
            camera_lookat=(3.0, 0.0, 0.6),  # Looking at the action
            camera_fov=50,  # Natural camera lens perspective
            max_FPS=60,
        ),
        show_viewer=args.vis,
        vis_options=gs.options.VisOptions(
            visualize_mpm_boundary=True,
            show_world_frame=False,  # Hide axis arrows

        ),
    )
    
    # Ground plane
    plane = scene.add_entity(morph=gs.morphs.Plane()) 
    
    # Add multiple houses at different positions
    # Creating a diagonal zigzag pattern
    house_positions = [
        (0.0, -0.8, 0.0),   # House 1: lower
        (1.5,  0.8, 0.0),   # House 2: diagonal upper-right
        (3.0, -0.8, 0.0),   # House 3: diagonal lower-right
        (4.5,  0.8, 0.0),   # House 4: diagonal upper-right
    ]
    
    houses = []
    print(f"Adding {len(house_positions)} houses to the scene...")
    for i, pos in enumerate(house_positions):
        print(f"  House {i+1} at position {pos}")
        house = add_complete_house(scene, offset=pos)
        houses.append(house)

    # --- Create the Flood Water ---
    # Multiple irregular water volumes for more random, natural flood appearance
    flood_waters = []
    
    # Create multiple water volumes at varying heights and positions
    # Keeping all positions within safe boundary: Y in [-1.9, 1.9], Z above -0.12
    water_volumes = [
        # (size, position) tuples
        ((0.5, 1.0, 0.8), (-1.3, -0.8, 0.5)),
        ((0.4, 0.8, 1.0), (-1.2, 0.2, 0.6)),
        ((0.6, 1.2, 0.7), (-1.4, 0.9, 0.4)),
        ((0.3, 0.9, 0.9), (-1.1, -0.3, 0.55)),
        ((0.5, 1.0, 0.6), (-1.5, -1.3, 0.4)),  # Fixed: reduced Y size and adjusted position
        ((0.4, 1.0, 0.8), (-1.2, 1.3, 0.5)),
    ]
    
    for i, (size, pos) in enumerate(water_volumes):
        water = scene.add_entity(
            morph=gs.morphs.Box(
                size=size,
                pos=pos
            ),
            material=gs.materials.MPM.Liquid(
                rho=1000.0,
                sampler="random",
            ),
            surface=gs.surfaces.Rough(
                color=(0.60, 0.80, 1.00, 0.30),
            ),
        )
        flood_waters.append(water)
    
    
    # Add camera for recording - positioned for cinematic/realistic video look
    cam = scene.add_camera(
        res=(1920, 1080),  # Full HD resolution
        pos=(1.5, -4.0, 2.2),  # Closer, at human eye-level height, slight side angle
        lookat=(3.0, 0.0, 0.6),  # Looking at houses where flood hits
        fov=50,  # More natural camera lens perspective
        GUI=False  # Don't show separate camera window
    )

    scene.build()

    horizon = 700  # Extended simulation time for larger scene

    # Set initial flood velocity for each water volume
    total_flood_particles = 0
    for water in flood_waters:
        n_particles = water.n_particles
        total_flood_particles += n_particles
        vel_np = np.tile(np.array([6.0, 0.0, 0.0], dtype=np.float32).reshape(1, 3), (n_particles, 1))
        vel_tensor = gs.Tensor(vel_np)
        water.set_vel(0, vel=vel_tensor)

    print(f"\n{'='*60}")
    print(f"Starting simulation with:")
    print(f"  - Environment size: 2x larger")
    print(f"  - Number of houses: {len(houses)}")
    print(f"  - Flood water volumes: {len(flood_waters)}")
    print(f"  - Flood particles: {total_flood_particles}")
    print(f"  - Simulation steps: {horizon}")
    print(f"{'='*60}\n")
    
    cam.start_recording()
    for i in range(horizon):
        scene.step()

        if i % 100 == 0:
            print(f"Simulation progress: {i}/{horizon} steps ({100*i//horizon}%)")
        
        # Camera stays at fixed position: (1.5, -4.0, 2.2) with cinematic angle
        cam.render()

    cam.stop_recording(save_to_filename='Desktop/genesis_workplace/video_sim_4.mp4', fps=60)

            
if __name__ == "__main__":
    main()
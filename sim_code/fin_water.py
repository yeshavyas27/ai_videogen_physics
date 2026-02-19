import argparse
import numpy as np
import genesis as gs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--vis", action="store_true", default=False)
    args = parser.parse_args()
    
    ########################## init ##########################
    gs.init(precision="32", logging_level="info")
    
    ########################## create a scene ##########################
    # SMALL COMPACT SCENE - just big enough for the fin and wave
    scene = gs.Scene(
        sim_options=gs.options.SimOptions(
            dt=4e-3,
            substeps=5,
            gravity=(0.0, 0.0, 0.0)
        ),
        mpm_options=gs.options.MPMOptions(
            lower_bound=(-2.0, -0.6, -0.2),  # Compact bounds around fin
            upper_bound=(2.0, 0.6, 2.2),     # Just enough space
            grid_density=40,
        ),
        viewer_options=gs.options.ViewerOptions(
            camera_pos=(0.0, -3.5, 1.0),  # Closer camera for small scene
            camera_lookat=(0.0, 0.0, 1.0),
            camera_fov=50,
            max_FPS=30,  # slower playback in viewer
        ),
        show_viewer=args.vis,
        vis_options=gs.options.VisOptions(
            visualize_mpm_boundary=False,
            show_world_frame=False,
        ),
    )
    
    # Ground plane
    plane = scene.add_entity(morph=gs.morphs.Plane())
    
    # Create UNDERWATER ENVIRONMENT - fills the entire scene
    # Light cyan ambient water that the fin and wave exist within
    # underwater_ambient = scene.add_entity(
    #     morph=gs.morphs.Box(
    #         size=(3.5, 1.0, 2.0),  # Fill the entire scene
    #         pos=(0.0, 0.0, 1.0)    # Centered
    #     ),
    #     material=gs.materials.MPM.Liquid(
    #         rho=1000.0,
    #         sampler="regular",
    #     ),
    #     surface=gs.surfaces.Rough(
    #         color=(0.4, 0.75, 0.85, 0.6),  # Light cyan ambient (more opaque)
    #     ),
    # )
    
    # This fin matches the teardrop/airfoilprofile shown in the simulation
    fin = scene.add_entity(
        morph=gs.morphs.Mesh(
            file='fin.obj',
            pos=(0.0, 0.0, 1.0),  # Centered in scene
            euler=(0, 0, 0),  # Horizontal orientation
            scale=0.8,
            fixed=True,  # Allow movement - fin will be pushed by wave!
        ),
        material=gs.materials.Rigid(),
        surface=gs.surfaces.Rough(
            color=(0.1, 0.1, 0.1, 1.0),  # WHITE/LIGHT GRAY fin - highly visible!
        ),
    )
    
    # Create BIG WAVE - BLUE water (lower half) - MORE OPAQUE
    # Large water volume positioned upstream that will slam into fin
    wave_blue = scene.add_entity(
        morph=gs.morphs.Box(
            size=(1.2, 1.0, 0.7),  # Large wave volume - lower half
            pos=(-1.3, 0.0, 0.7)   # Positioned to the LEFT, lower position
        ),
        material=gs.materials.MPM.Liquid(
            rho=1000.0,
            sampler="regular",
        ),
        surface=gs.surfaces.Rough(
            color=(0.05, 0.25, 0.95, 0.3),  # BRIGHT BLUE water - fully opaque
        ),
    )
    
    # Create BIG WAVE - RED/ORANGE water (upper half) - MORE OPAQUE
    wave_red = scene.add_entity(
        morph=gs.morphs.Box(
            size=(1.2, 1.0, 0.7),  # Large wave volume - upper half
            pos=(-1.3, 0.0, 1.4)   # Positioned to the LEFT, upper position
        ),
        material=gs.materials.MPM.Liquid(
            rho=1000.0,
            sampler="regular",
        ),
        surface=gs.surfaces.Rough(
            color=(0.95, 0.35, 0.15, 0.3),  # RED/ORANGE water - fully opaque
        ),
    )
    
    # Add camera for recording - close-up view for small scene
    cam = scene.add_camera(
        res=(1920, 1080),  # Full HD
        pos=(0.0, -3.5, 1.0),  # Closer for compact scene
        lookat=(0.0, 0.0, 1.0),
        fov=50,
        GUI=False
    )
    
    scene.build()
    
    
    # Set WAVE VELOCITY - big wave crashes into fin from LEFT
    wave_velocity = 3  # m/s - slower wave for slow-motion effect
    
    # Set velocity for BLUE wave (lower)
    n_blue_particles = wave_blue.n_particles
    vel_blue_np = np.tile(
        np.array([wave_velocity, 0.0, 0.0], dtype=np.float32).reshape(1, 3), 
        (n_blue_particles, 1)
    )
    vel_blue_tensor = gs.Tensor(vel_blue_np)
    wave_blue.set_vel(0, vel=vel_blue_tensor)
    
    # Set velocity for RED wave (upper)
    n_red_particles = wave_red.n_particles
    vel_red_np = np.tile(
        np.array([wave_velocity, 0.0, 0.0], dtype=np.float32).reshape(1, 3), 
        (n_red_particles, 1)
    )
    vel_red_tensor = gs.Tensor(vel_red_np)
    wave_red.set_vel(0, vel=vel_red_tensor)
    
    horizon = 150
    
    print(f"\n{'='*60}")
    print(f"Starting UNDERWATER WAVE IMPACT simulation:")
    print(f"  - Scene: FULLY UNDERWATER + Compact (fin-sized)")
    print(f"  - Ambient water: Light CYAN (more opaque)")
    print(f"  - Fin: WHITE AIRFOIL (airfoil_fin.obj) - HIGHLY VISIBLE!")
    print(f"  - Fin: SOLID & DEFORMABLE - Hydrodynamic shape!")
    print(f"  - Wave velocity: {wave_velocity} m/s - BIG WAVE!")
    print(f"  - Blue wave particles (FULLY OPAQUE): {n_blue_particles}")
    print(f"  - Red/Orange wave particles (FULLY OPAQUE): {n_red_particles}")
    print(f"  - Fin position: (0.0, 0.0, 1.0)")
    print(f"  - Simulation steps: {horizon}")
    print(f"  - RED/ORANGE water above, BLUE water below")
    print(f"  - Beautiful flow streamlines around white fin!")
    print(f"{'='*60}\n")
    
    cam.start_recording()
    
    for i in range(horizon):
        scene.step()
        cam.render()
        
        # Print progress every 150 steps
        if i % 5 == 0:
            print(f"Wave impact progress: {i}/{horizon} steps ({100*i//horizon}%)")
    
    cam.stop_recording(save_to_filename='fin_wave_impact.mp4', fps=15)
    print(f"\n{'='*60}")
    print(f"Simulation complete! Video saved to: fin_wave_impact.mp4")
    print(f"Watch the BIG WAVE slam into the fin!")
    print(f"RED water above, BLUE water below.")
    print(f"{'='*60}\n")
            
if __name__ == "__main__":
    main()
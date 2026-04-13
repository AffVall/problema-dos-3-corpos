from random import randint, uniform
from typing import List, Tuple, Dict
import numpy as np
from phisicBody import Body
from config import Config
import matplot as mp

COLORS = ['#FF6B6B', '#4ECDC4', "#09FF00", "#F107AB", '#FFE66D', '#FF9F1C', '#2EC4B6', '#E71D36', "#82FF69", '#A0E7E5']


def randomize_body_positions(config: Config, bodies: List[Dict]) -> None:
    config.log("RANDOMIZING BODY POSITIONS AND VELOCITIES")

    grid_w = config['grid_width']
    grid_h = config['grid_height']
    min_vel = config['min_velocity']
    max_vel = config['max_velocity']
    margin_w, margin_h = max(10, int(grid_w * 0.8)), max(10, int(grid_h * 0.8))
    
    for body_data in bodies:
        pos_x = randint(10,  margin_w)
        pos_y = randint(10,  margin_h)
        vel_x = uniform(min_vel, max_vel)
        vel_y = uniform(min_vel, max_vel)
        body_data['pos_x'] = float(pos_x)
        body_data['pos_y'] = float(pos_y)
        body_data['vel_x'] = float(vel_x)
        body_data['vel_y'] = float(vel_y)


def check_collision(bodies: List[Body], collision_dist: float) -> Tuple[bool, str, str]:
    for i, body1 in enumerate(bodies):
        for j in range(i + 1, len(bodies)):
            body2 = bodies[j]
            dist = np.sqrt((body2.position['x'] - body1.position['x'])**2 + 
                           (body2.position['y'] - body1.position['y'])**2)
            if dist < collision_dist * 5:
                return True, body1.name, body2.name
    return False, None, None


def check_boundary_exit(bodies: List[Body], grid_w: float, grid_h: float) -> Tuple[bool, str]:
    margin_w, margin_h = max(10, int(grid_w * 0.25)), max(10, int(grid_h * 0.25))
    for body in bodies:
        x, y = body.position['x'], body.position['y']
        if x < -margin_w or x > grid_w + margin_w or y < -margin_h or y > grid_h + margin_h:
            return True, body.name
    return False, None


def update_system(bodies: List[Body], time_step: float) -> None:
    for i, body in enumerate(bodies):
        other_bodies = bodies[:i] + bodies[i+1:]
        force = body.calculate_resultant_force(other_bodies)
        body.update_acceleration(force)
    
    for body in bodies:
        body.update_velocity(time_step)
    
    for body in bodies:
        body.update_position(time_step)


def run_simulation(config: Config, frames: list) -> Tuple[List[Body], Dict]:
    bodies = config.get('bodies')
    trajectories = {body.name: {'x': [], 'y': []} for body in bodies}
    
    max_cycles = config['simulation_cycles']
    time_step = config['time_step']
    grid_w, grid_h = config['grid_width'], config['grid_height']
    collision_dist = config['collision_distance']
    frame_interval = config['frame_interval']
    min_frames = config['min_frames']
    dpi = config['plot_dpi']
    
    config.log("THREE BODY PROBLEM SIMULATION", "TITLE")
    config.log(f"Max cycles: {max_cycles}")
    config.log(f"Time step: {time_step}")
    config.log(f"Grid: {grid_w}x{grid_h}")
    config.log(f"Collision distance: {collision_dist}")
    config.log(f"Min cycles required for {min_frames} frames")
    config.log(f"Bodies: {[body.name for body in bodies]}\n")
    config.log(f"Debug mode {'ON' if config['debug'] else 'OFF'}\n")
    
    termination = "max_cycles"
    
    
    for cycle in range(max_cycles * frame_interval):
        for body in bodies:
            trajectories[body.name]['x'].append(body.position['x'])
            trajectories[body.name]['y'].append(body.position['y'])
        
        update_system(bodies, time_step)
        
        if (cycle + 1) % frame_interval == 0:
            mp.plot_config(bodies, grid_w, grid_h)
            frames = mp.save_frame(bodies, frames, dpi)
            if len(frames) % 10 == 0:
                config.log(f"Cycle {cycle + 1}: Frame saved (Total frames: {len(frames)})", "DEBUG")
            collided, b1, b2 = check_collision(bodies, collision_dist)
            if collided:
                config.log(f" COLLISION: {b1} and {b2} at cycle {cycle + 1}", ">>>")
                termination = f"collision_{b1}_{b2}"
                if not config['end_on_collision']:
                    continue
                for body in bodies:
                    trajectories[body.name]['x'].append(body.position['x'])
                    trajectories[body.name]['y'].append(body.position['y'])

                break
        exited, name = check_boundary_exit(bodies, grid_w, grid_h)
        if exited:
            config.log(f" BOUNDARY EXIT: {name} at cycle {cycle + 1}", ">>>")
            termination = f"boundary_exit_{name}"
            for body in bodies:
                trajectories[body.name]['x'].append(body.position['x'])
                trajectories[body.name]['y'].append(body.position['y'])
            break
    
        
    config.log(f"Simulation completed: {termination}", '>>>')
    config.log(f"Total frames generated: {len(frames)}", "DEBUG")
    return bodies, trajectories


def validate_and_retry(config: Config, results_dir: str, frames: list,
                       retry_count: int = 0) -> Tuple[List[Body], Dict]:
    if retry_count > 0:
        frames.clear()
    
    if config['randomize_positions']:
        randomize_body_positions(config, config['bodies'])
    
    bodies, trajectories = run_simulation(config, frames)
    frame_count = len(frames)
    config.log(f"Simulation generated {frame_count} frames (min required: {config['min_frames']})", "DEBUG")
    
    if frame_count < config['min_frames'] and retry_count < config['max_retries'] and config['randomize_positions']:
        config.log(f"Insufficient frames ({frame_count}/{config['min_frames']}) - retrying simulation (attempt {retry_count + 1})", "WARNING")
        return validate_and_retry(config, results_dir, frames, retry_count + 1)
    
    config.log(f"SIMULATION VALIDATION SUCCESS: {frame_count} frames after {retry_count} retries.")
    config.log(f"Validation complete. Ready for visualization.", "DEBUG")
    return bodies, trajectories


def main() -> None:
    config = Config()
    frames = []

    config.log("="*60)
    config.log("THREE BODY PROBLEM SIMULATOR STARTED", "TITLE")
    config.log("="*60)
    config.log(f"Log file: {config.log_dir}", 'DEBUG')
    config.log(f"Results directory: {config.results_dir}", 'DEBUG')
    config.log(f"Configuration: debug={config['debug']}, randomize_pos={config['randomize_positions']}, calc_sizes={config['calculate_sizes']}", 'DEBUG')
    
    bodies, trajectories = validate_and_retry(config, config.results_dir, frames)
    
    config.log("\nFINAL STATE OF BODIES:")
    for body in bodies:
        config.log(str(body) + "\n")
    
    config.log("\nGENERATING VISUALIZATIONS...")
    config.log("Starting trajectory generation", "DEBUG")
    
    dpi = config['plot_dpi']
    hq = config['high_quality_plots']
    
    config.log("Generating trajectory plot...", "DEBUG")
    mp.plot_trajectories(trajectories, bodies, config.results_dir, dpi, hq)
    
    config.log("Generating distance plot...", "DEBUG")
    mp.plot_distances(trajectories, bodies, config.results_dir, dpi, hq)
    
    config.log("Generating velocity plot...", "DEBUG")
    mp.plot_velocities(trajectories, bodies, config.results_dir, dpi, hq)

    config.log('Saving frames as video...', "DEBUG")
    mp.video_from_frames(frames, config.results_dir, fps=10)
    
    config.log("="*60)
    config.log("SIMULATION COMPLETE - All files saved successfully!", "TITLE")
    config.log("="*60)


if __name__ == '__main__':
    main()

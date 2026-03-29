import os
from datetime import datetime
from random import randint, uniform
from typing import List, Tuple, Dict

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cv2

from phisicBodies import Body
from config import Config

COLORS = ['#FF6B6B', '#4ECDC4', '#45B7D1', "#F107AB", '#FFE66D', '#FF9F1C', '#2EC4B6', '#E71D36', "#82FF69", '#A0E7E5']


def calculate_body_size(body: Dict, config: Config) -> float:
    if config['calculate_sizes']:
        scale = config.get('size_scale_factor', 8)
        size = np.sqrt(body['mass']) * scale
        return max(10.0, min(100.0, size))
    return 25.0


def initialize_bodies(config: Config) -> List[Body]:
    config_bodies = config['bodies']
    bodies = []
    for body in config_bodies:
        name = body['name']
        mass = body['mass']
        size = calculate_body_size(body, config)
        pos_x = body['pos_x']
        pos_y = body['pos_y']
        vel_x = body['vel_x']
        vel_y = body['vel_y']
        
        config.log(f"Body {name}: mass={mass}, size={size:.2f}, pos=({pos_x}, {pos_y}), vel=({vel_x:.3f}, {vel_y:.3f})", "DEBUG")
        body_obj = Body(mass, {'x': vel_x, 'y': vel_y}, {'x': pos_x, 'y': pos_y}, size=size, name=name)
        bodies.append(body_obj)
    config.log(f"Initialized {len(bodies)} bodies", "DEBUG")
    return bodies


def randomize_body_positions(config: Config, bodies: List[Dict]) -> None:
    config.log("RANDOMIZING BODY POSITIONS AND VELOCITIES")

    grid_w = config['grid_width']
    grid_h = config['grid_height']
    min_vel = config['min_velocity']
    max_vel = config['max_velocity']
    margin = max(10, int(grid_w * 0.1)) 
    
    for body_data in bodies:
        pos_x = randint(margin, grid_w - margin)
        pos_y = randint(margin, grid_h - margin)
        vel_x = uniform(min_vel, max_vel)
        vel_y = uniform(min_vel, max_vel)
        
        if pos_x < grid_w / 2 and vel_x < 0:
            vel_x = abs(vel_x)
        elif pos_x >= grid_w / 2 and vel_x > 0:
            vel_x = -abs(vel_x)
        
        if pos_y < grid_h / 2 and vel_y < 0:
            vel_y = abs(vel_y)
        elif pos_y >= grid_h / 2 and vel_y > 0:
            vel_y = -abs(vel_y)

        body_data['pos_x'] = float(pos_x)
        body_data['pos_y'] = float(pos_y)
        body_data['vel_x'] = float(vel_x)
        body_data['vel_y'] = float(vel_y)


def check_collision(bodies: List[Body]) -> Tuple[bool, str, str]:
    for i, body1 in enumerate(bodies):
        for j in range(i + 1, len(bodies)):
            body2 = bodies[j]
            dist = np.sqrt((body2.position['x'] - body1.position['x'])**2 + 
                           (body2.position['y'] - body1.position['y'])**2)
            if dist < body1.size + body2.size:
                return True, body1.name, body2.name
    return False, None, None


def check_boundary_exit(bodies: List[Body], grid_w: float, grid_h: float, 
                        margin: float = 20) -> Tuple[bool, str]:
    for body in bodies:
        x, y = body.position['x'], body.position['y']
        if x < -margin or x > grid_w + margin or y < -margin or y > grid_h + margin:
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


def save_frame(bodies: List[Body], cycle: int, saved_frames: list, 
               grid_w: float, grid_h: float, dpi: int) -> List:
    """
    Salva um frame da simulação como imagem NumPy.
    
    Args:
        bodies: Lista de corpos
        cycle: Número do ciclo
        saved_frames: Lista para acumular frames
        grid_w: Largura do grid
        grid_h: Altura do grid
        dpi: Resolução dos gráficos
        
    Returns:
        Lista de frames atualizada
    """
    plt.figure(figsize=(10, 10))
    
    for body, b_color in zip(bodies, COLORS):
        plt.scatter(body.position['x'], body.position['y'],
                   s=body.size, color=b_color, alpha=0.8, edgecolors='black', 
                   linewidth=1.5, label=body.name)
    
    plt.xlim(-5, grid_w + 5)
    plt.ylim(-5, grid_h + 5)
    plt.xlabel('X (units)', fontsize=12, fontweight='bold')
    plt.ylabel('Y (units)', fontsize=12, fontweight='bold')
    plt.title(f'Three Body Problem - Cycle {cycle}', fontsize=14, fontweight='bold')
    plt.legend(loc='upper right', fontsize=10)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.gca().set_aspect('equal')
     
    frame = plt.gcf()
    frame.canvas.draw()
    width, height = frame.canvas.get_width_height()
    img = np.frombuffer(frame.canvas.tostring_argb(), dtype=np.uint8)
    img = img.reshape((height, width, 4))
    img = img[:, :, 1:] 
    saved_frames.append(img)
    plt.close()
    return saved_frames


def run_simulation(config: Config, frames: list) -> Tuple[List[Body], Dict]:
    bodies = initialize_bodies(config)
    trajectories = {body.name: {'x': [], 'y': []} for body in bodies}
    
    max_cycles = config['simulation_cycles']
    time_step = config['time_step']
    grid_w, grid_h = config['grid_width'], config['grid_height']
    collision_dist = config['collision_distance']
    frame_interval = config['frame_interval']
    min_frames = config['min_frames']
    dpi = config['plot_dpi']
    min_cycles = frame_interval * min_frames
    
    config.log("THREE BODY PROBLEM SIMULATION", "TITLE")
    config.log(f"Max cycles: {max_cycles}")
    config.log(f"Time step: {time_step}")
    config.log(f"Grid: {grid_w}x{grid_h}")
    config.log(f"Collision distance: {collision_dist}")
    config.log(f"Min cycles required for {min_frames} frames: {min_cycles}\n")
    config.log(f"Bodies: {[body.name for body in bodies]}\n")
    config.log(f"Debug mode {'ON' if config['debug'] else 'OFF'}\n")
    
    termination = "max_cycles"
    
    for cycle in range(max_cycles):
        for body in bodies:
            trajectories[body.name]['x'].append(body.position['x'])
            trajectories[body.name]['y'].append(body.position['y'])
        
        update_system(bodies, time_step)
        
        if (cycle + 1) % frame_interval == 0:
            frames = save_frame(bodies, cycle, frames, grid_w, grid_h, dpi)
        
        exited, name = check_boundary_exit(bodies, grid_w, grid_h)
        if exited:
            config.log(f"\n>>> BOUNDARY EXIT: {name} at cycle {cycle + 1}")
            termination = f"boundary_exit_{name}"
            for body in bodies:
                trajectories[body.name]['x'].append(body.position['x'])
                trajectories[body.name]['y'].append(body.position['y'])
            break
        
        if cycle >= min_cycles:
            collided, b1, b2 = check_collision(bodies)
            if collided:
                config.log(f"\n>>> COLLISION: {b1} and {b2} at cycle {cycle + 1}")
                termination = f"collision_{b1}_{b2}"
                for body in bodies:
                    trajectories[body.name]['x'].append(body.position['x'])
                    trajectories[body.name]['y'].append(body.position['y'])
                break
    config.log(f"Simulation completed: {termination}")
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
    
    if frame_count < config['min_frames'] and retry_count < config['max_retries']:
        config.log(f"Insufficient frames ({frame_count}/{config['min_frames']}) - retrying simulation (attempt {retry_count + 1})", "WARNING")
        return validate_and_retry(config, results_dir, frames, retry_count + 1)
    
    config.log(f"SIMULATION VALIDATION SUCCESS: {frame_count} frames after {retry_count} retries.")
    config.log(f"Validation complete. Ready for visualization.", "DEBUG")
    return bodies, trajectories


def plot_trajectories(trajectories: Dict, bodies: List[Body], 
                     results_dir: str, dpi: int, hq: bool) -> None:
    plt.figure(figsize=(14, 10) if hq else (12, 8))
    
    for body, b_color in zip(bodies, COLORS):
        x, y = trajectories[body.name]['x'], trajectories[body.name]['y']
        
        plt.plot(x, y, label=body.name, color=b_color, alpha=0.8, 
                linewidth=2 if hq else 1.5)
        
        plt.scatter(x[0], y[0], color=b_color, marker='o', 
                   s=body.size if hq else 100, edgecolors='black', 
                   linewidth=2.5, zorder=5, label=f'{body.name} (start)')
        
        plt.scatter(x[-1], y[-1], color=b_color, marker='*',
                   s=body.size*1.2 if hq else 500, edgecolors='black',
                   linewidth=2.5, zorder=5, label=f'{body.name} (end)')
    
    plt.xlabel('X (units)', fontsize=14, fontweight='bold')
    plt.ylabel('Y (units)', fontsize=14, fontweight='bold')
    plt.title('Orbital Trajectories (○=Start, ★=End)', fontsize=16, fontweight='bold', pad=20)
    plt.legend(loc='best', fontsize=11, framealpha=0.95)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.axis('equal')
    plt.tight_layout()
    
    output = os.path.join(results_dir, 'trajectories.png')
    plt.savefig(output, dpi=dpi, bbox_inches='tight', facecolor='white')
    print(f"[OK] Trajectories: {output}")
    plt.close()


def plot_distances(trajectories: Dict, bodies: List[Body],
                  results_dir: str, dpi: int, hq: bool) -> None:
    plt.figure(figsize=(14, 8) if hq else (12, 6))
    
    names = [b.name for b in bodies]
    pairs = [(0, 1), (0, 2), (1, 2)]
    
    for (i, j), color in zip(pairs, COLORS):
        distances = []
        for k in range(len(trajectories[names[i]]['x'])):
            x1, y1 = trajectories[names[i]]['x'][k], trajectories[names[i]]['y'][k]
            x2, y2 = trajectories[names[j]]['x'][k], trajectories[names[j]]['y'][k]
            dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            distances.append(dist)
        
        plt.plot(distances, label=f'{names[i]}-{names[j]}', 
                color=color, linewidth=2.5, alpha=0.8)
    
    plt.xlabel('Cycle', fontsize=14, fontweight='bold')
    plt.ylabel('Distance (units)', fontsize=14, fontweight='bold')
    plt.title('Inter-body Distances Over Time', fontsize=16, fontweight='bold', pad=20)
    plt.legend(loc='best', fontsize=11, framealpha=0.95)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    output = os.path.join(results_dir, 'distances.png')
    plt.savefig(output, dpi=dpi, bbox_inches='tight', facecolor='white')
    print(f"[OK] Distances: {output}")
    plt.close()


def plot_velocities(trajectories: Dict, bodies: List[Body],
                   results_dir: str, dpi: int, hq: bool) -> None:
    plt.figure(figsize=(14, 8) if hq else (12, 6))
    
    for body, color in zip(bodies, COLORS):
        name = body.name
        velocities = []
        
        for i in range(len(trajectories[name]['x']) - 1):
            x1, y1 = trajectories[name]['x'][i], trajectories[name]['y'][i]
            x2, y2 = trajectories[name]['x'][i + 1], trajectories[name]['y'][i + 1]
            vel = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            velocities.append(vel)
        
        plt.plot(velocities, label=name, color=color, linewidth=2.5, alpha=0.8)
    
    plt.xlabel('Cycle', fontsize=14, fontweight='bold')
    plt.ylabel('Velocity (units/cycle)', fontsize=14, fontweight='bold')
    plt.title('Velocity Evolution Over Time', fontsize=16, fontweight='bold', pad=20)
    plt.legend(loc='best', fontsize=11, framealpha=0.95)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    output = os.path.join(results_dir, 'velocity.png')
    plt.savefig(output, dpi=dpi, bbox_inches='tight', facecolor='white')
    print(f"[OK] Velocity: {output}")
    plt.close()


def video_from_frames(saved_frames: list, results_dir: str, fps: int = 10) -> None:
    height, width, _ = saved_frames[0].shape
    video_path = os.path.join(results_dir, 'simulation.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
    for frame in saved_frames:
        video.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    video.release()


def main() -> None:
    config = Config()
    results_dir = config.setup_output_directories()
    frames = []

    config.log("="*60)
    config.log("THREE BODY PROBLEM SIMULATOR STARTED", "TITLE")
    config.log("="*60)
    config.log(f"Log file: {config.log_dir}", 'DEBUG')
    config.log(f"Results directory: {results_dir}", 'DEBUG')
    config.log(f"Configuration: debug={config['debug']}, randomize_pos={config['randomize_positions']}, calc_sizes={config['calculate_sizes']}", 'DEBUG')
    
    bodies, trajectories = validate_and_retry(config, results_dir, frames)
    
    config.log("\nFINAL STATE OF BODIES:")
    for body in bodies:
        config.log(str(body) + "\n")
    
    config.log("\nGENERATING VISUALIZATIONS...")
    config.log("Starting trajectory generation", "DEBUG")
    
    dpi = config['plot_dpi']
    hq = config['high_quality_plots']
    
    config.log("Generating trajectory plot...", "DEBUG")
    plot_trajectories(trajectories, bodies, results_dir, dpi, hq)
    config.log("Trajectory plot complete", "DEBUG")
    
    config.log("Generating distance plot...", "DEBUG")
    plot_distances(trajectories, bodies, results_dir, dpi, hq)
    config.log("Distance plot complete", "DEBUG")
    
    config.log("Generating velocity plot...", "DEBUG")
    plot_velocities(trajectories, bodies, results_dir, dpi, hq)
    config.log("Velocity plot complete", "DEBUG")

    config.log('Saving frames as video...', "DEBUG")
    video_from_frames(frames, results_dir, fps=10)
    config.log('Video saved successfully', "DEBUG")
    
    config.log("="*60)
    config.log("SIMULATION COMPLETE - All files saved successfully!", "TITLE")
    config.log("="*60)


if __name__ == '__main__':
    main()

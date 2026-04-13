from typing import List, Tuple, Dict
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from os import path
from phisicBody import Body
import cv2

plt.ion()
fig, ax = plt.subplots(figsize=(10, 10))

def plot_trajectories(trajectories: Dict, bodies: List[Body], 
                     results_dir: str, dpi: int, hq: bool) -> None:
    plt.figure(figsize=(14, 10) if hq else (12, 8))
    
    for body in bodies:
        x, y = trajectories[body.name]['x'], trajectories[body.name]['y']
        
        plt.plot(x, y, label=body.name, color=body.color, alpha=0.8, 
                linewidth=2 if hq else 1.5)
        
        plt.scatter(x[0], y[0], color=body.color, marker='o', 
                   s=body.size if hq else 100, edgecolors='black', 
                   linewidth=2.5, zorder=5, label=f'{body.name} (start)')
        
        plt.scatter(x[-1], y[-1], color=body.color, marker='*',
                   s=body.size*1.2 if hq else 500, edgecolors='black',
                   linewidth=2.5, zorder=5, label=f'{body.name} (end)')
    
    plt.xlabel('X (units)', fontsize=14, fontweight='bold')
    plt.ylabel('Y (units)', fontsize=14, fontweight='bold')
    plt.title('Orbital Trajectories (○=Start, ★=End)', fontsize=16, fontweight='bold', pad=20)
    plt.legend(loc='best', fontsize=11, framealpha=0.95)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.axis('equal')
    plt.tight_layout()
    
    output = path.join(results_dir, 'trajectories.png')
    plt.savefig(output, dpi=dpi, bbox_inches='tight', facecolor='white')


def plot_distances(trajectories: Dict, bodies: List[Body],
                  results_dir: str, dpi: int, hq: bool) -> None:
    plt.figure(figsize=(14, 8) if hq else (12, 6))
    
    names = [b.name for b in bodies]
    pairs = [(0, 1), (0, 2), (1, 2)]
    
    for (i, j) in enumerate(pairs):
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


def video_from_frames(saved_frames: list, results_dir: str, fps: int = 10) -> None:
    height, width, _ = saved_frames[0].shape
    video_path = os.path.join(results_dir, 'simulation.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
    for frame in saved_frames:
        video.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    video.release()


def plot_config(bodies : list, grid_w: float, grid_h: float) -> None:
    
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlabel('X (units)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Y (units)', fontsize=12, fontweight='bold')
    ax.set_title(f'Three Body Problem', fontsize=14, fontweight='bold') 
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_aspect('equal', adjustable='box')
    xs = [body.position['x'] for body in bodies]
    ys = [body.position['y'] for body in bodies]
    ax.set_xlim(min(-10, (min(xs) - 10)), max((grid_w + 10), (max(xs) + 10)))
    ax.set_ylim(min(-10, (min(ys) - 10)), max((grid_h + 10), (max(ys) + 10)))
    return None


def save_frame(bodies: List[Body], saved_frames: list, dpi: int) -> List:
    for body in bodies:
        ax.scatter(body.position['x'], body.position['y'],
            s=body.size, color=body.color, alpha=0.8, edgecolors='black', 
            linewidth=1.5, label=body.name)
        ax.scatter(body.position['x'], body.position['y'],
                s=body.size, color=body.color, alpha=0.8,
                edgecolors='black', linewidth=1.5, label=body.name)
    ax.figure.set_dpi(dpi)
    fig.canvas.flush_events()
     
    frame = ax.get_figure()
    width, height = frame.canvas.get_width_height()
    img = np.frombuffer(frame.canvas.tostring_argb(), dtype=np.uint8)
    img = img.reshape((height, width, 4))
    img = img[:, :, 1:] 
    saved_frames.append(img)
    
    ax.clear()
    return saved_frames


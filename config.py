from configparser import ConfigParser
import os
from typing import Dict, Any
from datetime import datetime

class Config:

    DEFAULTS = {
        # Simulation settings
        'randomize_positions': False,
        'calculate_sizes': True,
        'end_on_collision': False,
        'size_scale_factor': 20,
        'debug': True,
        'simulation_cycles': 100000000,
        'body_mask' : 1.5,
        'min_velocity': -0.2,
        'max_velocity': 0.2,
        # Visualization settings
        'time_step': 0.01,
        'grid_width': 300,
        'grid_height': 300,
        'scale_factor': 0.1,
        'plot_dpi': 200,
        # Output settings
        'save_plots': True,
        'high_quality_plots': True,
        'collision_distance': 1.5,
        'frame_interval': 1500,
        'min_frames': 15,
        'max_retries': 30,
    }

    def __init__(self, config_file: str = 'config.ini'):
        self.config_file = config_file
        self.results_dir = None
        self.log_dir = None
        self.data = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        config = ConfigParser()
        try:
            config.read(self.config_file)
            data = self._parse_config(config)
            self.log(f"Config loaded successfully from '{self.config_file}'.", "INFO")
            return data
        except Exception as e:
            self.log(f"Error loading config: {e}. Using defaults.", "ERROR")
            return self.DEFAULTS


    def setup_output_directories(self) -> tuple[str, str]:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results_dir = f"resultados_{timestamp}"
        self.log_dir = os.path.join(self.results_dir, 'logs')
        DIRS = [self.results_dir, self.log_dir]
        for dir in DIRS:
            if not os.path.exists(dir):
                os.makedirs(dir)

        print(f"[INFO] Output directory: {self.results_dir}")
        return self.results_dir

    def log(self, message: str, level: str = "INFO") -> None:
        print(f"[{datetime.now()}][{level}] {message}")
        if level == "DEBUG" and not self.data.get('debug', False):
            return
        try:
            log_file = os.path.join(self.log_dir, 'simulation.log')
            with open(log_file, 'a') as f:
                f.write(f"[{datetime.now()}][{level}] {message}\n")
        except Exception as e:
            print(f"[ERROR] Failed to write log: {e}")

    def _parse_config(self, config: ConfigParser) -> Dict[str, Any]:
        data = {}

        # Simulation settings
        data['simulation_cycles'] = config.getint(
            'SIMULATION', 'simulation_cycles', fallback=self.DEFAULTS['simulation_cycles'])
        data['time_step'] = config.getfloat(
            'SIMULATION', 'time_step', fallback=self.DEFAULTS['time_step'])
        data['randomize_positions'] = config.getboolean(
            'SIMULATION', 'randomize_positions', fallback=self.DEFAULTS['randomize_positions'])
        data['calculate_sizes'] = config.getboolean(
            'SIMULATION', 'calculate_sizes', fallback=self.DEFAULTS['calculate_sizes'])
        data['debug'] = config.getboolean(
            'SIMULATION', 'debug', fallback=self.DEFAULTS['debug'])
        data['size_scale_factor'] = config.getfloat(
            'SIMULATION', 'size_scale_factor', fallback=self.DEFAULTS['size_scale_factor'])
        data['min_velocity'] = config.getfloat(
            'SIMULATION', 'min_velocity', fallback=self.DEFAULTS['min_velocity'])
        data['max_velocity'] = config.getfloat(
            'SIMULATION', 'max_velocity', fallback=self.DEFAULTS['max_velocity'])
        data['end_on_collision'] = config.getboolean(
            'SIMULATION', 'end_on_collision', fallback=self.DEFAULTS['end_on_collision'])
        
        # Visualization settings
        data['grid_width'] = config.getint(
            'VISUALIZATION', 'grid_width', fallback=self.DEFAULTS['grid_width'])
        data['grid_height'] = config.getint(
            'VISUALIZATION', 'grid_height', fallback=self.DEFAULTS['grid_height'])
        data['scale_factor'] = config.getfloat(
            'VISUALIZATION', 'scale_factor', fallback=self.DEFAULTS['scale_factor'])
        data['plot_dpi'] = config.getint(
            'VISUALIZATION', 'plot_dpi', fallback=self.DEFAULTS['plot_dpi'])
        data['save_plots'] = config.getboolean(
            'VISUALIZATION', 'save_plots', fallback=self.DEFAULTS['save_plots'])
        data['high_quality_plots'] = config.getboolean(
            'VISUALIZATION', 'high_quality_plots', fallback=self.DEFAULTS['high_quality_plots'])
        
        # Physics settings
        data['collision_distance'] = config.getfloat(
            'SIMULATION', 'collision_distance', fallback=self.DEFAULTS['collision_distance'])
        data['frame_interval'] = config.getint(
            'OUTPUT', 'frame_interval', fallback=self.DEFAULTS['frame_interval'])
        data['min_frames'] = config.getint(
            'OUTPUT', 'min_frames', fallback=self.DEFAULTS['min_frames'])
        data['max_retries'] = config.getint(
            'OUTPUT', 'max_retries', fallback=self.DEFAULTS['max_retries'])
        
        data['bodies'] = []
        for section in config.sections():
            if section != 'SIMULATION' and section != 'VISUALIZATION' and section != 'OUTPUT':
                data[section] = {
                    'name': section,
                    'mass': config.getfloat(section, 'mass'),
                    'pos_x': config.getfloat(section, 'pos_x'),
                    'pos_y': config.getfloat(section, 'pos_y'),
                    'vel_x': config.getfloat(section, 'vel_x'),
                    'vel_y': config.getfloat(section, 'vel_y')
                }
                data['bodies'].append(data[section])
        return data
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)
    
    def __getitem__(self, key: str) -> Any:
        return self.get(key)
    
    def __contains__(self, key: str) -> bool:
        return key in self.data

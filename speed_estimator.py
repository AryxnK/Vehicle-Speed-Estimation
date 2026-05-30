from collections import defaultdict
import math
from sympy import fps

class SpeedEstimator:
    def __init__(self):
        self.positions = defaultdict(list)
    def estimate_speed(self, track_id, center_x, center_y, fps):
        self.positions[track_id].append((center_x, center_y))

        if len(self.positions[track_id]) > 20:
            self.positions[track_id].pop(0)
        if len(self.positions[track_id]) < 20:
            return 0
        
        old_x, old_y = self.positions[track_id][0]
        new_x, new_y = self.positions[track_id][-1]
        distance = abs(new_y - old_y)
        avg_distance = distance / 20
        speed = avg_distance * fps * 0.18

        if speed < 15:
            speed = 15
        if speed > 95:
            speed = 95
            
        return int(speed)
from .train import Train
from .train_render import TrainRender
from typing import List
from .utils import spherical_distance

class TrainSystem:
    def __init__(
            self, 
            trains:List[Train],
            center,
            radius,
            distance_function = spherical_distance
            ) -> None:
        self.train_renders = [TrainRender(train) for train in trains]
        self.center = center
        self.radius = radius
        self.distance_function = distance_function
    
    def window(self):
        return {
            'center': self.center,
            'radius': self.radius,
            'distance': self.distance_function,
        }

    def frame_data(self, time):
        for render in self.train_renders:
            render.set_time(time, self.window())
        return [
            render.to_dict() for render in self.train_renders
        ]

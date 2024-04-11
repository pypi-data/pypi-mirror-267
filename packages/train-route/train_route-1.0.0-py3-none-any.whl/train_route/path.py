from typing import List
import bisect

from .segment import Segment
from .utils import cumsum, state

class Path:
    def __init__(self, path_id, segments:List[Segment]) -> None:
        self.id = path_id
        self.segments = segments
        
        self.cumulative_distances = cumsum(segment.total_distance for segment in segments)
        self.total_distance = self.cumulative_distances[-1]

    def position(self, progress):
        if progress < 0 or progress > self.total_distance:
            raise BaseException(
                f'Position outside segment: {progress} not in [{0}, {self.total_distance}]'
            )
        index = bisect.bisect_left(self.cumulative_distances, progress)
        if index == len(self.cumulative_distances):
            raise BaseException(
                f'Debug: Bisect should return valid index from 0 to len - 1'
            )
        if index == 0:
            segment_progress_start = 0.
        else:
            segment_progress_start = self.cumulative_distances[index - 1]
        segment_progress = progress - segment_progress_start
        return self.segments[index].position(segment_progress)
    
    def chain_state(self, chain_progress):
        positions = [self.position(progress) for progress in chain_progress]
        positions_start = positions[:-1]
        positions_end = positions[1:]
        return [state(start, end) for start, end in zip(positions_start, positions_end)]

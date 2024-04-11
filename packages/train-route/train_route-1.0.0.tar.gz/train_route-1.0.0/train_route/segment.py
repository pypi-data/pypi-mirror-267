import bisect

from .utils import cumulative_distance, interpolate

class Segment:
    "Segment is used for inner paths with missing time points"
    def __init__(self, 
                 segment_id, 
                 source, 
                 target, 
                 latitudes, 
                 longitudes, 
                 cumulative_distances = None
                 ) -> None:
        self.id = segment_id
        self.source = source
        self.target = target
        self.latitudes = latitudes
        self.longitudes = longitudes
        if cumulative_distances:
            self.cumulative_distances = cumulative_distances
        else:
            self.cumulative_distances = cumulative_distance(latitudes, longitudes)
        self.total_distance = self.cumulative_distances[-1]
    
    def position(self, progress):
        if progress < 0 or progress > self.total_distance:
            if abs(progress - self.total_distance) < 1e-8:
                return [self.latitudes[-1], self.longitudes[-1]]
            raise BaseException(
                f'Position outside segment: {progress} not in [{0}, {self.total_distance}]'
            )
        if progress == 0:
            return [self.latitudes[0], self.longitudes[0]]
        index = bisect.bisect_left(self.cumulative_distances, progress)
        if index == 0 or index == len(self.cumulative_distances):
            raise BaseException(
                f'Debug: Bisect should return valid index from 1 to len - 1'
            )
        d0 = self.cumulative_distances[index - 1]
        d1 = self.cumulative_distances[index]
        delta = (progress - d0) / (d1 - d0)
        if delta < 0 or delta > 1:
            raise BaseException(
                f'Debug: delta ({delta}) should be between 0 and 1: d0 = {d0}, d1 = {d1}'
            )
        latitude = interpolate(self.latitudes, index, delta)
        longitude = interpolate(self.longitudes, index, delta)
        return [latitude, longitude]
    
    def position_from_ratio(self, progress_ratio):
        if progress_ratio < 0 or progress_ratio > 1:
            raise BaseException(
                f'Debug: progress ratio ({progress_ratio}) should be between 0 and 1'
            )
        progress = self.total_distance * progress_ratio
        return self.position(progress)

    def to_dict(self):
        return {
            'segment_id': self.segment_id,
            'source': self.source,
            'target': self.target,
            'latitudes': self.latitudes,
            'longitudes': self.longitudes,
            'cumulative_distances': list(self.cumulative_distances),
        }
    
    def to_ref(self):
        return self.segment_id
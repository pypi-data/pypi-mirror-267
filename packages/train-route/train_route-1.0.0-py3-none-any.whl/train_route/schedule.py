import bisect

from train_route.path import Path

class Schedule:
    def __init__(self, schedule_id, path:Path, progress_points:list, timestamps:list) -> None:
        self.id = schedule_id
        self.path = path
        self.progress_points = progress_points
        self.timestamps = timestamps

        self.start_time = timestamps[0]
        self.end_time = timestamps[-1]

    def progress(self, time):
        if time < self.start_time or time > self.end_time:
            raise BaseException(
                f'Time outside schedule: {time} not in [{self.start_time}, {self.end_time}]'
            )
        if time == self.start_time:
            return self.progress_points[0]
        index = bisect.bisect_left(self.timestamps, time)
        if index == 0 or index == len(self.timestamps):
            raise BaseException(
                f'Debug: Bisect should return valid index from 1 to len - 1'
            )
        t0 = self.timestamps[index - 1]
        t1 = self.timestamps[index]
        delta_t = (time - t0) / (t1 - t0)
        if delta_t < 0 or delta_t > 1:
            raise BaseException(
                f'Debug: delta ({delta_t}) should be between 0 and 1: t0 = {t0}, t1 = {t1}'
            )
        p0 = self.progress_points[index - 1]
        p1 = self.progress_points[index]
        return p0 + delta_t * (p1 - p0)
    
    def position(self, time):
        progress = self.progress(time)
        return self.path.position(progress)
    
    def chain_state(self, time, chain_relative_progress):
        progress = self.progress(time)
        chain_progress = [progress + p for p in chain_relative_progress]
        return self.path.chain_state(chain_progress)
    
    def is_valid(self, time):
        "test if time is valid"
        return time >= self.start_time and time <= self.end_time

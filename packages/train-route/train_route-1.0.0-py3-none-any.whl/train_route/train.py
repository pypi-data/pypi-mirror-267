from train_route.schedule import Schedule

class Train():
    def __init__(
            self,
            train_id,
            schedule:Schedule,
            chain_relative_progress:list,
            start
    ) -> None:
        self.id = train_id
        self.schedule = schedule
        self.chain_relative_progress = chain_relative_progress
        self.start = start
        self.length = abs(chain_relative_progress[0] - chain_relative_progress[-1])

    def position(self, time):
        "position of head of chain"
        relative_time = time - self.start
        return self.schedule.position(relative_time)
    
    def chain_state(self, time):
        "state of chain"
        relative_time = time - self.start
        return self.schedule.chain_state(relative_time, self.chain_relative_progress)
    
    def is_active(self, time):
        "test if train has position"
        relative_time = time - self.start
        if not self.schedule.is_valid(relative_time):
            return False
        progress = self.schedule.progress(relative_time)
        if progress < self.length:
            return False
        return True
    

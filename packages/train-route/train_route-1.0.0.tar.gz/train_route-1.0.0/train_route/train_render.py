from .train import Train
from .utils import is_inside

class TrainRender:
    def __init__(self, train:Train) -> None:
        self.train = train
        self.current_position = None
        self.chain_state = None
        "position on screen"
        self.status:str = 'new'
    
    def set_time(self, time, window):
        if not self.train.is_active(time):
            self.status = 'inactive'
            return
            
        position = self.train.position(time)
        if self.current_position is None:
            self.status = 'active'
            self.current_position = position
            if self.train.length > 0.01 * window['radius']:
                self.chain_state = self.train.chain_state(time)
            else:
                self.chain_state = None
            return
        if position == self.current_position:
            self.status = 'sleep'
            return
        if not (is_inside(self.current_position, window) or is_inside(position, window)):
            self.status = 'sleep'
            return

        self.status = 'active'
        self.current_position = position
        if self.train.length > 0.01 * window['radius']:
            self.chain_state = self.train.chain_state(time)
        else:
            self.chain_state = None

    def to_dict(self):
        result = {
            'train_id': self.train.id,
            'status': self.status,
        }
        if self.status == 'active':
            result['position'] = self.current_position
            result['chain_state'] = self.chain_state
        return result

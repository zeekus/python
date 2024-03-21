#thread runs every six seconds and makes a recording.
class Listener(object):
    def start_stream(self):
        self.stream = self.input.open(**self._config)
    def record(self):
        """"""
        frames=[]
        while len(frames) < self.n_frames
            frames.append(
                   self.stream.read(self._config["frames_per_buffer"])
            )
        return np.fromstring(b''.join(frames),i dtype=np.int16)

from .Processor import Processor

class Generator(Processor):
    def __init__(self, name):
        super(Generator, self).__init__(name)
        self.is_generator = True

        # Variables for keeping track of progress.
        self.total = 0
        self.count = 0

    # These methods could/should be implemented by inheriting classes:

    # on_startup(self)
    # on_shutdown(self)
    # on_abort(self)
    # on_tick(self)
    # on_suspend(self)
    # on_resume(self)

    # If on_tick finishes on its own without external stop call, call self.stop() from there when done.

    def end_tick_reason(self):
        "If 'aborted', 'stopping' or not 'running'. 'suspended' is not a reason to leave the tick; handle this yourself."
        return self.aborted or self.stopping or not self.running
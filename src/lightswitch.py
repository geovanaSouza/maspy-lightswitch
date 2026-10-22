from maspy import *

class LightSwitch(Environment):
    def __init__(self):
        super().__init__()

class Flipper(Agent):
    @pl(gain, Goal("flipSwitch"))
    def flipSwitch(self, src):
        self.print("Flip Switch")
        self.stop_cycle()

if __name__ == "__main__":
    env = LightSwitch()
    ag = Flipper()
    ag.add(Goal("flipSwitch"))
    Admin().start_system()
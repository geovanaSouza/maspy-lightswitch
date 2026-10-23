from maspy import *
from maspy.learning import *

class LightSwitch(Environment):
    def __init__(self):
        super().__init__()
        self.create(Percept("switch", ("on", "off"), listed))

    ACTION_TO_STATE = {
        "turn_on": "on",
        "turn_off": "off"
    }

    def switch_transition(self, state: dict, action: str):
        current_state = state["switch"]
        target_state = self.ACTION_TO_STATE[action]
        
        reward = 1 if current_state != target_state else -1
        
        state["switch"] = target_state
        
        return state, reward

    @action(listed, ("turn_on", "turn_off"), switch_transition)
    def switch_light(self, agt, action: str):
        switch_percept = self.get(Percept("switch"), ck_values=False)

        current_state = switch_percept.values
        target_state = self.ACTION_TO_STATE[action]
        
        self.change(switch_percept, values=target_state)
        self.print(f"{agt} switched to {target_state} (was {current_state})")

class Flipper(Agent):
    @pl(gain, Goal("flipSwitch"))
    def flipSwitch(self, src):
        self.print("Fliping Switch")
        best_action = self.get_best_action("LightSwitch")
        if best_action is not None:
            action, _ = best_action
            self.switch_light(action)
        self.stop_cycle()

if __name__ == "__main__":
    # Define environment
    env = LightSwitch()
    print(env.percept_list)

    # Define model
    model = EnvModel(env, show_learning=True)
    model.learn(qlearning, max_steps=50, num_episodes=100)
    print("actions:", model.actions_list)
    print("states: ", model.states_list)
    print(dict(model.q_table))

    # Define agent
    ag = Flipper()
    ag.add_policy(model)
    ag.add(Goal("flipSwitch"))

    # Start simulation
    Admin().start_system()
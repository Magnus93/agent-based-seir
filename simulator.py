from agents import * 

class Simulator:
    def __init__(self, spec): 
        self.time = 0
        self.time_end = 5000
        self.timestep = 0.25 
        self.agents = Agents(spec) 
        self.prev_NS = self.agents["S"]
        self.prev_NE = self.agents["E"]
        self.prev_NI = self.agents["I"]
        self.prev_NR = self.agents["R"]
        
    def run(self, print_every=True, print_end=True):
        while(self.time <= self.time_end and self.agents["E"] + self.agents["I"] > 0):
            self.agents.step(self.timestep)
            if (print_every):
                if (self.prev_NS != self.agents["S"] or self.prev_NI != self.agents["I"] or self.prev_NR != self.agents["R"]):
                    print("t = {}:\t agents = {}".format(self.time, self.agents)) 
                self.prev_NS = self.agents["S"]
                self.prev_NE = self.agents["E"]
                self.prev_NI = self.agents["I"]
                self.prev_NR = self.agents["R"]

            self.time += self.timestep 

        if (print_end):
            print("==================")
            print("Duration: {} days \nEpidemic size: {}".format(self.time, self.agents["R"]))
    
    def get_results(self):
        return { "duration": self.time , "epidemic": self.agents["R"] } 

    def reset(self):
        self.agents.reset() 
        self.time = 0 
        self.prev_NS = self.agents["S"]
        self.prev_NI = self.agents["I"]
        self.prev_NR = self.agents["R"]

if __name__ == "__main__":
    
    specs = [
    {"amount": 500, "init_stage": "S", "p": 1/5000,}, 
    {"amount": 500, "init_stage": "S", "p": 1/15000,}, 
    {"amount": 1, "init_stage": "E"}
    ]
    sim = Simulator(specs)
    sim.run() 

    

    
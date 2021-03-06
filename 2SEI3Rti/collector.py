# collects results from multible simulations 
from simulator import * 
import random 
import math 
import pandas as pd 
import statistics
import time 
from aux_functions import * 
from prob import * 
import matplotlib.pyplot as plt  

class Collector:
    def __init__(self): 
        self.init_seed = 1236 
        random.seed(self.init_seed)

        # number of susceptibles at start 
        self.NS = 1000

        self.epidemic_limit = 0.1*self.NS 
        self.print_every = 10 
        self.skip_non_epidemics = False

        self.table = pd.DataFrame(columns = ['Duration', 'Epidemic', 'ep_high', 'ep_low', 'Rt'])

        # count the number of replications 
        self.i = 0  
        self.skipped = 0 
        self.below_epidemic_limit = 0 

    def set_skip_non_epidemics(bool_value):
        self.skip_non_epidemics = bool_value  

    def new_sim(self):
        self.NS_high = binomial(self.NS, 0.5) 
        self.NS_low = self.NS - self.NS_high 
        pop_specs = [
            { "amount": self.NS_high, "init_stage": "S", "p": 1/5000, "group_name": "high_risk" }, 
            { "amount": self.NS_low, "init_stage": "S", "p": 1/15000, "group_name": "low_risk" }, 
            { "amount": 1, "init_stage": "E" }
        ]
        return Simulator(pop_specs)

    def step(self):
        self.sim = self.new_sim() 
        self.sim.run(print_every=False)

        epidemic_size = self.NS - self.sim.get_num("S")

        if (self.skip_non_epidemics and epidemic_size < self.epidemic_limit):
            self.skipped += 1 
        else:
            self.i += 1 
            self.table.loc[len(self.table)] = [
                self.sim.time,
                epidemic_size,
                self.NS_high - self.sim.get_num("S", "high_risk"),
                self.NS_low - self.sim.get_num("S", "low_risk"),
                self.sim.get_num("S", "low_risk") * 15 * 1/15000 + self.sim.get_num("S", "high_risk") * 15 * 1/5000
            ] 
            if (epidemic_size < self.epidemic_limit):
                self.below_epidemic_limit += 1  
            
            if self.i%self.print_every == 0 and self.i != 0:
                time_past = time.time() - self.start_time 
                eta =  time_past*(self.num_reps - self.i) / self.i
                string = "iteration {} \t".format(self.i)
                string += "eta {} \t".format(sec_to_str(eta))
                print(string) 
                print("Epidemic avg: {}".format(statistics.mean(self.table["Epidemic"].tolist())))

    def run(self, num_reps):
        self.start_time = time.time()
        self.num_reps = num_reps 
        while self.i < self.num_reps:
            self.step()

        exec_time = time.time() - self.start_time
        print("####### Collection DONE #######")
        print("Exec. time: \t{}".format(sec_to_str(exec_time)))
        print("num. repl.: \t{}".format(self.i))
        print("Skipped replications: \t{}".format(self.skipped)) 
        print("Replications without epidemics: \t{}".format(self.below_epidemic_limit))
        print("timestep: \t{}".format(self.sim.timestep)) 
        
        filename = save_pandas_dataframe_as_csv(self.table, "abm-data-seed"+str(self.init_seed)+"-"+str(self.num_reps))
        print("Table saved as: {}".format(filename))

if __name__ == "__main__":
    import sys
    num_reps = 30 
    if len(sys.argv) >= 2:
        num_reps = int(sys.argv[1])

    collector = Collector() 
    collector.run(num_reps)
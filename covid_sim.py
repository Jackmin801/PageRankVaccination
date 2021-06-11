import matplotlib.pyplot as plt
import numpy as np
import random
import sys
input = sys.stdin.readline

class System():
    def __init__(self, nodes, edges, vaccinated, infectious_period, infection_probability):
        # Constants
        self.nodes = nodes
        self.edges = edges
        self.vaccinated = vaccinated
        self.infectious_period = infectious_period
        self.infection_probability = infection_probability

        # Inits
        self.adj = None
        self.immune = {}
        self.day = 0
        self.new_cases = 0
        self.active_cases = []
        self.frontier = []
        self.gen_natural()
        self.R = [0]*nodes
        self.R_0 = 0
        self.R_n = 0

    def gen_natural(self):
        """ Generate natural daily infection order """
        self.natural_infection = [i for i in range(self.nodes)]
        random.shuffle(self.natural_infection)

    def infect(self, p):
        """ Attempt to infect node p """
        if p in self.immune:
            return False
        else:
            self.frontier.append((p, self.infectious_period))
            self.immune.add(p)
            self.new_cases += 1
            return True

    def step(self):
        """ Process the day """
        self.new_cases = 0
        self.frontier = []
        # Infect the sad person
        self.infect(self.natural_infection[self.day])
        # Process active cases
        for case,period in self.active_cases:
            if period == 0:
                self.R_0 = self.R_0*(0.95) + self.R[case]*(0.05)
                if self.R_n == 0:
                    self.R_0 = self.R[case]
                self.R_n += 1
                continue
            self.frontier.append((case,period-1))
            if random.randint(0,99) < self.infection_probability:
                target = random.sample(self.adj[case],1)[0]
                if self.infect(target):
                    self.R[case] += 1
        # Move to next day
        self.active_cases = self.frontier
        self.day += 1

    def get_total_cases(self):
        return len(self.immune) - self.vaccinated

    def get_active_cases(self):
        return len(self.active_cases)

def main():
    ##########
    # Inputs #
    ##########
    n_days = int(sys.argv[1])
    pltfile = sys.argv[2]
    random.seed(sys.argv[-1])

    N,E,M = map(int,input().split())
    P,I = map(int,input().split())
    system = System(N,E,M,P,I)
    system.immune = set(map(int,input().split()))
    system.adj = [list(map(int,input().split())) for i in range(N)]

    #####################
    # Statistics stores #
    #####################
    n_active_cases, n_total_cases, n_new_cases, R = [],[],[],[]

    ##############
    # Simulation #
    ##############
    for i in range(n_days):
        system.step()
        n_active_cases.append(system.get_active_cases())
        n_total_cases.append(system.get_total_cases())
        n_new_cases.append(system.new_cases)
        R.append(system.R_0)

    #########    
    # Plots #
    #########
    max_active = max(n_active_cases)
    max_new = max(n_new_cases)
    fig, ax = plt.subplots(4,figsize=(7,15))
    ax[0].plot(np.arange(n_days),n_active_cases)
    ax[1].plot(np.arange(n_days),n_total_cases)
    ax[2].plot(np.arange(n_days),n_new_cases)
    ax[3].plot(np.arange(n_days),R)
    ax[0].set(ylabel="Active cases", title=f"Max active cases = {max_active} , Max new cases = {max_new}")
    ax[1].set(ylabel="Total cases")
    ax[2].set(xlabel="Days",ylabel="New cases")
    ax[3].set(xlabel="Days",ylabel="Exponential rolling average R")
    plt.savefig(pltfile)
    #plt.show()

main()



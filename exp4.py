import numpy as np
import heapq
import random
import matplotlib.pyplot as plt

MODLUS =2147483647
MULT1  =24112
MULT2 =26143

zrng=[         1,
 1973272912, 281629770,  20006270,1280689831,2096730329,1933576050,
  913566091, 246780520,1363774876, 604901985,1511192140,1259851944,
  824064364, 150493284, 242708531,  75253171,1964472944,1202299975,
  233217322,1911216000, 726370533, 403498145, 993232223,1103205531,
  762430696,1922803170,1385516923,  76271663, 413682397, 726466604,
  336157058,1432650381,1120463904, 595778810, 877722890,1046574445,
   68911991,2088367019, 748545416, 622401386,2122378830, 640690903,
 1774806513,2132545692,2079249579,  78130110, 852776735,1187867272,
 1351423507,1645973084,1997049139, 922510944,2045512870, 898585771,
  243649545,1004818771, 773686062, 403188473, 372279877,1901633463,
  498067494,2087759558, 493157915, 597104727,1530940798,1814496276,
  536444882,1663153658, 855503735,  67784357,1432404475, 619691088,
  119025595, 880802310, 176192644,1116780070, 277854671,1366580350,
 1142483975,2026948561,1053920743, 786262391,1792203830,1494667770,
 1923011392,1433700034,1244184613,1147297105, 539712780,1545929719,
  190641742,1645390429, 264907697, 620389253,1502074852, 927711160,
  364849192,2049576050, 638580085, 547070247 ]


def lcgrand( stream) :


    zi     = zrng[stream]
    lowprd = (zi & 65535) * MULT1
    hi31   = (zi >> 16) * MULT1 + (lowprd >> 16)
    zi     = ((lowprd & 65535) - MODLUS) +((hi31 & 32767) << 16) + (hi31 >> 15)
    if zi < 0:
       zi += MODLUS
    
    lowprd = (zi & 65535) * MULT2
    hi31   = (zi >> 16) * MULT2 + (lowprd >> 16)
    zi     = ((lowprd & 65535) - MODLUS) + ((hi31 & 32767) << 16) + (hi31 >> 15)
    if zi < 0:
       zi += MODLUS          
    
    zrng[stream] = zi
    return (zi >> 7 | 1) / 16777216.0



def lcgrandst ( zset,  stream) :            #/* Set the current zrng for stream
                                                    #   "stream" to zset. */
    zrng[stream] = zset

def lcgrandgt ( stream) : #/* Return the current zrng for stream "stream". */

    return zrng[stream]

def exponentialfunction( mean) :                  #/* Exponential variate generation function. */
                                    # /* Return an exponential random variate with mean "mean". */
    return -mean * np.log(lcgrand(1))



def queue_merge(queue,indx):
    
    sort=[]
    for x in range(len(queue)):
        sort.append(queue[x])
    
    if indx>0 and indx<len(queue)-1:
       l=len(queue[indx])
       lf=len(queue[indx-1])
       lr=len(queue[indx+1])
       while (lf-l)>=2 or (lr-l)>=2:
             if lr>=lf:
                m=queue[indx+1].pop()
                sort[indx].append(m)
                lr-=1
                l+=1

             if lf>lr:
                m=queue[indx-1].pop()
                sort[indx].append(m)
                lf-=1
                l+=1 
       return sort  
    elif indx==0 and len(queue)==1:
         return sort
    elif indx==0 and len(queue)>1:
         l=len(queue[indx])
         lr=len(queue[indx+1])

         while (lr-l)>=2 :
               m=queue[indx+1].pop()
               queue[indx].append(m)
               lr-=1
               l+=1
         return queue 
    elif indx>0 and indx==len(queue)-1:
         l=len(queue[indx])
         lf=len(queue[indx-1])

         while (lf-l)>=2 :
               m=queue[indx-1].pop()
               queue[indx].append(m)
               lf-=1
               l+=1         
                     
         return queue        


class Params:
    def __init__(self, lambd, mu, k):
        self.lambd = lambd  # interarrival rate
        self.mu = mu  # service rate
        self.k = k

    def print_analytic_result(self):

        Average_Queue_Length =np.square(self.lambd)/(self.mu*(self.mu-self.lambd))
        Average_Delay_Queue  = self.lambd/(self.mu*(self.mu-self.lambd))
        Server_Utilization_Factor=self.lambd/self.mu 
        print('\n\n\n')
        print('Analytic Avetotal_of_delaysrage  Queue Length: %lf' % (Average_Queue_Length))
        print('Analytic Average Delay in  Queue : %lf' % (Average_Delay_Queue))
        print('Analytic Server Utilization Factor : %lf' % (Server_Utilization_Factor))
    
class States:
    def __init__(self):
        # States
        self.queue = [[]]
        self.server_status=[]
        self.util = 0.0
        self.avgQdelay = 0.0
        self.avgQlength = 0.0
        self.served = 0
        self.total_of_delays = 0.0
        self.area_server_status = 0.0
        self.area_num_in_q=0.0
        self.time_last_event=0.0
        self.num_in_q_in_last_event=0.0
        self.available_server=0
        self.last_average_server_status=0
        self.last_average_queue_length=0

    def update(self, sim, event):

        time_since_last_event=sim.simclock-self.time_last_event
        self.time_last_event=sim.simclock
        average_queue_length=0
        p=0
        while p<len(self.queue):
              average_queue_length+=len(self.queue[p])
              p+=1
        average_queue_length=average_queue_length/len(self.queue) 
        self.area_num_in_q =self.area_num_in_q +(self.last_average_queue_length*time_since_last_event)
        count=0
        average_server_status=0
        for x in range(len(self.server_status)):
            if self.server_status[x]==0:
               count+=1    
        
        if len(self.server_status)>0:
           average_server_status=((len(self.server_status)-count))/len(self.server_status)
        self.area_server_status=self.area_server_status+(self.last_average_server_status*time_since_last_event)
        self.num_in_q_in_last_event=sim.num_in_q
        self.last_average_server_status=average_server_status
        self.last_average_queue_length=average_queue_length

 
    def finish(self, sim):
        self.util = self.area_server_status/(sim.simclock)
        self.avgQdelay = self.total_of_delays/(self.served)
        self.avgQlength = self.area_num_in_q/(sim.simclock)

    def printResults(self, sim):
         #DO NOT CHANGE THESE LINES
        print('MMk Results: lambda = %lf, mu = %lf, k = %d' % (sim.params.lambd, sim.params.mu, sim.params.k))
        print('MMk Total customer served: %d' % (self.served))
        print('MMk Average queue length: %lf' % (self.avgQlength))
        print('MMk Average customer delay in queue: %lf' % (self.avgQdelay))
        print('MMk Time-average server utility: %lf' % (self.util))
    #    sim.params.print_analytic_result()

    def getResults(self, sim):
        return (self.avgQlength, self.avgQdelay, self.util)
class Event:
    def __init__(self, sim):
        self.eventType = None
        self.sim = sim
        self.eventTime = None

    def process(self, sim):
        raise Exception('Unimplemented process method for the event!')


    def __repr__(self):
        return self.eventType
class StartEvent(Event):
    def __init__(self, eventTime, sim):
        self.eventTime = eventTime
        self.eventType = 'START'
        self.sim = sim

    def process(self, sim):
        sim.states.available_server=sim.params.k
        for x in range(sim.params.k-1):
            sim.states.queue.append([])
        for x in range(sim.params.k):
            sim.states.server_status.append(0)
        
        expon=exponentialfunction(1/sim.params.lambd)
        next_arrival_time=sim.simclock+expon
        sim.scheduleEvent(ArrivalEvent(next_arrival_time,sim))
        sim.scheduleEvent(ExitEvent(1000000,sim))
class ExitEvent(Event):
    def __init__(self, eventTime, sim):
        self.eventTime = eventTime
        self.eventType = 'EXIT'
        self.sim = sim

    def process(self, sim):
        print(sim.states.queue)

class ArrivalEvent(Event):

    def __init__(self, eventTime, sim):
        self.eventTime = eventTime
        self.eventType = 'ARRIVAL'
        self.sim = sim

    def process(self, sim):
        expon=exponentialfunction(1/sim.params.lambd)
        next_arrival_time=sim.simclock+expon
        sim.scheduleEvent(ArrivalEvent(next_arrival_time,sim))
        check=0
        n=0
        for x in range(sim.params.k):
            if sim.states.server_status[x]==0:
               sim.states.served+=1
               expon=exponentialfunction(1/sim.params.mu)
               next_arrival_time=sim.simclock+expon
               sim.scheduleEvent(DepartureEvent(next_arrival_time,sim))
               sim.states.server_status[x]=next_arrival_time 
               check=1
               break

        length=[]
        if  check==0:
            for x in range(sim.params.k):
                length.append(len(sim.states.queue[x]))

            indx=-2
            minm=100000000000000000000000000000000000000000000000
            for x in range(sim.params.k):
                if (length[x]<minm):
                    minm=length[x]
                    indx=x
            sim.states.queue[indx].append(sim.simclock)
            expon=exponentialfunction(1/sim.params.mu)
            next_arrival_time=sim.simclock+expon

class DepartureEvent(Event):

    def __init__(self, eventTime, sim):
        self.eventTime = eventTime
        self.eventType = 'DEPARTURE'
        self.sim = sim  
          
    def process(self, sim):

        indx=0
        for x in range(sim.params.k):
            if sim.states.server_status[x]==self.eventTime:
               indx=x
        if len(sim.states.queue[indx])==0:
           sim.states.queue=queue_merge(sim.states.queue,indx)
        if len(sim.states.queue[indx])==0:
           sim.states.server_status[indx]=0       

        if len(sim.states.queue[indx])>0:
           m=sim.states.queue[indx].pop(0)
           delay=sim.simclock-m
           sim.states.total_of_delays =sim.states.total_of_delays +delay
           sim.states.served += 1
           expon=exponentialfunction(1/sim.params.mu)
           next_arrival_time=sim.simclock+expon
           sim.scheduleEvent(DepartureEvent(next_arrival_time,sim))
           sim.states.server_status[indx]=next_arrival_time
class Simulator:
    def __init__(self, seed):
        self.eventQ = []
        self.simclock = 0
        self.seed = seed
        self.params = None
        self.states = None
        self.num_in_q = 0

    def initialize(self):
        self.simclock = 0
        self.scheduleEvent(StartEvent(0, self))

    def configure(self, params, states):
        self.params = params
        self.states = states

    def now(self):
        return self.simclock

    def scheduleEvent(self, event):
        heapq.heappush(self.eventQ, (event.eventTime, event))

    def run(self):
        random.seed(self.seed)
        self.initialize()

        while len(self.eventQ) > 0:
            time, event = heapq.heappop(self.eventQ)

            if event.eventType == 'EXIT':
                break

            if self.states != None:
                self.states.update(self, event)

            #print(event.eventTime, 'Event', event)
            self.simclock = event.eventTime
            event.process(self)

        self.states.finish(self)

    def printResults(self):
        self.states.printResults(self)

    def getResults(self):
        return self.states.getResults(self)


def experiment4(mu,lambd,k,no_of_queue):




    sim = Simulator(100)
    sim.configure(Params(lambd,mu,k), States())
    sim.run()
    result=sim.getResults()
    sim.printResults()
    return result

    '''

    seed = 110
    mu = 8.0 / 60
    lambd = 5.0/60 
    ratios = [u  for u in range(1, 3)]

    avglength = []
    avgdelay = []
    util = []
    

    for ro in ratios:
        sim = Simulator(seed)
        sim.configure(Params(lambd, mu,ro), States())
        sim.run()

        length, delay, utl = sim.getResults()
        avglength.append(length)
        avgdelay.append(delay)
        util.append(utl)
        zrng[1]=19732729123
        sim.printResults()
        print('\n')

    '''



    '''    
    plt.figure(1)
    plt.subplot(311)
    plt.plot(ratios, avglength)
    plt.xlabel('Ratio (K)')
    plt.ylabel('Avg Q length')

    plt.subplot(312)
    plt.plot(ratios, avgdelay)
    plt.xlabel('Ratio (K)')
    plt.ylabel('Avg Q delay (sec)')

    plt.subplot(313)
    plt.plot(ratios, util)
    plt.xlabel('Ratio (K)')
    plt.ylabel('Util')

    plt.show()
    '''
def main():
    experiment4()
   
if __name__ == "__main__":
    main()

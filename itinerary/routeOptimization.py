import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt, math, requests,json
from urllib.parse import urlencode
from .models import Location,Day,Schedule
from .serializers import ScheduleSerializer
api_key = "AIzaSyAPOOnlu8YXdWsyM3uUkz3tU7AeDWgoQqA"

def extract_lat_lng(address_or_postalcode,city, data_type = 'json'):
    endpoint = f"https://maps.googleapis.com/maps/api/geocode/{data_type}"
    params = {"address": address_or_postalcode+","+city, "key": api_key}
    url_params = urlencode(params)
    url = f"{endpoint}?{url_params}"
    r = requests.get(url)
    if r.status_code not in range(200, 299): 
        return {}
    latlng = {}
    try:
        latlng = r.json()['results'][0]['geometry']['location']
    except:
        pass
    return latlng.get("lat"), latlng.get("lng")
    

class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness= 0.0
    
    def routeDistance(self):
        if self.distance ==0:
            pathDistance = 0
            for i in range(0, len(self.route)):
                fromCity = self.route[i]
                toCity = None
                if i + 1 < len(self.route):
                    toCity = self.route[i + 1]
                else:
                    toCity = self.route[0]
                pathDistance += fromCity.distance(toCity)
            self.distance = pathDistance
        return self.distance
    
    def routeFitness(self):
        if self.fitness == 0:
            routeFitness=1 / float(self.routeDistance())
            self.fitness +=routeFitness
           
            timeFitness=0 #out of 10

            breakfastIndex = 0
            lunchIndex = len(self.route)/2
            dinnerIndex = len(self.route)-1
            nightLifeIndex = len(self.route)-2

            meals = 0
            for index,loc in enumerate(self.route):
                if(loc.type=="restaurants"):
                    meals+=1
                    
                    if(meals==1):
                        timeFitness-=abs(breakfastIndex-index)*routeFitness
                    elif(meals==2):
                        
                        timeFitness-=abs(lunchIndex-index)*routeFitness
                    else:
                        timeFitness-=abs(dinnerIndex-index)*routeFitness
                elif(loc.type=="nightlife"):
                    timeFitness-=abs(nightLifeIndex-index)*routeFitness
            timeFitness*=0.25
            self.fitness+=timeFitness
        
        return self.fitness

def createRoute(locList):
    route = random.sample(locList, len(locList))
    return route


def initialPopulation(popSize, locList):
    population = []

    for i in range(0, popSize):
        population.append(createRoute(locList))
    return population

def rankRoutes(population):
    fitnessResults = {}
    for i in range(0,len(population)):
        fitnessResults[i] = Fitness(population[i]).routeFitness()
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)


def selection(popRanked, eliteSize):
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100*random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i,3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults

def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool

def breed(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []
    
    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))
    
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])
        
    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    return child

def breedPopulation(matingpool, eliteSize):
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0,eliteSize):
        children.append(matingpool[i])
    
    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool)-i-1])
        children.append(child)
    return children

def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))
            
            city1 = individual[swapped]
            city2 = individual[swapWith]
            
            individual[swapped] = city2
            individual[swapWith] = city1
    return individual
def mutatePopulation(population, mutationRate):
    mutatedPop = []
    
    for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop
def nextGeneration(currentGen, eliteSize, mutationRate):
    popRanked = rankRoutes(currentGen)
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, eliteSize)
    nextGeneration = mutatePopulation(children, mutationRate)
    return nextGeneration

def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations):
    pop = initialPopulation(popSize, population)
    print("Initial distance: " + str(1 / rankRoutes(pop)[0][1]))
    
    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate)
    
    print("Final distance: " + str(1 / rankRoutes(pop)[0][1]))
    bestRouteIndex = rankRoutes(pop)[0][0]
    bestRoute = pop[bestRouteIndex]
    return bestRoute

def geneticAlgorithmPlot(population, popSize, eliteSize, mutationRate, generations):
    pop = initialPopulation(popSize, population)
    progress = []
    progress.append(1 / rankRoutes(pop)[0][1])
    
    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate)
        progress.append(1 / rankRoutes(pop)[0][1])
    
    plt.plot(progress)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.show()
def createSchedule(num_days,city,origin):
    landmarks=[]    
    with open('./cityLandmarks.json') as f:
        landmarks = json.load(f)[city]
    visit_count = {
        "attractions":random.randint(3,4),
        "nightlife":1,
        "restaurants":3,
        "entertainment":1,
        "shopping":1,


    }
    transportation="Car, "
    transportation+=", ".join(random.sample(landmarks["transportation"],2))
    curSchedule = Schedule(city=city,transportation=transportation,hotel=random.sample(landmarks["hotels"],1)[0], origin=origin,length=num_days)#add tranportation and hotels and num days
    curSchedule.save()
    for day in range(num_days):
        destinations=[]
        curDay = Day(schedule=curSchedule)
        curDay.save()
        for key in landmarks:
            if key != "hotels" and key!="transportation":
                print(len(landmarks[key]))
                for i in [landmarks[key].pop(random.randrange(len(landmarks[key]))) for _ in range(visit_count[key])]:
                    lat,lng = extract_lat_lng(i,city)
                    loc=Location(lat=lat,lng=lng,name=i,type=key,day=curDay)
                    
                    destinations.append(loc)
                    #famous plans,bugs with ariport, change airport, get hotel price and payment,check all features

                    #signup my completed trips and comment and have recommended bsaed on previous  and complete events
        #TODEO
        #didnt add bank account - log in, subscribable plans, pay for bookings
        #comments and reviews
        #editable/customizable #customize plan by removing locations and seeing best and worst reviews
        #human assisted booking
        #https://app.eightydays.me/magic/B43uHafV35DTSkEQDPoXldKhuXgBAbnEo0clm7oTdjRaP
        #add road trip option or travel by trains - different travel options and routes
        #ideathon/ hackathon
        #chooseable flights
        #book restaurants and hotel charge extra
        #details - flight arrival time all recommended stuff


        #add hotel bookings or link
        #flight search
        #shuttle buses, rental cars
        #add review and rating after "i went here" and add pay and schedule
        #get popular schedules for destination -premade trips
        #touches to look
        #enter adjective and go instead

        

        result = geneticAlgorithm(population=destinations, popSize=50, eliteSize=5, mutationRate=0.01, generations=100)
        for index,x in enumerate(result):
            x.order=index
            x.save()

    return curSchedule.id



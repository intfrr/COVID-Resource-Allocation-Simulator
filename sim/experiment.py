from env import Location, Simulation, AgentFactory
from agent import Agent
import pandas as pd
import itertools

# ==============================================================
# ADJUST PARAMETERS HERE
parameter_names = [
    'time_req_entrance',
    'time_req_pharmacy',
    'time_req_registration',
    'time_req_waiting_area',
    'size_entrance_x',
    'size_entrance_y',
    'size_pharmacy_x',
    'size_pharmacy_y',
    'size_registration_x',
    'size_registration_y',
    'size_waiting_area_x',
    'size_waiting_area_y',
    'creation_rate',
    'infected_rate',
]

experiment_parameters = {
    # Time required
    'time_req_entrance': [10],
    'time_req_pharmacy': [15],
    'time_req_registration': [20],
    'time_req_waiting_area': [60],

    # Size of locations
    'size_entrance_x': [20],
    'size_entrance_y': [10],

    'size_pharmacy_x': [8],
    'size_pharmacy_y': [8],

    'size_registration_x': [5],
    'size_registration_y': [5],

    'size_waiting_area_x': [10],
    'size_waiting_area_y': [10],

    # Agent properties
    'creation_rate': [10, 9, 8, 7],
    'infected_rate': [0.1, 0.2, 0.3, 0.4],
}
# DO NOT CHANGE ANYTHING BEYOND THIS POINT
# ==============================================================


def initialise_experiment(**parameters):
    # Initialise the environment graph
    entrance = Location("Entrance",
                        size=(parameters['size_entrance_x'], parameters['size_entrance_y']),
                        time_required=parameters['time_req_entrance'],
                        position=(400, 400))
    pharmacy = Location("Pharmacy",
                        size=(parameters['size_pharmacy_x'], parameters['size_pharmacy_y']),
                        time_required=parameters['time_req_pharmacy'],
                        position=(100, 100))
    registration = Location("Registration",
                            size=(parameters['size_registration_x'], parameters['size_registration_y']),
                            time_required=parameters['time_req_registration'],
                            position=(100, 500))
    waiting_area = Location("Waiting Area",
                            size=(parameters['size_waiting_area_x'], parameters['size_waiting_area_y']),
                            time_required=parameters['time_req_waiting_area'],
                            position=(500, 100))

    entrance.add_adj_room(coord=(0, 0), node=pharmacy)
    entrance.add_adj_room(coord=(0, parameters['size_entrance_y']), node=registration)
    entrance.add_adj_room(coord=(parameters['size_entrance_x']//2, 0), node=waiting_area)
    pharmacy.add_adj_room(coord=(parameters['size_pharmacy_x'], parameters['size_pharmacy_y']//2), node=entrance)
    registration.add_adj_room(coord=(parameters['size_registration_x'], 0), node=entrance)
    waiting_area.add_adj_room(coord=(parameters['size_waiting_area_x']//2, parameters['size_waiting_area_y']), node=entrance)
    locations = [entrance, registration, waiting_area, pharmacy]

    # Journeys
    journeys = [
        [entrance, pharmacy, entrance],
        [entrance, registration, entrance],
        [entrance, registration, entrance, pharmacy, entrance],
        [entrance, registration, entrance, waiting_area, entrance, pharmacy, entrance],
    ]

    # Agent Creation
    agent_factory = AgentFactory(creation_rate=parameters['creation_rate'],
                                 infected_rate=parameters['infected_rate'],
                                 journeys=journeys,
                                 entrance=entrance)

    return entrance, agent_factory

# ============= Run Experiment ============
experiment_data = {}
statistic_names = ['transmissions', 'agents', 'average_transmissions']
for stat in parameter_names + statistic_names:
    experiment_data[stat] = []


parameters = [experiment_parameters[para] for para in parameter_names]
for parameter_list in list(itertools.product(*parameters)):
    parameter_set = {}
    for i, para in enumerate(parameter_names):
        parameter_set[para] = parameter_list[i]

    # Add experiment parameters to experiment data
    for para in parameter_set:
        experiment_data[para].append(parameter_set[para])

    # Run simulation
    entrance, agent_factory = initialise_experiment(**parameter_set)
    sim = Simulation(location=entrance, agents=[])
    sim.run(agent_factory=agent_factory,
            epoch=1000)
    sim.print_statistics()

    # Add experiment statistics to experiment data
    for stat in statistic_names:
        experiment_data[stat].append(sim.statistics[stat])

pd.DataFrame(experiment_data).to_csv("data.csv", index=False)
from initialiser import *


# Helper processes
agent_factory = AgentFactory(creation_rate=10,
                             infected_rate=0.1,
                             journeys=journeys,
                             entrance=entrance)
renderer = Renderer(locations=locations,
                    agents=[],
                    delay=0.1)

# Run simulation
sim = Simulation(location=entrance, agents=[])
sim.run(agent_factory=agent_factory,
        renderer=renderer,
        epoch=1000,
        verbose=True)

# sim.run(agent_factory=agent_factory,
#         renderer=None,
#         epoch=1000,
#         verbose=True)
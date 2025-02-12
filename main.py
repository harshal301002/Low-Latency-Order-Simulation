#!/usr/bin/env python3
import time
from simulator.simulator import MarketSimulator
from simulator.logger import logger

def main():
    logger.info("Starting low-latency order execution simulator...")

    # Create a market simulator
    market_simulator = MarketSimulator()

    # Initialize the market simulator
    market_simulator.initialize()

    # Run the simulation loop
    # In a real scenario, this might listen to a live feed or an internal queue.
    try:
        while True:
            market_simulator.run_tick()
            time.sleep(0.1)  # Sleep or poll frequency for events in the simulation
    except KeyboardInterrupt:
        logger.info("Simulation interrupted by user.")
    finally:
        market_simulator.shutdown()

if __name__ == "__main__":
    main()

from Environment import Environment, Status
from Agents import StudentRobot, RandomRobot
import argparse

class SimulationRunner:
        
    def run(Robots, VisualizeSimulation=False):
        env = Environment()
        while env.game_status == Status.ONGOING:
            current_Robot = Robots[env.current_player]
            action = current_Robot.get_action(env)
            env.drop_piece(action)
            
            if VisualizeSimulation:
                print(f"Player {env.current_player} placed in column {action}")
                env.print_board()
        print(f"Game result: {env.game_status} wins!")        
        return env.game_status
    
    def run_trials(Robots, trials, visualizeSimulation):
        results = {Status.YELLOW: 0, Status.RED: 0, Status.DRAW: 0}
        for _ in range(trials):
            result = SimulationRunner.run(Robots, visualizeSimulation)
            results[result] += 1
        return results
    
    def main(visualizeSimulation, trials):
        
        robots = { Status.YELLOW: StudentRobot(), Status.RED: RandomRobot() }
        if trials == 1:
            SimulationRunner.run(robots, visualizeSimulation)
        else:
            results = SimulationRunner.run_trials(robots, trials, visualizeSimulation)
            print(f"Wins: {results[Status.YELLOW]} Losses: {results[Status.RED]} Draws: {results[Status.DRAW]}")
            
        

if __name__ == "__main__":
    # Argument parser
    parser = argparse.ArgumentParser(description="Robot Agent/Env Simulation.")
    parser.add_argument(
        "--visualizeSimulation", 
        action="store_true", 
        help="Enable board output after every turn"
    )   
    parser.add_argument(
        "--trials", 
        type=int, 
        default=1, 
        help="Enable multiple trials for the game"
    )

    # Parse arguments
    args = parser.parse_args()

    # Run Simulation
    SimulationRunner.main(args.visualizeSimulation, args.trials)
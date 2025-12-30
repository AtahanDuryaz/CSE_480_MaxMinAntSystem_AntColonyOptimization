"""
MMAS TSP Experiment Orchestrator
=================================
Runs multiple independent MMAS trials and aggregates results.

Usage:
    python experiment/main.py <instance_name>
    
Examples:
    python experiment/main.py validation
    python experiment/main.py eil51
"""

import sys
import os
import time
import random

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.tsp_utils import (
    get_validation_cities,
    parse_tsplib,
    calculate_distance_matrix,
    get_tour_length
)
from core.mmas import MMAS
from core.config import get_config
from experiment.results_tracker import ResultsTracker
from experiment.visualizer import Visualizer


def load_tsp_instance(instance_name, config):
    """
    Load TSP instance coordinates based on instance name.
    
    Args:
        instance_name (str): Instance identifier
        config (dict): Configuration dictionary
        
    Returns:
        tuple: (coordinates, instance_info_dict)
    """
    if instance_name == 'validation':
        # Use hardcoded validation dataset
        coordinates = get_validation_cities()
        info = {
            'name': 'Validation 5-city',
            'dimension': len(coordinates),
            'source': 'hardcoded'
        }
    else:
        # Load from TSPLIB file
        instance_path = config['instance_path']
        if not os.path.exists(instance_path):
            raise FileNotFoundError(f"Instance file not found: {instance_path}")
        
        parsed_data = parse_tsplib(instance_path)
        coordinates = parsed_data['coordinates']
        info = {
            'name': parsed_data['name'],
            'dimension': parsed_data['dimension'],
            'source': instance_path
        }
    
    return coordinates, info


def run_single_trial(distance_matrix, config, seed, trial_number):
    """
    Execute a single MMAS trial with a specific random seed.
    
    Args:
        distance_matrix (list): 2D distance matrix
        config (dict): Configuration parameters
        seed (int): Random seed for reproducibility
        trial_number (int): Trial identifier (1-based)
        
    Returns:
        dict: Trial results containing:
            - trial_number: Trial identifier
            - seed: Random seed used
            - best_cost: Best tour cost found
            - best_tour: Best tour (list of city indices)
            - best_cost_per_iteration: Convergence history
            - stagnation_counter: Final stagnation counter
            - runtime: Execution time in seconds
    """
    # Set random seed for reproducibility
    random.seed(seed)
    
    # Create MMAS instance
    mmas = MMAS(
        distance_matrix=distance_matrix,
        n_ants=config['n_ants'],
        alpha=config['alpha'],
        beta=config['beta'],
        rho=config['rho'],
        max_iterations=config['max_iterations'],
        stagnation_limit=config['stagnation_limit']
    )
    
    # Run algorithm and measure time
    start_time = time.time()
    result = mmas.run()
    runtime = time.time() - start_time
    
    # Package results
    return {
        'trial_number': trial_number,
        'seed': seed,
        'best_cost': result['best_cost'],
        'best_tour': result['best_tour'],
        'best_cost_per_iteration': result['best_cost_per_iteration'],
        'stagnation_counter': result['stagnation_counter'],
        'runtime': runtime
    }


def print_trial_summary(trial_result):
    """
    Print summary of a single trial.
    
    Args:
        trial_result (dict): Trial results dictionary
    """
    print(f"  Trial {trial_result['trial_number']}: "
          f"Cost = {trial_result['best_cost']:.4f}, "
          f"Time = {trial_result['runtime']:.2f}s, "
          f"Seed = {trial_result['seed']}")


def print_overall_summary(all_results, instance_info, config):
    """
    Print aggregated statistics across all trials.
    
    Args:
        all_results (list): List of trial result dictionaries
        instance_info (dict): TSP instance information
        config (dict): Configuration parameters
    """
    costs = [r['best_cost'] for r in all_results]
    runtimes = [r['runtime'] for r in all_results]
    
    best_idx = costs.index(min(costs))
    worst_idx = costs.index(max(costs))
    
    mean_cost = sum(costs) / len(costs)
    std_cost = (sum((c - mean_cost) ** 2 for c in costs) / len(costs)) ** 0.5
    
    print("\n" + "=" * 70)
    print("OVERALL SUMMARY")
    print("=" * 70)
    print(f"Instance: {instance_info['name']} ({instance_info['dimension']} cities)")
    print(f"Trials: {len(all_results)}")
    print(f"Parameters: n_ants={config['n_ants']}, α={config['alpha']}, "
          f"β={config['beta']}, ρ={config['rho']}")
    print(f"Max iterations: {config['max_iterations']}, "
          f"Stagnation limit: {config['stagnation_limit']}")
    print(f"Rounding: {'NINT (EUC_2D)' if config['round_result'] else 'None (floating-point)'}")
    
    if config.get('expected_optimum'):
        print(f"Known optimum: {config['expected_optimum']}")
    
    print("\nResults:")
    print(f"  Best cost:    {min(costs):.4f} (Trial {best_idx + 1})")
    print(f"  Worst cost:   {max(costs):.4f} (Trial {worst_idx + 1})")
    print(f"  Mean cost:    {mean_cost:.4f}")
    print(f"  Std dev:      {std_cost:.4f}")
    print(f"  Mean runtime: {sum(runtimes) / len(runtimes):.2f}s")
    
    if config.get('expected_optimum'):
        best_gap = ((min(costs) - config['expected_optimum']) / 
                   config['expected_optimum'] * 100)
        mean_gap = ((mean_cost - config['expected_optimum']) / 
                   config['expected_optimum'] * 100)
        print(f"  Best gap:     {best_gap:.2f}%")
        print(f"  Mean gap:     {mean_gap:.2f}%")
    
    print("=" * 70)


def main():
    """
    Main experiment orchestrator.
    
    Workflow:
    1. Parse command-line arguments
    2. Load TSP instance and configuration
    3. Build distance matrix
    4. Run 5 independent trials with different seeds
    5. Aggregate and display results
    6. (Placeholder) Save results and generate plots
    """
    # Parse command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python experiment/main.py <instance_name>")
        print("Available instances: validation, test5, eil51")
        sys.exit(1)
    
    instance_name = sys.argv[1]
    
    print("=" * 70)
    print(f"MMAS TSP Experiment: {instance_name}")
    print("=" * 70)
    
    # Load configuration
    try:
        config = get_config(instance_name)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Load TSP instance
    print("\nLoading TSP instance...")
    coordinates, instance_info = load_tsp_instance(instance_name, config)
    print(f"  Instance: {instance_info['name']}")
    print(f"  Cities: {instance_info['dimension']}")
    print(f"  Source: {instance_info['source']}")
    
    # Build distance matrix
    print(f"\nBuilding distance matrix (round_result={config['round_result']})...")
    distance_matrix = calculate_distance_matrix(
        coordinates,
        round_result=config['round_result']
    )
    print(f"  Matrix size: {len(distance_matrix)}x{len(distance_matrix)}")
    
    # Run 5 independent trials
    print("\nRunning 5 independent trials...")
    print("-" * 70)
    
    N_TRIALS = 5
    BASE_SEED = 42
    all_results = []
    
    for trial_num in range(1, N_TRIALS + 1):
        seed = BASE_SEED + trial_num
        trial_result = run_single_trial(
            distance_matrix=distance_matrix,
            config=config,
            seed=seed,
            trial_number=trial_num
        )
        all_results.append(trial_result)
        print_trial_summary(trial_result)
    
    print("-" * 70)
    
    # Print overall summary
    print_overall_summary(all_results, instance_info, config)
    
    # ========================================================================
    # Results Tracking and Persistence (STEP 5)
    # ========================================================================
    print("\nSaving results...")
    results_tracker = ResultsTracker(instance_name)
    for result in all_results:
        results_tracker.add_run(result['trial_number'], result)
    results_tracker.save_to_csv(f'outputs/results/{instance_name}_results.csv')
    results_tracker.save_to_json(f'outputs/results/{instance_name}_results.json')
    
    # ========================================================================
    # Visualization (STEP 6)
    # ========================================================================
    print("\nGenerating plots...")
    
    # Plot convergence curves for all runs
    Visualizer.plot_multiple_runs(
        all_results,
        title=f"Convergence - {instance_info['name']}",
        save_path=f"outputs/plots/{instance_name}_convergence.png"
    )
    
    # Plot best tour
    best_run = results_tracker.get_best_run()
    Visualizer.plot_tour(
        coordinates,
        best_run['best_tour'],
        best_run['best_cost'],
        title=f"Best Tour - {instance_info['name']}",
        save_path=f"outputs/plots/{instance_name}_tour.png"
    )
    
    print(f"\nExperiment completed for {instance_name}.")


if __name__ == '__main__':
    main()

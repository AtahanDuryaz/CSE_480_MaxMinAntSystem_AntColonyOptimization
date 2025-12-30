"""
Results Tracker Module
======================
Aggregates and persists multi-run experiment results.

Functionality:
- Collect results from multiple independent trials
- Compute summary statistics (mean, std, min, max)
- Export to CSV and JSON formats
"""

import json
import csv
import os
import statistics


class ResultsTracker:
    """
    Track and aggregate results from multiple MMAS trials.
    
    Args:
        instance_name (str): Name of the TSP instance being solved
    """
    
    def __init__(self, instance_name):
        self.instance_name = instance_name
        self.runs = []  # List of individual run results
    
    def add_run(self, run_id, result):
        """
        Add results from a single trial.
        
        Args:
            run_id (int): Trial identifier (1-based)
            result (dict): Trial results containing:
                - trial_number: Trial identifier
                - seed: Random seed used
                - best_cost: Best tour cost found
                - best_tour: Best tour (list of city indices)
                - best_cost_per_iteration: Convergence history (list)
                - stagnation_counter: Final stagnation counter
                - runtime: Execution time in seconds
        """
        self.runs.append({
            'run_id': run_id,
            'seed': result['seed'],
            'best_cost': result['best_cost'],
            'best_tour': result['best_tour'],
            'convergence_history': result['best_cost_per_iteration'],
            'stagnation_counter': result['stagnation_counter'],
            'runtime': result['runtime'],
            'iterations_completed': len(result['best_cost_per_iteration'])
        })
    
    def get_statistics(self):
        """
        Compute summary statistics across all trials.
        
        Returns:
            dict: Statistics containing:
                - n_runs: Number of trials
                - best_cost: Minimum cost across all trials
                - worst_cost: Maximum cost across all trials
                - mean_cost: Average cost
                - std_cost: Standard deviation of costs
                - median_cost: Median cost
                - best_tour: Tour corresponding to best cost
                - best_run_id: Trial number with best cost
                - mean_runtime: Average runtime
                - total_runtime: Sum of all runtimes
        """
        if not self.runs:
            return None
        
        costs = [run['best_cost'] for run in self.runs]
        runtimes = [run['runtime'] for run in self.runs]
        
        # Find best and worst runs
        best_idx = costs.index(min(costs))
        worst_idx = costs.index(max(costs))
        
        return {
            'n_runs': len(self.runs),
            'best_cost': min(costs),
            'worst_cost': max(costs),
            'mean_cost': statistics.mean(costs),
            'std_cost': statistics.stdev(costs) if len(costs) > 1 else 0.0,
            'median_cost': statistics.median(costs),
            'best_tour': self.runs[best_idx]['best_tour'],
            'best_run_id': self.runs[best_idx]['run_id'],
            'worst_run_id': self.runs[worst_idx]['run_id'],
            'mean_runtime': statistics.mean(runtimes),
            'total_runtime': sum(runtimes)
        }
    
    def save_to_csv(self, filepath):
        """
        Save results to CSV file.
        
        Format: One row per trial with summary statistics
        
        Args:
            filepath (str): Output CSV file path
        """
        # Ensure output directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Prepare data for CSV
        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = [
                'run_id',
                'seed',
                'best_cost',
                'runtime',
                'iterations_completed',
                'stagnation_counter',
                'tour'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write individual runs
            for run in self.runs:
                writer.writerow({
                    'run_id': run['run_id'],
                    'seed': run['seed'],
                    'best_cost': run['best_cost'],
                    'runtime': run['runtime'],
                    'iterations_completed': run['iterations_completed'],
                    'stagnation_counter': run['stagnation_counter'],
                    'tour': ' '.join(map(str, run['best_tour']))
                })
            
            # Write summary statistics
            stats = self.get_statistics()
            if stats:
                writer.writerow({})  # Empty row separator
                writer.writerow({
                    'run_id': 'SUMMARY',
                    'seed': '',
                    'best_cost': f"Best: {stats['best_cost']:.4f}",
                    'runtime': f"Mean: {stats['mean_runtime']:.2f}s",
                    'iterations_completed': '',
                    'stagnation_counter': '',
                    'tour': ''
                })
                writer.writerow({
                    'run_id': '',
                    'seed': '',
                    'best_cost': f"Mean: {stats['mean_cost']:.4f}",
                    'runtime': f"Total: {stats['total_runtime']:.2f}s",
                    'iterations_completed': '',
                    'stagnation_counter': '',
                    'tour': ''
                })
                writer.writerow({
                    'run_id': '',
                    'seed': '',
                    'best_cost': f"Std: {stats['std_cost']:.4f}",
                    'runtime': '',
                    'iterations_completed': '',
                    'stagnation_counter': '',
                    'tour': ''
                })
        
        print(f"Results saved to CSV: {filepath}")
    
    def save_to_json(self, filepath):
        """
        Save results to JSON file.
        
        Format: Structured JSON with individual runs and summary statistics
        
        Args:
            filepath (str): Output JSON file path
        """
        # Ensure output directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Prepare data structure
        data = {
            'instance_name': self.instance_name,
            'n_runs': len(self.runs),
            'runs': self.runs,
            'statistics': self.get_statistics()
        }
        
        # Write to JSON file
        with open(filepath, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=2)
        
        print(f"Results saved to JSON: {filepath}")
    
    def get_convergence_data(self):
        """
        Extract convergence histories from all trials.
        
        Useful for plotting multiple convergence curves.
        
        Returns:
            list: List of convergence histories, one per trial
                  Each history is a list of best costs per iteration
        """
        return [run['convergence_history'] for run in self.runs]
    
    def get_best_run(self):
        """
        Get the complete result from the best trial.
        
        Returns:
            dict: Best run's complete result dictionary
        """
        if not self.runs:
            return None
        
        costs = [run['best_cost'] for run in self.runs]
        best_idx = costs.index(min(costs))
        return self.runs[best_idx]

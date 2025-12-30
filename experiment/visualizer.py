"""
Visualizer Module
=================
Generate plots for MMAS TSP experiments.

Functionality:
- Convergence plots (multi-run)
- Tour visualization
"""

import matplotlib.pyplot as plt
import os


class Visualizer:
    """
    Visualization utilities for MMAS TSP experiments.
    """
    
    @staticmethod
    def plot_multiple_runs(all_results, title, save_path):
        """
        Plot convergence curves for multiple MMAS runs.
        
        Args:
            all_results (list): List of trial result dictionaries
            title (str): Plot title
            save_path (str): File path to save the plot
        """
        # Ensure output directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Create figure
        plt.figure(figsize=(10, 6))
        
        # Plot convergence curve for each run
        for result in all_results:
            convergence_history = result['best_cost_per_iteration']
            iterations = range(len(convergence_history))
            plt.plot(iterations, convergence_history, 
                    label=f"Trial {result['trial_number']}", 
                    alpha=0.7)
        
        # Configure plot
        plt.xlabel('Iteration', fontsize=12)
        plt.ylabel('Best Cost', fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.legend(loc='best')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Save to file
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Convergence plot saved: {save_path}")
    
    @staticmethod
    def plot_tour(coordinates, tour, cost, title, save_path):
        """
        Plot TSP tour as a 2D visualization.
        
        Args:
            coordinates (list): List of (x, y) tuples for city coordinates
            tour (list): Tour as list of city indices
            cost (float): Tour cost
            title (str): Plot title
            save_path (str): File path to save the plot
        """
        # Ensure output directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Create figure
        plt.figure(figsize=(10, 8))
        
        # Extract x and y coordinates
        x_coords = [coordinates[i][0] for i in range(len(coordinates))]
        y_coords = [coordinates[i][1] for i in range(len(coordinates))]
        
        # Plot cities as scatter points
        plt.scatter(x_coords, y_coords, c='red', s=100, zorder=3, label='Cities')
        
        # Plot tour edges
        for i in range(len(tour)):
            from_city = tour[i]
            to_city = tour[(i + 1) % len(tour)]  # Wrap around to complete tour
            
            x_from, y_from = coordinates[from_city]
            x_to, y_to = coordinates[to_city]
            
            plt.plot([x_from, x_to], [y_from, y_to], 'b-', alpha=0.6, linewidth=1.5)
        
        # Annotate cities with their indices
        for i, (x, y) in enumerate(coordinates):
            plt.annotate(str(i), (x, y), textcoords="offset points", 
                        xytext=(0, 8), ha='center', fontsize=9)
        
        # Configure plot
        plt.xlabel('X Coordinate', fontsize=12)
        plt.ylabel('Y Coordinate', fontsize=12)
        plt.title(f"{title}\nTour Cost: {cost:.4f}", fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.axis('equal')
        plt.tight_layout()
        
        # Save to file
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Tour plot saved: {save_path}")

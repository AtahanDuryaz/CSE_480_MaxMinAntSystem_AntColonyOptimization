"""
Max-Min Ant System (MMAS) Core Algorithm
=========================================
Implements the MMAS algorithm for TSP.

Algorithm characteristics:
- Blind learning (no greedy shortcuts during search)
- Pheromone bounds (tau_min, tau_max)
- Iteration-best vs global-best pheromone update switching
"""

import random
import math


class MMAS:
    """
    Max-Min Ant System for TSP.
    
    Args:
        distance_matrix (list): 2D distance matrix
        n_ants (int): Number of ants per iteration
        alpha (float): Pheromone importance (default: 1)
        beta (float): Heuristic importance (default: 3)
        rho (float): Evaporation rate (default: 0.1)
        max_iterations (int): Maximum number of iterations (default: 200)
        stagnation_limit (int): Stagnation counter limit (default: 20)
    """
    
    def __init__(self, distance_matrix, n_ants, alpha=1, beta=3, rho=0.1,
                 max_iterations=200, stagnation_limit=20):
        self.distance_matrix = distance_matrix
        self.n_cities = len(distance_matrix)
        self.n_ants = n_ants
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.max_iterations = max_iterations
        self.stagnation_limit = stagnation_limit
        
        # Heuristic information (eta_ij = 1 / distance_ij)
        self.eta = [[0.0 for _ in range(self.n_cities)] for _ in range(self.n_cities)]
        for i in range(self.n_cities):
            for j in range(self.n_cities):
                if i != j and distance_matrix[i][j] > 0:
                    self.eta[i][j] = 1.0 / distance_matrix[i][j]
        
        # Initialize pheromone matrix using nearest-neighbor heuristic
        self.pheromone = None
        self.tau_min = None
        self.tau_max = None
        self._initialize_pheromones()
        
        # Best solutions tracking
        self.global_best_tour = None
        self.global_best_cost = float('inf')
        self.best_cost_per_iteration = []
        
        # Stagnation tracking
        self.stagnation_counter = 0
    
    def _initialize_pheromones(self):
        """
        Initialize pheromone matrix using nearest-neighbor heuristic.
        
        tau_0 = 1 / (n_cities * L_nn)
        where L_nn is the tour length from nearest-neighbor construction.
        """
        # Construct nearest-neighbor tour (used ONLY for initialization)
        nn_tour = self._nearest_neighbor_tour()
        nn_cost = self._calculate_tour_cost(nn_tour)
        
        # Initial pheromone level
        tau_0 = 1.0 / (self.n_cities * nn_cost)
        
        # Initialize all edges with tau_0
        self.pheromone = [[tau_0 for _ in range(self.n_cities)] 
                          for _ in range(self.n_cities)]
        
        # Initialize bounds
        self.tau_max = tau_0
        self.tau_min = tau_0 / (2 * self.n_cities)
    
    def _nearest_neighbor_tour(self):
        """
        Construct a tour using nearest-neighbor heuristic.
        Used ONLY for pheromone initialization.
        
        Returns:
            list: Tour as list of city indices
        """
        unvisited = set(range(self.n_cities))
        current = random.choice(list(unvisited))
        tour = [current]
        unvisited.remove(current)
        
        while unvisited:
            nearest = min(unvisited, 
                         key=lambda city: self.distance_matrix[current][city])
            tour.append(nearest)
            unvisited.remove(nearest)
            current = nearest
        
        return tour
    
    def _calculate_tour_cost(self, tour):
        """
        Calculate total cost of a tour.
        
        Args:
            tour (list): List of city indices
            
        Returns:
            float: Total tour cost
        """
        cost = 0.0
        n = len(tour)
        for i in range(n):
            from_city = tour[i]
            to_city = tour[(i + 1) % n]
            cost += self.distance_matrix[from_city][to_city]
        return cost
    
    def _construct_ant_solution(self):
        """
        Construct a solution for one ant using probabilistic transition rule.
        
        P_ij = (tau_ij^alpha * eta_ij^beta) / sum(...)
        
        Returns:
            list: Tour as list of city indices
        """
        # Start from random city
        current = random.randint(0, self.n_cities - 1)
        tour = [current]
        unvisited = set(range(self.n_cities))
        unvisited.remove(current)
        
        # Construct tour by visiting all cities
        while unvisited:
            next_city = self._select_next_city(current, unvisited)
            tour.append(next_city)
            unvisited.remove(next_city)
            current = next_city
        
        return tour
    
    def _select_next_city(self, current, unvisited):
        """
        Select next city using probabilistic transition rule.
        
        Args:
            current (int): Current city index
            unvisited (set): Set of unvisited city indices
            
        Returns:
            int: Selected next city index
        """
        # Calculate probabilities for all unvisited cities
        probabilities = []
        cities = list(unvisited)
        
        for city in cities:
            tau = self.pheromone[current][city]
            eta = self.eta[current][city]
            # P_ij proportional to tau_ij^alpha * eta_ij^beta
            prob = (tau ** self.alpha) * (eta ** self.beta)
            probabilities.append(prob)
        
        # Normalize probabilities
        total = sum(probabilities)
        if total > 0:
            probabilities = [p / total for p in probabilities]
        else:
            # Fallback to uniform distribution if all probabilities are 0
            probabilities = [1.0 / len(cities) for _ in cities]
        
        # Select city based on probabilities
        selected = random.choices(cities, weights=probabilities, k=1)[0]
        return selected
    
    def _evaporate_pheromones(self):
        """
        Apply pheromone evaporation to all edges.
        
        tau_ij = (1 - rho) * tau_ij
        """
        for i in range(self.n_cities):
            for j in range(self.n_cities):
                self.pheromone[i][j] *= (1 - self.rho)
    
    def _deposit_pheromones(self, tour, cost):
        """
        Deposit pheromones for a given tour.
        
        Args:
            tour (list): Tour as list of city indices
            cost (float): Tour cost
        """
        delta_tau = 1.0 / cost
        
        n = len(tour)
        for i in range(n):
            from_city = tour[i]
            to_city = tour[(i + 1) % n]
            self.pheromone[from_city][to_city] += delta_tau
            self.pheromone[to_city][from_city] += delta_tau
    
    def _update_pheromone_bounds(self):
        """
        Update pheromone bounds based on current global best.
        
        tau_max = 1 / (rho * C_best)
        tau_min = tau_max / (2 * n_cities)
        """
        self.tau_max = 1.0 / (self.rho * self.global_best_cost)
        self.tau_min = self.tau_max / (2 * self.n_cities)
    
    def _clamp_pheromones(self):
        """
        Clamp all pheromone values to [tau_min, tau_max].
        """
        for i in range(self.n_cities):
            for j in range(self.n_cities):
                if self.pheromone[i][j] < self.tau_min:
                    self.pheromone[i][j] = self.tau_min
                elif self.pheromone[i][j] > self.tau_max:
                    self.pheromone[i][j] = self.tau_max
    
    def run(self):
        """
        Run the MMAS algorithm.
        
        Pheromone update strategy:
        - First 50% iterations: iteration-best ant deposits
        - Remaining iterations: global-best ant deposits
        
        Returns:
            dict: Results containing:
                - best_tour: Best tour found
                - best_cost: Best tour cost
                - best_cost_per_iteration: Best cost at each iteration
                - stagnation_counter: Final stagnation counter value
        """
        iteration_switch = self.max_iterations // 2
        
        for iteration in range(self.max_iterations):
            # Construct solutions for all ants
            iteration_best_tour = None
            iteration_best_cost = float('inf')
            
            for ant in range(self.n_ants):
                tour = self._construct_ant_solution()
                cost = self._calculate_tour_cost(tour)
                
                # Track iteration-best
                if cost < iteration_best_cost:
                    iteration_best_cost = cost
                    iteration_best_tour = tour
                
                # Track global-best
                if cost < self.global_best_cost:
                    self.global_best_cost = cost
                    self.global_best_tour = tour
                    self.stagnation_counter = 0
                    # Update bounds immediately after new global-best is found
                    self._update_pheromone_bounds()
            
            # Record best cost for this iteration
            self.best_cost_per_iteration.append(self.global_best_cost)
            
            # Increment stagnation counter if no improvement
            if iteration_best_cost >= self.global_best_cost:
                self.stagnation_counter += 1
            
            # Evaporate pheromones
            self._evaporate_pheromones()
            
            
            # Deposit pheromones based on update strategy
            if iteration < iteration_switch:
                # First 50% iterations: iteration-best deposits
                self._deposit_pheromones(iteration_best_tour, iteration_best_cost)
            else:
                # Remaining iterations: global-best deposits
                self._deposit_pheromones(self.global_best_tour, self.global_best_cost)
            
            # Clamp pheromones to [tau_min, tau_max]
            self._clamp_pheromones()
            if self.stagnation_counter>=self.stagnation_limit:
                print(f"Stagnation reached at iteration {iteration}. Stopping...")
                break
        
        return {
            'best_tour': self.global_best_tour,
            'best_cost': self.global_best_cost,
            'best_cost_per_iteration': self.best_cost_per_iteration,
            'stagnation_counter': self.stagnation_counter
        }

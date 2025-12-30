"""
Configuration Management Module
================================
Centralized parameter configuration for different TSP instances.

Locked parameters:
- α (alpha) = 1
- β (beta) = 3
- ρ (rho) = 0.1
- max_iterations = 200
- stagnation_limit = 20
"""


def get_config(instance_name):
    """
    Get configuration parameters for a specific TSP instance.
    
    Args:
        instance_name (str): Instance identifier
            - 'validation': 5-city hardcoded validation
            - 'test5': 5-city TSPLIB format test
            - 'eil51': TSPLIB eil51 benchmark
            
    Returns:
        dict: Configuration dictionary with keys:
            - n_ants: Number of ants per iteration
            - alpha: Pheromone importance (LOCKED: 1)
            - beta: Heuristic importance (LOCKED: 3)
            - rho: Evaporation rate (LOCKED: 0.1)
            - max_iterations: Maximum iterations (LOCKED: 200)
            - stagnation_limit: Stagnation counter limit (LOCKED: 20)
            - round_result: Whether to apply NINT rounding to distances
            - instance_path: Path to instance file (None for validation)
    """
    # Locked parameters (DO NOT CHANGE)
    ALPHA = 1
    BETA = 3
    RHO = 0.1
    MAX_ITERATIONS = 200
    STAGNATION_LIMIT = 20
    
    configs = {
        'validation': {
            'n_ants': 5,
            'alpha': ALPHA,
            'beta': BETA,
            'rho': RHO,
            'max_iterations': MAX_ITERATIONS,
            'stagnation_limit': STAGNATION_LIMIT,
            'round_result': False,  # Floating-point distances
            'instance_path': None,  # Uses hardcoded coordinates
            'expected_optimum': None  # Unknown for validation
        },
        
        'test5': {
            'n_ants': 5,
            'alpha': ALPHA,
            'beta': BETA,
            'rho': RHO,
            'max_iterations': MAX_ITERATIONS,
            'stagnation_limit': STAGNATION_LIMIT,
            'round_result': False,  # Floating-point distances
            'instance_path': 'benchmarks/small/test5.tsp',
            'expected_optimum': None  # Unknown
        },
        
        'eil51': {
            'n_ants': 10,
            'alpha': ALPHA,
            'beta': BETA,
            'rho': RHO,
            'max_iterations': MAX_ITERATIONS,
            'stagnation_limit': STAGNATION_LIMIT,
            'round_result': True,  # EUC_2D with NINT rounding
            'instance_path': 'benchmarks/tsplib/eil51.tsp',
            'expected_optimum': 426  # Known optimal tour length
        },
        'lin105': {
            'n_ants': 105,
            'alpha': ALPHA,
            'beta': BETA,
            'rho': RHO,
            'max_iterations': MAX_ITERATIONS,
            'stagnation_limit': STAGNATION_LIMIT,
            'round_result': True,  # EUC_2D with NINT rounding
            'instance_path': 'benchmarks/tsplib/lin105.tsp',
            'expected_optimum': 14379  # Known optimal tour length
        },
        'berlin52': {
            'n_ants': 15,
            'alpha': ALPHA,
            'beta': BETA,
            'rho': RHO,
            'max_iterations': MAX_ITERATIONS,
            'stagnation_limit': STAGNATION_LIMIT,
            'round_result': True,  # EUC_2D with NINT rounding
            'instance_path': 'benchmarks/tsplib/berlin52.tsp',
            'expected_optimum': 7542  # Known optimal tour length
        },
        'pr152': {
            'n_ants': 107,
            'alpha': ALPHA,
            'beta': BETA,
            'rho': RHO,
            'max_iterations': MAX_ITERATIONS,
            'stagnation_limit': STAGNATION_LIMIT,
            'round_result': True,  # EUC_2D with NINT rounding
            'instance_path': 'benchmarks/tsplib/pr152.tsp',
            'expected_optimum': 73542  # Known optimal tour length
        }
        

    }
    
    if instance_name not in configs:
        raise ValueError(f"Unknown instance: {instance_name}. "
                        f"Available: {list(configs.keys())}")
    
    return configs[instance_name]

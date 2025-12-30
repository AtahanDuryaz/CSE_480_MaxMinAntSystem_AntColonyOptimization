"""
TSP Utilities Module
====================
Provides infrastructure for TSP instance handling:
- TSPLIB file parsing
- Distance matrix computation (Euclidean)
- Validation dataset
"""

import math


# ============================================================================
# VALIDATION DATASET
# ============================================================================

def get_validation_cities():
    """
    Returns hardcoded 5-city validation dataset.
    
    Coordinates: (0,0), (4,0), (4,3), (0,3), (2,1.5)
    
    Returns:
        list: List of (x, y) coordinate tuples
    """
    return [
        (0, 0),
        (4, 0),
        (4, 3),
        (0, 3),
        (2, 1.5)
    ]


# ============================================================================
# TSPLIB PARSER
# ============================================================================

def parse_tsplib(filepath):
    """
    Parse TSPLIB format file.
    
    Reads:
    - NAME
    - DIMENSION
    - NODE_COORD_SECTION
    - EOF
    
    Ignores all other fields.
    
    Args:
        filepath (str): Path to .tsp file
        
    Returns:
        dict: Parsed data with keys 'name', 'dimension', 'coordinates'
              coordinates is a list of (x, y) tuples
    """
    name = None
    dimension = None
    coordinates = []
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Parse NAME
        if line.startswith('NAME'):
            name = line.split(':', 1)[1].strip()
        
        # Parse DIMENSION
        elif line.startswith('DIMENSION'):
            dimension = int(line.split(':', 1)[1].strip())
        
        # Parse NODE_COORD_SECTION
        elif line == 'NODE_COORD_SECTION':
            i += 1
            while i < len(lines):
                line = lines[i].strip()
                if line == 'EOF' or line == '':
                    break
                parts = line.split()
                if len(parts) >= 3:
                    #parts[0] is node ID, parts[1] is x, parts[2] is y
                    x = float(parts[1])
                    y = float(parts[2])
                    coordinates.append((x, y))
                i += 1
            continue
        
        # Stop at EOF
        elif line == 'EOF':
            break
        
        i += 1
    
    return {
        'name': name,
        'dimension': dimension,
        'coordinates': coordinates
    }


# ============================================================================
# DISTANCE MATRIX CALCULATOR
# ============================================================================

def calculate_distance_matrix(coordinates, round_result=False):
    """
    Calculate symmetric Euclidean distance matrix.
    
    Args:
        coordinates (list): List of (x, y) coordinate tuples
        round_result (bool): If True, apply NINT rounding (EUC_2D standard)
                            If False, use floating-point distances
    
    Returns:
        list: 2D distance matrix (list of lists)
              matrix[i][j] = distance from city i to city j
    """
    n = len(coordinates)
    matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = coordinates[i]
            x2, y2 = coordinates[j]
            
            # Euclidean distance
            distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            
            # Apply NINT rounding if requested (TSPLIB EUC_2D standard)
            if round_result:
                distance = int(distance + 0.5)  # NINT: nearest integer
            
            # Symmetric matrix
            matrix[i][j] = distance
            matrix[j][i] = distance
    
    return matrix


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_tour_length(tour, distance_matrix):
    """
    Calculate total length of a tour.
    
    Args:
        tour (list): List of city indices representing tour order
        distance_matrix (list): 2D distance matrix
        
    Returns:
        float: Total tour length
    """
    length = 0.0
    n = len(tour)
    
    for i in range(n):
        from_city = tour[i]
        to_city = tour[(i + 1) % n]  # Wrap around to complete the tour
        length += distance_matrix[from_city][to_city]
    
    return length

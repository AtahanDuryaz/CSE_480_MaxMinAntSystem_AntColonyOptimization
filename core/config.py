def get_config(instance_name):
    """
    Merkezi Konfigürasyon Yönetimi
    ------------------------------
    - Sabit Parametreler: α=1, β=3, ρ=0.1, MaxIter=200
    - Karınca Sayısı: n * 0.7 (Hesaplama verimliliği için)
    """
    
    # Kilitli Parametreler (Makale ve Proje Gereksinimi)
    ALPHA = 1
    BETA = 3
    RHO = 0.1
    MAX_ITERATIONS = 200
    STAGNATION_LIMIT = 20
    
    configs = {
        # --- ÖZEL TEST VE DOĞRULAMA SETLERİ (5 Şehir) ---
        'validation': {
            'n_ants': 5,
            'alpha': ALPHA, 'beta': BETA, 'rho': RHO,
            'max_iterations': MAX_ITERATIONS,
            'stagnation_limit': STAGNATION_LIMIT,
            'round_result': False,  # Hassas hesaplama
            'instance_path': None,  # Kod içindeki koordinatları kullanır
            'expected_optimum': None
        },
        'test5': {
            'n_ants': 5,
            'alpha': ALPHA, 'beta': BETA, 'rho': RHO,
            'max_iterations': MAX_ITERATIONS,
            'stagnation_limit': STAGNATION_LIMIT,
            'round_result': False,
            'instance_path': 'benchmarks/small/test5.tsp',
            'expected_optimum': None
        },

        # --- KÜÇÜK ÖLÇEKLİ TSPLIB BENCHMARK’LARI ---
        'eil51': {
            'n_ants': 35, # 51 * 0.7
            'alpha': ALPHA, 'beta': BETA, 'rho': RHO,
            'max_iterations': MAX_ITERATIONS,
            'stagnation_limit': STAGNATION_LIMIT,
            'round_result': True, # TSPLIB standardı: Tam sayı yuvarlama
            'instance_path': 'benchmarks/tsplib/eil51.tsp',
            'expected_optimum': 426
        },
        'berlin52': {
            'n_ants': 36, # 52 * 0.7
            'alpha': ALPHA, 'beta': BETA, 'rho': RHO,
            'max_iterations': MAX_ITERATIONS,
            'stagnation_limit': STAGNATION_LIMIT,
            'round_result': True,
            'instance_path': 'benchmarks/tsplib/berlin52.tsp',
            'expected_optimum': 7542
        },
        'st70': {
            'n_ants': 49, # 70 * 0.7
            'alpha': ALPHA, 'beta': BETA, 'rho': RHO,
            'max_iterations': MAX_ITERATIONS,
            'stagnation_limit': STAGNATION_LIMIT,
            'round_result': True,
            'instance_path': 'benchmarks/tsplib/st70.tsp',
            'expected_optimum': 675
        },

        # --- ORTA ÖLÇEKLİ TSPLIB BENCHMARK’LARI ---
        'pr76': {
            'n_ants': 53, # 76 * 0.7
            'alpha': ALPHA, 'beta': BETA, 'rho': RHO,
            'max_iterations': MAX_ITERATIONS,
            'stagnation_limit': STAGNATION_LIMIT,
            'round_result': True,
            'instance_path': 'benchmarks/tsplib/pr76.tsp',
            'expected_optimum': 108159
        },
        'kroA100': {
            'n_ants': 70, # 100 * 0.7
            'alpha': ALPHA, 'beta': BETA, 'rho': RHO,
            'max_iterations': MAX_ITERATIONS,
            'stagnation_limit': STAGNATION_LIMIT,
            'round_result': True,
            'instance_path': 'benchmarks/tsplib/kroA100.tsp',
            'expected_optimum': 21282
        },
        'lin105': {
            'n_ants': 73, # 105 * 0.7
            'alpha': ALPHA, 'beta': BETA, 'rho': RHO,
            'max_iterations': MAX_ITERATIONS,
            'stagnation_limit': STAGNATION_LIMIT,
            'round_result': True,
            'instance_path': 'benchmarks/tsplib/lin105.tsp',
            'expected_optimum': 14379
        },
        'ch130': {
            'n_ants': 91, # 130 * 0.7
            'alpha': ALPHA, 'beta': BETA, 'rho': RHO,
            'max_iterations': MAX_ITERATIONS,
            'stagnation_limit': STAGNATION_LIMIT,
            'round_result': True,
            'instance_path': 'benchmarks/tsplib/ch130.tsp',
            'expected_optimum': 6110
        },

        # --- BÜYÜK ÖLÇEKLİ TSPLIB BENCHMARK’LARI ---
        'pr152': {
            'n_ants': 106, # 152 * 0.7
            'alpha': ALPHA, 'beta': BETA, 'rho': RHO,
            'max_iterations': MAX_ITERATIONS,
            'stagnation_limit': STAGNATION_LIMIT,
            'round_result': True,
            'instance_path': 'benchmarks/tsplib/pr152.tsp',
            'expected_optimum': 73542
        },
        'rat195': {
            'n_ants': 136, # 195 * 0.7
            'alpha': ALPHA, 'beta': BETA, 'rho': RHO,
            'max_iterations': MAX_ITERATIONS,
            'stagnation_limit': STAGNATION_LIMIT,
            'round_result': True,
            'instance_path': 'benchmarks/tsplib/rat195.tsp',
            'expected_optimum': 2323
        },
        'lin318': {
            'n_ants': 222, # 318 * 0.7
            'alpha': ALPHA, 'beta': BETA, 'rho': RHO,
            'max_iterations': MAX_ITERATIONS,
            'stagnation_limit': STAGNATION_LIMIT,
            'round_result': True,
            'instance_path': 'benchmarks/tsplib/lin318.tsp',
            'expected_optimum': 42029
        }
    }
    
    if instance_name not in configs:
        raise ValueError(f"Bilinmeyen örnek (instance): {instance_name}")
    
    return configs[instance_name]
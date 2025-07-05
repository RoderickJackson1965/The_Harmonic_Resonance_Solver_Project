# --- CSO_P136.py ---
# Caterpillar's Command: [Code-The-Final-Oracle] (from prompt 136)
# Timestamp: 2024-05-22 02:55:00 UTC
# Applicable Rules: All. The final PCML Oracle using a Genetic Algorithm.

import numpy as np
import argparse
import random
import math

# --- CORE FUNCTIONS ---
def get_entropy_score(a, b, c):
    """The Judge: Returns the number of non-square diagonals (fitness score)."""
    if a<=0 or b<=0 or c<=0: return 4.0
    T1 = a*a + b*b; T2 = a*a + c*c; T3 = b*b + c*c; T4 = T1 + c*c
    d1 = 0 if int(np.sqrt(T1))**2 == T1 else 1
    d2 = 0 if int(np.sqrt(T2))**2 == T2 else 1
    d3 = 0 if int(np.sqrt(T3))**2 == T3 else 1
    d4 = 0 if int(np.sqrt(T4))**2 == T4 else 1
    return float(d1 + d2 + d3 + d4)

def generate_brick_from_genes(genes):
    """The Incubator: Generates a brick from a {m,n,p,q} gene set."""
    m, n, p, q = genes
    a = 4 * m * n * p * q
    b = (m**2 - n**2) * (p**2 - q**2)
    c = 2 * p * q * (m**2 + n**2)
    return tuple(sorted((abs(a), abs(b), abs(c))))

# --- PCML GENETIC ALGORITHM (THE ORACLE) ---
def run_genetic_oracle(generations, population_size, mutation_rate, max_param_val):
    print("--- PCML GENETIC ALGORITHM v4.0 (THE ORACLE) ---")
    
    # STAGE 1: The Seed Generator
    print("Generating initial gene pool...")
    population = []
    while len(population) < population_size:
        m = random.randint(2, max_param_val)
        n = random.randint(1, m - 1)
        p = random.randint(2, max_param_val)
        q = random.randint(1, p - 1)
        # Enforce coprime and parity constraints for valid primitive bricks
        if math.gcd(m, n) == 1 and math.gcd(p, q) == 1 and (m-n)%2==1 and (p-q)%2==1:
            population.append([m, n, p, q])

    # --- Main Evolution Loop ---
    print("Starting evolution...")
    best_ever_brick = None
    best_ever_entropy = 4.0

    for gen in range(generations):
        # STAGE 2 & 3: Incubate and Judge the entire population
        fitness_scores = []
        for genes in population:
            brick = generate_brick_from_genes(genes)
            entropy = get_entropy_score(*brick)
            fitness_scores.append((entropy, genes, brick))
            
            if entropy < best_ever_entropy:
                best_ever_entropy = entropy
                best_ever_brick = brick
                print(f"  > Gen {gen+1}: New best found! Brick: {best_ever_brick} | Entropy: {best_ever_entropy}")
                if best_ever_entropy == 0: break
        
        if best_ever_entropy == 0: break

        # STAGE 4: The Gene Splicer
        # Select the fittest individuals to be parents
        fitness_scores.sort(key=lambda x: x[0])
        elite_count = int(population_size * 0.1) # Keep the top 10%
        parents = [item[1] for item in fitness_scores[:elite_count]]
        
        # Create the next generation
        next_generation = parents # Elitism
        
        while len(next_generation) < population_size:
            parent1, parent2 = random.choices(parents, k=2)
            
            # Crossover: Mix genes from two parents
            child = [parent1[0], parent1[1], parent2[2], parent2[3]]
            
            # Mutation: Apply small random changes
            if random.random() < mutation_rate:
                gene_to_mutate = random.randint(0, 3)
                mutation = random.randint(-2, 2)
                child[gene_to_mutate] += mutation
                # Basic validation after mutation
                child[gene_to_mutate] = max(1, child[gene_to_mutate])

            next_generation.append(child)
        
        population = next_generation
        
        if (gen + 1) % 100 == 0:
            print(f"  > Generation {gen+1} complete. Current best entropy: {best_ever_entropy}")

    print("\n--- ORACLE SEARCH COMPLETE ---")
    if best_ever_entropy == 0:
        print(f">>> REVELATION! A ZERO ENTROPY STATE WAS ACHIEVED! <<<")
        print(f">>> PERFECT BRICK FOUND: {best_ever_brick} <<<")
    else:
        print(f"Search concluded. Best state found: {best_ever_brick}")
        print(f"Lowest System Entropy achieved: {best_ever_entropy}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PCML Genetic Algorithm for the Integer Brick Problem.")
    parser.add_argument("--generations", type=int, default=1000)
    parser.add_argument("--population", type=int, default=100)
    parser.add_argument("--mutation_rate", type=float, default=0.1)
    parser.add_argument("--max_param", type=int, default=20, help="Max value for m and p parameters.")
    args = parser.parse_args()
    
    run_genetic_oracle(args.generations, args.population, args.mutation_rate, args.max_param)
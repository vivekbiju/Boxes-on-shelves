import random
# Import logic from your other files
from models import load_data, generate_initial_population
from engine import evaluate, fast_non_dominated_sort, mutate, crossover

# Configuration
POPULATION_SIZE = 50
GENERATIONS = 20
MUT_RATE = 0.1

def run_main():
    print("🚀 Script started...")
    
    # 1. Load Data
    try:
        products_df, bay, shelves_df = load_data('data/products.txt', 'data/baytp1.txt', 'data/shelves.txt')
        BW, BH, BD = bay['w'], bay['h'], bay['d']
        print(f"✅ Data loaded. Bay dimensions: {BW}x{BH}x{BD}")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return

    # 2. Generate Initial Population
    print("📦 Generating initial population...")
    population = generate_initial_population(POPULATION_SIZE, products_df, shelves_df, BW, BH, BD)
    print(f"✅ Initial population of {len(population)} solutions created.")

    # 3. Evolutionary Loop
    for g in range(GENERATIONS):
        # Calculate fitness
        fitness_values = [evaluate(sol, shelves_df, BW, BH, BD) for sol in population]
        
        # Offspring generation
        offspring = []
        for _ in range(POPULATION_SIZE // 2):
            p1, p2 = random.sample(population, 2)
            c1, c2 = crossover(p1, p2)
            offspring.extend([
                mutate(c1, MUT_RATE, shelves_df, BW, BH, BD),
                mutate(c2, MUT_RATE, shelves_df, BW, BH, BD)
            ])
            
        # Selection logic (Simplified NSGA-II selection)
        combined = population + offspring
        combined_fits = [evaluate(s, shelves_df, BW, BH, BD) for s in combined]
        fronts = fast_non_dominated_sort(combined, combined_fits)
        
        population = []
        for f in fronts:
            if len(population) + len(f) <= POPULATION_SIZE:
                population.extend([combined[i] for i in f])
            else:
                population.extend([combined[i] for i in f[:POPULATION_SIZE - len(population)]])
                break
        
        print(f"🧬 Generation {g} complete. Best Utilization: {max(f[0] for f in fitness_values):.2%}")

    print("🏁 Optimization finished.")

# THIS IS THE PART YOU WERE MISSING:
if __name__ == "__main__":
    run_main()
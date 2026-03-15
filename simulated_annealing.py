import math
import random
import matplotlib.pyplot as plt

# 10 cities as (x, y) coordinates
cities = [
    (0,0), (1,5), (3,2), (6,4), (8,1),
    (7,7), (4,9), (2,7), (5,5), (9,3)
]
# distance between two cities
def dist(a, b):
    return math.sqrt((cities[a][0] - cities[b][0])**2 + (cities[a][1] - cities[b][1])**2)

# total tour distance (route + return to start)
def tour_cost(route):
    total = 0
    for i in range(len(route)):
        total += dist(route[i], route[(i + 1) % len(route)])
    return total

# swap two random cities to get a neighbor
def get_neighbor(route):
    new_route = route[:]
    i, j = random.sample(range(len(route)), 2)
    new_route[i], new_route[j] = new_route[j], new_route[i]
    return new_route


# ==========================================
# PART A + B - Simulated Annealing (geometric cooling)
# ==========================================
def simulated_annealing(schedule='geometric', T0=1000, alpha=0.995, iterations=10000):

    # start with a random route
    current = list(range(len(cities)))
    random.shuffle(current)
    current_cost = tour_cost(current)

    best = current[:]
    best_cost = current_cost

    T = T0
    cost_history = []

    for i in range(iterations):
        # cool down based on schedule
        if schedule == 'geometric':
            T = T0 * (alpha ** i)
        elif schedule == 'linear':
            T = T0 - (T0 / iterations) * i
            if T <= 0:
                T = 0.0001   # avoid zero or negative temp

        neighbor = get_neighbor(current)
        neighbor_cost = tour_cost(neighbor)

        delta = neighbor_cost - current_cost

        # accept better solution always, worse solution with some probability
        if delta < 0:
            current = neighbor
            current_cost = neighbor_cost
        else:
            prob = math.exp(-delta / T)
            if random.random() < prob:
                current = neighbor
                current_cost = neighbor_cost

        # track best found so far
        if current_cost < best_cost:
            best = current[:]
            best_cost = current_cost

        cost_history.append(best_cost)

    return best, best_cost, cost_history


# ==========================================
# PART C - Run and report results
# ==========================================
def report(route, cost, schedule_name):
    print(f"-------------------------------")
    print(f"  Schedule : {schedule_name}")
    print(f"-------------------------------")
    print(f"  Best tour  : {route}")
    city_names = " -> ".join(str(c) for c in route) + f" -> {route[0]}"
    print(f"  Path       : {city_names}")
    print(f"  Total dist : {cost:.4f}\n")


# ==========================================
# PART C - Plot cost vs iteration
# ==========================================
def plot_cost_curve(hist_geo, hist_lin):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(hist_geo, color='steelblue', linewidth=1)
    axes[0].set_title('Geometric Cooling - Cost vs Iteration', fontsize=11)
    axes[0].set_xlabel('Iteration')
    axes[0].set_ylabel('Best Tour Cost')
    axes[0].grid(True, linestyle='--', alpha=0.5)

    axes[1].plot(hist_lin, color='tomato', linewidth=1)
    axes[1].set_title('Linear Cooling - Cost vs Iteration', fontsize=11)
    axes[1].set_xlabel('Iteration')
    axes[1].set_ylabel('Best Tour Cost')
    axes[1].grid(True, linestyle='--', alpha=0.5)

    plt.suptitle('Simulated Annealing - TSP Cost Convergence', fontsize=13)
    plt.tight_layout()
    plt.savefig('sa_cost_curve.png', dpi=150)
    plt.show()
    print("Plot saved -> sa_cost_curve.png")


# ==========================================
# PART D - Compare cooling schedules
# ==========================================
def compare_schedules(cost_geo, cost_lin, hist_geo, hist_lin):
    print("-------------------------------")
    print("  Schedule Comparison")
    print("-------------------------------")
    print(f"  Geometric final cost : {cost_geo:.4f}")
    print(f"  Linear    final cost : {cost_lin:.4f}")

    # find iteration where each first reached its final best
    for i, val in enumerate(hist_geo):
        if val == cost_geo:
            geo_converge = i
            break

    for i, val in enumerate(hist_lin):
        if val == cost_lin:
            lin_converge = i
            break

    print(f"  Geometric converged at iteration : {geo_converge}")
    print(f"  Linear    converged at iteration : {lin_converge}")
    print("""
  Observation:
  Geometric cooling keeps temperature high for longer, so it
  explores more of the search space early on. This usually leads
  to better final tour costs but takes more iterations to settle.

  Linear cooling drops temperature faster, which means it stops
  accepting bad moves sooner. It converges quicker but can get
  stuck in a local optimum with a slightly higher tour cost.
""")


# ==========================================
# MAIN
# ==========================================
if __name__ == "__main__":
    random.seed(42)

    # part b + c - geometric cooling
    best_geo, cost_geo, hist_geo = simulated_annealing(schedule='geometric')
    report(best_geo, cost_geo, "Geometric (T0=1000, alpha=0.995)")

    # part d - linear cooling
    best_lin, cost_lin, hist_lin = simulated_annealing(schedule='linear')
    report(best_lin, cost_lin, "Linear (T0=1000, steps=10000)")

    # part c - plot
    plot_cost_curve(hist_geo, hist_lin)

    # part d - comparison
    compare_schedules(cost_geo, cost_lin, hist_geo, hist_lin)

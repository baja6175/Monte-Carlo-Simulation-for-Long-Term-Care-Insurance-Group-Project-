import numpy as np
import pandas as pd

# -------------------------------
# PARAMETERS
# -------------------------------
N = 100  # number of policyholder simulations
epsilon = 1e-2  # convergence tolerance
premium_guess = 2000.0  # initial premium guess
premium_step = 100.0  # adjustment step size
discount_rate = 0.002  # monthly rate (e.g., 0.2%)
entry_age = 60
max_age = 100

# -------------------------------
# SIMULATION COMPONENTS
# -------------------------------

def simulate_lifetime():
    return np.random.normal(loc=85, scale=5)  # age at death

def simulate_dependency_entry():
    return np.random.normal(loc=75, scale=3)  # age at dependency

def simulate_dependency_duration():
    return np.random.weibull(2) * 3  # duration in years

def simulate_claim_cost(level=2):
    return {1: 1500, 2: 1000, 3: 600, 4: 400}.get(level, 1000)

def discount_cashflow(amount, t):
    return amount / ((1 + discount_rate) ** (t * 12))  # yearly discounting

# -------------------------------
# ALGORITHM 1: BREAK-EVEN PREMIUM
# -------------------------------

def compute_npv(premium):
    npv_sum = 0
    for _ in range(N):
        age_at_death = simulate_lifetime()
        entry = simulate_dependency_entry()
        duration = simulate_dependency_duration()
        level = np.random.choice([1, 2, 3, 4], p=[0.2, 0.3, 0.3, 0.2])
        benefit = simulate_claim_cost(level)

        if entry > age_at_death:
            claims = 0
        else:
            claim_years = min(duration, age_at_death - entry)
            claims = sum(discount_cashflow(benefit * 12, t) for t in range(1, int(claim_years) + 1))

        # Premiums (paid until age 65)
        premium_years = range(entry_age, int(min(age_at_death, 65)) + 1)
        premiums = sum(discount_cashflow(premium, t) for t in premium_years)

        npv_sum += premiums - claims

    return npv_sum / N

# Find break-even premium
premium = premium_guess
iteration = 0
while True:
    avg_npv = compute_npv(premium)
    if abs(avg_npv) <= epsilon or iteration > 200:
        break
    premium += -premium_step if avg_npv > 0 else premium_step
    iteration += 1
    print(f"${avg_npv}")

break_even_premium = round(premium, 2)
print(f"Break-even premium: $ {break_even_premium}")

# -------------------------------
# ALGORITHM 2: RISK METRICS
# -------------------------------

npvs = []
for _ in range(N):
    age_at_death = simulate_lifetime()
    entry = simulate_dependency_entry()
    duration = simulate_dependency_duration()
    level = np.random.choice([1, 2, 3, 4], p=[0.2, 0.3, 0.3, 0.2])
    benefit = simulate_claim_cost(level)

    if entry > age_at_death:
        claims = 0
    else:
        claim_years = min(duration, age_at_death - entry)
        claims = sum(discount_cashflow(benefit * 12, t) for t in range(1, int(claim_years) + 1))

    premium_years = range(entry_age, int(min(age_at_death, 65)) + 1)
    premiums = sum(discount_cashflow(break_even_premium, t) for t in premium_years)

    npvs.append(premiums - claims)

npvs = np.array(npvs)

# Risk Metrics
mean_npv = round(np.mean(npvs), 2)
std_npv = round(np.std(npvs), 2)
prob_loss = round(np.mean(npvs < 0), 4)
var_95 = round(np.percentile(npvs, 5), 2)

summary = pd.DataFrame({
    "Break-Even Premium": [break_even_premium],
    "Mean NPV": [mean_npv],
    "Std NPV": [std_npv],
    "Prob(NPV < 0)": [prob_loss],
    "VaR (95%)": [var_95]
})

print("\nRisk Metrics Summary:")
print(summary.to_string(index=False))

# -------------------------------
# SENSITIVITY ANALYSIS
# -------------------------------

def recompute_break_even():
    premium = premium_guess
    iteration = 0
    while True:
        avg_npv = compute_npv(premium)
        if abs(avg_npv) <= epsilon or iteration > 200:
            break
        premium += -premium_step if avg_npv > 0 else premium_step
        iteration += 1
    return round(premium, 2)

def risk_metrics_for_premium(prem):
    npvs_local = []
    for _ in range(N):
        age_at_death = simulate_lifetime()
        entry = simulate_dependency_entry()
        duration = simulate_dependency_duration()
        level = np.random.choice([1, 2, 3, 4], p=[0.2, 0.3, 0.3, 0.2])
        benefit = simulate_claim_cost(level)

        if entry > age_at_death:
            claims = 0.0
        else:
            claim_years = min(duration, age_at_death - entry)
            claims = sum(discount_cashflow(benefit * 12, t) for t in range(1, int(claim_years) + 1))

        premium_years = range(entry_age, int(min(age_at_death, 65)) + 1)
        premiums = sum(discount_cashflow(prem, t) for t in premium_years)

        npvs_local.append(premiums - claims)

    npvs_local = np.array(npvs_local)
    return {
        "Mean NPV": round(np.mean(npvs_local), 2),
        "Std NPV": round(np.std(npvs_local), 2),
        "Prob(NPV < 0)": round(np.mean(npvs_local < 0), 4),
        "VaR (95%)": round(np.percentile(npvs_local, 5), 2),
    }

def run_scenario(name, cost_mult=1.0, duration_mult=1.0, dr_bp_annual=0):
    
    global discount_rate, simulate_dependency_duration, simulate_claim_cost

    # backups
    base_dr = discount_rate
    base_duration_fn = simulate_dependency_duration
    base_cost_fn = simulate_claim_cost

    try:
        discount_rate = base_dr + (dr_bp_annual / 10000.0) / 12.0

        
        def duration_wrapped():
            return base_duration_fn() * duration_mult

        def cost_wrapped(level=2):
            return base_cost_fn(level) * cost_mult

        simulate_dependency_duration = duration_wrapped
        simulate_claim_cost = cost_wrapped

        be = recompute_break_even()
        metrics = risk_metrics_for_premium(be)
        metrics.update({"Scenario": name, "Break-Even Premium": be})
        return metrics

    finally:
     
        discount_rate = base_dr
        simulate_dependency_duration = base_duration_fn
        simulate_claim_cost = base_cost_fn

# Build scenarios
scenarios = [
    ("Cost +10%",       1.10, 1.00,   0),
    ("Cost -10%",       0.90, 1.00,   0),
    ("Duration +10%",   1.00, 1.10,   0),
    ("Duration -10%",   1.00, 0.90,   0),
    ("Discount +50 bp", 1.00, 1.00,  50),
    ("Discount -50 bp", 1.00, 1.00, -50),
]


baseline_row = {
    "Scenario": "Baseline",
    "Break-Even Premium": break_even_premium,
    "Mean NPV": mean_npv,
    "Std NPV": std_npv,
    "Prob(NPV < 0)": prob_loss,
    "VaR (95%)": var_95
}

# Run sensitivity
sens_results = [baseline_row] + [run_scenario(name, cm, dm, bp) for (name, cm, dm, bp) in scenarios]
sens_df = pd.DataFrame(sens_results, columns=["Scenario","Break-Even Premium","Mean NPV","Std NPV","Prob(NPV < 0)","VaR (95%)"])

print("\nSensitivity Analysis:")
print(sens_df.to_string(index=False))

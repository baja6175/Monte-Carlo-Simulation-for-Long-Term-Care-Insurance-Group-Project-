# 📊 Monte Carlo Simulation of NPV in Long-Term Care Insurance  

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)  
[![NumPy](https://img.shields.io/badge/NumPy-✓-orange.svg)](https://numpy.org/) [![Pandas](https://img.shields.io/badge/Pandas-✓-green.svg)](https://pandas.pydata.org/) 
---

## 📌 Overview  
This project applies **Monte Carlo simulation** to model the **Net Present Value (NPV)** of **Long-Term Care (LTC) insurance** policies from the insurer’s perspective.  

Unlike traditional fixed-average methods, our stochastic framework accounts for:  
- 👵 Mortality & longevity risk  
- 🏥 Dependency onset & duration of care  
- 💰 Claim cost severity  
- 📉 Discount rate & economic volatility  

The analysis was completed as part of **ST474/674 – Monte Carlo and Simulation Methods** at **Wilfrid Laurier University (Aug 2025)**.  

---

## 👥 Team Members  
- **Diya Bajaj**  
- Ariana Qianyi  
- Sherry Huang  
- Joel Huebner  


---

## ⚙️ Methodology  

### 🔹 1. Break-Even Premium Estimation  
- Simulate policyholder lifetimes (mortality, dependency, duration, severity).  
- Compute inflows vs. outflows.  
- Adjust premium iteratively until **mean NPV ≈ 0**.  

### 🔹 2. Risk Quantification  
At the break-even premium, calculate:  
- 📈 Mean NPV  
- 📊 Standard deviation of NPV  
- ❌ Probability of loss  
- ⚠️ 95% Value-at-Risk (VaR)  

### 🔹 3. Sensitivity Analysis  
Stress test the model by perturbing:  
- 💵 Claim costs ±10%  
- ⏳ Care duration ±10%  
- 💹 Discount rate ±50 bps  

---

## 📊 Results  

Key Findings:  

- Break-even premium ≈ **\$14,280**  
- Probability of insurer loss ≈ **42%** at break-even  
- 95% VaR ≈ **\$35,000** per policy  
- Claim costs & care duration = biggest risk drivers  

| 📐 Metric              | 🔢 Value   | 📎 Range             |
|------------------------|-----------:|----------------------|
| Break-even Premium     | 14,280     | 13,900 – 14,700     |
| Mean NPV               |   -708     | -2,780 – 2,926      |
| Std. Dev. of NPV       | 18,020     | 14,121 – 20,952     |
| Prob(NPV < 0)          | 41.9%      | 31% – 49%           |
| VaR (95%)              | -35,098    | -47,418 – -26,347   |

*(Negative values = insurer loss)*  

## 🖥️ Code Structure  

File: `monte_carlo_sim.py`  

- `simulate_lifetime()` → mortality distribution  
- `simulate_dependency_entry()` → onset of LTC needs  
- `simulate_dependency_duration()` → Weibull duration model  
- `simulate_claim_cost()` → severity-level costs  
- `compute_npv()` → per-policy NPV  
- **Algorithm 1** → break-even premium search  
- **Algorithm 2** → risk metrics & sensitivity scenarios  

---

## 🛠️ Tech Stack  
- 🐍 **Python 3.10+**  
- 🔢 **NumPy** – random simulation  
- 📊 **Pandas** – risk metric reporting  
- 📉 **Matplotlib** – visualization  

---

## 📚 References

Bodily, P., & Furman, J. (2016). Long-term care insurance decisions: Assessing the value of coverage. Society of Actuaries.

Lazoğlu, M. A., & Büyükyazici, M. (2023). Pricing for longevity risk in long-term care insurance using semi-Markov models. Insurance: Mathematics and Economics, 111, 102942.

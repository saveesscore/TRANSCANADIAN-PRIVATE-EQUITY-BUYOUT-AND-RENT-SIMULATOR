# RENT DESK — Trans-Canadian Private Equity Buyout & Tenancy Law Simulator

An institutional quantitative finance and housing-policy simulator evaluating how **provincial landlord-tenant statutes**, **vacancy decontrol loopholes**, and **interest-rate regimes** govern private equity leveraged buyout (LBO) returns and household buy-vs.-rent wealth across six major Canadian markets: **Toronto, Vancouver, Montreal, Halifax, Calgary, and Edmonton**.

> **Live Interactive Dashboard:** `https://<your-username>.github.io/<your-repo-name>/` *(Update with your GitHub Pages URL once deployed)*

---

## 1. Executive Summary & Research Motivation

Canadian residential real estate sits at the intersection of **corporate financial engineering** and **provincial statutory law**. Because landlord-tenant regulation is governed at the provincial level rather than federally, Canada functions as a natural policy laboratory for testing how legal constraints alter capital allocation and tenant affordability.

This repository models two core questions across a standardized **60-unit multi-family apartment building** and a **single-unit household purchase**:

1. **The Institutional Question (Private Equity LBO):** Can a private equity real estate fund achieve its standard **15.0% Internal Rate of Return (IRR) hurdle** across major Canadian cities while operating under strict statutory rent caps—or does the math structurally depend on **Vacancy Decontrol** (aggressive tenant turnover and unit renovations to reset rents to market)?
2. **The Household Question (Buy vs. Rent + Invest):** Accounting for mortgage amortization, property taxes, maintenance, condo fees, selling friction, and statutory rent protections, at what **mortgage interest rate** and **time horizon** does buying a home outperform renting and investing the cost differential in a diversified equity index?

---

## 2. Key Quantitative & Policy Findings

* **The Low-Yield / High-Gap Dynamic (Toronto & Vancouver):** High acquisition prices create compressed Day-1 going-in cap rates (**~3.45%–3.51%**). At a 5.0% commercial borrowing rate, leveraged acquisitions experience negative initial cash flow after debt service. Achieving a 15%+ IRR relies heavily on **Vacancy Decontrol** to capture the **36%–40% gap** between sitting-tenant rents and asking market rents.
* **The Statutory Bottleneck (Montreal):** Quebec's Civil Code and *Tribunal administratif du logement* (TAL) Section G lease disclosure rules restrict arbitrary rent resets between tenants. Even with a ~34.5% gap between occupied and market rents, statutory turnover constraints compress 5-year leveraged returns.
* **Free-Market Cash Yield (Calgary & Edmonton):** Without statutory percentage rent caps, sitting rents closely track market rents (~8.6%–8.9% gap), while higher Day-1 cap rates (**~4.45%–4.49%**) allow buildings to clear debt service organically without relying on aggressive turnover.
* **Monetary Policy Sensitivity:** Rising mortgage rates disproportionately penalize high-valuation coastal markets, pushing debt service coverage ratios below break-even unless offset by elevated tenant turnover or equity infusions.

---

## 3. Provincial Legal & Regulatory Framework Modeled

| City | Province | Governing Statute / Tribunal | Annual Renewal Cap (2026 Baseline) | Turnover Rule (Between Tenants) |
| :--- | :--- | :--- | :--- | :--- |
| **Toronto** | Ontario | *Residential Tenancies Act, 2006* (LTB) | **2.1%** (units occupied pre-Nov 15, 2018); exempt post-2018 | **Vacancy Decontrol** (unrestricted reset to market) |
| **Vancouver** | British Columbia | *Residential Tenancy Act* (RTB) | **2.3%** across all residential tenancies | **Vacancy Decontrol** (unrestricted reset to market) |
| **Montreal** | Quebec | *Civil Code of Québec* / *TAL* | **~3.1%** TAL calculation benchmark (tenant right of refusal) | **Restricted** (Section G prior-rent disclosure & TAL fixation) |
| **Halifax** | Nova Scotia | *Residential Tenancies Act* | **5.0%** temporary statutory rent cap | **Vacancy Decontrol** (unrestricted reset to market) |
| **Calgary** | Alberta | *Residential Tenancies Act* | **No statutory cap** (limited to 1 increase per 12 months) | **Free Market** (unrestricted) |
| **Edmonton** | Alberta | *Residential Tenancies Act* | **No statutory cap** (limited to 1 increase per 12 months) | **Free Market** (unrestricted) |

---

## 4. Mathematical Methodology

### A. Institutional Leveraged Buyout (LBO) Engine (`lbo_engine.py`)

* **Net Operating Income (NOI) & Exit Valuation:**

\[\text{NOI}_t = (\text{Units} \times \overline{\text{Rent}}_t \times 12) \times (1 - \text{Expense Ratio})\]

\[\text{Exit Value}_5 = \frac{\text{NOI}_5}{\text{Cap Rate}_{\text{entry}} + 0.0025}\]

* **Cohort Rent Blending:** Each year \(t \in \{1, 2, 3, 4, 5\}\), units are partitioned into retained tenancies \((1 - \tau)\) and vacated units \((\tau)\):

\[\overline{\text{Rent}}_t = (1 - \tau)\cdot \overline{\text{Rent}}_{t-1}\left(1 + \min(g_{\text{cap}}, g_{\text{mkt}})\right) + \tau \cdot \text{Rent}_{\text{turnover}}\]

where \(\text{Rent}_{\text{turnover}} = \text{Rent}_{\text{mkt}, t}\) if `Vacancy_Decontrol == True`, and \(\overline{\text{Rent}}_{t-1}(1 + g_{\text{cap}})\) under strict unit-tied rent control.

* **Internal Rate of Return (IRR):** Solved numerically via polynomial root-finding (`numpy.roots`) across the 5-year levered cash-flow vector \(CF_0 \dots CF_5\):

\[\sum_{t=0}^{5} \frac{CF_t}{(1 + \text{IRR})^t} = 0\]

### B. Household Buy vs. Rent + Invest Engine (`buy_vs_rent.py`)

* **Fixed-Rate Mortgage Amortization:** Models a 25-year amortization schedule (\(n = 300\) months) with a 20% down payment:

\[M = P \cdot \frac{i(1 + i)^{300}}{(1 + i)^{300} - 1}\]

* **Net Worth Comparison:** Tracks cumulative home equity net of remaining principal and 5% transaction/selling costs against an equivalent renter portfolio compounding the initial down payment and monthly cash-flow savings at a 7.5% annualized equity return.

---

## 5. Repository Structure

```text
TRANSCANADIAN-PRIVATE-EQUITY-BUYOUT-AND-RENT-SIMULATOR/
├── index.html          # Interactive RENT DESK web application (HTML/CSS/JS)
├── city_data.py        # 6-city baseline financial parameters & provincial legal rules
├── lbo_engine.py       # 5-year Private Equity LBO, turnover & policy stress-test engine
├── buy_vs_rent.py      # 10-year household Buy vs. Rent + Invest amortization simulator
├── stress_test.py      # Mortgage interest-rate sensitivity matrix (3.0% to 7.0%)
├── visualize.py        # Static high-DPI Matplotlib chart generator
├── build_website.py    # Static dashboard compiler
├── charts/             # Exported PNG visualizations for reports
└── README.md           # Project documentation, legal synthesis & methodology
```

---

## 6. How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com<your-username>/<your-repo-name>.git
   cd <your-repo-name>
   ```
2. **Install Python dependencies:**
   ```bash
   pip install pandas numpy matplotlib plotly
   ```
3. **Run the simulation modules or launch the web dashboard:**
   ```bash
   python lbo_engine.py      # Run 5-year PE LBO scenarios in terminal
   python stress_test.py     # Run mortgage rate sensitivity matrix
   python buy_vs_rent.py     # Run household Buy vs. Rent comparison
   start index.html          # Open RENT DESK interactive web app in browser (Windows)
   ```

---

## 7. Limitations & Future Extensions

* **Baseline Calibration:** Default city figures represent illustrative multi-family baselines calibrated to Canadian market dynamics; users can update `city_data.py` directly with annual **CMHC Rental Market Report** and **Rentals.ca** releases.
* **Deterministic Cash Flows:** The current engine models steady annual growth rates; a planned extension incorporates **Monte Carlo simulation** (`numpy.random`) for stochastic interest-rate paths and vacancy shocks.
* **Financing Nuances:** Does not yet model **CMHC MLI Select** insured multi-unit financing (up to 95% LTV and 50-year amortizations) or Ontario **Above Guideline Increases (AGIs)** for major capital expenditures.

---

*Disclaimer: This project is an academic quantitative modeling exercise exploring housing economics and statutory tenancy frameworks. It does not constitute financial, legal, or investment advice.*

# Case study: Wildfire logistics contingency analysis

## Context
During wildfire seasons, road closures and changing deployment locations can disrupt food distribution to responders and supporting personnel. My real-world analytical work at Sysco includes evaluating alternative origin/route options with SQL Server, QGIS and Tableau. This public case study **illustrates the workflow using synthetic inputs**, not employer or emergency records.

## The challenge
The normal origin (illustratively Kelowna) is exposed to a simulated road closure. A separate scenario shifts the delivery point following changes to operational conditions. The question is whether an alternative origin (illustratively Calgary) can provide a feasible path within a delivery window.

## Analytical contribution
1. Extract/validate source and destination records in SQL Server/SSMS.
2. Standardize origins, destinations, inventory availability, route segments, pricing and freight assumptions.
3. Use scenario-specific route availability and a Python shortest-path algorithm to check alternatives.
4. Rank feasible routes by estimated arrival first, then delivered cost.
5. Prepare QGIS maps of alternative locations and Tableau scenario-comparison dashboards for review.

## Results from SYNTHETIC scenario data

| Scenario | Route selected | Estimated delivery time | Illustrative total cost |
|---|---|---:|---:|
| Normal operations | Kelowna → Site A | 4.1 h | $3,769.50 |
| Kelowna edges closed | Calgary → Site A | 9.5 h | $4,373.40 |
| Delivery site relocated | Calgary → Site B | 6.6 h | $3,981.00 |

These results are **not historical wildfire outcomes**. They only verify the behavior of the demo algorithm under hypothetical closures and relocations.

## Decisions and interpretation
- The normal nearest/fastest origin may become unusable after route closures.
- An alternative supply point can be evaluated using a common framework for route feasibility, dispatch time, inventory and delivered cost.
- When a support destination changes, analysts must rerun the scenario rather than reuse a prior route recommendation.
- A human dispatcher and authorized emergency operations personnel must validate real roads, safety restrictions and delivery feasibility.

## Transferable skills
SQL Server and data QA; QGIS spatial visualization; Tableau operational dashboards; Python scenario modeling; multi-criteria prioritization; stakeholder communication under changing conditions.

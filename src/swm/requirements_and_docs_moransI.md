# Spatial Autocorrelation Analysis

## Questions


Global Moran's I


Local Moran's I

### Question 1 — Global Moran's I

> Is the distribution of variable X spatially structured, or could it have occurred by chance regardless of geography?

In our particular case:
> Is the distribution of children with migration backgrounds across Münster's 
> neighborhoods spatially random, or does it show significant clustering?

This question is answered by Global Moran's I computed under each W type.
A significant positive I means similar neighborhoods cluster together.
A non-significant result means the distribution is spatially random.

### Question 2 — Local Moran's I
> Given that a global spatial structure exists, which specific locations drive that structure, where do similar values cluster, and where do anomalous outliers break the pattern?

In our particular case:
> Where exactly in Münster does clustering of children with migration backgrounds 
> occur, and which neighborhoods are spatial outliers?

This question is answered by Local Moran's I, but only when the Global result 
is significant (p < 0.05) and meaningful (|Moran's I| >= 0.15). Local Moran's I 
decomposes the global signal into specific locations — HH clusters, LL clusters, 
and outliers. Running it on a non-significant global result produces noise.

### Question 3 — Socioeconomic W
> Does the clustering of children with migration backgrounds strengthen when 
> spatial connections are weighted by structural similarity in poverty 
> (pct_welfare_15_64) rather than by geography alone?

This question is answered by comparing Global Moran's I under the standard 
geographic W types against the Socio-Similarity W. If I increases under the 
socioeconomic W, it means poverty similarity, not just physical proximity,
organizes the spatial distribution of migration background. **That is a spatial 
justice finding.**

---

## Requirements

### compute_global_morans

#### Inputs
- [ ] A GeoDataFrame is needed containing the variable to be analyzed
- [ ] A libpysal W object is needed defining the spatial structure to measure through
- [ ] The variable name must be passed explicitly, not hardcoded

#### Computation
- [ ] The variable values must be extracted as a numpy array before passing to esda
- [ ] The result object must preserve the full esda.Moran output, not just scalar values

#### Output
- [ ] The return type must be an esda.Moran object so callers can access .I, .p_sim, and .z_sim
- [ ] The result must be usable directly by build_morans_table without transformation

### build_morans_table

#### Inputs
- [ ] A dictionary mapping W type names to libpysal W objects is needed
- [ ] The same analysis variable must be used consistently across all W types
- [ ] W type names must be human-readable strings suitable for the final report

#### Computation
- [ ] Global Moran's I must be computed for every W type in the dictionary
- [ ] Each result must capture I, p-value, z-score, and a significance flag

#### Output
- [ ] The return type must be a pandas DataFrame with one row per W type
- [ ] The significance flag must be a human-readable label, not a boolean

---

### print_morans_table

#### Inputs
- [ ] A DataFrame returned by build_morans_table is needed
- [ ] The analysis variable name must be included in the printed header

#### Output
- [ ] The table must be readable in a terminal without truncation
- [ ] The variable name must appear in the header so the output is self-documenting

---

### save_morans_table

#### Inputs
- [ ] A DataFrame returned by build_morans_table is needed
- [ ] The output directory must be configurable, not hardcoded
- [ ] The filename must include the variable name so multiple runs do not overwrite each other

#### Output
- [ ] The file must be saved as CSV for portability
- [ ] The output directory must be created if it does not exist


---
(Optional - With time)
### compute_local_morans

#### Inputs
- [ ] A GeoDataFrame is needed containing the variable to be analyzed
- [ ] A libpysal W object is needed defining the spatial structure
- [ ] The variable name must be passed explicitly, not hardcoded

#### Gate condition
- [ ] This function must only be called when Global Moran's I is significant (p < 0.05)
- [ ] This function must only be called when Global Moran's I is meaningful (|I| >= threshold)
- [ ] The gate must be enforced at the caller level, not inside this function

#### Output
- [ ] The return type must be an esda.Moran_Local object for direct use in plot_local_morans

---
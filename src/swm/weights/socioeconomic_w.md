# On socioeconomic weighting

Based on our Spatial weights matrix exploration and our data, we want to answer the following question:

> Do children with migration backgrounds cluster among neighborhoods that are structurally similar in poverty?

That's a spatial justice question with real meaning for Germany. It asks whether immigration and poverty are spatially co-organized, which they are in most German cities, but Münster is supposedly the exception. Let the data answer it.


## SocioWeight

- [ ] A controlled vocabulary is needed to restrict valid weighting strategies to exactly three options
- [ ] Each strategy must encode a distinct theory of how socioeconomic position drives spatial connection
- [ ] Invalid strategy names must be rejected at the type level, not at runtime

## create_socio_swm

### Inputs
- [ ] A base neighbor structure is needed that defines who is connected, independent of how strongly
- [ ] The socioeconomic attribute must be read from the data, not hardcoded
- [ ] The weighting strategy must be selectable at call time with a safe default

### Normalization
- [ ] The index values must be comparable across any dataset regardless of original scale or unit
- [ ] Zero variance in the input column must be detected and rejected before computation

### Weight computation
- [ ] For each connected pair, a weight must be derived from their relative socioeconomic positions
- [ ] The computation must be strategy-agnostic at the loop level — the enum selects the formula

### Row standardization
- [ ] Each neighborhood's outgoing weights must sum to 1 so results are comparable across W types
- [ ] Neighborhoods with all-zero weights must not cause division by zero

### Output
- [ ] The return type must be identical to all other weight-building functions in the module
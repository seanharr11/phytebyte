0. Cluster.get_encoded_cmpd(...) -> should be concurrent
0. Finding positive_cmpds should be broken apart (into clusters?)
by whether or not it is an inducer, or an inhibitor.
0. All concurrent calls to fingerprint.fingerprint_and_encode(...) should be DRY'ed out
1. Imeplement Phenotype2GeneTargetInput
 -- OMIM (NCBI) (Online Mendelian Inheritance in Man)
 -- GWAS Catalog (EBI) (50,000 rows)
2. Implement model_training graphing module (use functions in chemogenomics)
3. Need a module to handle preprocessing food_cmpds (like in bioactive_cmpds)
4. Implement phytebyte.py -> PhyteByte._load_config()
5. Multi-processing on Deserializing FoodCmpds
6. When passing Fingerprinters to set_positive_clustere() and set_negative_sampler(), replace arg with a kwarg with better naming (as opposed to the convoluted passing of Fingerprint.create('foo') obejcts to the set_*() methods"
7. SVD Model to get Latent Feature Vector & apply Cosine Similarity
# Kenny...
5. Compound -> Cmpd
6. Handle compounds that share a same SMiLES (we may care about the assay data on each!)
7. !! Ensure uniqueness on positive_compounds
8. Functionality to facilitate querying metadata on compounds, and just passing around SMiLES (especially for FoodCmpd)

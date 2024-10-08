# ELT Practice 2024

## Reminder to be inside `/src/elt_practice_2024/` when running `python` statements

For instance, this repo assumes that you're inside of `src/_practice_2024` and that you're running `python` like this: 

```python
python data_extraction.py
```

This ensures that the local import statements remain the same between application code and the test code.

## Plan

1. Create `client_data_sources.json` data structure as an array where each element is a dictionary that contains information for different file types for each client.
2. Create `.py` files that read in `client_data_sources.json` file, download the raw data, and process it.
3. Ingest the processed data into client specific schemas
4. Explore `dbt` so that we can start transforming the data
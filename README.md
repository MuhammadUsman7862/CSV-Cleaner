# CSV Cleaner

A small, dependency-light Python script that reads a CSV file with pandas,
cleans missing values, removes duplicate rows, and writes the result to a
new CSV file.

## Features

- Reads any CSV file with pandas
- Reports which columns have missing values, and how much
- Drops columns that are mostly empty (configurable threshold)
- Fills remaining missing values using one of several strategies:
  - `mean` (default) — numeric columns filled with column mean
  - `median` — numeric columns filled with column median
  - `zero` — numeric columns filled with 0
  - `drop` — drops any row with a missing value
- Text/categorical columns are filled with `"Unknown"`
- Removes exact duplicate rows
- Saves a cleaned copy without touching the original file

## Requirements

- Python 3.8+
- pandas

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Basic usage:

```bash
python clean_csv.py input.csv
```

This creates `input_cleaned.csv` in the same folder.

Specify a custom output path:

```bash
python clean_csv.py input.csv --output cleaned_data.csv
```

Choose a fill strategy:

```bash
python clean_csv.py input.csv --strategy median
```

Change the column-drop threshold (drop columns with more than 70% missing):

```bash
python clean_csv.py input.csv --drop-threshold 0.7
```

## Example

A sample file, `sample_data.csv`, is included for testing:

```bash
python clean_csv.py sample_data.csv
```

Example output:

```
Loading: sample_data.csv
Loaded 7 rows, 4 columns.

Missing values before cleaning:
  - age: 2 missing (28.6%)
  - city: 1 missing (14.3%)
  - salary: 1 missing (14.3%)
Removed 1 duplicate row(s).

Cleaned data saved to: sample_data_cleaned.csv
Final shape: 6 rows, 4 columns.
```

## Project Structure

```
csv-cleaner/
├── clean_csv.py       # Main script
├── sample_data.csv    # Example input file
├── requirements.txt   # Dependencies
├── .gitignore
└── README.md
```

## License

MIT

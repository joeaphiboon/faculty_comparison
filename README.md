# Faculty Performance Dashboard

Interactive dashboard for visualizing faculty performance metrics across different skill groups based on the PISA framework.

## Local Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/faculty-dashboard.git
cd faculty-dashboard
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

4. Create data directory and add your data:
```bash
mkdir data
# Place your Faculty_Comparison_of_Z-Scores.csv in the data directory
```

5. Create .env file:
```bash
echo "DATA_PATH=data/Faculty_Comparison_of_Z-Scores.csv" > .env
```

6. Run the dashboard:
```bash
streamlit run app.py
```

## Streamlit Cloud Deployment

1. Fork this repository
2. In Streamlit Cloud:
   - Create new app pointing to your fork
   - Add your data in Settings > Secrets:
     ```toml
     csv_data = "YOUR_BASE64_ENCODED_CSV_DATA"
     ```

## Features

- Interactive radar charts for skill visualization
- Comparative analysis across faculties
- Multiple skill group views:
  - Core Skills
  - PISA Communication
  - PISA Leadership
  - PISA Global Competence

## Data Security

The dashboard is configured to protect sensitive data:
- CSV file is not included in the repository
- Download buttons are disabled
- Data is loaded securely via environment variables or secrets
- Raw data access is restricted

## Contact

For access to the data file or questions about the dashboard, please contact [Your Contact Information].
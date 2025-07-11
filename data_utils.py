import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def generate_dummy_data(num_employees=1000):
    """Generates a dummy dataset for employee analytics with random names."""
    np.random.seed(42)  # for reproducibility

    first_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy",
                   "Kevin", "Linda", "Mike", "Nancy", "Oscar", "Pamela", "Quinn", "Rachel", "Steve", "Tina"]
    last_names = ["Smith", "Jones", "Williams", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson",
                  "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson", "Clark"]

    data = {
        'EmployeeID': range(1, num_employees + 1),
        'Name': [f"{np.random.choice(first_names)} {np.random.choice(last_names)}" for _ in range(num_employees)],
        'Department': np.random.choice(['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations'], num_employees),
        'Role': np.random.choice(['Manager', 'Senior Associate', 'Associate', 'Analyst', 'Specialist'], num_employees),
        'HireDate': pd.to_datetime('2015-01-01') + pd.to_timedelta(np.random.randint(0, 365 * 7, num_employees), unit='D'),
        'Salary': np.random.normal(70000, 20000, num_employees).astype(int),
        'PerformanceRating': np.random.randint(1, 6, num_employees),  # 1-5 scale
        'EngagementScore': np.random.randint(60, 100, num_employees),  # 0-100 scale
        'Attrition': np.random.choice([0, 1], num_employees, p=[0.9, 0.1]),  # 10% attrition rate
        'Gender': np.random.choice(['Male', 'Female', 'Non-binary'], num_employees, p=[0.48, 0.48, 0.04]),
    }
    df = pd.DataFrame(data)

    # Introduce some patterns for diagnostic/predictive simulation
    # Higher attrition in Engineering for demo purposes
    df.loc[df['Department'] == 'Engineering', 'Attrition'] = np.random.choice([0, 1], df[df['Department'] == 'Engineering'].shape[0], p=[0.7, 0.3])
    # Lower engagement for some attrition cases
    df.loc[df['Attrition'] == 1, 'EngagementScore'] = np.random.randint(40, 70, df[df['Attrition'] == 1].shape[0])

    df['TenureYears'] = (pd.to_datetime('today') - df['HireDate']).dt.days / 365.25
    return df
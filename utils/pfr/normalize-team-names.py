import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('data/pfr/normalized_pfr_odds.csv')  # Update with the actual path to your CSV file

# Function to extract away and home teams from the Title
def extract_teams(title):
    # Split the title by ' at ' to separate away and home teams
    teams = title.split(' at ')
    away_team = teams[0].strip().replace('"', '')  # Remove leading/trailing spaces and quotes
    home_team = teams[1].split(' - ')[0].strip()  # Extract home team before the dash and date
    return away_team, home_team

# Apply the function to extract teams and create new columns
df[['away_team', 'home_team']] = df['Title'].apply(lambda x: pd.Series(extract_teams(x)))

# Display the updated DataFrame
print(df.head())

# Save the updated DataFrame if needed
df.to_csv('data/pfr/final_pfr_odds.csv', index=False)  # Update with the desired save path

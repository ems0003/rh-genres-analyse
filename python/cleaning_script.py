#Import the libraries
import pandas as pd

#Charge the dataset
df_raw = pd.read_excel('./data/raw_chomageDataset.xlsx')

#Melt  the year columns (from 2015 to 2024)
years_columns = [str(year) for year in range(2015, 2025)] # Create a list of year columns in one line

df_cleaned = pd.melt(
    df_raw,
    id_vars=['SEX','AGE','ISO'],
    value_vars=years_columns,
    var_name='ANNEE',
    value_name='TAUX_CHOMAGE'
)

#Check the data types of the columns
df_cleaned['TAUX_CHOMAGE'] = pd.to_numeric(df_cleaned['TAUX_CHOMAGE'], errors='coerce') # Convert the 'TAUX_CHOMAGE' column to numeric, coercing errors to NaN
df_cleaned['ANNEE'] = df_cleaned['ANNEE'].astype(int) # Convert the 'ANNEE' column to integer type  

#delete the rows with NaN values in the 'TAUX_CHOMAGE' column
df_cleaned = df_cleaned.dropna(subset=['TAUX_CHOMAGE']) # Drop rows where 'TAUX_CHOMAGE' is NaN 

#Save the cleaned dataset to a new CSV file
df_cleaned.to_excel('./data/cleaned_chomageDataset.xlsx',sheet_name='Cleaned Data', index=False) # Save the cleaned DataFrame to a new Excel file without the index   
df_cleaned.to_csv('./data/cleaned_chomageDataset.csv', index=False) 
print("Nettoyage terminé. Le fichier nettoyé a été enregistré sous le nom 'cleaned_chomageDataset.xlsx'.") # Print a message indicating that the cleaning is complete and the file has been saved        

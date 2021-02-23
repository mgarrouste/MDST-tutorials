"""
Checkpoint 1b

*First complete the steps in checkpoint1a.pdf

Here you will create a script to preprocess the data given in starbucks.csv. You may want to use
a jupyter notebook or python terminal to develop your code and test each function as you go... 
you can import this file and its functions directly:

    - jupyter notebook: include the lines `%autoreload 2` and `import preprocess`
                        then just call preprocess.remove_percents(df) to test
                        
    - python terminal: run `from importlib import reload` and `import preprocess`
                       each time you modify this file, run `reload(preprocess)`

Once you are finished with this program, you should run `python preprocess.py` from the terminal.
This should load the data, perform preprocessing, and save the output to the data folder.

"""
import pandas as pd

def remove_convert(percentage):
        return float(percentage[:-1])
    
def remove_percents(df, col):
    df[col] = df[col].apply(remove_convert) 
    return df

def replace(value):
    if isinstance(value, str):
        return remove_convert(value)
    elif isinstance(value, float): 
        return value
    else :
        return float('nan')

def fill_zero_iron(df):
    df['Iron (% DV)'] = df['Iron (% DV)'].apply(replace)
    df['Iron (% DV)'].fillna(value=df['Iron (% DV)'].mean(), inplace=True)
    return df
    
def fix_caffeine(df):
    def convert(value): 
        try: 
            float(value)
            return float(value)
        except:
            return float('Nan')
    df['Caffeine (mg)'] = df['Caffeine (mg)'].apply(convert)
    df['Caffeine (mg)'].fillna(value=df['Caffeine (mg)'].mean(), inplace=True)
    df.fillna(df.mean(), inplace=True)
    return df

def replace_nonalpha(name):
    import re
    new_name = re.sub("[^0-9a-zA-Z]+", " ", name)
    return new_name

def fix_strings(df,col):
    df[col] = df[col].apply(replace_nonalpha)
    df[col] = df[col].apply(str.lower)
    return df

def clean_title(title):
    split_title = title.split("(",1)
    new_title = split_title[0].strip().lower()
    return new_title 

def standardize_names(df):
    df.rename(mapper = clean_title, axis = 1, inplace=True)
    return df


def main():
    
    # first, read in the raw data
    df = pd.read_csv('../data/starbucks.csv')
    
    # the columns below represent percent daily value and are stored as strings with a percent sign, e.g. '0%'
    # complete the remove_percents function to remove the percent symbol and convert the columns to a numeric type
    pct_DV = ['Vitamin A (% DV)', 'Vitamin C (% DV)', 'Calcium (% DV)']
    for col in pct_DV:
        df = remove_percents(df, col)
    df.head()
    # the column 'Iron (% DV)' has missing values when the drink has no iron
    # complete the fill_zero_iron function to fix this
    df = fill_zero_iron(df)

    # the column 'Caffeine (mg)' has some missing values and some 'varies' values
    # complete the fix_caffeine function to deal with these values
    # note: you may choose to fill in the values with the mean/median, or drop those values, etc.
    df = fix_caffeine(df)
    
    # the columns below are string columns... starbucks being starbucks there are some fancy characters and symbols in their names
    # complete the fix_strings function to convert these strings to lowercase and remove non-alphabet characters
    names = ['Beverage_category', 'Beverage']
    for col in names:
        df = fix_strings(df, col)
    
    # the column names in this data are clear but inconsistent
    # complete the standardize_names function to convert all column names to lower case and remove the units (in parentheses)
    df = standardize_names(df)
    
    # now that the data is all clean, save your output to the `data` folder as 'starbucks_clean.csv'
    # you will use this file in checkpoint 2
    #print(df)
    df.to_csv('../data/starbucks_clean.csv')
    
    

if __name__ == "__main__":
    main()

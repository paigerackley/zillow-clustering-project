import pandas as pd
import numpy as np

import os
from env import get_db_url

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler

## ACQUIRE ##

def get_zillow():
    '''
    This function acquires the requisite zillow data from the Codeup SQL database and caches it locally it for future use in a csv 
    document; once the data is accessed the function then returns it as a dataframe.
    '''
    filename = "zillow.csv"
    
    url = get_db_url('zillow')

    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        query = '''
   SELECT
        prop.*,
        predictions_2017.logerror,
        predictions_2017.transactiondate,
        air.airconditioningdesc,
        arch.architecturalstyledesc,
        build.buildingclassdesc,
        heat.heatingorsystemdesc,
        landuse.propertylandusedesc,
        story.storydesc,
        construct.typeconstructiondesc
    FROM properties_2017 prop
    JOIN (
        SELECT parcelid, MAX(transactiondate) AS max_transactiondate
        FROM predictions_2017
        GROUP BY parcelid
    ) pred USING(parcelid)
    JOIN predictions_2017 ON pred.parcelid = predictions_2017.parcelid
                          AND pred.max_transactiondate = predictions_2017.transactiondate
    LEFT JOIN airconditioningtype air USING (airconditioningtypeid)
    LEFT JOIN architecturalstyletype arch USING (architecturalstyletypeid)
    LEFT JOIN buildingclasstype build USING (buildingclasstypeid)
    LEFT JOIN heatingorsystemtype heat USING (heatingorsystemtypeid)
    LEFT JOIN propertylandusetype landuse USING (propertylandusetypeid)
    LEFT JOIN storytype story USING (storytypeid)
    LEFT JOIN typeconstructiontype construct USING (typeconstructiontypeid)
    WHERE prop.latitude IS NOT NULL
      AND prop.longitude IS NOT NULL
      AND transactiondate <= '2017-12-31'
      AND propertylandusedesc = "Single Family Residential"
'''

## SPLIT ##
def train_validate_test_split(df, seed=123):
    '''
    This function takes in a dataframe, the name of the target variable, and an integer for a setting a seed
    and splits the data into train, validate and test.
    Test is 20% of the original dataset, validate is .30*.80= 24% of the
    original dataset, and train is .70*.80= 56% of the original dataset.
    The function returns, in this order, train, validate and test dataframes.
    '''
    train_validate, test = train_test_split(df, test_size=0.2,
                                            random_state=123, stratify = df.fips)
    train, validate = train_test_split(train_validate, test_size=0.3,
                                       random_state=123, stratify = df.fips)
    return train, validate, test



def handle_missing_values(df, prop_required_column = .5, prop_required_row = .75):
    threshold = int(round(prop_required_column*len(df.index),0))
    df.dropna(axis=1, thresh=threshold, inplace=True)
    threshold = int(round(prop_required_row*len(df.columns),0))
    df.dropna(axis=0, thresh=threshold, inplace=True)
    return df

#### Wrangle / Prep ####

def wrangle_zillow():
    """
    Acquires Zillow data
    Handles nulls
    optimizes or fixes data types
    handles outliers w/ manual logic
    returns a clean dataframe
    """ 
    
    # Acquire function 
    df = get_zillow()

    df = handle_missing_values(df)

    # handle nulls
    df = df.drop(columns=['calculatedbathnbr', 'finishedsquarefeet12', 'fullbathcnt', 'id', 'id.1'], axis=1)
    df = df.drop(columns=['buildingqualitytypeid', 'regionidcity', 'regionidzip', 'regionidneighborhood', 'roomcnt', 'unitcnt'], axis=1)
    df = df.drop(columns=['numberofstories','structuretaxvaluedollarcnt', 'landtaxvaluedollarcnt', 'taxvaluedollarcnt', 'taxamount', 'assessmentyear'],  axis=1)
    df = df.drop(columns=['airconditioningdesc', 'airconditioningtypeid', 'heatingorsystemdesc', 'heatingorsystemtypeid', 'regionidcounty'], axis=1)
    df = df.drop(columns=['propertyzoningdesc','censustractandblock', 'rawcensustractandblock'], axis=1)
    df[['garagecarcnt', 'garagetotalsqft']] = df[['garagecarcnt', 'garagetotalsqft']].fillna(0)
    df['poolcnt'] = df['poolcnt'].fillna(0)
    
    # rename counties
    counties = {6037: 'los_angeles',
                6059: 'orange',
                6111: 'ventura'}
    # map counties to fips codes
    df.fips = df.fips.map(counties)
    df.rename(columns=({ 'fips': 'county'}), inplace=True)

    # remove outliers
    df = df[df.bathroomcnt >= 1]
    df = df[df.bathroomcnt <= 5]
    df = df[df.bedroomcnt >= 1]
    df = df[df.bedroomcnt <= 5]
    df = df[df.logerror < 0.5]
    df = df[df.logerror > (-0.31)]
    df = df[df.yearbuilt >= 1910]
    df = df[df.calculatedfinishedsquarefeet >= 650]
    df = df[df.calculatedfinishedsquarefeet <= 5500]
    df = df[df.taxvaluedollarcnt > 40000.0]
    df = df[df.taxvaluedollarcnt < 3000000.0]
    df = df.dropna(thresh=df.shape[0]*0.2,how='all',axis=1)

    # get single unit homes
    single_unit = [261, 262, 263, 264, 266, 268, 273, 276, 279]
    df = df[df.propertylandusetypeid.isin(single_unit)]

    







## all together

# Scaling??

# def wrangle_split_scale():
    
    df = wrangle_zillow()
    train, validate, test = train_validate_test_split(df)
    train_scaled, validate_scaled, test_scaled = scale_data(train, validate, test)
    
    return train_scaled, validate_scaled, test_scaled


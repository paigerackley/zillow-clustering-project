# <center><a name="top"></a>Clustering Project: Zillow Logerror Prediction
![](https://github.com/paigerackley/zillow-clustering-project/blob/main/images/zill.png)

by: Paige Rackley </center>

<p>
  <a href="https://github.com/paigerackley" target="_blank">
    <img alt="Paige" src="https://img.shields.io/github/followers/paigerackley?label=Follow_Paige&style=social" />
  </a>

 * * *  
[[Project Description](#project_description)]
[[Project Planning](#planning)]
[[Data Dictionary](#dictionary)]
[[Data Acquire and Prep](#wrangle)]
[[Data Exploration](#explore)]
[[Modeling](#model)]
[[Conclusion](#conclusion)]
___



## <a name="project_description"></a>Project Description:
The goal of this project is to identify drivers of error looking at logerror. The reason we want to be able to predict logerror to to better improve our current models. Improving our models helps better serve our customers at Zillow because we can give them the data they request without error. We want our customers to trust us and the best way to get them to do that is to be able to give them info that is accurate.



  
***
## <a name="planning"></a>Project Planning:
  
  
 ### Business Goals: 
 - Use clustering algorithms to help determine predictors of logerror to help improve the performance of our current model.
 - Using drivers of logerror to help imrpove our model of property values.
 - Improve understanding of logerror to better inform the use of models for property prediction.

 ### Audience:
 - My audience is the Zillow Data Science team. 
  
 ### Deliverables:
 - A final report notebook to be walked through during presentation.
 - Notebooks used while working through data. 
 - Modules used during project to be used to replicate.

###  Executive Summary: 
Our goal was to find drivers, find clusters, and test them to see if there was any strong relationship. With those, we tested to see if we can beat our baseline model. We did not get to beat the baseline. 
        
### Initial Hypothesis/Questions: 
- There is a relationship between yearbuilt and logerror.
- There is a relationship between county and logerror, but not specifically one county.
- There is a relationship between bedroomcnt and logerror.
- There was not a strong relationship between the clusters created.


[[Back to top](#top)]


## <a name="dictionary"></a>Data Dictionary  
Target|Datatype|Definition|
|:-------|:--------|:----------|
| logerror | float64 | Log Error |

|Feature|Datatype|Definition|
|:-------|:--------|:----------|
| bedroomcnt       | float64 |    number of bedrooms |
| bathroomcnt        | float64 |    number of bathrooms |
| scalculatedfinishedsquarefeet       | float64 |    total square feet of home |
| county       | object |    county/zipcode |
| latitude      | float64 |    latitude of home |
| longitude       | float64 |    longitude of home |
| lotsizesquarefeet | float64 | Square feet of lot |
| propertylandusetypeid | float64 | Property Land Use type ID |
| rawcensustractandblock | float64 | Raw Census |
| regionidcounty | float64 | Region ID for county |
| regionidzip | float64 | Region ID for zipcode |
| yearbuilt | float64 | Year home was built |
| taxvaluedollarcnt | float64 | Tax Vallue total |
| assessmentyear | float64 | Assessment Year |
  
  
  
  
[[Back to top](#top)]

## <a name="wrangle"></a>Data Acquisition and Preparation
  
 ## Acquire
#### Data was acquired from Zillow database in MySQL Workbench.
  
  In this step, I used SQL queries to pull what I wanted from Zillows tables.


  
## Prepare

In this step, I created multiple functions that were meant to help me prepare my data for both exploration and modeling.

<b><font color = 'green'> handle_missing_values:</b></font> How to handle missing values based on minimum percentage of values for rows and columns

<b><font color = 'green'> wrangle_zillow:</b></font> The wrangle function has the acquire and handle_missing_values nested in it. This function is to explore on independent variables, which will help us decide what to use for clustering later.

Steps implemented: 

    - Get rid of null values in my columns (lose a lot of bulk, nearly no data loss) and redundant columns.
    - For the 'fips' column I both encode the zip codes to the appropriate countys (Los Angeles, Ventura, Orange County) and rename the column to 'County' for readability.
    - Removed outliers to many columns:
       - Bathroom and bedroom count range to 1 - 5
       - Logerror range to 0.5 to -0.31
       - Year built houses older than 1910
       - calculatefinishedsquarefeet range to 650 - 5500
       - taxvalluedollarcnt range to 40000 - 300000
<b><font color = 'green'> split:</b></font> This function splits the data into the 3 sets needed for exploring and statistical tests. I stratify on 'county' in this step.

<b><font color = 'green'>scale_data:</b></font> This function scales the the 3 split data sets. 

<b><font color = 'green'>wrangle_split_scale:</b></font>  This function combines everything in to one. We will do our clustering, testing, and modeling here.

  
[[Back to top](#top)]


  
## <a name="explore"></a>Data Exploration:
###  Explore

## The Big Questions: Can clustering help us predict logerror? Can clustering help us beat the baseline?

Our target variable is logerror, so we will be comparing it to individual features as well as combinations of features (clusters). 

For this Zillow project, since we would be using clustering, I wanted to focus on the major key features we have to work with and cluster features that are similar. I came up with three major themes:
1. Land - refers to the house itself. The size, year it was built, how many rooms, etc.
2. Location - refers to the geological location of the home.
3. Tax - refers to the taxes paid on the home. 

  
   
 
[[Back to top](#top)]

### Takeaways from exploration:
 - All 3 clusters after testing failed to reject null hypothesis and didn't have any significant results.


## <a name="model"></a>Modeling:
  

  
[[Back to top](#top)]



## <a name="conclusion"></a>Conclusion:

## In conclusion:

- The model does not do better than the baseline.
- Using the unstructured ML method of cluster models does not show to be the best model method when it comes to determining logerror predictions.
- <b> yearbuilt</b> may be an indicator of logerror; however, this requires more investigation.
- Most important takeaway is that more time is needed to explore the data.
- Although some Key drivers were found, and while they do have a relationship with logerror, many do not have a strong positive relationship with logerror.




### With more time:
- logerror outliers would be beneficial to focus on.
- I would like to try classification models on the data. This may or may not beat the baseline model, but it could still bring in new takeaways.


### Recommendations: 
- I would recommend to continue improving upon the baseline model as it works well enough given the current situation.
- I would recommend pursuing further identifications of key drivers for logerror to potentially construct better accurate predictors.

[[Back to top](#top)]
  
  
  **How to Reproduce**
- [x] Read this README.md
- [ ] Download modules into your working directory.
- [ ] Create a .gitignore for env.py since it contains confidential info such as username and password to access SQL databases.
- [ ] Have fun doing your own exploring, modeling, and more! 

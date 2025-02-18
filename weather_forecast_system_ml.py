# -*- coding: utf-8 -*-
"""Weather Forecast System_ML

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ebRpdN5GE9zIk2zodQ5VPagveGVJS2Bv
"""

# Importing the fundamental libraries of data science

import pandas as pd                       # For Data Analysis and Preprocessing
import numpy as np                        # For Mathematical Operations on Data
import matplotlib.pyplot as plt           # For Visualization and Setting Graph Elements
import seaborn as sns                     # Consists of Easy and Interactive Statistical Graphics

url = "https://raw.githubusercontent.com/AmanCSE-1/Smart-Weather-Prediction-using-ML/main/India%20Weather%20History.csv"
df = pd.read_csv(url)                     # Reading the Dataset

df.head()                                 # Printing the First 5 Rows of the Dataset

df.shape                          # Returns the number of rows and number of columns of dataset

df.columns                        # Returns the name of columns of dataset

df.info()           # to get a consice summary of the dataframe

# Converts arguement to datetime
df['Formatted Date'] = pd.to_datetime(df['Formatted Date'], utc=True)

# Checking the datatype of the column by using dtype attribute
df['Formatted Date'].dtype

import datetime as dt

# Extracting Date (yyyy-mm-dd) from 'Formatted Date' column
df['Date'] = df['Formatted Date'].dt.date
df['Date'] = pd.to_datetime(df['Date'])

# Extracting Time (hh) from 'Formatted Date' column (Note: We are only extracting hour because all observations have {mm-ss} as {00-00})
df['Time'] = df['Formatted Date'].dt.hour

df.drop(columns='Formatted Date', inplace=True)                 # Now, we drop the Formatted Date column

# We want to place the recently created columns-'Date' and 'Time' as first two columns in our DataFrame
# So, first we pop them out and insert them into 0th and 1th position respectively

first_column = df.pop('Date')
second_column = df.pop('Time')

df.insert(0, 'Date', first_column)
df.insert(1, 'Time', second_column)

df.head()

df.describe()         # Used to describe various statistical measures for quantitative columns
                      # Mean, Median(Q2) describes the characteristic of distribution of column
                      # 25% (Q1),  50% (Q2) and 75 (Q3) are Quartiles of the features.
                      # std is Standard Deviation i.e. depicts spread  of the distribution
                      # min and max are known to everybody :)

df.isna().sum()             # Returns the sum of rows that contains null values for each column

month = df['Date'].dt.month

monthly_avg = df.groupby(month)['Temperature (C)'].mean()

# Dropping the 'Loud Cover' Column as it contains all rows with value '0'.
# It will not add any value to the model

df.drop('Loud Cover', axis=1, inplace=True)

month = df['Date'].dt.month

monthly_avg = df.groupby(month)['Temperature (C)'].mean()

year = df['Date'].dt.year

annual_avg = df.groupby(year)['Temperature (C)'].mean()

plt.subplots_adjust(left=0, right=2, bottom=0, top=1, wspace=0.3, hspace=0.1)

plt.subplot(1, 2, 1)
month_abb = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
sns.lineplot(x=month_abb, y=monthly_avg.values, color='blue', linestyle="-")
plt.xlabel('Months')
plt.ylabel("Average Temperature in \N{DEGREE SIGN}C")
plt.title('Variation of Mean Monthly Temperature')

plt.subplot(1, 2, 2)
sns.lineplot(x=annual_avg.index, y=annual_avg.values, color='orange', linestyle="solid")
plt.xlim([2006, 2016])
plt.xlabel('Year')
plt.ylabel("Average Temperature in \N{DEGREE SIGN}C")
plt.title('Variation of Mean Annual Temperature')

plt.show()

# To visualize the relation between two columns, we will plot scatterplot
# Here, our predictor variable for Linear Regression model is Temperature

# used to adjust the subplot size and spacing between them
plt.subplots_adjust(left=0, right=2, bottom=0, top=1, wspace=0.3, hspace=0.1)

# First subplot - Relation between Temperature and Humidity
plt.subplot(1,2,1)
plt.title('Relation between Temperature and Humidity')
sns.scatterplot(data=df.sample(1000, random_state=1), x='Temperature (C)', y='Humidity')

# Second subplot - Relation between Temperature and Apparent Temperature
plt.subplot(1,2,2)
plt.title('Relation between Temperature and Apparent Temperature')
sns.scatterplot(data=df.sample(1000, random_state=1), x='Temperature (C)', y='Apparent Temperature (C)')

plt.show()

df['Summary'].value_counts()

df['Precip Type'].nunique()

plt.figure(figsize=(8,6))
precip = sns.countplot(x=df['Precip Type'])
plt.title('Graph of occurence of values of Precip Type')

for p in precip.patches:
  txt = str(round(p.get_height()/df.shape[0]*100, 2)) + '%'
  txt_x = p.get_x() + p.get_width()/2 -0.07
  txt_y = p.get_height()+400
  precip.text(txt_x, txt_y, txt, size=12)

plt.show()

plt.figure(figsize=(8,6))
precip = sns.countplot(x=df['Precip Type'])
plt.title('Graph of occurence of values of Precip Type')

for p in precip.patches:
  txt = str(round(p.get_height()/df.shape[0]*100, 2)) + '%'
  txt_x = p.get_x() + p.get_width()/2 -0.07
  txt_y = p.get_height()+400
  precip.text(txt_x, txt_y, txt, size=12)

plt.show()

plt.figure(figsize=(14,7))

df['Summary'].value_counts().plot(kind='bar')

plt.ylabel('Count')
plt.xlabel('Weather Summary')
plt.title('Visualization of Weather Summary Feature')
plt.xticks(rotation=80)
plt.show()

# We will first estimate their percentage of occurence within the dataset.

# The below code uses "Boolean Masking" technique of python.
# Here, we will not consider the rows have ['Partly Cloudy', 'Mostly Cloudy', 'Overcast', 'Foggy' and 'Clear']
df[(df['Summary']!='Partly Cloudy') & (df['Summary']!='Mostly Cloudy') &
     (df['Summary']!='Overcast') & (df['Summary']!='Foggy') & (df['Summary']!='Clear')].shape[0]/df.shape[0]*100

# storing the index for unclean data for preprocessing
uncleanData_index = df[(df['Summary']!='Partly Cloudy') & (df['Summary']!='Mostly Cloudy') &
     (df['Summary']!='Overcast') & (df['Summary']!='Foggy') & (df['Summary']!='Clear')].index

# Creating a copy of dataset
df_preprocessed = df.copy()

# Iterating through the unclean_data index
for row in uncleanData_index:

      # Using string matching technique
      if 'Partly Cloudy' in df_preprocessed['Summary'][row]:
          df_preprocessed.loc[row, 'Summary'] = 'Partly Cloudy'

      elif 'Mostly Cloudy' in df_preprocessed['Summary'][row]:
          df_preprocessed.loc[row, 'Summary'] = 'Mostly Cloudy'

      elif 'Overcast' in df_preprocessed['Summary'][row]:
          df_preprocessed.loc[row, 'Summary'] = 'Overcast'

      elif 'Foggy' in df_preprocessed['Summary'][row]:
          df_preprocessed.loc[row, 'Summary'] = 'Foggy'

# We check that preprocessed data has retained all the rows of the original dataset

df_preprocessed.shape

df_preprocessed['Summary'].value_counts()

uncleanData_index = df_preprocessed[(df_preprocessed['Summary']!='Partly Cloudy') & (df_preprocessed['Summary']!='Mostly Cloudy') &
     (df_preprocessed['Summary']!='Overcast') & (df_preprocessed['Summary']!='Foggy') & (df_preprocessed['Summary']!='Clear')].index

uncleanData_index.shape[0]/df.shape[0]*100

df_preprocessed.drop(index=uncleanData_index, inplace=True)

plt.figure(figsize=(14,8))

df_preprocessed['Summary'].value_counts().plot(kind='bar')

plt.ylabel('Count')
plt.xlabel('Weather Summary')
plt.title('Summary Feature after Preprocessing')
plt.xticks(rotation=0)
plt.show()

precip_na_index = df_preprocessed.loc[pd.isna(df_preprocessed['Precip Type']), :].index

for row in precip_na_index:
    if df_preprocessed.loc[row, 'Temperature (C)']<=0:
        df_preprocessed.loc[row, 'Precip Type'] = 'snow'
    else :
        df_preprocessed.loc[row, 'Precip Type'] = 'rain'

df_preprocessed['Precip Type'].isna().sum()

from sklearn.preprocessing import LabelBinarizer, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, confusion_matrix, accuracy_score, classification_report
import joblib

## Model Selection - Splitting Training and Test Dataset
x = df_preprocessed.loc[:, ['Apparent Temperature (C)', 'Humidity']]
y = df_preprocessed.loc[:, 'Temperature (C)']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

## Building the Model
from sklearn.linear_model import LinearRegression

lrmodel = LinearRegression()

lrmodel.fit(x_train, y_train)
temp_predict = lrmodel.predict(x_test)

## Linear regression Model Evaluation
r2_value = r2_score(temp_predict, y_test)
print("R-Squared Score of the Linear Regression Model is", round(r2_value, 4))

mean_sq_error = mean_squared_error(temp_predict, y_test)
print("Mean Square Error of the Linear Regression Model is", round(mean_sq_error, 2))

## Visualizing the Prediction
from yellowbrick.regressor import PredictionError

visualizer = PredictionError(lrmodel).fit(x_train, y_train)
visualizer.score(x_test.sample(500, random_state=1), y_test.sample(500, random_state=1))

visualizer.poof()

## Encoding the Categorical Variables
lb = LabelBinarizer()

df_preprocessed['Precip Type Binary'] = lb.fit_transform(df_preprocessed['Precip Type'])
df_preprocessed['Precip Type Binary'].value_counts()

## Splitting Dataset
x = df_preprocessed.loc[:, ['Temperature (C)', 'Humidity', 'Visibility (km)']]
y = df_preprocessed.loc[:, 'Precip Type Binary']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

## Building the Model
from sklearn.linear_model import LogisticRegression

logmodel = LogisticRegression()
logmodel.fit(x_train, y_train)
precip_predict = logmodel.predict(x_test)


## Logistic Regression Model Evaluation
print("R-Squared Score of the Logistic Regression Model is", round(r2_score(precip_predict, y_test), 4))

print("Accuracy is", round(accuracy_score(y_test, precip_predict), 4))

plt.figure(figsize=(6, 4))
cf_matrix = confusion_matrix(y_test, precip_predict)

sns.heatmap(cf_matrix, annot=True, cmap='Blues', fmt='0')
plt.xlabel('Predicted Class')
plt.ylabel('True Class')

plt.title('Confusion Matrix for Logistic Regression Model')
plt.show()

print(classification_report(y_test, precip_predict))

user_input_temp = int(input('Enter the Temperature in Celsius : '))
user_input_humid = float(input('Enter the Humidity : '))
user_input_visiblity = float(input('Enter the Visibility : '))


result2 = logmodel.predict([[user_input_temp, user_input_humid, user_input_visiblity]])
result2 = lb.inverse_transform(result2)
print("Expected Precipitation Type is :", result2[0])

df_preprocessed['Month'] = df_preprocessed['Date'].dt.month

le = LabelEncoder()

df_preprocessed['Summary Encoded'] = le.fit_transform(df_preprocessed.loc[:, 'Summary'])

x = df_preprocessed.loc[:, ['Temperature (C)', 'Humidity', 'Visibility (km)', 'Pressure (millibars)', 'Wind Speed (km/h)', 'Month']]
y = df_preprocessed.loc[:, 'Summary Encoded']

from imblearn.over_sampling import SMOTE

smote = SMOTE()

x, y = smote.fit_resample(x, y)

x.shape[0], y.shape[0]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

from sklearn.naive_bayes import GaussianNB

classifier  = GaussianNB()

classifier.fit(x_train, y_train)
summary_predict = classifier.predict(x_test)

print("Accuracy of Naive Bayes Algorithm is {}".format(round(accuracy_score(y_test, summary_predict), 2)*100))

from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=25)
knn.fit(x_train, y_train)
summary_predict = knn.predict(x_test)

print("Accuracy of KNN Algorithm is " + '%.2f' %(round(accuracy_score(y_test, summary_predict), 2)*100))

from sklearn.ensemble import RandomForestClassifier

rforest = RandomForestClassifier(max_depth=55, random_state=1)

rforest.fit(x_train, y_train)
summary_predict = rforest.predict(x_test)

print("Accuracy of Random Forest Algorithm is", round(accuracy_score(y_test, summary_predict), 2)*100)

user_input = [30,0.10,0.1,1000, 45 ,10]

result3 = rforest.predict([user_input])
result3
print(le.inverse_transform(result3))

plt.title('Confusion Matrix for Random Forest Classifier')
sns.heatmap(confusion_matrix(y_test, summary_predict), annot=True, fmt='0', cmap='Blues')
plt.xlabel('Predicted Class')
plt.ylabel('True Class')
plt.show()

print(classification_report(y_test, summary_predict))
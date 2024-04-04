# -*- coding: utf-8 -*-
"""House Prices

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11cBR_W7B0xF5G4sIrDBYZBVOHFDIfMfk
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from sklearn.metrics import mean_squared_error

# loading the dataset from drive
!pip install -Uqq fastbook
import fastbook
fastbook.setup_book()
from fastbook import *

! [ -e /content ] && pip install -Uqq fastai

from google.colab import drive
drive.mount('/content/drive')

from fastai.vision import *
path1 = '/content/drive/MyDrive/HousePrices/train.csv'
path2 = '/content/drive/MyDrive/HousePrices/test.csv'

# loading the dataset to Pandas Dataframe
house_test = pd.read_csv('/content/drive/MyDrive/HousePrices/test.csv')
house_train = pd.read_csv('/content/drive/MyDrive/HousePrices/train.csv')

print(house_train)

house_train.head()

house_train.tail()

house_train.info()

house_train.isnull().sum()

#remove unnecessary variables from train and test data
house_train.drop(columns = ['MiscFeature', 'Fence', 'PoolQC', 'FireplaceQu', 'MasVnrType', 'Alley', 'LotFrontage'], axis = 1, inplace = True)
house_test.drop(columns = [ 'MiscFeature', 'Fence', 'PoolQC', 'FireplaceQu', 'MasVnrType', 'Alley', 'LotFrontage'], axis = 1, inplace = True)

#Display summary statistics of numerical features
house_train.describe()

house_train.isnull().sum()

import seaborn as sns
import matplotlib.pyplot as plt

# Select numerical variables for correlation analysis
numerical_variables = ['GrLivArea', 'TotalBsmtSF', 'SalePrice', 'OverallQual', 'OverallCond']

# Calculate correlation matrix
correlation_matrix = house_train[numerical_variables].corr()

# Create heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Correlation Heatmap of Numerical Variables')
plt.show()

# Set style for seaborn
sns.set(style="whitegrid")

# Plot histograms and density plots for numerical variables
numerical_variables = ['GrLivArea', 'TotalBsmtSF', 'SalePrice']

# Create subplots
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(12, 12))

# Plot histograms
for i, var in enumerate(numerical_variables):
    sns.histplot(house_train[var], kde=True, ax=axes[i, 0], color='skyblue', bins=30)
    axes[i, 0].set_title(f'Histogram of {var}')
    axes[i, 0].set_xlabel(var)
    axes[i, 0].set_ylabel('Frequency')

# Plot density plots
for i, var in enumerate(numerical_variables):
    sns.kdeplot(house_train[var], ax=axes[i, 1], color='salmon', fill=True)
    axes[i, 1].set_title(f'Density Plot of {var}')
    axes[i, 1].set_xlabel(var)
    axes[i, 1].set_ylabel('Density')

# Adjust layout
plt.tight_layout()

# Show plot
plt.show()

# Box Plots
plt.figure(figsize=(12, 6))
sns.boxplot(x='OverallQual', y='SalePrice', data=house_train)
plt.title('Box Plot of SalePrice by OverallQual')
plt.xlabel('OverallQual')
plt.ylabel('SalePrice')
plt.show()

# Scatter Plots
plt.figure(figsize=(10, 6))
sns.scatterplot(x='GrLivArea', y='SalePrice', data=house_train)
plt.title('Scatter Plot of SalePrice vs GrLivArea')
plt.xlabel('GrLivArea')
plt.ylabel('SalePrice')
plt.show()

# Regression Line Plot
plt.figure(figsize=(10, 6))
sns.regplot(x='GrLivArea', y='SalePrice', data=house_train, scatter_kws={"color": "blue"}, line_kws={"color": "red"})
plt.title('Regression Line Plot of SalePrice vs GrLivArea')
plt.xlabel('GrLivArea')
plt.ylabel('SalePrice')
plt.show()

# Bar Plots
plt.figure(figsize=(10, 6))
sns.barplot(x='Neighborhood', y='SalePrice', data=house_train, ci=None)
plt.title('Average SalePrice by Neighborhood')
plt.xlabel('Neighborhood')
plt.ylabel('Average SalePrice')
plt.xticks(rotation=45)
plt.show()

# Preprocessing for training data
data_train = house_train[['GrLivArea', 'BedroomAbvGr', 'FullBath', 'HalfBath', 'SalePrice']].copy()
data_train.dropna(inplace=True)
X_train = data_train.drop(columns=['SalePrice'])
y_train = data_train['SalePrice']

# Preprocessing for test data
data_test = house_test[['GrLivArea', 'BedroomAbvGr', 'FullBath', 'HalfBath']].copy()
data_test.dropna(inplace=True)
X_test = data_test

# Initialize and train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test data
y_pred = model.predict(X_test)

# Optionally, you can save the predictions to a CSV file if needed
# Create a DataFrame for the predictions
predictions_df = pd.DataFrame({
    'Id': house_test['Id'],
    'SalePrice': y_pred
})

predictions_df.to_csv('/content/drive/MyDrive/HousePrices/predictions.csv', index=False)

from sklearn.metrics import r2_score
# y_test: true target values of the test set

# Calculate R^2 score
r2 = r2_score(y_test, y_pred)
print("R^2 Score:", r2)
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from collections import Counter
"""
place to write functions for use in other files
"""


"""
-- Scale Inputs --
Inputs should either be...
1. Normalized
- Scaled to a range between 0 and 1
If the distribution of a feature is NOT normal than it should be normalized.  You don't want to mess with the funky
distribution, but embrace and learn on it.
Will probably most of the time normalize
or 
2. Standardized
- Scaled to a mean of 0 and standard deviation of 1
If the distribution of a feature is normal (gaussian bell curve) then it should be standardized
"""


def normalize_input_features(dataframe, columnNames=[], returnScaleUserInputList=False):
    """
    Normalize between 0 and 1
    function to normalize input features of a given pandas dataframe.  When not given a list of columnNames it will
    normalize all features including categorical by converting to numbered ints and then normalizing.

    When returnScaleUserInputList is set to True it will also return an object for normalizing other input later on.  Can be useful
    for normalizing user input.
    """
    if not columnNames:  # list is empty, process all input features
        columnNames = dataframe.columns.values.tolist()[:-1]  # get column names except last column
    scaler = MinMaxScaler()  # initialize scaler object with sklearn MinMaxScaler
    scaleUserInputList = []  # setup scaleList to be populated with information for normalizing user input
    for col in columnNames:
        try:  # try to process data as numerical
            _ = int(dataframe[col].iloc[0])  # ensure that feature is float/int
            # save min and max values for processing user input
            scaleUserInputList.append(["numerical", [dataframe[col].min(), dataframe[col].max()], col])
            dataframe[[col]] = scaler.fit_transform(dataframe[[col]])  # normalize between 0 and 1
        except:  # process data that is categorical
            # change categorical data to numerical ints starting at zero
            dataframe, targetLookupTable = scale_categorical_data(dataframe=dataframe, columnNames=[col],
                                                                  returnTargetLookupTable=True)
            # reverse the targetLookupTable so it can be used to transform user input to numerical ints
            intLookupTable = {}
            for key, value in targetLookupTable.items():
                intLookupTable[value] = key
            dataframe[[col]] = scaler.fit_transform(dataframe[[col]])  # normalize
            # save lookup table for processing user input
            scaleUserInputList.append(["categorical", intLookupTable, col])
    if returnScaleUserInputList:
        return dataframe, scaleUserInputList
    return dataframe


def scale_categorical_data(dataframe, columnNames=[], returnTargetLookupTable=False):
    if not columnNames:  # list is empty, only update last col
        columnNames = [list(dataframe.columns)[-1]]
    for col in columnNames:
        uniques = dataframe[col].unique()
        targetLookupTable = {}  # only really works on last column
        for index, category in enumerate(uniques):
            # print(index, category)  # print out values
            if returnTargetLookupTable:
                targetLookupTable[index] = category
            dataframe.loc[dataframe[col] == category, col] = index
    if returnTargetLookupTable:
        return dataframe, targetLookupTable
    return dataframe


def scale_user_input(userInput, scale):
    min = scale[0]
    max = scale[1]
    if userInput < min:
        print("userInput lower than min value")
        return userInput
    if userInput > max:
        print("userInput greater than max value")

    scaledInput = (userInput - min) / (max - min)
    return scaledInput


def print_out_balance_info(dataframe, target_column=-1):
    dataList = list(dataframe[dataframe.columns[target_column]])  # get only target values
    # sort our dataList so that minor spelling errors (not including first letter) that create two categories out of one are obvious
    sorted(dataList)  
    total_items = 0
    cat_count = 0
    for category, count in Counter(dataList).items():
        cat_count += 1
        total_items += count

    print(f"number of categories: {cat_count}")
    print(f"total items in all categories: {total_items}")
    category_string, count_string, percent_string = "category", "count", "percent"

    # logic to increase the padding if any category has really long text
    category_pad = 10
    for category in dataList:
        if len(category) > category_pad:
            category_pad = len(category) + 1
    
    print(f"{'category':{category_pad}}\t{'count':7}\t{'percent':5}")
    print(f"-"*(category_pad + 21))
    
    for category, count in Counter(dataList).items():
        print(f"{category:{category_pad}}\t{count:5}\t{count / total_items:>6.3f}%")
    return


def create_balance_info_csv(dataframe, target_column=-1, filename="balance_info.csv"):
    dataList = list(dataframe[dataframe.columns[target_column]])  # get only target values
    # sort our dataList so that minor spelling errors (not including first letter) that create two categories out of one are obvious
    sorted(dataList)  
    total_items = 0
    cat_count = 0
    for category, count in Counter(dataList).items():
        cat_count += 1
        total_items += count

    category_string, count_string, percent_string = "category", "count", "percent"

    with open(filename, "w", encoding='utf-8') as outfile:
        outfile.write(f"{'category'},{'count'},{'percent'}\n")
        for category, count in Counter(dataList).items():
            outfile.write(f"{category},{count},{count / total_items:>6.3f}\n")
    return


def create_category_list(dataframe, target_column=-1, filename="category_list.txt"):
    dataList = list(dataframe[dataframe.columns[target_column]])  # get only target values
    # sort our dataList so that minor spelling errors (not including first letter) that create two categories out of one are obvious
    sorted(dataList)

    with open(filename, "w", encoding='utf-8') as outfile:
        for category, count in Counter(dataList).items():
            outfile.write(f"{category}\n")
    return

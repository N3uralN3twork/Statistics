"""This is for the SF-36 project in Dr. Quinn's consulting class
Source 1: https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
Source 2: https://medium.com/better-programming/two-replacements-for-switch-statements-in-python-85e09638e451
Source 3: https://docs.scipy.org/doc/numpy/reference/generated/numpy.nan_to_num.html
Source 4: https://docs.scipy.org/doc/numpy/reference/generated/numpy.nanmean.html
Source 5: https://stackoverflow.com/questions/44033422/how-to-recode-integers-to-other-values-in-python
Source 6: https://stackoverflow.com/questions/11904981/local-variable-referenced-before-assignment


If I was really good, I would have this all as one big function so that the user could choose which item she would like
to be scored. But that's for future me to figure out."""
#Set working directory where contents will be stored:
import os
os.chdir(path = "C:/Users/MatthiasQ.MATTQ/Desktop/R Projects")
os.listdir()

#Import the necessary libraries:
import numpy as np
import pandas as pd

#Read in the sample dataset:
data = pd.read_excel("C:/Users/MatthiasQ.MATTQ/Desktop/R Projects/Practice SF-36 data.xlsx",
                     sheet_name = "Practice SF-36 data")
data.head(3)

##################################################################
###                         Data Preparation:                  ###
##################################################################

#Set up variables to be worked with
#You cannot include the calculated variables because they all have NaN at the moment
columns = ['Q1', 'Q2', 'Q3a', 'Q3b', 'Q3c',
           'Q3d', 'Q3e', 'Q3f', 'Q3g', 'Q3h',
           'Q3i', 'Q3j', 'Q4a', 'Q4b', 'Q4c',
           'Q4d', 'Q5a', 'Q5b', 'Q5c', 'Q6',
           'Q7', 'Q8', 'Q9a', 'Q9b', 'Q9c',
           'Q9d', 'Q9e', 'Q9f', 'Q9g', 'Q9h',
           'Q9i', 'Q10', 'Q11a', 'Q11b', 'Q11c', 'Q11d']

data = data.astype({"Q1": "float64"}) #For later problems
df = data.copy() #Don't just type "df = data" 'cause you'll have linked changes
df.dtypes

"""Steps: 1. Change Decimals to NA"
"       2. Change Negatives to NA /
"       3. Change out-of-range values to NA"""

#1. Change entries with decimals to NA:

#This took forever to figure out
df[columns] = df[columns].applymap(lambda x: np.where(x.is_integer(), x, None))


#2. Change Negatives to NA:
df[columns] = df[columns].applymap(lambda x: np.where(x > 0, x, None))


#3. Change out-of-range values to NA:
#Question Ranges:
"""[3a. - 3j.] = [1-3] /
[4a. - 4d.] = [1-5] 
7. = [1-6]
8. = [1-5 if no 7, 1-6 if yes 7]
1. = [1-5]
[11a. - 11d.] = [1-5]
[9a. - 9i] = [1-5]
6. = [1-5]
10. = [1-5]
[5a. - 5c.] = [1-5]
2. = [1-5]"""

#Questions 3a. through 3j. should only go from 1 to 3
#Anything other than that should be considered wrong and translated to NaN

OneToThreeColumns = ['Q3a', 'Q3b', 'Q3c',
             'Q3d', 'Q3e', 'Q3f', 'Q3g', 'Q3h',
             'Q3i', 'Q3j']

df[OneToThreeColumns] = df[OneToThreeColumns].applymap(lambda x: np.where(x in range(1,4) , x, None))
del OneToThreeColumns
#It appears that python's range function doesn't include the stop= number


#Questions 4a. through 4d., 8., 1., 11a. through 11d., 9a through 9i., 6., 10., 5a through 5c., and 2
#all have a range from 1 to 5


OneToFiveColumns = ["Q1", "Q2", "Q4a", "Q4b", "Q4c", "Q4d",
                    "Q5a", "Q5b", "Q5c", "Q6", "Q8", "Q9a",
                    "Q9b", "Q9c", "Q9d", "Q9e", "Q9f", "Q9g",
                    "Q9h", "Q9i", "Q10", "Q11a", "Q11b", "Q11c",
                    "Q11d"]

df[OneToFiveColumns] = df[OneToFiveColumns].applymap(lambda x: np.where(x in range(1,6) , x, None))
del OneToFiveColumns

#Question 7. is the only one that goes from 1-6, so commit to the same process as others,
#only increasing the upper bound by 1 this time.

OneToSixColumns = ["Q7"]

df[OneToSixColumns] = df[OneToSixColumns].applymap(lambda x: np.where(x in range(1,7) , x, None))
del OneToSixColumns

##################################################################
###                     Raw Score Calculations                 ###
##################################################################
#This is the hard-part
#So, the rules:
    "If an item is missing 50% or more of its items, don't compute the raw score"
    "If more than 50% answered but an item is missing, replace it with the list's average"
    "If question 7 and 8 is not answered, then don't calculate Bodily Pain score"

"1. Raw Physical Functioning (PF) Score:"
    #PF = Sum(3a. - 3j)
    #Range = [10 - 30]
    #If an item is missing, it's replaced with the average of the list
        #Thank god it's not something more advanced, like a weighted mean
    #If more than 50% of the items are missing, return None

#Custom Function
def RAW_PF(a,b,c,d,e,f,g,h,i,j):
    list = pd.Series([a,b,c,d,e,f,g,h,i,j])
    Mean = np.mean(list)
    Missing = list.isna().sum()
    if Missing > 5:
        return None
    elif Missing > 0 and Missing < 5:
        list2 = list.replace(np.nan, Mean)
        return sum(list2)
    else:
        return sum(list)

#Testing the function
RAW_PF(2,1,3,2,3,2,1,1,np.nan,3) #20
RAW_PF(3,3,2,2,2,3,3,3,2,2) #25
RAW_PF(np.nan,3,np.nan,3,np.nan,1,np.nan,2,np.nan,np.nan) #None

#So the function works on test data!
#Now how do I apply it to my dataset specifically?
#It seems to work with individual inputs, but not a dataset of inputs?

#Okay, what did we learn?
#Use lambda functions to iterate a custom function across rows
#Don't forget to include "row" because that is where the parameters for your function are contained
#Applying the function
df["Raw_PF"] = df.apply(lambda row: RAW_PF(row["Q3a"], row["Q3b"], row["Q3c"],
                                           row["Q3d"], row["Q3e"], row["Q3f"],
                                           row["Q3g"], row["Q3h"], row["Q3i"], row["Q3j"]), axis = 1)

df["Raw_PF"].describe() #To check for the range
#I did it!


"2. Raw Role-Physical (RP) Score"
    #RP = sum(4a + 4b + 4c + 4d)
    #Ranges from [4 - 20]
    #Pretty sure it follows the same routine as RAW_PF
def RAW_RP(a,b,c,d):
    list = pd.Series([a,b,c,d])
    Mean = np.mean(list)
    Missing = list.isna().sum()
    if Missing > 2:
        return None
    elif Missing > 0 and Missing < 2:
        list2 = list.replace(np.nan, Mean)
        return sum(list2)
    else:
        return sum(list)

#Testing:
RAW_RP(5,2,1,1) #9
RAW_RP(np.nan, 1,2,5) #10.67
#It works in pre-testing

#Applying to the dataset
df["Raw_RP"] = df.apply(lambda row: RAW_RP(row["Q4a"], row["Q4b"],
                                           row["Q4c"], row["Q4d"]), axis = 1)
df["Raw_RP"].describe()
#Success

#Once you get the first one, the rest become easy

"3. Raw Bodily Pain (BP) Score"
    #Sum(7. + 8.)
    #Range = [2, 12]
    #If both columns are there: sum(7 + 8)
        #If both items 7/8 are 1, then BP = 12
        #If item8 = 1 and item7 > 1, then BP = sum(5+item7)
        #If item8 = 2 and item7 > 1, then BP = sum(4 +
    #If only 7 is there: then BP = None
    #If both columns missing: then BP = None
    #Might have to use a "while" statement
    #Items are precalculated

def RAW_BP(item7, item8):
    while np.isnan(item7) and np.isnan(item8): # Both are missing
        return None
    while item7 > 0 and np.isnan(item8): # Only 7 answered
        return None
    while np.isnan(item7) and item8 > 0: # Only 8 answered
        switcher = {                     # Using a switcher case statement here
            1: 12, 2: 9.5,
            3: 7, 4: 4.5, 5: 2}
        return switcher.get(item8, None)
    while item7 > 0 and item8 > 0: # Both items answered
        if item7 == 1 and item8 == 1: return 12
        elif item7 == 1 and item8 == 2: return 10
        elif item7 == 1 and item8 == 3: return 9
        elif item7 == 1 and item8 == 4: return 8
        elif item7 == 1 and item8 == 5: return 7
        elif item7 == 2 and item8 == 1: return 10.4
        elif item7 == 2 and item8 == 2: return 9.4
        elif item7 == 2 and item8 == 3: return 8.4
        elif item7 == 2 and item8 == 4: return 7.4
        elif item7 == 2 and item8 == 5: return 6.4
        elif item7 == 3 and item8 == 1: return 9.2
        elif item7 == 3 and item8 == 2: return 8.2
        elif item7 == 3 and item8 == 3: return 7.2
        elif item7 == 3 and item8 == 4: return 6.2
        elif item7 == 3 and item8 == 5: return 5.2
        elif item7 == 4 and item8 == 1: return 8.1
        elif item7 == 4 and item8 == 2: return 7.1
        elif item7 == 4 and item8 == 3: return 6.1
        elif item7 == 4 and item8 == 4: return 5.1
        elif item7 == 4 and item8 == 5: return 4.1
        elif item7 == 5 and item8 == 1: return 7.2
        elif item7 == 5 and item8 == 2: return 6.2
        elif item7 == 5 and item8 == 3: return 5.2
        elif item7 == 5 and item8 == 4: return 4.2
        elif item7 == 5 and item8 == 5: return 3.2
        elif item7 == 6 and item8 == 1: return 6
        elif item7 == 6 and item8 == 2: return 5
        elif item7 == 6 and item8 == 3: return 4
        elif item7 == 6 and item8 == 4: return 3
        elif item7 == 6 and item8 == 5: return 2
        else:
            return None

#Testing Phase
RAW_BP(np.nan, np.nan) #None
RAW_BP(1, np.nan) #None
RAW_BP(np.nan, 9) #None
RAW_BP(np.nan, 2) #9.5
RAW_BP(1, 5) #7

#Applying to the data set
df["Raw_BP"] = df.apply(lambda row: RAW_BP(row["Q7"], row["Q8"]), axis = 1)
test = df[["Identifier", "Q7", "Q8", "Raw_BP"]]
#Success!


"4. Raw General Health (GH) score"
    #sum (1 + 11a + 11b + 11c + 11d)
    #Range = [5 - 25]
    #If 3 or more missing, then GH = None
    #Definitely reached the most complex one of the 8 items
        #Good lord...

def RAW_GH(item1, item11a, item11b, item11c, item11d):
    Item1Dict = {np.nan: np.nan, 1: 5, 2: 4.4, 3: 3.4, 4: 2, 5: 1}
    if item1 in Item1Dict: #Recode
        global a #Define "a" as a global variable
        a = Item1Dict[item1] #Go through and check dictionary
    b = item11a  # Don't change
    c = (np.abs(item11b - 5) + 1) #Recode
    d = item11c
    e = (np.abs(item11d - 5) + 1) #Recode
    List = pd.Series([a,b,c,d,e])
    Missing = List.isna().sum()
    if Missing == 0: #All present
        return np.sum([a,b,c,d,e])
    elif Missing >= 3: #3 or more missing
        return None
    elif (Missing == 1 or Missing == 2):
        a2 = np.nanmean([b, c, d, e])
        b2 = np.nanmean([a, c, d, e])
        c2 = np.nanmean([a, b, d, e])
        d2 = np.nanmean([a, b, c, e])
        e2 = np.nanmean([a, b, c, d])
        return np.nansum([a2 + b2 + c2 + d2 + e2])
    else:
        return "Error"

#Testing:
RAW_GH(2,1,5,3,2) #13.4
RAW_GH(5,2,2,3,3) #13
RAW_GH(2, np.nan, np.nan, np.nan, 2) #None
RAW_GH(4,3,np.nan,3,5) #11.25
RAW_GH(np.nan,1,3,3,1) #15
#Looks like it works for all of the test cases!!!

#Applying to the data set:
df["Raw_GH"] = df.apply(lambda row: RAW_GH(row["Q1"], row["Q11a"], row["Q11b"],
                                           row["Q11c"], row["Q11d"]), axis = 1)
test = df[["Identifier", "Q1", "Q11a", "Q11b", "Q11c", "Q11d", "Raw_GH"]]
#Nice


"5. Raw Vitality (VT) Score"
    #Sum (9a + 9e + 9g + 9i)
    #Range = [4, 20] Nice
    #If 3 or more are missing, then VT = None
    #This one was tough to figure out

def RAW_VT(item9a, item9e, item9g, item9i):
    item9a = np.abs(item9a - 5) + 1 #Recode before computation
    item9e = np.abs(item9e - 5) + 1
    item9g = item9g #Keep same
    item9i = item9i #Keep same
    List = pd.Series([item9a, item9e, item9g, item9i])
    Missing = List.isna().sum()
    if Missing >= 3: #3 or more are missing
        return None
    elif Missing == 0: #Nonemissing
        return (item9a + item9e + item9g + item9i)
    elif (Missing == 1): #Only 1 item missing
       a3 = np.nanmean([item9e, item9e, item9i])
       b3 = np.nanmean([item9a, item9g, item9i])
       c3 = np.nanmean([item9a, item9e, item9i])
       d3 = np.nanmean([item9a, item9e, item9g])
       return (a3+b3+c3+d3)
    elif (Missing == 2): #Just 2 missing
        return (2 * (item9g+item9i)) #Yes, this is cheating a bit
    else:
        return None

#Testing:
RAW_VT(5,5,1,2) #It works if all are there
RAW_VT(np.nan, np.nan, np.nan, 6) #It works if 3 or more aren't there
RAW_VT(np.nan, np.nan, 3,1) #8

#Applying to the data set:
df["Raw_VT"] = df.apply(lambda row: RAW_VT(row["Q9a"], row["Q9e"],
                                           row["Q9g"], row["Q9i"]), axis = 1)
test = df[["Identifier", "Q9a", "Q9e", "Q9g", "Q9i", "Raw_VT"]]

#Success


"6. Raw Social Functioning (SF) Score"
    #Apparently, instead of straight-up using using the final item values
    #for question 6, they made it so a 1 is a 5, a 2 is a 4, etc.
    #Essentially, Final_6 = (abs(Item6-5)+1)
    #However, they left the scale the same for question 10 like wtf?
    #Range = [2 - 10]
    #If both are missing, then None
    #If just 6 is missing, then the score is just double item 10
    #If just 10 is missing, then the score is 2 * ((abs(Item6)-5)+1)
        #For example, a 2 in item 6 would be 8
    #If both are there, then the score is (abs(Item6-5)+1) + item10

def RAW_SF(item6, item10):
    while np.isnan(item6) and np.isnan(item10): #Both missing
        return None
    while np.isnan(item6) and item10 > 0: #Just 6 missing
        return (2 * item10)
    while item6 > 0 and np.isnan(item10): #Just 10 missing
        return (2 * ((np.abs(item6 -5))+1))
    while item6 > 0 and item10 > 0:
        return ((np.abs(item6 - 5)) + item10 + 1)
    else:
        return None

#Testing:
RAW_SF(np.nan, np.nan) #None
RAW_SF(np.nan, 2) #4
RAW_SF(2, np.nan) #8
RAW_SF(2, 2) #6
#It appears to be working as intended!

#Applying to the data set:
df["Raw_SF"] = df.apply(lambda row: RAW_SF(row["Q6"], row["Q10"]), axis = 1)
test = df[["Identifier", "Q6", "Q10", "Raw_SF"]]

#Success!


"7. Raw Role-Emotional (RE) Score"
    #Sum of 5a, 5b, 5c
    #Range = [3 - 15]
    #If 2 or more items missing, then RE = None
    #If all items present, then RE = simple sum of all items
    #If one missing, replace with average of other two, then RE = simple sum of items

def RAW_RE(item5a, item5b, item5c):
    List = pd.Series([item5a, item5b, item5c])
    Missing = np.isnan(List).sum()
    Mean = np.mean(List)
    while np.isnan(item5a) and np.isnan(item5b) and np.isnan(item5c): #All missing
        return None
    while Missing >= 2:
        return None
    while item5a > 0 and item5b > 0 and item5c > 0: #All items present
        return (item5a + item5b + item5c)
    while Missing == 1: #If only missing one item
        List2 = List.replace(np.nan, Mean)
        return sum(List2)
    else: #Prolly run forever without the below statement
        return None


#Testing:
RAW_RE(np.nan, 2, 4) #9
RAW_RE(np.nan, np.nan, 2) #None
RAW_RE(2, 1, 3) #6
#It seems to work on the test, cases so that's good

#Applying to the data set:
df["Raw_RE"] = df.apply(lambda row: RAW_RE(row["Q5a"], row["Q5b"], row["Q5c"]), axis = 1)

test = df[["Identifier", "Q5a", "Q5b", "Q5c", "Raw_RE"]]
#And it works!



"8. Raw Mental Health (MH)"
    #sum of (9b + 9c + 9d + 9f + 9h)
    #Range = [5 - 25]

def RAW_MH(item9b, item9c, item9d, item9f, item9h):
    item9b = item9b #Keep same
    item9c = item9c
    item9d = (np.abs(item9d - 5) + 1) #Recode
    item9f = item9f #Keep same
    item9h = (np.abs(item9h - 5) + 1) #Recode
    List = pd.Series([item9b, item9c, item9d, item9f, item9h])
    Missing = List.isna().sum()
    if Missing >= 3: #3 or more missing
        return None
    elif Missing == 0: #All items present
        return (item9b + item9c + item9d + item9f + item9h)
    elif (Missing > 0 or Missing < 3):
       b2 = np.nanmean([item9c, item9d, item9f, item9h])
       c2 = np.nanmean([item9b, item9d, item9f, item9h])
       d2 = np.nanmean([item9b, item9c, item9f, item9h])
       f2 = np.nanmean([item9b, item9c, item9d, item9h])
       h2 = np.nanmean([item9b, item9c, item9d, item9f])
       return (b2 + c2 + d2 + f2 + h2)
    else:
        return "Error"

#Testing:
RAW_MH(4,5,4,4,4) #Works when all items present
RAW_MH(np.nan, np.nan, np.nan, 1, 3) #Works when missing >= 3
RAW_MH(np.nan, np.nan, np.nan, np.nan, 3)
RAW_MH(np.nan, np.nan, 5,2,5) #6.67
RAW_MH(np.nan, 4,1,4,5) #17.5
#Holy shit it works wtf

#Applying to the data set:
df["Raw_MH"] = df.apply(lambda row: RAW_MH(row["Q9b"], row["Q9c"], row["Q9d"],
                                           row["Q9f"], row["Q9h"]), axis = 1)
test = df[["Identifier", "Q9b", "Q9c", "Q9d", "Q9f", "Q9h", "Raw_MH"]]






##################################################################
###                    Score Transformations                   ###
##################################################################
"""The next step involves transforming each raw scale score to a 0-100
   scale using the formula shown below.
   
   Transformed_Scale = [(ActualRawScore - LowestPossibleRawScore)]
                       ___________________________________________ * 100
                       [Possible Raw Score Range                 ]
   These scores represent a % of the total possible score received. 
   Reference: pg. 43 (17 in online mode)
    """
#Not sure if I should treat the min. and range as variables in case someone wants to change them later

df["Transformed_PF"] = ((df["Raw_PF"] - 10) / 20) * 100
df["Transformed_RP"] = ((df["Raw_RP"] - 4) / 16) * 100
df["Transformed_BP"] = ((df["Raw_BP"] - 2) / 10) * 100
df["Transformed_GH"] = ((df["Raw_GH"] - 5) / 20) * 100
df["Transformed_VT"] = ((df["Raw_VT"] - 4) / 16) * 100
df["Transformed_SF"] = ((df["Raw_SF"] - 2) / 8) * 100
df["Transformed_RE"] = ((df["Raw_RE"] - 3) / 12) * 100
df["Transformed_MH"] = ((df["Raw_MH"] - 5) / 20) * 100

#Testing:
test = df[["Identifier", "Transformed_PF", "Transformed_RP", "Transformed_BP", "Transformed_GH",
           "Transformed_VT", "Transformed_SF", "Transformed_RE", "Transformed_MH"]]


#That was so easy compared to the preceding step, holy
#Took like 10 minutes



##################################################################
###                    Standardized Scores                     ###
##################################################################
"""Based on the 1998 general U.S. population lol
   The first step is computing a z-score for each of the scales.
   Z = (x - mean) / std. dev.
   Reference: pg. 44 (18 in online mode) and pg. 51 (25 in online mode)
   """

df["Standardized_PF"] = ((df["Transformed_PF"] - 83.29094) / 23.75883)
df["Standardized_RP"] = ((df["Transformed_RP"] - 82.50964) / 25.52028)
df["Standardized_BP"] = ((df["Transformed_BP"] - 71.32527) / 23.66224)
df["Standardized_GH"] = ((df["Transformed_GH"] - 70.84570) / 20.97821)
df["Standardized_VT"] = ((df["Transformed_VT"] - 58.31411) / 20.01923)
df["Standardized_SF"] = ((df["Transformed_SF"] - 84.30250) / 22.91921)
df["Standardized_RE"] = ((df["Transformed_RE"] - 87.39733) / 21.43778)
df["Standardized_MH"] = ((df["Transformed_MH"] - 74.98685) / 17.75604)

test = df[["Identifier", "Standardized_PF", "Standardized_RP", "Standardized_BP",
           "Standardized_GH", "Standardized_VT", "Standardized_SF",
           "Standardized_RE", "Standardized_MH"]]

#Once again, 10 minutes maybe compared to the other section...


##################################################################
###                    Norm-Based Scores                       ###
##################################################################
"""Transforming each score to the norm-based (50, 10) scoring scale.
   This is done by the following:
   Norm-based PF = 50 + (PF_Z * 10)"""

df["NormBased_PF"] = (50 + (df["Standardized_PF"] * 10))
df["NormBased_RP"] = (50 + (df["Standardized_RP"] * 10))
df["NormBased_BP"] = (50 + (df["Standardized_BP"] * 10))
df["NormBased_GH"] = (50 + (df["Standardized_GH"] * 10))
df["NormBased_VT"] = (50 + (df["Standardized_VT"] * 10))
df["NormBased_SF"] = (50 + (df["Standardized_SF"] * 10))
df["NormBased_RE"] = (50 + (df["Standardized_RE"] * 10))
df["NormBased_MH"] = (50 + (df["Standardized_MH"] * 10))

test = df[["Identifier", "NormBased_PF", "NormBased_RP", "NormBased_BP", "NormBased_GH",
           "NormBased_VT", "NormBased_SF", "NormBased_RE", "NormBased_MH"]]

##################################################################
###                   Write Results to File                    ###
##################################################################
"""Welp, it's been quite a long journey (3 days) to complete this task.
But we actually managed to do it so that's really cool"""

df.shape

Questions = data.iloc[:, 0:37] #Select the original questions
Answers = df.iloc[:, 38:69]    #Select the scored answers

FinalScoredData = pd.concat([Questions, Answers], axis = 1)
FinalScoredData


#Write the final file to .csv

pd.DataFrame.to_csv(FinalScoredData, "C:/Users/MatthiasQ.MATTQ/Desktop/R Projects/FinalScoredData.csv",
                    header = True, index = False)


#And that's it.
#What a project.




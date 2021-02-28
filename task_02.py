"""
PURPOSE OF USING DECORATOR :
   Decorator allows a user to add new functionality to an existing object without modifying its structure and its basically 
   belongs to the family of Design patterns so while creating or working in a Existing framework the decorator implementation  
   is much needed and Flask or Django have a native Decorator support while using the app or in the login purposes!
"""

"""
Packages Used for Computation
"""
import pandas as pd

"""
Reading the Csv file from a github repository
Get the Head count of 03 
"""
df_covid19 = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv")#Read csv
df_covid19.head(3)

class ClsDFInfo:
    """ 
    This is a class for computing Dataframe. 
      
    Attributes: 
        dataframe (df): Data frame of covid 19 Cases based on country  
    """
   
    def __init__(self, f):
        """
        The Constructor for Data Frame Manipulation 

        parameter :
            f (Functionality) :Functionalities to manipulate Data frame of covid 19 Cases based on country
        """
        self.f = f    
       
    def __call__(self):
        """
        Call Method for a Data Frame Manipulation 

        parameters:
            f (Functionality) :Apply Decorator for Data Frame Manipulation based on their function calls 
        
        Summary line 
            Extended desciption for Call method 
            get_df_cols ()
            get_df_len ()
        """

        print("Decorating", self.f.__name__, "\n")        
        self.f(self.get_df_cols,"cols in df:")        
        self.f(self.get_df_len, "len of df:")
        self.f(self.get_df_types,"type of values in df")  
       
   
    def get_df_cols(self, df):   
        """
        This Function will get Data Frame 
        parameters : 
            arg1 (df) : Data frame of covid 19 Cases based on country
        returns:
            pandas.core.indexes.base.Index : Listing the Columns
        """     
        return df.columns
   
    def get_df_len(self, df):  
        """
        This Function will get Data Frame 
        parameters : 
            arg1 (df) : Data frame of covid 19 Cases based on country
        returns:
            int : Length or number of columns
        """         
        return len(df.columns)

    def get_df_types(self, df):  
        """
        This Function will get Data Frame 
        parameters : 
            arg1 (df) : Data frame of covid 19 Cases based on country
        returns:
            df : type of df columns
        """ 
        return df.dtypes

   
@ClsDFInfo
def df_info(func, desc):
    """
    This Function will get Method and execute over a Df

    Printing the executed Dataframe result 
    """
    z = func(df_covid19)
    print(desc, "----------\n", z, "\n\n")

#Method Called by Without decorator   
def df_info_wod(func, desc):
    """
    This Function will get Method from the Non decorator and execute over a Df

    Printing the executed Dataframe result 
    """
    z = func(df_covid19)
    print(desc, "----------\n", z, "\n\n")
   
df_info()  
# WITHOUT DECORATOR

print("------------------# WITHOUT DECORATOR ----------------")

"""
Without Using the decorator Creating a object from the class and Extinsively make that available for the process
Attributes:
    class(object) : Class ClsDFInfo @ func
    func(method)      : df_info_wod 
    func(pd_df)      :  get_df_cols
    func(int)      : get_df_len
    func(pd_df)      : get_df_types

"""
func = ClsDFInfo(df_info_wod) #Getting Func as Object

z = func.get_df_cols(df_covid19) #Calling get column names method  
print(z, "\n\n")

z2 = func.get_df_len(df_covid19) #calling the Method get number of columns 
print(z2, "\n\n")

z3 = func.get_df_types(df_covid19)#calling the method get data type of each column 
print(z3, "\n\n")

print("---------------# Visualize Doc String --------------------------")

help(ClsDFInfo)#Visualize doc string of Class
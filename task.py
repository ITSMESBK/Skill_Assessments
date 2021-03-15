#Python BMI Calculator Coding Challenge

"""
Doc string: 
    Params:
        Input : [{"Gender": "Male", "HeightCm": 171, "WeightKg": 96 }, { "Gender": "Male", "HeightCm": 161, "WeightKg":85 },
                 { "Gender": "Male", "HeightCm": 180, "WeightKg": 77 }, { "Gender": "Female", "HeightCm": 166,"WeightKg": 62},
                 {"Gender": "Female", "HeightCm": 150, "WeightKg": 70}, {"Gender": "Female","HeightCm": 167, "WeightKg": 82}
                ]
        Output : Computed data in Csv and Corresponding Graph ploted         
    
"""
#Packages 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import json
import warnings
warnings.filterwarnings("ignore")
import logging

#Inhouse Packages 
from variable import *


class bmi_calc():
    def __init__(self):
        """
        Initiate all the Tweeks over Constructor 
        """
        self.sucess = True
        self.Failure = False

    def read_data(self,json_data=None,Input_File_Name=None):
        """
        Summary : 
            Input : 
                input json (File) : Get the input as a File of '.json'
                input json (Json) : Get the Input Json data directly 
            Return : 
                output (Json) : Return the Read Json for computation
        """
        try:
                
            if Input_File_Name:
                with open(Input_File_Name) as file_name:
                    self.input_json = json.load(file_name)
            
            elif json_data:        
                self.input_json = json_data

        except Exception as e:
            logging.critical(e, exc_info=True)
            Logs = "Issue In Get/Parsing data!"
            print(Logs)
            return self.Failure

        return self.sucess

    def write_data(self):

        try:
            self.input_df.to_csv(Csv_File_Name,index=False)
            print("-->File Stored On Code Running Environment<--")
        except Exception as e:
            logging.critical(e, exc_info=True)
            Logs = "Issue In Put/Writting data!"
            print(Logs)
            return self.Failure

    def get_bmi_compute(self): 

        """
        BMI_FORMULA = mass (kg) / height (m)
        
        params:
            Mass => kg : input_json[Iterator]["WeightKg"]
            Height => cm : input_json[Iterator]["HeightCm"]

        functionality:
            Cm to Meter Conversion 
            Height => M : input_json[Iterator]["Height_Meter"]  

        Extended_summary :
            input (df)  : cm to m Converted df 
            return (csv) : Final computed csv file will store in local machine / server            
        """
        try:

            self.input_df["BMI_Range"] = self.input_df["WeightKg"].div( self.input_df["Height_Meter"]).round(2) #Create BMI Range

            #BMI Category

            df_ops =  [self.input_df['BMI_Range'].between(NORMAL_WEIGHT[0],NORMAL_WEIGHT[1]), 
                        self.input_df['BMI_Range'].between(OVER_WEIGHT[0],OVER_WEIGHT[1]), 
                        self.input_df['BMI_Range'].between(MODERATELY_OBESE[0],MODERATELY_OBESE[1]),
                        self.input_df['BMI_Range'].between(SEVERLY_OBESE[0],SEVERLY_OBESE[1]),
                        (self.input_df['BMI_Range'] <= UNDER_WEIGHT),
                        (self.input_df['BMI_Range'] >= VERY_SEVERLY_OBESE)
                        ]

            BMI_Category_Labels = ["NORMAL WEIGHT","OVER WEIGHT","MODERATELY OBESE","SEVERLY_OBESE","UNDER WEIGHT","VERY SEVERLY OBESE"]

            BMI_Risk_Labels = ["LOW RISK","ENHANCED RISK","MEDIUM RISK","HIGH RISK","MALNUTRITION RISK","VERY HIGH RISK"]

            lable_list = [BMI_Category_Labels,BMI_Risk_Labels]

            def BMI_Category_Risk_mapper(label_val):
                if label_val == 0 :
                    col_name = "BMI Category"
                else:
                    col_name = "BMI Risk"
                self.input_df[col_name] = np.select(df_ops, lable_list[label_val], 0)
            list(map(BMI_Category_Risk_mapper,range(len(lable_list))))    

        except Exception as e:
            logging.critical(e, exc_info=True)
            Logs = "Issue In Get/Parsing data!"
            print(Logs)
            return self.Failure

        print(self.input_df)
        return self.sucess

    def get_centimeter_to_meter(self):
        
        """
        Formula : cm /100.0
        params :
            input (json): input_json
            return (df) : Computed data frame
        """
        try:
            self.input_df = pd.DataFrame.from_dict(self.input_json, orient='columns') #Convert the json to pd_df 
            self.input_df["Height_Meter"] = self.input_df["HeightCm"].div(100.0).round(2) #Apply Formula 
        except Exception as e:
            logging.critical(e, exc_info=True)
            Logs = "Issue In Computation over Dataframe cm to m!"
            print(Logs)
            return self.Failure

        return self.sucess   

    def get_report(self):

        """
        Summary:
            params : 
                input (df) : Get the Computed columns 
                return (png): bmi_analysis_report.png will store on the local machine 
        """
        try:
            fig = plt.figure()
            ax = fig.add_axes([0,0,2,2])
            weights = self.input_df["WeightKg"]
            bmi_vals = self.input_df["BMI_Range"]
            ax.bar(weights,bmi_vals)
            plt.xlabel("Weight in Kg")
            plt.ylabel("BMI value")
            plt.title("Weight and Corresponding BMI VALUE") 
            #plt.show()
            plt.savefig(Graph_Name)
            print("-->Graph Saved On Code Running Environment<--")
        except Exception as e:
            logging.critical(e, exc_info=True)
            Logs = "Issue In Get/Plooting Graph data!"
            print(Logs)
            return self.Failure

        return self.sucess

def Run_BMI_Framework():
    """
    The Run BMI Framework is the Master snippet to tweek the process
    As per the user need we can tweek and get things 
    """
    BMI_OBJECT = bmi_calc() #Object of the class

    Read_Status = BMI_OBJECT.read_data(Input_File_Name=Input_File_Name) #Read Json File
    if Read_Status == False:
        print("User-Log:Process Stalled | Read_status")
        return False
    
    Conversion_status = BMI_OBJECT.get_centimeter_to_meter() #Convert Cm to M
    if Conversion_status ==False:
        print("User-Log:Process Stalled | Conversion_status")
        return False

    Computation_status = BMI_OBJECT.get_bmi_compute() #Compute BMI
    if Computation_status == False:
        print("User-Log:Process Stalled | Computation_status")
        return False
    
    Report_status = BMI_OBJECT.get_report() #get the Graph
    if Report_status == False:
        print("User-Log:Process Stalled | Report_status")
        return False
    
    Write_status = BMI_OBJECT.write_data() #Write output_data
    if Write_status == False:
        print("User-Log:Process Stalled | Write_status")
        return False



if __name__ == '__main__':
    #Auto Run Tweek
    Run_BMI_Framework()

    #Uncomment to Visualize the doc string 
    #help(bmi_calc)
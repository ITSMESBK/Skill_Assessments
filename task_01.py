#Packages
import numpy as np
import pandas as pd 
import requests
import matplotlib.pyplot as plt 
import warnings
warnings.filterwarnings("ignore")
import logging
#Api Packages
from flask import Flask, jsonify, request 

app = Flask(__name__) 

"""
API gateway Parms: 
    => /get_csv_files
    => /computation

Usage : 
    =>Get files using get_csv Api 
    =>compute solution will use files from above api and compute the result

API calls sample using curl request in local:
    => curl http://127.0.0.1:5000/get_csv_files
       |
       --> {"Download_status":"success","File status":"200"} 
        --> Additional Logs report on local flask server
          --> Files stored in local machine 

    => curl http://127.0.0.1:5000/computation        
       |
       --> {"Computation Status":"200"}
        --> Additional Logs report on local flask server
          --> Graphs stored in local system as Recovery_data_over_cities.png      
"""

class covid_stat:   
    def __init__(self):
        self.sucess = 200

    def get_csv_files(self):
        #Url 
        csv_url_country_wise_latest = "https://storage.googleapis.com/kagglesdsdata/datasets/494766/1402868/country_wise_latest.csv?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20210225%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20210225T074624Z&X-Goog-Expires=259199&X-Goog-SignedHeaders=host&X-Goog-Signature=4c136302136f9e74fd5692bdfcb8ba6ec41244c964462807d4e5e5e686425c89af81e643001e4b2283d65d0807c40c0dea2b3e38db64a383cd934e4a01c2ea5ac5ed31a6f096f9bb669bec3d8aec756e0b833232935fb83e15fa47a670fe1e25df3a8cd08b89a53b4803c6891409461401a848c5aadf405d32321b9f7534ad3058fa7da419f97bea643e71503154de79fbf69a6bff3db90278556e7cfb8ddb0609cb1169ff04fcbe4f543886a018135312382769b0cd811629ff3d03d790375920f9bef2bfdabfe9e467c49aea7b71b4417b93c285846759c45eeafd0ec08f3aefb86a2bb5fe592fef72031b065f20d8d79363af1b9936d633c7af532d7a6d2d"
        csv_url_WHO = "https://query.data.world/s/3tutgdvjwp3xypqouxci6jikgpq74d"

        #GET REQUESTS
        try:
            cwl_req = requests. get(csv_url_country_wise_latest)
            who_req = requests. get(csv_url_WHO)
            print("request_status:",self.sucess)
        except Exception as e:
            logging.critical(e, exc_info=True)
            Logs = "Issue In Get/Parsing Url!"
            print(Logs)
            return False 

        #FETCH CONTENT
        try:
            cwl_url_content = cwl_req. content
            who_url_content = who_req. content 

            #PREPARE FOR DOWNLOAD
            self.cwl = 'country_wise_latest.csv'
            self. who = 'WHO.csv'

            cwl_csv_file = open(self.cwl, 'wb')
            who_csv_file = open( self. who, 'wb')

            cwl_csv_file. write(cwl_url_content)
            cwl_csv_file. close()

            who_csv_file. write(who_url_content)
            who_csv_file. close()
            print("csv files stored on local")
        except Exception as e:
            logging.critical(e, exc_info=True)
            Logs = "Issue in Df Manipulation!"
            print(Logs)
            return False
        return True

    def compute_df(self):
        """
        Hit the get_csv_files api and fetch the csv files for computation 
        parameters : 
            cwl_df (df) : Data Frame of Covid 19
        """
        try:
            covid_stat.get_csv_files(self)#Inner call to get files

            cwl_df = pd.read_csv(self.cwl) #read csv
        except Exception as e:
            logging.critical(e, exc_info=True)
            Logs = "Issue in Getting Csv!"
            print(Logs)
            return False

        #COMPUTATION 01
        # Get countrywise  Recovery percentage 

        """
        Initialization of df and series under pandas library
        Summary line :
            Traversal over the dataframe and do the computation for the Percentage of Confirmed case | Recovered 
            Compute data for all the countries
        """
        try:
            computed_df = pd.DataFrame()
            get_recovery_stat = pd.Series({})
            get_death = pd.Series({})
            recovered = pd.Series({})
            confrimed = pd.Series({})


            for group,frame in cwl_df.groupby('Country/Region'):
                """
                Traversal over the Dataframe based on the Groupby Ops
                get by Country/Region 
                Data cleaning | Taking required data for computation 
                """
                tmp_df = cwl_df[cwl_df['Country/Region'] == group]
                tmp_df = tmp_df[['Country/Region', 'Deaths', 'Recovered', 'Confirmed']].tail(1)

                tmp_series = tmp_df.reset_index().set_index('Country/Region').iloc[0]
                
                #Get required columns
                get_death[group] = tmp_series.loc['Deaths']
                recovered[group] = tmp_series.loc['Recovered']
                confrimed[group] = tmp_series.loc['Confirmed']
                
                """
                Calculating the Percentage based on Recovered and Confirmed 
                """
                if(tmp_series.loc['Recovered'] > 0.0):
                    calc_percent = round((tmp_series.loc['Recovered'] / tmp_series.loc['Confirmed'])*100,2)
                    get_recovery_stat[group] = calc_percent

            """
            Sorting based on Descending Order
            Insertion over new df as computed df
            """
            get_recovery_stat = get_recovery_stat.sort_values(ascending=False)

            computed_df.insert(0, "Recovery Percentage", get_recovery_stat)
            computed_df.insert(1, "Deaths", get_death)
            computed_df.insert(2, "Recovered", recovered)
            computed_df.insert(3, "Confirmed", confrimed)
            computed_df.head(20)

            computed_df[['Confirmed','Recovered']].plot()

            computed_df.head()
        except Exception as e:
            logging.critical(e, exc_info=True)
            Logs = "Issue in df Traversal/compute-01"
            print(Logs)
            return False

        #computation 02
        """
        Get Confirmed Cases greater than 1500 
        
        Respected Graphs attached below 
        """
        try:
            computed_df_02 = computed_df[computed_df['Confirmed'] > 1500]
            computed_df_02.head(10)
            plt.plot(np.log(computed_df['Recovery Percentage'][:20]))
            plt.savefig('Recovery_data_over_cities.png')
            print("-->Graph Saved On local Machine<--")
            #return jsonify({"Computation_status":"200"})
            print("computation 01 and 02 sucessfully executed")
        except Exception as e:
            logging.critical(e, exc_info=True)
            Logs = "Issue in df pandas value calc /compute-02"
            print(Logs)
            return False
        return True

@app.route('/get_csv_files', methods = ['GET'])
def call_get_csv_api():
    """
    Functional Api for Get Csv Files

    Download Files into local machine

    return : Json status
    """
    covid_obj = covid_stat()
    Flag = covid_obj.get_csv_files()
    if Flag == True:
        return jsonify({"File status":"200","Download_status":"success"})
    else:
        return jsonify({"File status":"400","Download_status":"failure"})

@app.route('/computation', methods = ['GET'])
def call_compute_api():
    """
    Functional Api for computation 

    Compute has Two plase 01 an 02 

    return : json status
    """
    covid_obj = covid_stat()    
    Flag = covid_obj.compute_df()
    if Flag == True:
        return jsonify({"Computation Status":"200"})
    else:
        return jsonify({"Computation Status":"400"})

if __name__ == '__main__':
    app.run()


import pandas as pd
import numpy as np
import requests


class CallExternalApi():

    url = "https://corona-virus-world-and-india-data.p.rapidapi.com/api_india"

    headers = {
        'x-rapidapi-host': "corona-virus-world-and-india-data.p.rapidapi.com",
        'x-rapidapi-key': "65a3776284mshe3cfb3d30f2126bp10458ejsn7a8d5865fb2c"
        }
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    all_data = data['total_values']
    state_wise_data = pd.DataFrame(data['state_wise'])
    indx = state_wise_data.index
    indx = indx.drop('district')

    def featch_state_data(self, stg):

        dic = {}
        for i in self.state_wise_data.columns:
            if i == stg:
                for j in self.indx:
                    dic.update([[j, self.state_wise_data[i][j]]])
        return dic

    """For featching data district"""
    def featch_district_data(self, str_district):
        dic = {}
        for i in self.data['state_wise'].keys():
            for j in self.data['state_wise'][i].keys():
                if j == 'district':
                    if str_district in self.data['state_wise'][i][j].keys():
                        dic = self.data['state_wise'][i][j][str_district]
        return dic

    """api return some district name as "Unknown" 
    so for those Unknown district name we can use below methode """
    # def featch_district_data(self, str_district):
    #     dic = {}
    #     l = []
    #
    #     for i in self.data['state_wise'].keys():
    #         for j in self.data['state_wise'][i].keys():
    #             if j == 'district':
    #                 if str_district in self.data['state_wise'][i][j].keys():
    #                     dic = self.data['state_wise'][i][j][str_district]
    #                     l.append([self.data['state_wise'][i][j][str_district]])
    #     return dic, l

    def featch_all_India_data(self):
        total_active = []
        total_confirm = []
        total_deaths = []
        for i in ['active', 'confirmed', 'deaths']:
            if i == 'active':
                total_active = self.all_data[i]
            if i == 'confirmed':
                total_confirm = self.all_data[i]
            if i == 'deaths':
                total_deaths = self.all_data[i]
        return total_active, total_confirm, total_deaths

# ob = CallExternalApi()
# temp_1 = ob.featch_state_data('Uttarakhand')
# temp_2 = ob.featch_district_data('Nagpur')
# print(temp_1)
# print(temp_2)
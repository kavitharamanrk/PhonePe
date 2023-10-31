# PhonePe
PhonePe Pulse Data Analysis from Jan 2018 to Jun 2023

I have created a dashboard to visualize Phonepe pulse Github repository data using Streamlit and Plotly in Python

workflow:
1. Zip Data downloaded from https://github.com/PhonePe/pulse for the period Jan 2018 to June 2023. 
2. Downloaded Data has unzipped
    data folder has 3 main folders  Aggregated, Map and Top 
    Each has 2 folders transactions and user

    Data file tree
        data\aggregated\transaction\country\india\state\district\year
        data\aggregated\user\country\india\state\district\year
        data\map\transaction\hover\country\india\state\district\year
        data\map\user\hover\country\india\state\district\year
        data\top\transaction\country\india\state\district\year
        data\top\user\country\india\state\district\year

3. Each year has json files for 4 quarters. 2023 has first 2 quarters data only.
    1. Jan - Mar
    2. Apr - Jun
    3. Jul - Sep
    4. Oct - Nov 
4.This Json file data inserted into mysql dashboard thro python page

5. From mysql db data visualized in Dashboard as Geo Visualization and other charts based on the stored data

Main component of Dashboard is Geo Visualization

Dashboard contains 4 menus

1 Explore Data: 
Geo-Visualization:The India map shows the state wise Total Transactions of PhonePe.
                  It comes with zoom option and on hover displays the content related to that particular state.The                       main functions I have used to create this map are (User can give year and quarter input to show how                     the data changed over time)
                  
                    Plotlys choropleth for drawing the states in India map  

                    State/District/Pincode top 10 leading data displayed

                    Transaction type wise counts also displayed

2 Analysis: The Transactions data mainly contains the total Transactions count and total amount in each state and district.
            And User data contains which brand mostly used by user.I have used different graphs available in plotly and streamlit to represent this data

3 Reports:  Total states and its district's overall transaction count is displayed in sunburst chart

4 About : Gives the data of project technology and short notes of this phone pe project.

Technolog used: Python, plotly, streamlit, pandas and mysql

Linked in Url
https://www.linkedin.com/posts/kavitha-raman-3287a2293_phone-pe-pulse-data-analysis-activity-7124992760574607362-N2sc/

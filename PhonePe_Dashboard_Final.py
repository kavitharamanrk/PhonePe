import pandas as pd 
import plotly.express as px
import streamlit as st 
import mysql.connector 
from PIL import Image
import matplotlib.pyplot as plt

# My SQL DB Connection
def mySqlConnection(query):
  try:
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="",
    )
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute(query)
    out=mycursor.fetchall()
    mydb.close()  
  except Exception as e:
    print("SQL DB Connection error:",{e})
  finally:
    print("DB Connected")  
    return out

# India map display
def phonepe_map():
    df = pd.read_csv("https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/active_cases_2020-07-17_0800.csv")
    
    hquery=f"select state, sum(count), round(sum(amount),2), round(avg(count),2) from agg_transaction where Year= {year} and Quarter= {quarter} group by state"
    hlis=mySqlConnection(hquery)

    df_map=pd.DataFrame(hlis,columns=['state','Transactions','Amount','Average'])
    dfstate=df_map.copy()

    hover_data_cols_df = ['Transactions', 'Amount', 'Average']
    fig = px.choropleth(
            df_map,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='state',
            color='state',
            color_continuous_scale='reds',
            hover_name = 'state',
            hover_data = hover_data_cols_df
    )
    fig.update_geos(fitbounds="locations", visible=False)
    return fig,dfstate

# All transactions 
def transaction_display():
    query1=f"select sum(count) ,sum(amount),avg(amount)   from agg_transaction where Year= {year} and Quarter= {quarter}"
    query2=f"select sum(count) ,sum(amount),avg(amount) from map_transaction where Year= {year} and Quarter= {quarter}"
    query3=f"select sum(count) ,sum(amount),avg(amount) from top_transaction where Year= {year} and Quarter= {quarter}"
    lis1=mySqlConnection(query1)
    d1=pd.DataFrame(lis1)        

    lis2=mySqlConnection(query2)
    d2=pd.DataFrame(lis2)
    
    
    lis3=mySqlConnection(query3)
    d3=pd.DataFrame(lis3)
    
    total_trans=float(d1[0])+float(d2[0])+float(d3[0])
    total_amnt=float(d1[1])+float(d2[1])+float(d3[1])
    avg_amnt=float(d1[2])+float(d2[2])+float(d3[2])
    return total_trans,total_amnt,avg_amnt

# transaction Type wise display
def category_display():
    query4=f"select Transaction_Type,sum(Amount)  from agg_transaction where Year= {year} and Quarter= {quarter} group by Transaction_Type "        
    lis5=mySqlConnection(query4)
    cat_data=pd.DataFrame(lis5,columns=['Type','Amount'])
    return cat_data

# Page setting
icon = Image.open("phonepe_logo.png")
st.set_page_config(page_title= "PhonePe Pulse - Kavitha",
                page_icon= icon,
                layout= "wide",
                initial_sidebar_state= "expanded",
                )


st.subheader(":violet[Phone Pe Pulse | THE BEAT OF PROGRESS]")
tab1, tab2 ,tab3,tab4= st.tabs([":violet[EXPLORE DATA]",":violet[ANALYSIS]",":violet[REPORTS]",":violet[ABOUT]"])

with tab1:

    col1,col2,col3,col4=st.columns(4)
    with col1:
        Year = st.selectbox("",['INDIA'])
    with col2:
        query_lst=['Transactions','Users']
        qryselect=st.selectbox(":violet[Select Transactions/Users]",query_lst)
    with col3:
        Year = st.selectbox(
        ":violet[Please select the Year]",
        ('2018', '2019', '2020','2021','2022','2023'))
    with col4:
        Quarter = st.selectbox(
        ':violet[Please select the Quarter]',
        ('1', '2', '3','4'))

    year=int(Year)
    quarter=int(Quarter)
    if (year==2023 and (quarter==3 or quarter==4)):
        st.warning("This app contains the data from 1st quarter of 2018 to 2nd quarter of 2023 only")
        pass 

    col5,col6 = st.columns([7,3])
    with col5:
        map_fig,df_state=phonepe_map()
        st.plotly_chart(map_fig, use_container_width=True)
    with col6:
        cap="Top 10 States"
        if qryselect=='Transactions':           
            st.subheader(":violet[Transactions]")
            st.caption(":violet[All PhonePe transactions(UPI+Cards+Wallets)]") 
            tot_trans,tot_amnt,avg_amt=transaction_display()   
            st.write(round(tot_trans))
            
            col_trans1,col_trans2 = st.columns([6,4])
            with col_trans1:
                st.caption(":violet[Total Payment value]")
                st.write(round(tot_amnt,2))
            with col_trans2:      
                st.caption(":violet[Avg. transaction value]")
                st.write(round(avg_amt,2))
                
            st.subheader(":violet[Categories]") 
            st.dataframe(category_display(), hide_index=True)
            
            # state,district, pincode
            query=f"select state,sum(count) as count  from agg_transaction where Year= {year} and Quarter= {quarter} group by state order by count desc limit 10"
            lis4=mySqlConnection(query)
            data=pd.DataFrame(lis4,columns=['State','Count'])
            
            col_trans_state,col_trans_dist,col_trans_pin = st.columns(3)
            with col_trans_state:
                if st.button(":violet[State]"):
                    cap="Top 10 States"
                    query=f"select state,sum(count) as count  from agg_transaction where Year= {year} and Quarter= {quarter} group by state order by count desc limit 10"
                    lis4=mySqlConnection(query)
                    data=pd.DataFrame(lis4,columns=['State','Count'])                    
            with col_trans_dist:
                if st.button(":violet[District]"):
                    cap="Top 10 Districts"
                    query=f"select district,sum(count) as count  from map_transaction where Year= {year} and Quarter= {quarter} group by district order by count desc limit 10"
                    lis4=mySqlConnection(query)
                    data=pd.DataFrame(lis4,columns=['District','Count'])
            with col_trans_pin:
                if st.button(":violet[Pincode]"):
                    cap="Top 10 Pincodes"
                    query=f"select Pincode ,sum(count) as count  from top_transaction where Year= {year} and Quarter= {quarter} group by pincode order by count desc limit 10"
                    lis4=mySqlConnection(query)
                    data=pd.DataFrame(lis4,columns=['Postal Codes','Count']) 
                    
        elif qryselect=='Users':
            if (year==2023 and (quarter==3 or quarter==4)):
                st.warning("This app contains the data from 1st quarter of 2018 to 2nd quarter of 2023 only")
                pass
            
            user_qry=f"select sum(AppOpens), sum(Registered_User) from map_user  where Year= {year} and Quarter= {quarter}"
            
            user_lis=mySqlConnection(user_qry)
            df_user=pd.DataFrame(user_lis,columns=['App','User'])        

            reg_user,app_opens='',''

            reg_user=lis1[0][0]
            app_opens=lis1[0][1]

            st.subheader(":violet[Users]") 

            st.caption(":violet[Registered PhonePe users]")    
            st.write(reg_user)

            st.caption(":violet[PhonePe App Opens]")
            st.write(app_opens)
            
            # state,district, pincode
            state_qry=f"select state,sum(count) as count from agg_user where Year= {year} and Quarter= {quarter} group by state order by count desc limit 10"
            state_lis=mySqlConnection(state_qry)
            data=pd.DataFrame(state_lis,columns=['State','Count'])
            
            col_usr_state,col_usr_dist,col_usr_pin = st.columns(3)
            with col_usr_state:
                if st.button(":violet[States]"):
                    cap="Top 10 States"
                    query=f"select state,sum(count) as count from agg_user where Year= {year} and Quarter= {quarter} group by State order by count desc limit 10"
                    lis4=mySqlConnection(query)
                    data=pd.DataFrame(lis4,columns=['State','Count'])
            with col_usr_dist:
                if st.button(":violet[Districts]"):
                    cap="Top 10 Districts"
                    query=f"select district,sum(registered_user)  registered_user from map_user where Year= {year} and Quarter= {quarter} group by district order by registered_user desc limit 10"
                    lis4=mySqlConnection(query)
                    data=pd.DataFrame(lis4,columns=['District','Count'])
            with col_usr_pin:
                if st.button(":violet[Pincodes]"):
                    cap="Top 10 Pincodes"
                    query=f"select pincode, sum(registered_user) as registered_user from top_user where Year= {year} and Quarter= {quarter} group by pincode order by registered_user desc limit 10"
                    lis4=mySqlConnection(query)
                    data=pd.DataFrame(lis4,columns=['Postal Codes','Count']) 
        st.caption(cap)          
        st.dataframe(data, hide_index=True)
        
    # User queries
    query_lst=['1.Which states are using Phone Pe for transactions in India ?',
    '2.What are the transaction types are used in phone pe and how much they used?',
    '3.In which mobiles brands mostly used Phone Pe ?',
    '4.List out Top 10 states using Phone Pe in India ?',
    '5.List out Top 10 districts using Phone Pe in India?',
    '6.List out Top 10 districts has highest registered users using phone pe?',
    '7.Which state has highest transaction in 2022 thro phone pe?',
    '8.What is average transactions of all transactions in each states and what are their corresponding state names',
    '9.Which brand is used mostly  phone pe and their corresponding state name?',
    '10.In which pincode has max transaction count and its state?'
    ]
    qryselect=st.selectbox(":violet[Select your queries]",query_lst)
    if qryselect==query_lst[0]:
        header="States In India using Phone pe"
        qquery="SELECT state,sum(Count),sum(amount)from agg_transaction group by state"
        qlis=mySqlConnection(qquery)
        ldata=pd.DataFrame(qlis,columns=['State','Transaction Count','Amount'])    

    elif qryselect==query_lst[1]:
        header="Transaction Type"
        qquery="select Transaction_type , sum(count) as count from agg_transaction group by transaction_type order by count desc"
        qlis=mySqlConnection(qquery)
        ldata=pd.DataFrame(qlis,columns=['Transaction_Type','Count']) 
  
    elif qryselect==query_lst[2]:
        header="Top Brands"
        qquery="select brand, sum(count) from agg_user group by brand"
        qlis=mySqlConnection(qquery)
        ldata=pd.DataFrame(qlis,columns=['Brand','Total Transactions'])    

    elif qryselect==query_lst[3]:
        header="Top 10 States In India using Phone pe"
        qquery="SELECT state,sum(Count) as count from agg_transaction group by state limit 10"
        qlis=mySqlConnection(qquery)
        ldata=pd.DataFrame(qlis,columns=['State','Transaction Count'])    

    elif qryselect==query_lst[4]:
        header="Top District's transactions In India using Phone pe"
        qquery="SELECT state,district,sum(Count) as count,sum(amount) from map_transaction group by state,district order by count desc limit 10"
        qlis=mySqlConnection(qquery)
        ldata=pd.DataFrame(qlis,columns=['State','District','Transaction Count','Amount'])    

    elif qryselect==query_lst[5]:
        header="Top District's User In India using Phone pe"
        qquery="SELECT state,district,sum(registered_user) as count from map_user group by state,district order by count desc limit 10"
        qlis=mySqlConnection(qquery)
        ldata=pd.DataFrame(qlis,columns=['State','District','User'])    

    elif qryselect==query_lst[6]:        
        header="Leading State in 2022 Transactions"
        qquery="SELECT state,sum(count) as count,sum(amount),avg(amount) from agg_transaction where year=2022 group by state order by count desc limit 1"
        qlis=mySqlConnection(qquery)
        ldata=pd.DataFrame(qlis,columns=['State','Transaction Count','Amount','Average Amount'])

    elif qryselect==query_lst[7]:
        header="Average Transactions"
        qquery="SELECT state,avg(amount) from agg_transaction group by state"
        qlis=mySqlConnection(qquery)
        ldata=pd.DataFrame(qlis,columns=['State','Average Amount'])    
 
    elif qryselect==query_lst[8]:
        header="Leading brand"
        qquery="select brand, sum(count) as count from agg_user group by brand order by count desc limit 1"
        qlis=mySqlConnection(qquery)
        ldata=pd.DataFrame(qlis,columns=['Brand','Count'])    

    elif qryselect==query_lst[9]:
        header="Pincode Wise Transactions"
        qquery="select state, pincode, sum(count) as count from top_transaction group by state,pincode order by count desc"
        qlis=mySqlConnection(qquery)
        ldata=pd.DataFrame(qlis,columns=['State','Pincode','Count'])     
    st.caption(header)  
    st.dataframe(ldata, hide_index=True)
with tab2:
    tab2col1,tab2col2=st.columns(2)
    with tab2col1:
        st.subheader(":violet[Transactions Analysis from  Jan 2018 to Jun 2023]")
        t2state=st.selectbox(":violet[Select State]",df_state['state'])
        t2squery=f"select transaction_type, sum(count) from agg_transaction where state='{t2state}' group by state,transaction_type"
        t2slis=mySqlConnection(t2squery)
        data=pd.DataFrame(t2slis,columns=['Type','Count'])  
        fig1 = px.bar(data, x='Type', y='Count',color="Type",
                 color_continuous_scale="reds")   
        st.plotly_chart(fig1,use_container_width=True)
        
        t2yquery=f"select district, sum(count) from map_transaction where state='{t2state}' group by district"
        t2ylis=mySqlConnection(t2yquery)
        ydata=pd.DataFrame(t2ylis,columns=["district","count"])        

        fig2 = px.pie(ydata, values='count', names='district',color_discrete_sequence=px.colors.sequential.Viridis, title='Total Transactions')
        st.plotly_chart(fig2)        
 
        
    with tab2col2:
        st.subheader(":violet[User Analysis from  Jan 2018 to Jun 2023]")
        t2uquery=f"select brand,sum(count) from agg_user where state='{t2state}' group by brand"
        t2ulis=mySqlConnection(t2uquery)
        bdata=pd.DataFrame(t2ulis,columns=["Brand","Count"])        

        fig3 = px.pie(bdata, values='Count', names='Brand',color_discrete_sequence=px.colors.sequential.Greens_r, title='Total Brands')
        st.plotly_chart(fig3) 
        
        t2dquery=f"select district,sum(registered_user) from map_user where state='{t2state}' group by district"
        t2dlis=mySqlConnection(t2dquery)
        ddata=pd.DataFrame(t2dlis,columns=["district","user"])        
        fig4 = px.area(ddata, x='district', y='user',color_discrete_sequence=px.colors.sequential.Oranges_r, title='Total Registered Users')
        st.plotly_chart(fig4)      
  
with tab3:
       
    t3query=f"select a.state,b.district,sum(a.count) from agg_transaction a, map_transaction b where a.state=b.state  group by state,district "
    t3lis=mySqlConnection(t3query)
    rdata=pd.DataFrame(t3lis,columns=["state","district","count"])        

    fig5 = px.sunburst(rdata, values='count', path=['state','district'],color_discrete_sequence=px.colors.sequential.Oranges_r, title='Total States/Districts')
    st.plotly_chart(fig5)        


with tab4:  
    st.caption(":violet[Technologies used : Cloning from Github, Python,  MySQL, Streamlit and Plotly.]")
    st.caption(":violet[Overview : In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on.]")
    st.caption(":violet[Analysis : Bar,Pie,area, sunburst charts and Geo map visualization are used to get some insights.]")        

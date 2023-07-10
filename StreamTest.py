# import module

import streamlit as st
import pandas as pd
import numpy as np


import subprocess
import sys
#subprocess.check_call([sys.executable, "-m", "pip", "install", 'panel'])
#subprocess.check_call([sys.executable, "-m", "pip", "install", 'matplotlib'])
#subprocess.check_call([sys.executable, "-m", "pip", "install", 'plotly'])


from datetime import datetime, date,timedelta
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import panel as pn
import plotly.express as px

from datetime import date, timedelta
pn.extension('tabulator')



#st.topbar.write("Exampler Dashboard")


# Title
st.title("Exemplar Dashboard")


## reading the data from url and looking for site from it

df=pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vQi5lnVESmIFGng5PeZj2QYEM1hEcrGxmpTCidXkbHZmR-7eswXAsSqI0ZC02tdsJ5aTKzs56F_G0n7/pub?output=csv")
df2=pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vQSjwmOOwc1iHvIl_gc1mlUB9Pa_rB7pwg__Agq7JQowZ8XvycnGG2AxsXyk9WDJ4h_clBt0jiceTDl/pub?output=csv")
df3=pd.read_csv( "https://docs.google.com/spreadsheets/d/e/2PACX-1vT10tMtolzQfzmikUWpdP3K_r-9mC7K9xaOyzt7hwmKKF3WT9UTGPaNO4CndArmgsPVduNELK4Oeo1n/pub?gid=0&single=true&output=csv")

# # taking site values
# site_values= df['Site '].unique()

# ## making a dropdown with all the sites

# ##selection box using all the unique values in site

# site = st.selectbox(" Our Sites: ", site_values)
 
# # print the selected hobby
# st.write("Your selected site is : ", site)


###___________________________

###   Working right now head counts code
###____________________________________________

st.header('WORKING RIGHT NOW')

site_values = df2['Site'].unique()


site_numbers = len(site_values)


sites = []
counts = []

for site in site_values:
     df_filter = df2[df2['Site'] == site]
     sites.append(site)
     c= df_filter[df_filter['Status'] == "Started"]['Name '].count()
     counts.append(c)


working_rightnow = dict(zip(sites, counts))
st.bar_chart(working_rightnow)




###_____________________________________________________________________________

## Highest priority Work  (SIDEBAR)

###_____________________________________________________________________________



# Top 10 priority task

st.sidebar.header ("Top 10 Highest priority work")
#creatin a column with high priority work
#creatin a column with high priority work
df2['Work_with_high_priority'] = df2['Work Order'].dropna().apply(lambda x: x.startswith(('AH','SH','AM','SM'))) 

print(df2['Work_with_high_priority'])    
def priority_table(df, selected_value):
    filtered_df = df[df['Work_with_high_priority'] == selected_value ]
    filtered_df= filtered_df[ filtered_df['Status']!='Completed']    
    return filtered_df[[ 'Name ', 'Status']][:10]

print(priority_table(df2,True))

st.sidebar.table(priority_table(df2, True))



###_____________________________________________________________________________

## Name of the people checked In today(SIDEBAR)

###_____________________________________________________________________________

#st.sidebar.markdown('<p1 class="nicebar">People Clocked In Today </p1>', unsafe_allow_html=True)
st.sidebar.header("People Clocked In Today")
today = datetime.today().strftime("%m/%d/%Y")
print(today)

checkin_df = df3[df3['Date'] == today]
checkin_df = checkin_df[['Name', 'Checkin_Time','Checkout_Time','Total_Hours']]

# Getting today's time
time_now = datetime.now()
#st.write(time_now)

# Calculate the duration for each row
checkin_df['Duration'] = None
for index, row in checkin_df.iterrows():
    if pd.isnull(row['Checkout_Time']):
        t = datetime.strptime(row['Checkin_Time'], "%I:%M:%S %p")  # Parse the time string
        t = t.replace(year=time_now.year, month=time_now.month, day=time_now.day)  # Set the date to today's date

        time_difference = round(((time_now - t).total_seconds() / 3600), 2)
        checkin_df.at[index, 'Duration'] = (time_difference)
    else:
        checkin_df.at[index, 'Duration'] = row['Total_Hours']

st.sidebar.write(checkin_df[['Name', 'Checkin_Time','Duration']])

#st.sidebar.write(checkin_df)


####__________________________________________________________________________


#writing 3 columns for Today's Hours work , Yesterday Hours work and Past week work

####_________________________________________________________________________


st.header("Time Tracker")

col1, col2, col3 = st.columns(3)


with col1:
    st.header("Today's Hours")
    st.write(today)
    #fig_ = px.bar(checkin_df, x=checkin_df['Name'], y=checkin_df['Duration'])
    #fig_.show()
    #st.plotly_chart(fig_, theme=None, use_container_width=True)
    today_whours={}
    
    st.bar_chart(data=checkin_df, x='Name',y='Duration')
   

with col2:
    st.header("Yesterday's Hours")
    today = datetime.today()
    previous_day = date.today() - timedelta(days=1)
    previous_day_str = previous_day.strftime("%m/%d/%Y")
    #st.write( today)
    st.write(previous_day_str)

    worker_hours = {}

    for i in range(1, 6):
        date_col = f"Date{i}"
        duration_col = f"Duration{i}"
    
        try:






            df_filtered = df2[df2[date_col] == previous_day_str]
        
            for index, row in df_filtered.iterrows():
                name = row['Name ']
                duration = row[duration_col]
                
                if pd.notnull(duration):
                    duration = str(duration)  # Convert duration to string
                
                if ':' in duration:
                    # duration_parts = duration.split(':')
                    # hours = int(duration_parts[0])
                    # minutes = int(duration_parts[1])
                    # seconds = int(duration_parts[2].split()[0])
                    
                    total_hours = 0
                    pass
                    
                    if name in worker_hours:
                        worker_hours[name] += round(total_hours,2)
                    else:
                        worker_hours[name] = round(total_hours,2)
                else:
                    if name in worker_hours:
                        worker_hours[name] += round(float(duration),2)
                    else:
                        worker_hours[name] = round(float(duration),2)
        except KeyError:
            continue

    # Display the bar chart
    #st.write(worker_hours)
    st.bar_chart(worker_hours)

    # Get the names and hours as separate lists
# names = list(worker_hours.keys())
# hours = list(worker_hours.values())

# # Create a dataframe from the lists
# data = { 'Hours': hours,'Name': names}
# dfw = pd.DataFrame(data)

# Display the bar chart with customized x-axis and y-axis
#st.bar_chart(dfw.set_index('Hours'),use_container_width=False)
    # for name, hours in worker_hours.items():
    #     st.write(f"{name}: {hours} hours")

    #st.image("https://static.streamlit.io/examples/cat.jpg")



with col3:
   
   st.header("Last Week's Hours")
   # Get the dates for the previous week
   today = datetime.today()
   last_sun = today - timedelta(days=today.weekday() + 1)
   last_sunday = last_sun.strftime('%m/%d/%Y')

   last_mon = last_sun - timedelta(days=6)
   last_monday = last_mon.strftime("%m/%d/%Y")

# print(last_monday)
# print(last_sunday)
   st.write (last_monday,"to",last_sunday)
   worker_hours2 = {}

   for i in range(1, 6):
    date_col = f"Date{i}"
    duration_col = f"Duration{i}"
    
    try:
        df_filtered = df2[(pd.to_datetime(df2[date_col]) >= pd.to_datetime(last_monday)) & (pd.to_datetime(df2[date_col]) <= pd.to_datetime(last_sunday))]
        
        for index, row in df_filtered.iterrows():
            name = row['Name ']
            duration = row[duration_col]
            
            if pd.notnull(duration):
                duration = str(duration)  # Convert duration to string
                
                if ':' in duration:
                    # duration_parts = duration.split(':')
                    # hours = int(duration_parts[0])
                    # minutes = int(duration_parts[1])
                    # seconds = int(duration_parts[2].split()[0])
                    
                    total_hours = 0
                    pass
                    
                    if name in worker_hours2:
                        worker_hours2[name] += round(total_hours,2)
                    else:
                        worker_hours2[name] = round(total_hours,2)
                else:
                    if name in worker_hours2:
                        worker_hours2[name] += round(float(duration),2)
                    else:
                        worker_hours2[name] = round(float(duration),2)
    except KeyError:
        continue

# Display the names and total hours
    for name, hours in worker_hours2.items():
        print(f"{name}: {hours} hours")
    print(worker_hours2)

   #st.write(worker_hours2)
   st.bar_chart(worker_hours2)
   #st.image("https://static.streamlit.io/examples/dog.jpg")today = datetime.today()
   # Get the dates for the previous week
   

    

#########____________________________________________________________


# Past pay period code and Curreent pay period graph 

#########_________________________________________________________


col1, col2 = st.columns(2)




with col2:

   st.header("Last Pay Period")

   today = datetime.today()
   #today=pd.to_datetime('06/01/2023')
   if today.day >= 16:
    start_date = datetime(today.year, today.month, 1)
    end_date = datetime(today.year, today.month, 15)
   else:
    last_month_end = today.replace(day=1) - timedelta(days=1)
    start_date = datetime(last_month_end.year, last_month_end.month, 16)
    end_date = last_month_end

   start_date_str = start_date.strftime("%m/%d/%Y")
   end_date_str = end_date.strftime("%m/%d/%Y")
   #print(start_date_str)
   #print(end_date_str)

   st.write(start_date_str ,"to", end_date_str)
   worker_hours3 = {}

   for i in range(1, 6):
    date_col = f"Date{i}"
    duration_col = f"Duration{i}"
    
    try:
        df_filtered = df2[(pd.to_datetime(df2[date_col]) >= pd.to_datetime(start_date_str)) & (pd.to_datetime(df2[date_col]) <= pd.to_datetime(end_date_str))]
        
        for index, row in df_filtered.iterrows():
            name = row['Name ']
            
            duration = row[duration_col]
            
            if pd.notnull(duration):
                duration = str(duration)  # Convert duration to string

                if ':' in duration:
                    # duration_parts = duration.split(':')
                    # hours = int(duration_parts[0])
                    # minutes = int(duration_parts[1])
                    # seconds = int(duration_parts[2].split()[0])
                    
                    total_hours2 = 0
                    pass 
                    
                    if name in worker_hours3:
                        worker_hours3[name] += round(total_hours2,2)
                    else:
                        worker_hours3[name] = round(total_hours2,2)
                else:
                    if name in worker_hours3:
                        worker_hours3[name] += round(float(duration),2)
                    else:
                        worker_hours3[name] = round(float(duration),2)
                
    except KeyError:
        continue


    # for name, hours in worker_hours3.items():
    #     print(f"{name}: {hours} hours")
   st.bar_chart(worker_hours3)


with col1:
    st.header("Current Pay Period")
   

    curr_stdate=end_date +  timedelta(days=1)
    curr_stdate_str=curr_stdate.strftime("%m/%d/%Y")
    curr_end_date=datetime.today() - timedelta(days=1)
    curr_endate_str=curr_end_date.strftime("%m/%d/%Y")
    st.write(curr_stdate_str,"to",curr_endate_str)
    #print(curr_stdate_str)
    #print(curr_endate_str)


    ## writind code to plot the duration graph between this time range

    worker_hours4 = {}

    for i in range(1, 6):
        date_col = f"Date{i}"
        duration_col = f"Duration{i}"
        
        try:
            df_filtered = df2[(pd.to_datetime(df2[date_col]) >= pd.to_datetime(curr_stdate_str)) & (pd.to_datetime(df2[date_col]) <= pd.to_datetime(curr_endate_str))]
            
            for index, row in df_filtered.iterrows():
                name = row['Name ']
                
                duration = row[duration_col]
                
                if pd.notnull(duration):
                    duration = str(duration)  # Convert duration to string

                    if ':' in duration:
                        # duration_parts = duration.split(':')
                        # hours = int(duration_parts[0])
                        # minutes = int(duration_parts[1])
                        # seconds = int(duration_parts[2].split()[0])
                        
                        total_hours3 = 0
                        pass 
                        
                        if name in worker_hours4:
                            worker_hours4[name] += round(total_hours3,2)
                        else:
                            worker_hours4[name] = round(total_hours3,2)
                    else:
                        if name in worker_hours4:
                            worker_hours4[name] += round(float(duration),2)
                        else:
                            worker_hours4[name] = round(float(duration),2)
                    
        except KeyError:
            continue
    st.bar_chart(worker_hours4)

###________________________________________________________________


## UTILAZATION /SPEEDOMETER

###_____________________________________________________________________________

st.header(" KPIs")
col1, col2 = st.columns(2)
with col1: 
    

    # Get the dates for the previous week
    today = datetime.today()
    last_sun = today - timedelta(days=today.weekday() + 1)
    last_sunday=last_sun.strftime('%m/%d/%Y')

    last_mon = last_sun - timedelta(days=6)
    last_monday=last_mon.strftime("%m/%d/%Y")

    print(last_monday)
    print(last_sunday)


    #get the name off all people and add all the duration in 
    df_filtered = df3[(pd.to_datetime(df3["Date"]) >= pd.to_datetime(last_monday)) & (pd.to_datetime(df3["Date"]) <= pd.to_datetime(last_sunday))]

    #if we have checkin time and checkout time is there 


    checkin_hours={}

    for index, row in df_filtered.iterrows():
        name = row['Name']
        duration = row['Total_Hours']
                
        if pd.notnull(duration):
            if name in checkin_hours:
                checkin_hours[name] += float(duration)
            else:
                checkin_hours[name] = float(duration)



    ## calculating the efficency of each people in past week
    name_utl=[]
    utl=[]
    for item,values in worker_hours2.items():
        #print(item)
        for i,v in checkin_hours.items():
            if(item==i):
                name_utl.append(item)
                e=float((values/v)*100)
                utl.append(e)

    #creating the name and efficiencis dectionary
    utilization_dict=dict(zip(name_utl,utl))
    #print(efficiency_dict)
    #cheating a dropbox to chose the me form the

    st.markdown(
        """
        <style>
        .nicebar {
            background-color: lightblue;
            color: black;
            font-weight: bold;
            padding: 8px;
            border-radius: 4px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<p class="nicebar">Utilization Past Week</p>', unsafe_allow_html=True)

    selectes_name=st.selectbox("UTILIZATION LIST",utilization_dict.keys())
    st.write("Name: ",selectes_name)

    st.write("Utilization:",utilization_dict[selectes_name])
    v=utilization_dict[selectes_name]
    fig = go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = v,
        mode = "gauge+number",
        title = {'text': "UTILIZATION "},
        gauge = {'axis': {'range': [None, 500]},
                'steps' : [
                    {'range': [0, 250], 'color': "yellow"},
                    {'range': [250, 500], 'color': "lavender"}],
                'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}}))


    st.plotly_chart(fig, theme=None, use_container_width=True)

###_____________________________________________________________________________

## EFFICIENCY /SPEEDOMETER for past week

###_____________________________________________________________________________

# Get the dates for the previous week

with col2: 
    today = datetime.today()
    last_sun = today - timedelta(days=today.weekday() + 1)
    last_sunday = last_sun.strftime('%m/%d/%Y')

    last_mon = last_sun - timedelta(days=6)
    last_monday = last_mon.strftime("%m/%d/%Y")

    #st.write(last_monday,"to",last_sunday)
    #print(last_sunday),

    worker_hours2 = {}

    for i in range(1, 6):
        date_col = f"Date{i}"
        duration_col = f"Duration{i}"
        work_order_col = f"Work Order"
        name_col = "Name "  # Adjust the column name here
        
        try:
            df_filtered = df2[(pd.to_datetime(df2[date_col]) >= pd.to_datetime(last_monday)) & (pd.to_datetime(df2[date_col]) <= pd.to_datetime(last_sunday))]
            
            for index, row in df_filtered.iterrows():
                work_order = row[work_order_col]
                duration = row[duration_col]
                name = row[name_col]
                
                if pd.notnull(duration):
                    duration = str(duration)  # Convert duration to string
                    
                    if ':' in duration:
                        
                        # Convert the duration to total hours
                        pass
                        
    #                     if work_order in worker_hours2:
    #                         worker_hours2[work_order] += total_hours
    #                     else:
    #                         worker_hours2[work_order] = total_hours
                    else:
                        if work_order in worker_hours2:
                            worker_hours2[work_order] += float(duration)
                        else:
                            worker_hours2[work_order] = float(duration)
        
        except KeyError:
            continue

    # Create a DataFrame from the worker_hours2 dictionary
    table_ef = {'Work Order': worker_hours2.keys(),
                'Assigned Hours': [df2[df2['Work Order'] == wo]['Assigned_Hours'].sum() for wo in worker_hours2.keys()],
                'Total Duration': worker_hours2.values(),
                'Name': [df2[df2['Work Order'] == wo][name_col].values[0] for wo in worker_hours2.keys()]}  # Adjust the column name here
    ef_table = pd.DataFrame(table_ef)

    # Display the table
    print(ef_table)
    # st.write(ef_table)

    #converting the string to float
    ef_table['Assigned Hours']=ef_table['Assigned Hours'].astype(float)

    # in the abobe table writing effenciency formula and addin a new coulmn of effenciecy 
    ef_final= { 'Work Order':ef_table['Work Order'],
            'Name': ef_table['Name'],
            'Efficiency': round((ef_table['Assigned Hours']/ef_table['Total Duration']*100),2)}
    efficiency_table=pd.DataFrame(ef_final)
    #st.write(efficiency_table)

   
    #using css from avobe
    st.markdown('<p class="nicebar">Efficiencies Past Week </p>', unsafe_allow_html=True)

    selected_wo=st.selectbox("Efficiencies of workorder ", efficiency_table['Work Order'])
    st.write("Work Order: ",selected_wo)

    selected_row = efficiency_table[efficiency_table['Work Order'] == selected_wo]

    # Display the selected work order
    # st.write(selected_row)
    st.write("Name: ",selected_row['Name'].iloc[0])
    st.write("Efficiency: ", selected_row['Efficiency'].iloc[0])
    e=selected_row['Efficiency'].iloc[0]
    # print(e)

    fig2= go.Figure(go.Indicator(
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = e,
        mode = "gauge+number",
        title = {'text': "Efficiency"},
        gauge = {'axis': {'range': [None, 300]},
                'steps' : [
                    {'range': [0, 250], 'color': "yellow"},
                    {'range': [250, 500], 'color': "lavender"}],
                'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 290}}))

    st.plotly_chart(fig2, theme=None, use_container_width=True)





###_____________________________________________________________________________

## Order by sites code

###_____________________________________________________________________________


# code for order by sites
#st.markdown('<p1 class="nicebar">Work Order by sites </p1>', unsafe_allow_html=True)
st.header("Work Order Status")
site_values = df2['Site'].unique()
site_values=np.append(site_values,"All_Sites")




sl_site = st.selectbox(" Sites: ", site_values)

if sl_site=="All_Sites":
    workby_site=df2[['Name ', 'Work Order', 'Status', 'Description', 'Site', 'Date Created',
       'Time Created', 'Assigned_Hours']]
    #st.write(workby_site)
    sl_list=df2['Status'].unique()
    sl_list=np.append(sl_list, "All_WorkOrders")
    #st.write(sl_list)
    sl_status =st.selectbox("Status", sl_list)

    # for i in sl_list:
    #     sl_status =st.checkbox(i)
    if sl_status=="All_WorkOrders":
        st.write(workby_site)
    else:
        sl_df= workby_site[workby_site['Status']==sl_status]
        st.write(sl_df)   


else:
    workby_site=df2[df2['Site']==sl_site]
    
    workby_site=workby_site[['Name ', 'Work Order', 'Status', 'Description', 'Site', 'Date Created',
       'Time Created', 'Assigned_Hours']]

    # radio box for status of work oreder at each site
    sl_list=df2['Status'].unique()
    sl_list=np.append(sl_list, "All_WorkOrders")
    #st.write(sl_list)
    sl_status =st.selectbox("Status", sl_list)

    # for i in sl_list:
    #     sl_status =st.checkbox(i)
    if sl_status=="All_WorkOrders":
        st.write(workby_site)
    else:
        sl_df= workby_site[workby_site['Status']==sl_status]
        st.write(sl_df)   




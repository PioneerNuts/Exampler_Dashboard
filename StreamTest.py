# import module
import streamlit as st
import pandas as pd
import numpy as np
import panel as pn
import matplotlib.pyplot as plt

from datetime import date, timedelta
pn.extension('tabulator')



# st.topbar.write("Exampler Dashboard")


# Title
st.title("Exampler Dashboard")


## reading the data from url and looking for site from it
df=pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vQi5lnVESmIFGng5PeZj2QYEM1hEcrGxmpTCidXkbHZmR-7eswXAsSqI0ZC02tdsJ5aTKzs56F_G0n7/pub?output=csv")

# taking site values
site_values= df['Site '].unique()

## making a dropdown with all the sites

##selection box using all the unique values in site

site = st.selectbox(" Our Sites: ", site_values)
 
# print the selected hobby
st.write("Your selected site is : ", site)

###___________________________

###   Working right now head counts code
###____________________________________________

st.header('WORKING RIGHT NOW')

# Get unique site values
site_values = df['Site '].unique()

# Count the number of sites
site_numbers = len(site_values)

print("Workers right now")

# Initialize empty lists
sites = []
counts = []

# Iterate over each site value
for site in site_values:
    # Filter the dataframe for the current site
    df_filter = df[df['Site '] == site]
    
    # Append the site value to the 'sites' list
    sites.append(site)
    
    # Print the names of workers at the current site
    #print(df_filter[['Name','Site ']])
    
    # Count the number of workers with 'Status' as 'Started'
    c = df_filter[df_filter['Status'] == "Started"]['Name'].count()
    print(c)
    
    # Append the count to the 'counts' list
    counts.append(c)

# Create a dictionary mapping sites to worker counts
working_rightnow = dict(zip(sites, counts))
st.bar_chart(working_rightnow)



####__________________________________________________________________________


#writing 3 columns for HOURSwors in a day/ Work in each week/ Works in month

####_________________________________________________________________________


st.header("Hour's tracker for workers")

col1, col2, col3 = st.columns(3)

with col1:
    st.header("Hour's Last day")
    df2=pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vQSjwmOOwc1iHvIl_gc1mlUB9Pa_rB7pwg__Agq7JQowZ8XvycnGG2AxsXyk9WDJ4h_clBt0jiceTDl/pub?output=csv")
    previous_day = date.today() - timedelta(days=1)
    previous_day_str = previous_day.strftime("%m/%d/%Y")

    # Create an empty dictionary to store names and total hours
    worker_hours = {}

    # Iterate over the columns containing dates and durations
    for i in range(1, 6): 
        date_col = f"Date{i}"
        duration_col = f"Duration{i}"
        
        try:
        
            df_filtered = df2[df2[date_col] == previous_day_str]
            
            # Calculate the total hours for each worker
            for index, row in df_filtered.iterrows():
                name = row['Name ']
                duration = row[duration_col]
                
                if pd.notnull(duration):
                    if name in worker_hours:
                        worker_hours[name] += float(duration)
                    else:
                        worker_hours[name] = float(duration)
        except KeyError:
            
            continue

    # # Print the names and total hours
    # Display the names and total hours as a table using Streamlit
    table_data = {'Name': [], 'Hours': []}
    for name, hours in worker_hours.items():
        table_data['Name'].append(name)
        table_data['Hours'].append(hours)

    #st.table(pd.DataFrame(table_data))

    st.bar_chart(data=table_data,x='Hours',y='Name')
    # for name, hours in worker_hours.items():
    #     st.write(f"{name}: {hours} hours")

    #st.image("https://static.streamlit.io/examples/cat.jpg")



with col2:
   st.header("Hour's Last week")

   from dateutil.relativedelta import relativedelta, MO,SU
   # getting today's current local date
   todayDate = date.today()

   todayDate1=todayDate.strftime("%m/%d/%Y")
   st.write('Today Date:',todayDate1)


   lastMonday = todayDate + relativedelta(weekday=MO(-2))
   lastMonday1=lastMonday.strftime("%m/%d/%Y")
   # printing the last Monday date
   st.write("The last Monday date:", lastMonday1)

   lastSunday=todayDate + relativedelta(weekday=SU(-1))
   lastSunday=lastSunday.strftime("%m/%d/%Y")
   st.write("last sunday was ", lastSunday)

   #st.image("https://static.streamlit.io/examples/dog.jpg")

with col3:
   st.header("Hour's Last Month")
   
   #st.image("https://static.streamlit.io/examples/owl.jpg")


###_____________________________________________________________________________

## utilazation

###_____________________________________________________________________________




# # I am creating a table where the site is selected site and having workorder/ priorty /name/ status and Date started as a column for each

# def filter_by_site(df, selected_site):
#     filtered_df = df[df['Site '] == selected_site]  
#     return filtered_df[['WorkOrder', 'Name', 'Status', 'Date Started']] 


# #selected_site = 'Break' 

# filtered_table = filter_by_site(df, site)

# # Displaying the table
# st.table(filtered_table)  



# creating th hed count of all the workers in each sites















# # Creating  the pie chart
# status_counts = df['Status'].value_counts()
# plt.figure(figsize=(10,6))
# status_pie = plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%')
# plt.title('Status Distribution')

# # Save the pie chart as an image
# plt.savefig("piechart.png", format='png')
# plt.close()  # Close the plot to free up resources

# # Display the saved image using Streamlit
# st.image("piechart.png")
#creatin a column with high priority work




df['Work_with_high_priority'] = df['WorkOrder'].dropna().apply(lambda x: x.startswith(('AH', 'SH')))
# print(df['Work_with_high_priority'])    
def priority_table(df, selected_value):
    filtered_df = df[df['Work_with_high_priority'] == selected_value]  
    return filtered_df[['WorkOrder', 'Name', 'Status']]     

priority_table=priority_table(df, True)

# Displaying the priority table
st.title('Higest Priority Running work')
st.table(priority_table) 









# # Create a list of options for the dropdown
# options = df['Name'].unique().tolist()

# # Create the dropdown widget
# dropdown = pn.widgets.Select(name='Employee', options=options)



# st.sidebar.title(":black[Select an Employee]")

# emp_dropdown = st.sidebar.selectbox("Choose Employee: ", df['Name'].unique())

# # Create the dropdown widget
# #selected_name = st.selectbox("Select Name", df['Name'])



# # Filter the dataframe based on the selected name
# filtered_df = df[df['Name'] == emp_dropdown]

# # Display the information
# if not filtered_df.empty:
#     st.sidebar.write(f"Work Orders assigned to {emp_dropdown}:")
#     workorder_status = st.sidebar.selectbox("Choose Status of WorkOrder you want to view : ", filtered_df['Status'].unique())
    
#     for index, work_order in filtered_df['WorkOrder'].items():
        
#         #st.sidebar.write(filtered_df[['WorkOrder']])
#         if st.sidebar.button(work_order):
#         # Handle button click event
#             #st.sidebar.write(f"You clicked on {work_order}")
#             st.sidebar.write(f":red [WorkOrder ID:] :red[{work_order}]")


#             st.sidebar.write(filtered_df['Description']) 
#             #st.write()
#     # if st.button("WorkOrder"):
#     #     # Handle button click event
#     #     st.write(f"The button for {selected_name}'s WOrkOrder was clicked!")
# else:
#     st.sidebar.write(f"No information found for {emp_dropdown}.")

# Top 10 priority task

st.sidebar.write ("Top 10 Heigest priority work")
#creatin a column with high priority work
df['Work_with_high_priority'] = df['WorkOrder'].dropna().apply(lambda x: x.startswith(('AH','SH','AM','SM'))) 

print(df['Work_with_high_priority'])    
def priority_table(df, selected_value):
    filtered_df = df[df['Work_with_high_priority'] == selected_value ]
    #filtered_data= filtered_df[[ 'Name', 'Status']]
    #filtered_df2=filtered_df[filtered_df[['Status']]=='Created']
        #print(filtered_df[['Status']])
    
    return filtered_df[[ 'Name', 'Status']][:10]


st.sidebar.table(priority_table(df, True))

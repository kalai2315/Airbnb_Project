import pandas as pd
import streamlit as st
import plotly.express as px
import pymongo
from pymongo import MongoClient
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
import pymysql
from sqlalchemy import create_engine




# Set page configuration
st.set_page_config(
    page_title="Airbnb Data Analysis",
    page_icon=":house:",
    layout="wide"
)

image = Image.open('F:\project\Airbnb\download (1).png')
st.image(image)
# Title and description
st.title('Airbnb Data Analysis')
st.write("Explore insights from the Airbnb dataset.")

# CREATING CONNECTION WITH MONGODB ATLAS AND RETRIEVING THE DATA
client = pymongo.MongoClient("mongodb+srv://kalaiselvimaheshkumar:DevDhakshi@cluster0.hgirp18.mongodb.net/sample_airbnb?retryWrites=true&w=majority")
db = client.sample_airbnb
collection = db.listingsAndReviews

# Load the data
df = pd.read_csv('F:\project\Airbnb\Airbnb_Data.csv')

st.markdown(
    """
    <style>
    /* Adjust the width of the select boxes */
    div[data-baseweb="select"] > div:first-child {
        max-width: 150px;  /* Set the maximum width */
    }
    </style>
    """,
    unsafe_allow_html=True
)
Airbnb_data = []
for i in collection.find():
    data = {
        '_id': i['_id'],
        'Listing_url': i['listing_url'],
        'Name': i.get('name'),
        'Description': i['description'],
        'House_rules': i.get('house_rules'),
        'Property_type': i['property_type'],
        'Room_type': i['room_type'],
        'Bed_type': i['bed_type'],
        'Min_nights': int(i['minimum_nights']),
        'Max_nights': int(i['maximum_nights']),
        'Cancellation_policy': i['cancellation_policy'],
        'Accomodates': i['accommodates'],
        'Total_bedrooms': i.get('bedrooms'),
        'Total_beds': i.get('beds'),
        'Price': i['price'],
        'Security_deposit': i.get('security_deposit'),
        'Cleaning_fee': i.get('cleaning_fee'),
        'Extra_people': i['extra_people'],
        'Guests_included': i['guests_included'],
        'No_of_reviews': i['number_of_reviews'],
        'Review_scores': i['review_scores'].get('review_scores_rating'),
        'Amenities': ', '.join(i['amenities']),
        'Host_id': i['host']['host_id'],
        'Host_name': i['host']['host_name'],
        'Neighbourhood':i['host']['host_neighbourhood'],
        'Street': i['address']['street'],
        'Country': i['address']['country'],
        'Country_code': i['address']['country_code'],
        'Location_type': i['address']['location']['type'],
        'Longitude': i['address']['location']['coordinates'][0],
        'Latitude': i['address']['location']['coordinates'][1],
        'Is_location_exact': i['address']['location']['is_location_exact']
    }
    Airbnb_data.append(data)


# Filter by country
selected_country = st.sidebar.selectbox('Select Country', df['Country'].unique())

# Filter DataFrame based on the selected country
filtered_df = df[df['Country'] == selected_country]

# Group by property type and count listings
property_type_counts = filtered_df['Property_type'].value_counts().reset_index()
property_type_counts.columns = ['Property_type', 'Count']

# Create bar chart for property types
fig = px.bar(property_type_counts, x='Property_type', y='Count', title=f'Property Types in {selected_country}')
st.plotly_chart(fig)



# Filter by property type
selected_property_type = st.sidebar.selectbox('Property Type', df['Property_type'].unique())

# Filter DataFrame based on the selected property type
filtered_df = df[df['Property_type'] == selected_property_type]

bed_type_counts = filtered_df['Bed_type'].value_counts().reset_index()
bed_type_counts.columns = ['Bed_type', 'Count']

neighborhood_counts = filtered_df['Neighbourhood'].value_counts().reset_index()
neighborhood_counts.columns = ['Neighbourhood', 'Count']

# Create bar chart using Plotly
fig_bar = px.bar(neighborhood_counts, x='Neighbourhood', y='Count', title='Neighbourhood Distribution',
                 labels={'Neighbourhood': 'Neighbourhood Type', 'Count': 'Number of Listings'})
st.plotly_chart(fig_bar)

# Group by room type and count listings
room_type_counts = filtered_df['Room_type'].value_counts().reset_index()
room_type_counts.columns = ['Room_type', 'Count']

# Calculate percentage of bed type and room type
total_bed_type_listings = bed_type_counts['Count'].sum()
total_room_type_listings = room_type_counts['Count'].sum()
bed_type_counts['Percentage'] = bed_type_counts['Count'] / total_bed_type_listings * 100
room_type_counts['Percentage'] = room_type_counts['Count'] / total_room_type_listings * 100

# Create bar chart using Plotly
fig_bar = px.bar(bed_type_counts, x='Bed_type', y='Count', title='Bed Type Distribution',
                 labels={'Bed_type': 'Bed Type', 'Count': 'Number of Listings'})
st.plotly_chart(fig_bar)

# Create pie chart using Plotly
fig_pie = px.pie(room_type_counts, values='Count', names='Room_type', title='Room Type Distribution',
                 labels={'Room_type': 'Room Type', 'Count': 'Number of Listings'})
st.plotly_chart(fig_pie)

# Group by minimum nights and count listings
min_nights_counts = filtered_df['Min_nights'].value_counts().reset_index()
min_nights_counts.columns = ['Min_nights', 'Count']

# Group by maximum nights and count listings
max_nights_counts = filtered_df['Max_nights'].value_counts().reset_index()
max_nights_counts.columns = ['Max_nights', 'Count']

# Create figure for minimum nights distribution
fig_min_nights = px.bar(min_nights_counts, x='Min_nights', y='Count', 
                         labels={'Min_nights': 'Minimum Nights', 'Count': 'Number of Listings'},
                         title='Minimum Nights Distribution')
fig_min_nights.update_layout(xaxis=dict(type='category'))

# Create figure for maximum nights distribution
fig_max_nights = px.bar(max_nights_counts, x='Max_nights', y='Count', 
                         labels={'Max_nights': 'Maximum Nights', 'Count': 'Number of Listings'},
                         title='Maximum Nights Distribution')
fig_max_nights.update_layout(xaxis=dict(type='category'))

# Display the figures using Plotly
with st.expander("Minimum Nights Distribution"):
    st.plotly_chart(fig_min_nights)
with st.expander("Maximum Nights Distribution"):
    st.plotly_chart(fig_max_nights)

import plotly.figure_factory as ff

# Define the list of unique bed types and room types
bed_types = filtered_df['Bed_type'].unique()
room_types = filtered_df['Room_type'].unique()

# Create columns for layout
col1, col2 = st.columns(2)

# Selectbox widgets for bed type and room type
with col1:
    selected_bed_type = st.selectbox('Select Bed Type', bed_types)

with col2:
    selected_room_type = st.selectbox('Select Room Type', room_types)

# Filter DataFrame based on selected bed type and room type
filtered_df_selection = filtered_df[(filtered_df['Bed_type'] == selected_bed_type) &
                                    (filtered_df['Room_type'] == selected_room_type)]

# Display the filtered DataFrame within the expander
with st.expander("Property_type wise Room_type and Minimum stay nights"):
    df_sample = filtered_df_selection[["Host_name", "Neighbourhood", "Price", "Min_nights"]]
    fig = ff.create_table(df_sample, colorscale="Cividis")
    st.write(df_sample)


# Count the number of listings for each value of Accommodates
accommodates_counts = filtered_df['Accomodates'].value_counts().reset_index()
accommodates_counts.columns = ['Accomodates', 'Count']

# Count the number of listings for each value of Total_bedrooms
bedrooms_counts = filtered_df['Total_bedrooms'].value_counts().reset_index()
bedrooms_counts.columns = ['Total_bedrooms', 'Count']

# Count the number of listings for each value of Total_beds
beds_counts = filtered_df['Total_beds'].value_counts().reset_index()
beds_counts.columns = ['Total_beds', 'Count']

# Create Streamlit columns
col1, col2 = st.columns(2)


with col1:
    fig_bedrooms = px.bar(bedrooms_counts, x='Total_bedrooms', y='Count', 
                      labels={'Total_bedrooms': 'Bedrooms', 'Count': 'Count'},
                      title='Bedrooms Distribution')
    st.plotly_chart(fig_bedrooms)
with col2:
   fig_beds = px.bar(beds_counts, x='Total_beds', y='Count', 
                  labels={'Total_beds': 'Beds', 'Count': 'Count'},
                  title='Beds Distribution')
   st.plotly_chart(fig_beds)



# Select country (with unique key)
selected_country = st.selectbox('Select Country', df['Country'].unique(), key='country_select')

# Filter DataFrame based on the selected country
filtered_df = df[df['Country'] == selected_country]

# Tabs for different analyses
tab1, tab2, tab3, tab4 = st.tabs(['Price', 'Cleaning Fee', 'Extra People', 'Guests Included'])

# Price Analysis
with tab1:
    # Extract the necessary columns
    price_analysis_df = filtered_df[['Property_type', 'Room_type', 'Price']]

    # Handle missing values if needed
    price_analysis_df.dropna(inplace=True)  # Drop rows with missing values

    # Create Streamlit columns layout
    col1, col2 = st.columns(2)

    # Plot bar chart for price distribution by property type in the first column
    with col1:
        st.subheader(f'Price Distribution Analysis')
        fig = px.bar(price_analysis_df, x='Property_type', y='Price', title=f'Price Distribution by Property Type in {selected_country}')
        fig.update_layout(xaxis_title='Property Type', yaxis_title='Price')
        st.plotly_chart(fig)

    with col2:        
        fig = px.bar(price_analysis_df, x='Room_type', y='Price', title=f'Price Distribution by Room Type in {selected_country}')
        fig.update_layout(xaxis_title='Room Type', yaxis_title='Price')
        st.plotly_chart(fig)
# Cleaning Fee Analysis
with tab2:
    
    cleaning_fee_analysis_df = filtered_df[['Cleaning_fee']]

    # Handle missing values if needed
    cleaning_fee_analysis_df.dropna(inplace=True)  # Drop rows with missing values

        #st.subheader(f'Cleaning Fee Distribution in {selected_country}')
    fig = px.histogram(cleaning_fee_analysis_df, x='Cleaning_fee', title=f'Cleaning Fee Distribution in {selected_country}', nbins=20)
    fig.update_layout(xaxis_title='Cleaning Fee', yaxis_title='Frequency')
    st.plotly_chart(fig)

with tab3:
    # Extra People Analysis
    extra_people_analysis_df = filtered_df[['Extra_people']]

    # Handle missing values if needed
    extra_people_analysis_df.dropna(inplace=True)  # Drop rows with missing values

    # Plot histogram for extra people charges distribution using Plotly
    fig = px.histogram(extra_people_analysis_df, x='Extra_people', nbins=20,
                    title=f'Extra People Charges Distribution in {selected_country}',
                    labels={'Extra_people': 'Extra People Charges', 'count': 'Frequency'},
                    marginal='rug', color_discrete_sequence=['#FFA15A'])  
    fig.update_layout(xaxis_title='Extra People Charges', yaxis_title='Frequency')
    st.plotly_chart(fig)

with tab4:
    # Guests Included Analysis
    guests_included_analysis_df = filtered_df[['Guests_included']]

    # Handle missing values if needed
    guests_included_analysis_df.dropna(inplace=True)  # Drop rows with missing values

    # Plot bar chart for guests included distribution
    fig = px.histogram(guests_included_analysis_df, x='Guests_included',
                    title=f'Number of Guests Included Distribution in {selected_country}',
                    labels={'Guests_included': 'Number of Guests Included', 'count': 'Count'},
                    color_discrete_sequence=['#FFFF00'])  
    fig.update_layout(xaxis_title='Number of Guests Included', yaxis_title='Count')
    st.plotly_chart(fig)




from collections import Counter

st.subheader("Top 10 Amenities")
amenities_data = filtered_df['Amenities']

# Parse amenities and count frequency
amenities_list = []
for amenities in amenities_data:
    amenities_list.extend(amenities.strip('{}').split(','))

# Count frequency of each amenity
amenities_count = Counter(amenities_list)

# Convert to DataFrame
amenities_df = pd.DataFrame(amenities_count.items(), columns=['Amenity', 'Count'])

# Sort DataFrame by count in descending order
amenities_df = amenities_df.sort_values(by='Count', ascending=False)

# Select top 10 amenities
top_10_amenities = amenities_df.head(10)

# Create bar chart using Plotly
fig = px.bar(top_10_amenities, x='Count', y='Amenity', orientation='h',
             title=f'Top 10 Amenities in {selected_country}', labels={'Count': 'Frequency', 'Amenity': 'Amenity'})
st.plotly_chart(fig)


st.subheader("Review Distribution Analysis")
reviews_analysis_df = filtered_df[['No_of_reviews', 'Review_scores']]


reviews_analysis_df.dropna(inplace=True)  # Drop rows with missing values

# Group by country and calculate total reviews and average review scores
reviews_by_country = df.groupby('Country').agg({'No_of_reviews': 'sum', 'Review_scores': 'mean'}).reset_index()

# Create DataFrame for total reviews
total_reviews_df = reviews_by_country[['Country', 'No_of_reviews']]

# Create DataFrame for average review scores
average_scores_df = reviews_by_country[['Country', 'Review_scores']]

# Create pie chart for total reviews
fig_total_reviews = px.pie(total_reviews_df, values='No_of_reviews', names='Country', title='Total Reviews by Country')

# Create pie chart for average review scores
fig_average_scores = px.pie(average_scores_df, values='Review_scores', names='Country', title='Average Review Scores by Country')

# Display pie charts in two columns using Streamlit
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_total_reviews)

with col2:
    st.plotly_chart(fig_average_scores)


# Group by cancellation policy and count listings for each policy
cancellation_policy_counts = filtered_df['Cancellation_policy'].value_counts().reset_index()
cancellation_policy_counts.columns = ['Cancellation_policy', 'Count']

# Calculate the percentage of listings for each cancellation policy
total_listings = cancellation_policy_counts['Count'].sum()
cancellation_policy_counts['Percentage'] = cancellation_policy_counts['Count'] / total_listings * 100

# Plot the line chart
fig = px.bar(cancellation_policy_counts, x='Cancellation_policy', y='Percentage',
              title='Cancellation Policy Distribution')
st.plotly_chart(fig)






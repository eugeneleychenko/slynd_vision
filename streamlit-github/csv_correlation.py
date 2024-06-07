import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# Set page title
st.set_page_config(page_title='Campaign Analysis')

# Add a title and description
st.title('Campaign Analysis')
st.write('Upload a CSV file to analyze correlations between different dimensions.')

# File uploader
uploaded_file = st.file_uploader('Choose a CSV file', type='csv')

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    # Load a default file from the server's filesystem
    data = pd.read_csv('Slynd.csv')
    st.write('No file uploaded. Loaded default Slynd.csv')

# Display the first few rows of the data
st.subheader('Data Preview')
st.write(data.head())

# Specify the input columns
input_columns = ['Patient Type', 'Funnel', 'Link to Post', 'Link', 'Preview', 'Caption Copy',
                 'Post Format', 'Media Style', 'Production Type', 'Talent', 'Conversational Tone',
                 'Emotional Tone', 'Educational/Informative?', 'IRI?', 'About Slynd?', 'LLEB Messaging?', 'Topic']

# Perform correlation analysis only on numeric data
st.subheader('Correlation Analysis')
numeric_data = data.select_dtypes(include=[np.number])
corr_matrix = numeric_data.corr()

# Plot the default correlation heatmap
st.caption('Correlation Heatmap')
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
st.pyplot(plt)

# Add a selector for input columns
selected_columns = st.multiselect('Select input columns to include in the heatmap', input_columns)

if selected_columns:
    # Perform one-hot encoding for selected categorical variables
    encoded_data = pd.get_dummies(data[selected_columns])
    
    # Combine encoded categorical variables with numeric variables
    combined_data = pd.concat([numeric_data, encoded_data], axis=1)
    
    # Calculate the correlation matri
    corr_matrix = combined_data.corr()
    
    # Plot the updated correlation heatmap
    st.caption('Updated Correlation Heatmap')
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    st.pyplot(plt)

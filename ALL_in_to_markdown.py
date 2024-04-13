import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
import altair as alt

# Set Streamlit page configuration
st.set_page_config(layout='wide')

st.markdown(
    """
    <style>
    .reportview-container .main .block-container {
        max-width: 70%;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Just a quick instruction on the possibility of zoom in and out on the charts
st.markdown("""
<p style='font-size: 12px'>
<strong>Tip for Users:</strong> You can zoom in on any part of the chart by clicking and dragging your mouse to select a specific area. To reset the view, double-click on the chart.
</p>
""", unsafe_allow_html=True)


# here is the content of data app
st.title('The process of Reindustrialization ')
st.write('During recent decades, the share of industrial output in national GDP has been declining year by year in many developed countries. Because of the consideration in environment and costs, the developed countries chose to keep high-tech industries or financial industries in their own domain, the big company chose to remove the basic manufactory parts to developing countries.')
st.write('But along with this structural transformation of the economy, which can be defined as a deindustrialization, many social problems have been gradually exposed. Facing these side-effects, some developed countries came up with the policies to achieve reindustrialization.')

# Reading data from Excel files in your repository
export_sum_df = pd.read_excel('export_sum.xlsx')
import_sum_df = pd.read_excel('import_sum.xlsx')


# For demonstration, let's assume you want to visualize the 'export_sum.xlsx' data similarly
# Update the column names according to your actual Excel file structure
# Melt the DataFrame to long format
# Filter the DataFrame for specific countries
countries_of_interest = ['France', 'Germany', 'Japan', 'United Kingdom', 'United States of America']
export_sum_filtered_df = export_sum_df[export_sum_df['Reporting Economy'].isin(countries_of_interest)]

# Melt the filtered DataFrame to long format for animation
export_long_filtered_df = export_sum_filtered_df.melt(id_vars=["Reporting Economy", "Product/Sector"],
                                                      var_name="Year", value_name="ExportValue")

# Convert 'Year' to integer for plotly animation_frame to work correctly
export_long_filtered_df["Year"] = export_long_filtered_df["Year"].astype(int)

base_colors = {
    'France': 'blue',
    'Germany': 'red',
    'Japan': 'green',
    'United Kingdom': 'purple',
    'United States of America': 'orange'
}

# Define a shade for each sector (1 to 3) for each country
# This is a simplistic approach; you might need to adjust the shades according to your needs
color_shades = {
    ('France', 1): 'lightblue',
    ('France', 2): 'blue',
    ('France', 3): 'darkblue',
    ('Germany', 1): 'salmon',
    ('Germany', 2): 'red',
    ('Germany', 3): 'darkred',
    ('Japan', 1): 'lightgreen',
    ('Japan', 2): 'green',
    ('Japan', 3): 'darkgreen',
    ('United Kingdom', 1): 'lavender',
    ('United Kingdom', 2): 'purple',
    ('United Kingdom', 3): 'darkvioletstre',
    ('United States of America', 1): 'lightcoral',
    ('United States of America', 2): 'orange',
    ('United States of America', 3): 'darkorange'
}
export_long_filtered_df['CustomColor'] = export_long_filtered_df.apply(
    lambda row: color_shades[(row['Reporting Economy'], row['Product/Sector'])], axis=1)

sector_descriptions = {
    1: 'Light Industry',
    2: 'Basic Industry',
    3: 'Raw Materials'
}

# Apply the mapping to the dataframe
export_long_filtered_df['SectorDescription'] = export_long_filtered_df['Product/Sector'].map(sector_descriptions)

# Apply the logarithm to the 'ExportValue' for the visualization
export_long_filtered_df['LogExportValue'] = np.log(export_long_filtered_df['ExportValue'])


# Titles and subtitles using Markdown (adapt titles as needed)
#animation_title = '<p style="font-family:Arial Bold; color:black; font-size: 30px;">Five major economies exports by sector over time</p>'
sub_title1 = '<p style="font-family:Arial Bold Italic; color:black; font-size: 20px;">During recent decades, the share of industrial output in national GDP has been declining year by year in 5 major developed countries. The value are in Million USD</p>'
sub_title2 = '<p style="text-align: right; font-family: Arial Bold Italic; color: black; font-size: 15px;">Source: https://stats.wto.org/</p>'

# st.markdown(animation_title, unsafe_allow_html=True)
st.markdown(sub_title1, unsafe_allow_html=True)
# st.markdown(sub_title2, unsafe_allow_html=True)

# Visualization (example using 'export_sum_df')
# Adjust 'x', 'y' to use the logarithmic scale values, and include 'LogExportValue' in hover_data
animation = px.scatter(
    data_frame=export_long_filtered_df,
    x="ExportValue",
    y="LogExportValue",
    size="ExportValue",
    color="CustomColor",  # Use the custom color for differentiation
    title="Log of World Exports by Sector Over Time for Five Major Economies",
    labels={"LogExportValue": "Log of Export Value", "ExportValue": "Export Value"},
    log_x=False,  # log_x is now False because we've already transformed the value manually
    range_y=[export_long_filtered_df["LogExportValue"].min(), export_long_filtered_df["LogExportValue"].max()],
    hover_name="Reporting Economy",
    hover_data={"Year": True, "ExportValue": ':,', "SectorDescription": True, "LogExportValue": ':.2f'},  # Include sector description and log value in hover
    animation_frame="Year",
    height=650,
    size_max=100
)

# Plot the chart in Streamlit
st.plotly_chart(animation, use_container_width=True)
st.markdown(sub_title2, unsafe_allow_html=True)

import_sum_filtered_df = import_sum_df[import_sum_df['Reporting Economy'].isin(countries_of_interest)]
import_long_filtered_df = import_sum_filtered_df.melt(id_vars=["Reporting Economy", "Product/Sector"],
                                                      var_name="Year", value_name="ImportValue")
import_long_filtered_df["Year"] = import_long_filtered_df["Year"].astype(int)

# Apply the same color shades for consistency
import_long_filtered_df['CustomColor'] = import_long_filtered_df.apply(
    lambda row: color_shades[(row['Reporting Economy'], row['Product/Sector'])], axis=1)

# Apply the sector descriptions
import_long_filtered_df['SectorDescription'] = import_long_filtered_df['Product/Sector'].map(sector_descriptions)

# Apply logarithm to the 'ImportValue' for the visualization on the y-axis
import_long_filtered_df['LogImportValue'] = np.log(import_long_filtered_df['ImportValue'])

#animation_title2 = '<p style="font-family:Arial Bold; color:black; font-size: 30px;">Five major economies Imports by sector over time</p>'
sub_title12 = '<p style="font-family:Arial Bold Italic; color:black; font-size: 20px;">Importation is useful to understand if a country has the related sector goods inside their countries or not. The value are in Million USD</p>'
sub_title22 = '<p style="text-align: right; font-family: Arial Bold Italic; color: black; font-size: 15px;">Source: https://stats.wto.org/</p>'

#st.markdown(animation_title2, unsafe_allow_html=True)
st.markdown(sub_title12, unsafe_allow_html=True)
st.write('The fluctuation of merchandise import value by basic industrial and raw material products in United States of America, Germany, France and Japan from 2005 to 2022. According to WTO technical notes, basic industrial and raw material products include fuels and mining products, iron and steel, chemicals and pharmaceuticals. In the processing of reindustrialization, they are necessary to improve innovation and production efficiency to achieve green transformation and upgrading of industries.')

# Line chart visualization for the imports data
import_animation = px.line(
    data_frame=import_long_filtered_df,
    x="Year",
    y="LogImportValue",
    color="Reporting Economy",
    line_dash="SectorDescription",  # Different dashes for sectors
    title="Log of World Imports by Sector Over Time for Five Major Economies",
    labels={"LogImportValue": "Log of Import Value", "ImportValue": "Import Value", "Year": "Year"},
    hover_name="Reporting Economy",
    hover_data={"ImportValue": ':,', "SectorDescription": True},
    markers=True,  # Add markers for each data point
    height=700,
)

# Add the import visualization to the Streamlit page after the export chart
st.plotly_chart(import_animation, use_container_width=True)
st.markdown(sub_title22, unsafe_allow_html=True)

# Third part - Visualization
# Load data
bubble_data = pd.read_excel("percent_foreign_trade_dependency.xlsx", sheet_name=0, header=0)
years = sorted(bubble_data['Year'].unique(), reverse=True)

# Function to create the chart
def create_chart(economy, year_range):
    chart = alt.Chart(bubble_data).mark_point(opacity=0.5).encode(
        x='EX_Dependency:Q',
        y='IM_Dependency:Q',
        color=alt.Color('Year', scale=alt.Scale(domain=years, reverse=True)),
        tooltip=[
            alt.Tooltip('Reporting Economy:N'),
            alt.Tooltip('Product/Sector:N'),
            alt.Tooltip('Year'),
            alt.Tooltip('EX_Dependency:Q'),
            alt.Tooltip('IM_Dependency:Q')
        ],
        shape='Product/Sector:N'
    ).transform_filter(
        (alt.datum['Reporting Economy'] == economy) &
        (alt.datum['Year'] >= year_range[0]) &
        (alt.datum['Year'] <= year_range[1])
    ).properties(
        width=800,
        height=600
    ).interactive()

    return chart

st.write('Many developed countries have experienced a clear process of deindustrialization and have introduced many policies to promote reindustrialization. After 2005, international trade has undergone drastic changes. The reindustrialization process of developed countries is interrupted and driven by many events like global crisis, regional cooperation, local conflict and tariff policy. ')

# Set up the Streamlit interface
# st.title('International Trade Dependency ')

st.markdown("""
<p style='font-size: 12px'>
Overall economic growth can boost both imports and exports. To eliminate the impact of absolute value changes and better observe shifts in the proportions of imports and exports, the trade dependency ratio has been calculated.</p>
""", unsafe_allow_html=True)

sub_title111 = '<p style="font-family:Arial Bold Italic; color:black; font-size: 20px;">A Tale of Two Continents: USA Progress vs European Struggles</p>'
st.markdown(sub_title111, unsafe_allow_html=True)

year_range = st.slider(
    'Select Year Range',
    int(bubble_data['Year'].min()),
    int(bubble_data['Year'].max()),
    (int(bubble_data['Year'].min()), int(bubble_data['Year'].max()))
)

# Interaction widgets
selected_economy = st.selectbox(
    'Select Reporting Economy',
    options=bubble_data['Reporting Economy'].unique(),
    index=list(bubble_data['Reporting Economy'].unique()).index('United States of America')
)

st.write('It shows that the reindustrialization of the United States has achieved a phased success, that is, while the international competitiveness of high-tech products has continued to improve, its dependence on primary industrial products and light industrial products has been reduced in a high extent.')

# Update chart based on user input
resulting_chart = create_chart(selected_economy, year_range)
st.altair_chart(resulting_chart)
st.markdown(sub_title22, unsafe_allow_html=True)

st.write("In the journey of reindustrialization, the United States has consistently made stable progress, achieving notable milestones. In contrast, Europe's path towards reindustrialization has encountered significant challenges, including high energy prices, geopolitical crises, and protective policies from allies. These hurdles have so far prevented Europe from making substantial advancements, highlighting the divergent outcomes in the global industrial landscape.")

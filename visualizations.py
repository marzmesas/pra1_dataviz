import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st


def rental_properties_pie_chart(df, year):
    apt_yearly = df.groupby(['year','Type'])['Type'].count().to_frame().rename(columns={'Type':'count'}).reset_index()
    # Filter data for the given year
    yearly = apt_yearly[apt_yearly['year'] == year]

    # Check if data is available for the given year
    if yearly.empty:
        st.write(f"No data available for the year {year}")
        return

    # Create the Plotly pie chart
    fig = go.Figure(data=[go.Pie(
        values=yearly['count'],
        labels=yearly['Type'],
        rotation=90,
        hole=0.3,
    )])

    # Customize the layout
    fig.update_layout(
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='Arial, sans-serif',  # Modern font family
            size=14,
            color='#ffffff'  # Dark grey text color
        ),
        margin=dict(l=60, r=10, t=10, b=0),  # Adjust margins
        annotations=[dict(
            text=f'{year}',
            x=0.5,
            y=0.5,
            font_size=20,
            showarrow=False
        )]
    )

    # Show the plot using Streamlit
    st.plotly_chart(fig, use_container_width=True)

def room_vs_rent(df):
    # Calculate average rent per room type
    room_type_rent = df.groupby('Type')['Rent'].mean().sort_values(ascending=True).reset_index()

    # Create the Plotly horizontal bar chart
    fig = px.bar(room_type_rent, y='Type', x='Rent', 
                 orientation='h',  # Horizontal orientation
                 title='Tipo de Alojamiento vs Precio del Alquiler',
                 labels={'Type': 'Tipo de Alojamiento', 'Rent': 'Precio medio del Alquiler'},
                 color='Rent',
                 color_continuous_scale='rainbow')  # More modern color scale

    # Customize the layout
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='Arial, sans-serif',  # Modern font family
            size=15,
            color='#ffffff'  # Dark grey text color
        ),
        title={
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        height=600,
        xaxis=dict(showgrid=False),
        yaxis=dict(
            title='Tipo de Alojamiento',
            showgrid=False
        )
    )

    # Add annotations for the bars
    for idx, row in room_type_rent.iterrows():
        fig.add_annotation(
            x=row['Rent'],  # Position based on Rent value
            y=row['Type'],
            text=f"{row['Rent']:,.2f}",
            showarrow=False,
            font=dict(size=12, color='white')
        )

    # Show the plot
    st.plotly_chart(fig, use_container_width=True)

def top_n_locations(df, n_loc):
    # Calculate average rent per location
    locations_rent = df.groupby('Location')['Rent_per_sqft'].mean().sort_values(ascending=False).head(n_loc).reset_index()

    # Create the Plotly barplot
    fig = px.bar(locations_rent, x='Location', y='Rent_per_sqft', 
                title=f'Top {n_loc} ubicaciones más caras en relación a superficie alquilada',
                labels={'Location': 'Ubicación', 'Rent_per_sqft': 'Alquiler por sqft'},
                color='Rent_per_sqft',
                color_continuous_scale='tealrose')  # Updated color scale

    # Customize the layout
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='Arial, sans-serif',  # Modern font family
            size=14,
            color='#ffffff'  # Dark grey text color
        ),
        title={
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        height=600,  # Adjusting the height
        margin=dict(l=50, r=50, t=100, b=50),  # Add margins for better spacing
        yaxis = dict(showgrid=False)
    )

    # Add annotations for the bars
    for idx, row in locations_rent.iterrows():
        y_offset = row['Rent_per_sqft'] * 0.1  # Adjust the factor for spacing
        fig.add_annotation(
            x=row['Location'],
            y=row['Rent_per_sqft'] + y_offset,
            text=f"{row['Rent_per_sqft']:,.2f}",
            showarrow=False,
            font=dict(size=12, color='white')
        )

    # Rotate x-axis labels for better readability
    fig.update_xaxes(tickangle=45)

    # Show the plot using st.plotly_chart centered
    st.plotly_chart(fig, use_container_width=True)

def city_area_rent_graph(df):
    # Calculate average area and rent per city
    city_area_rent = df.groupby('City').agg({'Area_in_sqft': 'mean', 'Rent': 'mean'}).reset_index()

    # Create the Plotly barplot for Rent
    fig2 = px.bar(city_area_rent, x='City', y='Rent', 
                  title='Alquiler medio por ciudad',
                  labels={'City': 'Ciudad', 'Rent': 'Alquiler medio'},
                  color='Rent',
                  color_continuous_scale='algae')

    # Customize the layout for the second plot
    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='Arial, sans-serif',  # Modern font family
            size=14,
            color='#ffffff'  # Dark grey text color
        ),
        title={
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        yaxis=dict(range=[0, 250000], showgrid=False)
    )
    for idx, row in city_area_rent.iterrows():
        y_offset = row['Rent'] * 0.1  # Adjust the factor for spacing
        fig2.add_annotation(
            x=row['City'],
            y=row['Rent'] + y_offset,
            text=f"{row['Rent']:,.2f}",
            showarrow=False,
            font=dict(size=12, color='white')
        )


    st.plotly_chart(fig2, use_container_width=True)

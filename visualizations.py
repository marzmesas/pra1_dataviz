import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st


def rental_properties_pie_chart(df, year):
    apt_yearly = df.groupby(['year','Type'])['Type'].count().to_frame().rename(columns={'Type':'count'}).reset_index()

    yearly = apt_yearly[apt_yearly['year'] == year]

    if yearly.empty:
        st.write(f"No data available for the year {year}")
        return

    fig = go.Figure(data=[go.Pie(
        values=yearly['count'],
        labels=yearly['Type'],
        rotation=90,
        hole=0.3,
    )])

    fig.update_layout(
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='Arial, sans-serif',  
            size=14,
            color='#ffffff'
        ),
        margin=dict(l=60, r=10, t=10, b=0),
        annotations=[dict(
            text=f'{year}',
            x=0.5,
            y=0.5,
            font_size=20,
            showarrow=False
        )]
    )

    st.plotly_chart(fig, use_container_width=True)

def room_vs_rent(df):

    room_type_rent = df.groupby('Type')['Rent'].mean().sort_values(ascending=True).reset_index()

    fig = px.bar(room_type_rent, y='Type', x='Rent', 
                 orientation='h',
                 title='Tipo de Alojamiento vs Precio del Alquiler',
                 labels={'Type': 'Tipo de Alojamiento', 'Rent': 'Precio medio del Alquiler'},
                 color='Rent',
                 color_continuous_scale='rainbow')


    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='Arial, sans-serif',
            size=15,
            color='#ffffff' 
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

    for idx, row in room_type_rent.iterrows():
        fig.add_annotation(
            x=row['Rent'],
            y=row['Type'],
            text=f"{row['Rent']:,.2f}",
            showarrow=False,
            font=dict(size=12, color='white')
        )

    st.plotly_chart(fig, use_container_width=True)

def top_n_locations(df, n_loc):
    locations_rent = df.groupby('Location')['Rent_per_sqft'].mean().sort_values(ascending=False).head(n_loc).reset_index()

    fig = px.bar(locations_rent, x='Location', y='Rent_per_sqft', 
                title=f'Top {n_loc} ubicaciones más caras en relación a superficie alquilada',
                labels={'Location': 'Ubicación', 'Rent_per_sqft': 'Alquiler por sqft'},
                color='Rent_per_sqft',
                color_continuous_scale='tealrose')

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='Arial, sans-serif',
            size=14,
            color='#ffffff'
        ),
        title={
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        height=600,
        margin=dict(l=50, r=50, t=100, b=50),
        yaxis = dict(showgrid=False)
    )

    for idx, row in locations_rent.iterrows():
        y_offset = row['Rent_per_sqft'] * 0.1
        fig.add_annotation(
            x=row['Location'],
            y=row['Rent_per_sqft'] + y_offset,
            text=f"{row['Rent_per_sqft']:,.2f}",
            showarrow=False,
            font=dict(size=12, color='white')
        )


    fig.update_xaxes(tickangle=45)


    st.plotly_chart(fig, use_container_width=True)

def city_area_rent_graph(df):

    city_area_rent = df.groupby('City').agg({'Area_in_sqft': 'mean', 'Rent': 'mean'}).reset_index()

    fig2 = px.bar(city_area_rent, x='City', y='Rent', 
                  title='Alquiler medio por ciudad',
                  labels={'City': 'Ciudad', 'Rent': 'Alquiler medio'},
                  color='Rent',
                  color_continuous_scale='algae')

    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='Arial, sans-serif',
            size=14,
            color='#ffffff'
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
        y_offset = row['Rent'] * 0.1 
        fig2.add_annotation(
            x=row['City'],
            y=row['Rent'] + y_offset,
            text=f"{row['Rent']:,.2f}",
            showarrow=False,
            font=dict(size=12, color='white')
        )


    st.plotly_chart(fig2, use_container_width=True)

import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import visualizations
from streamlit_option_menu import option_menu
from utils import open_page


# Define the main function for Streamlit app
def main():
    
    st.set_page_config(page_title='Data Visualization App', layout='wide', initial_sidebar_state='collapsed')


    with st.sidebar:
        selection = option_menu(
            menu_title="App Menu",  # required
            options=["Home", "Graphs"],  # required
            icons=["house", "bar-chart"],  # optional
            default_index=0,  # optional
        )
    alt.themes.enable("dark")

    if selection == 'Graphs':
        df= pd.read_csv('dubai_properties.csv')

        #Drop some useless columns identified in EDA
        columns_to_drop = ['Address','Frequency','Purpose','Latitude','Longitude']
        df = df.drop(columns_to_drop,axis=1)

        #EDA operations
        df['Posted_date'] = df['Posted_date'].astype('datetime64[ns]')
        df['year'] = df['Posted_date'].dt.year

        # Title and selection bar
        st.title('Selecciona tu punto de interés')
        st.markdown(
            """
            <style>
            .main {
                background-image: url("https://img.freepik.com/free-vector/gradient-grainy-texture_23-2148976750.jpg");
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        graph_type = st.selectbox('Áreas de información', ['','Ubicaciones más caras en relación a su superficie', 
                                                    'Precio medio por tipo de alojamiento',
                                                    'Tipos de propiedades a lo largo de los años', 
                                                    'Comparativa entre ciudades'])

        # Depending on the selection, call the corresponding function
        if graph_type == 'Ubicaciones más caras en relación a su superficie':
            n_loc = st.number_input('Enter number of locations', min_value=1, max_value=15, value=5, step=1)
            visualizations.top_n_locations(df, n_loc)
        if graph_type == 'Precio medio por tipo de alojamiento':
            visualizations.room_vs_rent(df)
        if graph_type == 'Tipos de propiedades a lo largo de los años':
            year = st.number_input('Enter your desired year', min_value=df['year'].unique().min(), max_value=df['year'].unique().max(), value=df['year'].unique().min(), step=1)
            visualizations.rental_properties_pie_chart(df,year)
        if graph_type == 'Comparativa entre ciudades':
            visualizations.city_area_rent_graph(df)
        else:
            pass

    else:
        st.markdown("""
            <style>
                h3 {
                    text-align: top;
                    color: white;
                    font-family: Courier;
                    font-weight: lighter;
                }
            </style>
        """, unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: white;'> Mercado Inmobiliario en UAE</h1>", unsafe_allow_html=True)

        st.markdown("<h3 style='text-align: center; color: white;'>El objetivo de esta aplicación es entregar \
                    al usuario una pincelada informativa acerca de los datos extraídos del dataset aceca del mercado inmobiliario en UAE.\
                    Asimismo se busca entregar una experiencia de usuario sencilla y directa a través de menús y diversos tipos de gráficos interactivos. \
                    </h3>", unsafe_allow_html=True)
        # Add background image
        st.markdown(
            """
            <style>
            .main {
                background-image: url("https://dynamic-media-cdn.tripadvisor.com/media/photo-o/24/c8/5b/c4/caption.jpg?w=1100&h=-1&s=1&cx=515&cy=290&chk=v1_d5a1d528484c0818588b");
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        dataset_url='https://www.kaggle.com/code/animeshshedge/data-visualization-uae-real-estate'
        st.button('Dataset Original', on_click=open_page, args=(dataset_url,))

if __name__ == '__main__':
    main()
    
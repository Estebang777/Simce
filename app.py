import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt

# ----------- Logo y créditos -----------
st.image("https://campusvirtual.academia.cl/pluginfile.php/265/block_html/content/logo-web-bottom.png",
         
         width=200)
st.markdown("<h3 style='text-align: left;'>SIMCE Comparador</h3>", unsafe_allow_html=True)
st.markdown("""
    <style>
    .credits {
        position: fixed;
        bottom: 10px;
        right: 20px;
        color: #888;
        font-size: 16px;
        background-color: rgba(255,255,255,0.7);
        padding: 4px 12px;
        border-radius: 12px;
        z-index: 9999;
    }
    </style>
    <div class="credits">
        Creado por Esteban Gonzalez, Joaquin Riveros Y Rodny Araujo
    </div>
    """, unsafe_allow_html=True)

# ----------- Cargar datos --------------
simce = pd.read_csv('simce.csv', encoding='latin-1')

# ----------- Sidebar filtros -----------
st.sidebar.title("Filtros SIMCE")

regiones_mostrar = [
    "tarapacá",
    "maule",
    "la araucanía",
    "aysén del general carlos ibáñez del campo",
    "magallanes y de la antártica chilena",
    "metropolitana"
]

simce['region'] = simce['region'].str.lower()
regiones = [r for r in simce['region'].unique() if r in regiones_mostrar]
region_sel = st.sidebar.selectbox('Región', regiones)

provincias = simce[simce['region'] == region_sel]['provincia'].unique()
prov_sel = st.sidebar.selectbox('Provincia', provincias)

comunas = simce[(simce['region'] == region_sel) & (simce['provincia'] == prov_sel)]['comuna'].unique()
comuna_sel = st.sidebar.selectbox('Comuna', comunas)

asignatura = st.sidebar.radio('Asignatura', ['Lenguaje', 'Matemáticas'])

# ----------- Contenido central ---------
st.write(f"**Región seleccionada:** {region_sel.title()}")
st.write(f"**Provincia seleccionada:** {prov_sel}")
st.write(f"**Comuna seleccionada:** {comuna_sel}")
st.write(f"**Asignatura seleccionada:** {asignatura}")

datos_filtrados = simce[
    (simce['region'] == region_sel) &
    (simce['provincia'] == prov_sel) &
    (simce['comuna'] == comuna_sel)
]

if asignatura == 'Lenguaje':
    columna_puntaje = 'lenguaje'
else:
    columna_puntaje = 'matematicas'

if not datos_filtrados.empty:
    df_comuna = datos_filtrados.groupby('agno')[columna_puntaje].mean().reset_index()
    df_comuna['tipo'] = 'Comuna'

    df_nacional = simce.groupby('agno')[columna_puntaje].mean().reset_index()
    df_nacional['tipo'] = 'Nacional'

    df_grafico = pd.concat([df_comuna, df_nacional])

    # --- Gráfico Matplotlib ---
    fig, ax = plt.subplots()
    for tipo, grupo in df_grafico.groupby('tipo'):
        ax.plot(grupo['agno'], grupo[columna_puntaje], marker='o', label=tipo)

    ax.set_title(f'Evolución Puntaje SIMCE en {asignatura} - {comuna_sel.title()} vs Nacional')
    ax.set_xlabel('Año')
    ax.set_ylabel('Puntaje Promedio')
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

 # --- Métricas del mayor y menor puntaje de Lenguaje y Matemáticas en la región ---
    datos_region = simce[simce['region'] == region_sel]

    # Mayor puntaje de Lenguaje
    max_lenguaje_row = datos_region.loc[datos_region['lenguaje'].idxmax()]
    max_lenguaje = max_lenguaje_row['lenguaje']
    max_lenguaje_comuna = max_lenguaje_row['comuna']
    max_lenguaje_agno = int(max_lenguaje_row['agno'])

    # Menor puntaje de Lenguaje
    min_lenguaje_row = datos_region.loc[datos_region['lenguaje'].idxmin()]
    min_lenguaje = min_lenguaje_row['lenguaje']
    min_lenguaje_comuna = min_lenguaje_row['comuna']
    min_lenguaje_agno = int(min_lenguaje_row['agno'])

    # Mayor puntaje de Matemáticas
    max_mate_row = datos_region.loc[datos_region['matematicas'].idxmax()]
    max_mate = max_mate_row['matematicas']
    max_mate_comuna = max_mate_row['comuna']
    max_mate_agno = int(max_mate_row['agno'])

    # Menor puntaje de Matemáticas
    min_mate_row = datos_region.loc[datos_region['matematicas'].idxmin()]
    min_mate = min_mate_row['matematicas']
    min_mate_comuna = min_mate_row['comuna']
    min_mate_agno = int(min_mate_row['agno'])

    st.markdown("---")
    st.subheader("🏆 Mayores y Menores Puntajes Regionales por Asignatura")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
         st.metric(
            label=f"MAX LENGUAJE | {max_lenguaje_comuna.title()} | {max_lenguaje_agno}",
            value=f"{max_lenguaje:.1f}",
            delta=(max_lenguaje_comuna)
         )
    with col2:
         st.metric(
            label=f"MIN LENGUAJE | {min_lenguaje_comuna.title()} | {min_lenguaje_agno}",
            value=f"{min_lenguaje:.1f}",
            delta=(min_lenguaje_comuna)
        )
    with col3:
        st.metric(
            label=f"MAX MATEMÁTICAS | {max_mate_comuna.title()} | {max_mate_agno}",
            value=f"{max_mate:.1f}",
            delta=(max_mate_comuna)
        )
    with col4:
        st.metric(
            label=f"MIN MATEMÁTICAS | {min_mate_comuna.title()} | {min_mate_agno}",
            value=f"{min_mate:.1f}",
            delta=(min_mate_comuna)
        )
    
else:
    st.warning("No hay datos para los filtros seleccionados.")

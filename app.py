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
        Creado por Esteban Gonzalez y Joaquin Riveros
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

  # ----------- Métricas Regionales y Nacionales (debajo del gráfico) -----------
    datos_region = simce[simce['region'] == region_sel]

    # Último año disponible en la región
    if not datos_region.empty:
        ultimo_anio_region = datos_region['agno'].max()
        df_region_ultimo = datos_region[datos_region['agno'] == ultimo_anio_region]
        prom_regional = df_region_ultimo[columna_puntaje].mean()
        max_regional = df_region_ultimo[columna_puntaje].max()
        min_regional = df_region_ultimo[columna_puntaje].min()
    else:
        ultimo_anio_region = None
        prom_regional = None
        max_regional = None
        min_regional = None

    # Promedio nacional para ese año y asignatura
    prom_nacional = simce[simce['agno'] == ultimo_anio_region][columna_puntaje].mean() if ultimo_anio_region else None

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label=f"Promedio Regional ({ultimo_anio_region if ultimo_anio_region else '-'})",
            value=f"{prom_regional:.1f}" if prom_regional is not None else "N/A"
        )
    with col2:
        st.metric(
            label=f"Promedio Nacional ({ultimo_anio_region if ultimo_anio_region else '-'})",
            value=f"{prom_nacional:.1f}" if prom_nacional is not None else "N/A"
        )
    with col3:
        st.metric(
            label=f"Máximo Puntaje Región ({ultimo_anio_region if ultimo_anio_region else '-'})",
            value=f"{max_regional:.1f}" if max_regional is not None else "N/A"
        )
    with col4:
        st.metric(
            label=f"Mínimo Puntaje Región ({ultimo_anio_region if ultimo_anio_region else '-'})",
            value=f"{min_regional:.1f}" if min_regional is not None else "N/A"
        )
    st.caption("📊 Métricas regionales y nacionales para el año más reciente seleccionado.")
    
else:
    st.warning("No hay datos para los filtros seleccionados.")

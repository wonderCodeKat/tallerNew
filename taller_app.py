import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import uuid
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(
    page_title="AutoTaller Pro",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejorar la apariencia
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .service-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .success-msg {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-msg {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .sidebar .stSelectbox > div > div {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# Inicialización de datos en session_state
def init_session_state():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'clientes' not in st.session_state:
        st.session_state.clientes = pd.DataFrame({
            'id': ['CLI001', 'CLI002'],
            'nombre': ['Juan Pérez', 'María García'],
            'telefono': ['123456789', '987654321'],
            'email': ['juan@email.com', 'maria@email.com'],
            'fecha_registro': [datetime.now().strftime('%Y-%m-%d')] * 2
        })
    
    if 'vehiculos' not in st.session_state:
        st.session_state.vehiculos = pd.DataFrame({
            'id': ['VEH001', 'VEH002'],
            'cliente_id': ['CLI001', 'CLI002'],
            'marca': ['Toyota', 'Honda'],
            'modelo': ['Corolla', 'Civic'],
            'año': [2020, 2019],
            'placa': ['ABC123', 'XYZ789']
        })
    
    if 'citas' not in st.session_state:
        st.session_state.citas = pd.DataFrame({
            'id': ['CIT001', 'CIT002'],
            'cliente_id': ['CLI001', 'CLI002'],
            'vehiculo_id': ['VEH001', 'VEH002'],
            'servicio': ['Cambio de aceite', 'Revisión general'],
            'fecha': [(datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
                     (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')],
            'hora': ['10:00', '14:00'],
            'estado': ['Confirmada', 'Pendiente'],
            'precio': [50000, 120000]
        })
    
    if 'inventario' not in st.session_state:
        st.session_state.inventario = pd.DataFrame({
            'id': ['INV001', 'INV002', 'INV003', 'INV004'],
            'item': ['Aceite motor 5W-30', 'Filtro aire', 'Pastillas freno', 'Bujías'],
            'stock': [25, 15, 8, 30],
            'stock_minimo': [10, 10, 5, 20],
            'precio': [25000, 35000, 80000, 15000],
            'proveedor': ['Lubricantes S.A.', 'Filtros Pro', 'Frenos Total', 'Bujías Max']
        })
    
    if 'servicios' not in st.session_state:
        st.session_state.servicios = [
            {'nombre': 'Cambio de aceite', 'precio': 50000, 'duracion': '30 min'},
            {'nombre': 'Revisión general', 'precio': 120000, 'duracion': '2 horas'},
            {'nombre': 'Alineación y balanceo', 'precio': 80000, 'duracion': '1 hora'},
            {'nombre': 'Cambio de frenos', 'precio': 150000, 'duracion': '1.5 horas'},
            {'nombre': 'Diagnóstico computarizado', 'precio': 70000, 'duracion': '45 min'},
            {'nombre': 'Cambio de filtros', 'precio': 60000, 'duracion': '45 min'}
        ]

init_session_state()

# Funciones de autenticación
def login():
    st.title("🔐 Acceso Administrativo")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        
        if st.button("Iniciar Sesión"):
            if username == "admin" and password == "admin123":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Credenciales incorrectas")

# Función para generar ID únicos
def generate_id(prefix):
    return f"{prefix}{str(uuid.uuid4())[:6].upper()}"

# Pantalla de inicio
def pantalla_inicio():
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🔧 AutoTaller Pro</h1>
        <h3>Tu taller de confianza desde 1995</h3>
        <p>Especialistas en mantenimiento y reparación automotriz</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Información principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 📍 Información del Taller")
        
        # Horarios
        st.markdown("### 🕒 Horarios de Atención")
        st.info("""
        **Lunes a Viernes:** 8:00 AM - 6:00 PM  
        **Sábados:** 8:00 AM - 2:00 PM  
        **Domingos:** Cerrado  
        """)
        
        # Ubicación
        st.markdown("### 📍 Ubicación")
        st.success("""
        **Dirección:** Av. Principal 123, San Isidro, Lima  
        **Teléfono:** (01) 234-5678  
        **Email:** contacto@autotaller.com  
        """)
        
        # Mapa (simulado con iframe de Google Maps)
        st.markdown("### 🗺️ Ubicación en el Mapa")
        st.markdown("""
        <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3901.3119!2d-77.0428!3d-12.0464!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMTLCsDAyJzQ3LjAiUyA3N8KwMDInMzQuMSJX!5e0!3m2!1ses!2spe!4v1"
        width="100%" height="300" style="border:0;" allowfullscreen="" loading="lazy">
        </iframe>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("## 🛠️ Nuestros Servicios")
        
        for servicio in st.session_state.servicios[:4]:
            st.markdown(f"""
            <div class="service-card">
                <h4>{servicio['nombre']}</h4>
                <p><strong>Precio:</strong> ${servicio['precio']:,}</p>
                <p><strong>Duración:</strong> {servicio['duracion']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Botón para agendar cita
        if st.button("📅 Agendar Cita", type="primary"):
            st.session_state.page = "citas"
            st.rerun()
        
        # Estadísticas rápidas
        st.markdown("## 📊 Estadísticas")
        
        total_citas = len(st.session_state.citas)
        citas_hoy = len(st.session_state.citas[
            st.session_state.citas['fecha'] == datetime.now().strftime('%Y-%m-%d')
        ])
        
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric("Total Citas", total_citas)
        with col_stat2:
            st.metric("Citas Hoy", citas_hoy)

# Módulo de citas
def modulo_citas():
    st.title("📅 Gestión de Citas")
    
    tabs = st.tabs(["Agendar Cita", "Mis Citas", "Buscar Cliente"])
    
    with tabs[0]:
        st.markdown("### Agendar Nueva Cita")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Datos del cliente
            st.markdown("#### Información del Cliente")
            cliente_nuevo = st.checkbox("¿Cliente nuevo?")
            
            if cliente_nuevo:
                nombre = st.text_input("Nombre completo")
                telefono = st.text_input("Teléfono")
                email = st.text_input("Email")
            else:
                clientes_list = st.session_state.clientes['nombre'].tolist()
                cliente_seleccionado = st.selectbox("Seleccionar cliente", clientes_list)
                cliente_data = st.session_state.clientes[
                    st.session_state.clientes['nombre'] == cliente_seleccionado
                ].iloc[0]
        
        with col2:
            # Datos del vehículo
            st.markdown("#### Información del Vehículo")
            if cliente_nuevo:
                marca = st.text_input("Marca")
                modelo = st.text_input("Modelo")
                año = st.number_input("Año", min_value=1990, max_value=2024, value=2020)
                placa = st.text_input("Placa")
            else:
                vehiculos_cliente = st.session_state.vehiculos[
                    st.session_state.vehiculos['cliente_id'] == cliente_data['id']
                ]
                if len(vehiculos_cliente) > 0:
                    vehiculo_info = vehiculos_cliente.iloc[0]
                    st.text_input("Marca", value=vehiculo_info['marca'], disabled=True)
                    st.text_input("Modelo", value=vehiculo_info['modelo'], disabled=True)
                    st.text_input("Año", value=str(vehiculo_info['año']), disabled=True)
                    st.text_input("Placa", value=vehiculo_info['placa'], disabled=True)
        
        # Detalles de la cita
        col3, col4 = st.columns(2)
        
        with col3:
            servicios_nombres = [s['nombre'] for s in st.session_state.servicios]
            servicio_seleccionado = st.selectbox("Servicio", servicios_nombres)
            servicio_data = next(s for s in st.session_state.servicios if s['nombre'] == servicio_seleccionado)
            
            fecha_cita = st.date_input("Fecha de la cita", 
                                     min_value=datetime.now().date())
        
        with col4:
            horarios = ["08:00", "09:00", "10:00", "11:00", "14:00", "15:00", "16:00", "17:00"]
            hora_cita = st.selectbox("Hora", horarios)
            
            st.markdown(f"**Precio estimado:** ${servicio_data['precio']:,}")
            st.markdown(f"**Duración:** {servicio_data['duracion']}")
        
        # Botón para agendar
        if st.button("Confirmar Cita", type="primary"):
            if cliente_nuevo:
                # Crear nuevo cliente
                nuevo_cliente_id = generate_id("CLI")
                nuevo_cliente = pd.DataFrame({
                    'id': [nuevo_cliente_id],
                    'nombre': [nombre],
                    'telefono': [telefono],
                    'email': [email],
                    'fecha_registro': [datetime.now().strftime('%Y-%m-%d')]
                })
                st.session_state.clientes = pd.concat([st.session_state.clientes, nuevo_cliente], 
                                                    ignore_index=True)
                
                # Crear nuevo vehículo
                nuevo_vehiculo_id = generate_id("VEH")
                nuevo_vehiculo = pd.DataFrame({
                    'id': [nuevo_vehiculo_id],
                    'cliente_id': [nuevo_cliente_id],
                    'marca': [marca],
                    'modelo': [modelo],
                    'año': [año],
                    'placa': [placa]
                })
                st.session_state.vehiculos = pd.concat([st.session_state.vehiculos, nuevo_vehiculo], 
                                                     ignore_index=True)
                
                cliente_id_cita = nuevo_cliente_id
                vehiculo_id_cita = nuevo_vehiculo_id
            else:
                cliente_id_cita = cliente_data['id']
                vehiculo_id_cita = vehiculos_cliente.iloc[0]['id']
            
            # Crear nueva cita
            nueva_cita_id = generate_id("CIT")
            nueva_cita = pd.DataFrame({
                'id': [nueva_cita_id],
                'cliente_id': [cliente_id_cita],
                'vehiculo_id': [vehiculo_id_cita],
                'servicio': [servicio_seleccionado],
                'fecha': [fecha_cita.strftime('%Y-%m-%d')],
                'hora': [hora_cita],
                'estado': ['Confirmada'],
                'precio': [servicio_data['precio']]
            })
            
            st.session_state.citas = pd.concat([st.session_state.citas, nueva_cita], 
                                             ignore_index=True)
            
            st.markdown(f"""
            <div class="success-msg">
                ✅ <strong>¡Cita agendada exitosamente!</strong><br>
                <strong>ID de cita:</strong> {nueva_cita_id}<br>
                <strong>Fecha:</strong> {fecha_cita.strftime('%d/%m/%Y')} a las {hora_cita}<br>
                <strong>Servicio:</strong> {servicio_seleccionado}
            </div>
            """, unsafe_allow_html=True)
    
    with tabs[1]:
        st.markdown("### Lista de Citas")
        
        # Filtros
        col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
        
        with col_filtro1:
            filtro_fecha = st.date_input("Filtrar por fecha", value=None)
        with col_filtro2:
            estados = ['Todas', 'Confirmada', 'Pendiente', 'Completada', 'Cancelada']
            filtro_estado = st.selectbox("Filtrar por estado", estados)
        with col_filtro3:
            if st.button("Limpiar filtros"):
                filtro_fecha = None
                filtro_estado = 'Todas'
        
        # Aplicar filtros
        citas_filtradas = st.session_state.citas.copy()
        
        if filtro_fecha:
            citas_filtradas = citas_filtradas[
                citas_filtradas['fecha'] == filtro_fecha.strftime('%Y-%m-%d')
            ]
        
        if filtro_estado != 'Todas':
            citas_filtradas = citas_filtradas[
                citas_filtradas['estado'] == filtro_estado
            ]
        
        # Mostrar citas
        if len(citas_filtradas) > 0:
            for _, cita in citas_filtradas.iterrows():
                cliente_info = st.session_state.clientes[
                    st.session_state.clientes['id'] == cita['cliente_id']
                ].iloc[0]
                
                vehiculo_info = st.session_state.vehiculos[
                    st.session_state.vehiculos['id'] == cita['vehiculo_id']
                ].iloc[0]
                
                col_cita1, col_cita2, col_cita3 = st.columns([2, 1, 1])
                
                with col_cita1:
                    st.markdown(f"""
                    **Cliente:** {cliente_info['nombre']}  
                    **Vehículo:** {vehiculo_info['marca']} {vehiculo_info['modelo']} ({vehiculo_info['placa']})  
                    **Servicio:** {cita['servicio']}  
                    **Fecha:** {cita['fecha']} - {cita['hora']}  
                    **Estado:** {cita['estado']}  
                    **Precio:** ${cita['precio']:,}
                    """)
                
                with col_cita2:
                    if st.button(f"Cancelar", key=f"cancel_{cita['id']}"):
                        st.session_state.citas.loc[
                            st.session_state.citas['id'] == cita['id'], 'estado'
                        ] = 'Cancelada'
                        st.rerun()
                
                with col_cita3:
                    if cita['estado'] == 'Confirmada':
                        if st.button(f"Completar", key=f"complete_{cita['id']}"):
                            st.session_state.citas.loc[
                                st.session_state.citas['id'] == cita['id'], 'estado'
                            ] = 'Completada'
                            st.rerun()
                
                st.divider()
        else:
            st.info("No hay citas que coincidan con los filtros seleccionados.")
    
    with tabs[2]:
        st.markdown("### Buscar Cliente")
        busqueda = st.text_input("Buscar por nombre, teléfono o email")
        
        if busqueda:
            clientes_encontrados = st.session_state.clientes[
                st.session_state.clientes['nombre'].str.contains(busqueda, case=False, na=False) |
                st.session_state.clientes['telefono'].str.contains(busqueda, case=False, na=False) |
                st.session_state.clientes['email'].str.contains(busqueda, case=False, na=False)
            ]
            
            if len(clientes_encontrados) > 0:
                st.dataframe(clientes_encontrados, use_container_width=True)
            else:
                st.warning("No se encontraron clientes.")

# Lista de servicios
def lista_servicios():
    st.title("🛠️ Servicios Disponibles")
    
    # Mostrar servicios en cards
    col1, col2 = st.columns(2)
    
    for i, servicio in enumerate(st.session_state.servicios):
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"""
            <div class="service-card">
                <h3>{servicio['nombre']}</h3>
                <p><strong>💰 Precio:</strong> ${servicio['precio']:,}</p>
                <p><strong>⏱️ Duración:</strong> {servicio['duracion']}</p>
            </div>
            """, unsafe_allow_html=True)

# Registro de clientes y vehículos
def registro_clientes():
    st.title("👥 Registro de Clientes y Vehículos")
    
    tabs = st.tabs(["Clientes", "Vehículos", "Nuevo Cliente"])
    
    with tabs[0]:
        st.markdown("### Lista de Clientes")
        st.dataframe(st.session_state.clientes, use_container_width=True)
    
    with tabs[1]:
        st.markdown("### Lista de Vehículos")
        # Combinar datos de vehículos con información del cliente
        vehiculos_con_cliente = st.session_state.vehiculos.merge(
            st.session_state.clientes[['id', 'nombre']], 
            left_on='cliente_id', 
            right_on='id', 
            suffixes=('', '_cliente')
        )
        vehiculos_con_cliente = vehiculos_con_cliente[
            ['id', 'nombre', 'marca', 'modelo', 'año', 'placa']
        ]
        vehiculos_con_cliente.columns = ['ID', 'Cliente', 'Marca', 'Modelo', 'Año', 'Placa']
        st.dataframe(vehiculos_con_cliente, use_container_width=True)
    
    with tabs[2]:
        st.markdown("### Registrar Nuevo Cliente")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Datos del Cliente")
            nombre = st.text_input("Nombre completo")
            telefono = st.text_input("Teléfono")
            email = st.text_input("Email")
        
        with col2:
            st.markdown("#### Datos del Vehículo")
            marca = st.text_input("Marca")
            modelo = st.text_input("Modelo")
            año = st.number_input("Año", min_value=1990, max_value=2024, value=2020)
            placa = st.text_input("Placa")
        
        if st.button("Registrar Cliente y Vehículo", type="primary"):
            if nombre and telefono and marca and modelo and placa:
                # Crear cliente
                nuevo_cliente_id = generate_id("CLI")
                nuevo_cliente = pd.DataFrame({
                    'id': [nuevo_cliente_id],
                    'nombre': [nombre],
                    'telefono': [telefono],
                    'email': [email],
                    'fecha_registro': [datetime.now().strftime('%Y-%m-%d')]
                })
                st.session_state.clientes = pd.concat([st.session_state.clientes, nuevo_cliente], 
                                                    ignore_index=True)
                
                # Crear vehículo
                nuevo_vehiculo_id = generate_id("VEH")
                nuevo_vehiculo = pd.DataFrame({
                    'id': [nuevo_vehiculo_id],
                    'cliente_id': [nuevo_cliente_id],
                    'marca': [marca],
                    'modelo': [modelo],
                    'año': [año],
                    'placa': [placa]
                })
                st.session_state.vehiculos = pd.concat([st.session_state.vehiculos, nuevo_vehiculo], 
                                                     ignore_index=True)
                
                st.success(f"✅ Cliente y vehículo registrados exitosamente. ID Cliente: {nuevo_cliente_id}")
            else:
                st.error("Por favor, complete todos los campos obligatorios.")

# Inventario
def inventario():
    st.title("📦 Gestión de Inventario")
    
    tabs = st.tabs(["Inventario Actual", "Agregar Item", "Stock Bajo"])
    
    with tabs[0]:
        st.markdown("### Inventario Actual")
        
        # Mostrar inventario con alertas de stock bajo
        inventario_display = st.session_state.inventario.copy()
        inventario_display['Estado'] = inventario_display.apply(
            lambda row: '🔴 Stock Bajo' if row['stock'] <= row['stock_minimo'] else '✅ OK', 
            axis=1
        )
        
        st.dataframe(inventario_display, use_container_width=True)
        
        # Gráfico de stock
        fig = px.bar(
            st.session_state.inventario, 
            x='item', 
            y='stock',
            title='Niveles de Stock por Item',
            color='stock',
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tabs[1]:
        st.markdown("### Agregar Nuevo Item")
        
        col1, col2 = st.columns(2)
        
        with col1:
            item_nombre = st.text_input("Nombre del item")
            stock_inicial = st.number_input("Stock inicial", min_value=0, value=0)
            stock_minimo = st.number_input("Stock mínimo", min_value=1, value=5)
        
        with col2:
            precio = st.number_input("Precio unitario", min_value=0.0, value=0.0, step=0.01)
            proveedor = st.text_input("Proveedor")
        
        if st.button("Agregar Item", type="primary"):
            if item_nombre and proveedor:
                nuevo_item_id = generate_id("INV")
                nuevo_item = pd.DataFrame({
                    'id': [nuevo_item_id],
                    'item': [item_nombre],
                    'stock': [stock_inicial],
                    'stock_minimo': [stock_minimo],
                    'precio': [precio],
                    'proveedor': [proveedor]
                })
                st.session_state.inventario = pd.concat([st.session_state.inventario, nuevo_item], 
                                                      ignore_index=True)
                st.success(f"✅ Item agregado exitosamente. ID: {nuevo_item_id}")
            else:
                st.error("Complete todos los campos.")
        
        st.markdown("### Actualizar Stock")
        
        if len(st.session_state.inventario) > 0:
            item_seleccionado = st.selectbox(
                "Seleccionar item", 
                st.session_state.inventario['item'].tolist()
            )
            
            item_actual = st.session_state.inventario[
                st.session_state.inventario['item'] == item_seleccionado
            ].iloc[0]
            
            col3, col4 = st.columns(2)
            
            with col3:
                st.info(f"Stock actual: {item_actual['stock']}")
                nuevo_stock = st.number_input("Nuevo stock", min_value=0, value=int(item_actual['stock']))
            
            with col4:
                if st.button("Actualizar Stock"):
                    st.session_state.inventario.loc[
                        st.session_state.inventario['item'] == item_seleccionado, 'stock'
                    ] = nuevo_stock
                    st.success("Stock actualizado exitosamente")
                    st.rerun()
    
    with tabs[2]:
        st.markdown("### Items con Stock Bajo")
        
        items_bajo_stock = st.session_state.inventario[
            st.session_state.inventario['stock'] <= st.session_state.inventario['stock_minimo']
        ]
        
        if len(items_bajo_stock) > 0:
            st.warning(f"⚠️ {len(items_bajo_stock)} items con stock bajo:")
            
            for _, item in items_bajo_stock.iterrows():
                st.markdown(f"""
                <div class="warning-msg">
                    <strong>{item['item']}</strong><br>
                    Stock actual: {item['stock']} | Stock mínimo: {item['stock_minimo']}<br>
                    Proveedor: {item['proveedor']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ Todos los items tienen stock suficiente")

# Panel administrativo
def panel_admin():
    if not st.session_state.authenticated:
        login()
        return
    
    st.title("⚙️ Panel Administrativo")
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_clientes = len(st.session_state.clientes)
        st.metric("👥 Total Clientes", total_clientes)
    
    with col2:
        total_citas = len(st.session_state.citas)
        st.metric("📅 Total Citas", total_citas)
    
    with col3:
        citas_hoy = len(st.session_state.citas[
            st.session_state.citas['fecha'] == datetime.now().strftime('%Y-%m-%d')
        ])
        st.metric("📅 Citas Hoy", citas_hoy)
    
    with col4:
        ingresos_mes = st.session_state.citas[
            st.session_state.citas['estado'] == 'Completada'
        ]['precio'].sum()
        st.metric("💰 Ingresos", f"${ingresos_mes:,}")
    
    st.divider()
    
    # Tabs del panel administrativo
    tabs = st.tabs(["📊 Dashboard", "📅 Calendario", "📋 Reportes", "⚙️ Configuración"])
    
    with tabs[0]:
        st.markdown("### Dashboard Principal")
        
        # Gráfico de citas por estado
        col_graph1, col_graph2 = st.columns(2)
        
        with col_graph1:
            citas_por_estado = st.session_state.citas['estado'].value_counts()
            fig_estados = px.pie(
                values=citas_por_estado.values,
                names=citas_por_estado.index,
                title="Distribución de Citas por Estado"
            )
            st.plotly_chart(fig_estados, use_container_width=True)
        
        with col_graph2:
            # Ingresos por servicio
            ingresos_servicio = st.session_state.citas.groupby('servicio')['precio'].sum().sort_values(ascending=False)
            fig_ingresos = px.bar(
                x=ingresos_servicio.values,
                y=ingresos_servicio.index,
                orientation='h',
                title="Ingresos por Tipo de Servicio",
                labels={'x': 'Ingresos ($)', 'y': 'Servicio'}
            )
            st.plotly_chart(fig_ingresos, use_container_width=True)
        
        # Tabla de próximas citas
        st.markdown("### 📅 Próximas Citas")
        proximas_citas = st.session_state.citas[
            (st.session_state.citas['fecha'] >= datetime.now().strftime('%Y-%m-%d')) &
            (st.session_state.citas['estado'].isin(['Confirmada', 'Pendiente']))
        ].sort_values('fecha').head(5)
        
        if len(proximas_citas) > 0:
            for _, cita in proximas_citas.iterrows():
                cliente_info = st.session_state.clientes[
                    st.session_state.clientes['id'] == cita['cliente_id']
                ].iloc[0]
                
                col_prox1, col_prox2, col_prox3 = st.columns([2, 1, 1])
                
                with col_prox1:
                    st.markdown(f"""
                    **{cliente_info['nombre']}** - {cita['servicio']}  
                    📅 {cita['fecha']} - {cita['hora']} | 💰 ${cita['precio']:,}
                    """)
                
                with col_prox2:
                    st.markdown(f"**Estado:** {cita['estado']}")
                
                with col_prox3:
                    if st.button(f"Ver detalle", key=f"detail_{cita['id']}"):
                        st.info(f"ID Cita: {cita['id']}")
        else:
            st.info("No hay citas próximas.")
    
    with tabs[1]:
        st.markdown("### 📅 Calendario de Citas")
        
        # Filtros de calendario
        col_cal1, col_cal2 = st.columns(2)
        
        with col_cal1:
            fecha_desde = st.date_input("Desde", value=datetime.now().date())
        
        with col_cal2:
            fecha_hasta = st.date_input("Hasta", value=datetime.now().date() + timedelta(days=7))
        
        # Filtrar citas por rango de fechas
        citas_periodo = st.session_state.citas[
            (st.session_state.citas['fecha'] >= fecha_desde.strftime('%Y-%m-%d')) &
            (st.session_state.citas['fecha'] <= fecha_hasta.strftime('%Y-%m-%d'))
        ].sort_values(['fecha', 'hora'])
        
        if len(citas_periodo) > 0:
            # Agrupar por fecha
            for fecha in sorted(citas_periodo['fecha'].unique()):
                st.markdown(f"#### 📅 {fecha}")
                
                citas_dia = citas_periodo[citas_periodo['fecha'] == fecha]
                
                for _, cita in citas_dia.iterrows():
                    cliente_info = st.session_state.clientes[
                        st.session_state.clientes['id'] == cita['cliente_id']
                    ].iloc[0]
                    
                    vehiculo_info = st.session_state.vehiculos[
                        st.session_state.vehiculos['id'] == cita['vehiculo_id']
                    ].iloc[0]
                    
                    # Color según estado
                    color = {
                        'Confirmada': 'success',
                        'Pendiente': 'warning', 
                        'Completada': 'info',
                        'Cancelada': 'error'
                    }.get(cita['estado'], 'secondary')
                    
                    st.markdown(f"""
                    <div style="padding: 10px; margin: 5px 0; border-left: 4px solid {'#28a745' if color=='success' else '#ffc107' if color=='warning' else '#17a2b8' if color=='info' else '#dc3545'}; background: #f8f9fa;">
                        <strong>{cita['hora']}</strong> - {cliente_info['nombre']}<br>
                        <strong>Servicio:</strong> {cita['servicio']}<br>
                        <strong>Vehículo:</strong> {vehiculo_info['marca']} {vehiculo_info['modelo']} ({vehiculo_info['placa']})<br>
                        <strong>Estado:</strong> {cita['estado']} | <strong>Precio:</strong> ${cita['precio']:,}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No hay citas en el período seleccionado.")
    
    with tabs[2]:
        st.markdown("### 📋 Reportes")
        
        # Selector de tipo de reporte
        tipo_reporte = st.selectbox(
            "Tipo de reporte",
            ["Resumen General", "Ingresos por Período", "Servicios Más Solicitados", "Clientes Frecuentes"]
        )
        
        if tipo_reporte == "Resumen General":
            st.markdown("#### Resumen General del Taller")
            
            col_rep1, col_rep2, col_rep3 = st.columns(3)
            
            with col_rep1:
                st.metric("Total Clientes Registrados", len(st.session_state.clientes))
                st.metric("Total Vehículos", len(st.session_state.vehiculos))
                st.metric("Items en Inventario", len(st.session_state.inventario))
            
            with col_rep2:
                st.metric("Citas Totales", len(st.session_state.citas))
                st.metric("Citas Completadas", len(st.session_state.citas[st.session_state.citas['estado'] == 'Completada']))
                st.metric("Citas Pendientes", len(st.session_state.citas[st.session_state.citas['estado'] == 'Pendiente']))
            
            with col_rep3:
                total_ingresos = st.session_state.citas[st.session_state.citas['estado'] == 'Completada']['precio'].sum()
                ingreso_promedio = st.session_state.citas[st.session_state.citas['estado'] == 'Completada']['precio'].mean()
                st.metric("Ingresos Totales", f"${total_ingresos:,}")
                st.metric("Ingreso Promedio", f"${ingreso_promedio:,.0f}" if not pd.isna(ingreso_promedio) else "$0")
        
        elif tipo_reporte == "Ingresos por Período":
            st.markdown("#### Ingresos por Período")
            
            # Crear datos de ejemplo por mes
            citas_completadas = st.session_state.citas[st.session_state.citas['estado'] == 'Completada'].copy()
            if len(citas_completadas) > 0:
                citas_completadas['fecha'] = pd.to_datetime(citas_completadas['fecha'])
                ingresos_mes = citas_completadas.groupby(citas_completadas['fecha'].dt.to_period('M'))['precio'].sum()
                
                fig_ingresos_tiempo = px.line(
                    x=ingresos_mes.index.astype(str),
                    y=ingresos_mes.values,
                    title="Evolución de Ingresos Mensuales",
                    labels={'x': 'Mes', 'y': 'Ingresos ($)'}
                )
                st.plotly_chart(fig_ingresos_tiempo, use_container_width=True)
            else:
                st.info("No hay citas completadas para mostrar ingresos.")
        
        elif tipo_reporte == "Servicios Más Solicitados":
            st.markdown("#### Servicios Más Solicitados")
            
            servicios_count = st.session_state.citas['servicio'].value_counts()
            
            fig_servicios = px.bar(
                x=servicios_count.index,
                y=servicios_count.values,
                title="Servicios Más Solicitados",
                labels={'x': 'Servicio', 'y': 'Cantidad de Citas'}
            )
            fig_servicios.update_xaxis(tickangle=45)
            st.plotly_chart(fig_servicios, use_container_width=True)
            
            # Tabla detallada
            st.dataframe(servicios_count.to_frame('Cantidad de Citas'), use_container_width=True)
        
        elif tipo_reporte == "Clientes Frecuentes":
            st.markdown("#### Clientes Más Frecuentes")
            
            clientes_freq = st.session_state.citas['cliente_id'].value_counts().head(10)
            
            # Obtener nombres de clientes
            clientes_nombres = []
            for cliente_id in clientes_freq.index:
                nombre = st.session_state.clientes[
                    st.session_state.clientes['id'] == cliente_id
                ]['nombre'].iloc[0]
                clientes_nombres.append(nombre)
            
            fig_clientes = px.bar(
                x=clientes_nombres,
                y=clientes_freq.values,
                title="Top 10 Clientes Más Frecuentes",
                labels={'x': 'Cliente', 'y': 'Número de Citas'}
            )
            fig_clientes.update_xaxis(tickangle=45)
            st.plotly_chart(fig_clientes, use_container_width=True)
    
    with tabs[3]:
        st.markdown("### ⚙️ Configuración del Sistema")
        
        col_config1, col_config2 = st.columns(2)
        
        with col_config1:
            st.markdown("#### Gestión de Servicios")
            
            # Agregar nuevo servicio
            with st.expander("Agregar Nuevo Servicio"):
                nombre_servicio = st.text_input("Nombre del servicio")
                precio_servicio = st.number_input("Precio", min_value=0, step=1000)
                duracion_servicio = st.text_input("Duración", placeholder="ej: 1 hora")
                
                if st.button("Agregar Servicio"):
                    if nombre_servicio and precio_servicio > 0 and duracion_servicio:
                        nuevo_servicio = {
                            'nombre': nombre_servicio,
                            'precio': precio_servicio,
                            'duracion': duracion_servicio
                        }
                        st.session_state.servicios.append(nuevo_servicio)
                        st.success("Servicio agregado exitosamente")
                        st.rerun()
            
            # Lista de servicios actuales
            st.markdown("**Servicios Actuales:**")
            for i, servicio in enumerate(st.session_state.servicios):
                st.markdown(f"• {servicio['nombre']} - ${servicio['precio']:,} ({servicio['duracion']})")
        
        with col_config2:
            st.markdown("#### Configuración General")
            
            # Horarios de atención
            st.markdown("**Horarios de Atención:**")
            hora_inicio = st.selectbox("Hora inicio", ["07:00", "08:00", "09:00"], index=1)
            hora_fin = st.selectbox("Hora fin", ["17:00", "18:00", "19:00"], index=1)
            
            # Información del taller
            st.markdown("**Información del Taller:**")
            nombre_taller = st.text_input("Nombre del taller", value="AutoTaller Pro")
            telefono_taller = st.text_input("Teléfono", value="(01) 234-5678")
            
            if st.button("Guardar Configuración"):
                st.success("Configuración guardada exitosamente")
        
        # Botón de logout
        st.divider()
        if st.button("🚪 Cerrar Sesión", type="secondary"):
            st.session_state.authenticated = False
            st.rerun()

# Navegación principal
def main():
    # Sidebar de navegación
    with st.sidebar:
        st.title("🔧 AutoTaller Pro")
        
        if 'page' not in st.session_state:
            st.session_state.page = "inicio"
        
        # Menú de navegación
        menu_options = {
            "🏠 Inicio": "inicio",
            "📅 Citas": "citas", 
            "🛠️ Servicios": "servicios",
            "👥 Clientes": "clientes",
            "📦 Inventario": "inventario",
            "⚙️ Admin": "admin"
        }
        
        for label, page in menu_options.items():
            if st.button(label, key=f"nav_{page}", use_container_width=True):
                st.session_state.page = page
                st.rerun()
        
        st.divider()
        
        # Información rápida
        st.markdown("### 📊 Estado Rápido")
        st.metric("Citas Hoy", len(st.session_state.citas[
            st.session_state.citas['fecha'] == datetime.now().strftime('%Y-%m-%d')
        ]))
        
        items_bajo_stock = len(st.session_state.inventario[
            st.session_state.inventario['stock'] <= st.session_state.inventario['stock_minimo']
        ])
        st.metric("Items Stock Bajo", items_bajo_stock)
        
        st.divider()
        st.markdown("**📞 Contacto:**")
        st.markdown("Tel: (01) 234-5678")
        st.markdown("📧 contacto@autotaller.com")
    
    # Contenido principal según la página seleccionada
    if st.session_state.page == "inicio":
        pantalla_inicio()
    elif st.session_state.page == "citas":
        modulo_citas()
    elif st.session_state.page == "servicios":
        lista_servicios()
    elif st.session_state.page == "clientes":
        registro_clientes()
    elif st.session_state.page == "inventario":
        inventario()
    elif st.session_state.page == "admin":
        panel_admin()

# Ejecutar la aplicación
if __name__ == "__main__":
    main()
import streamlit as st

def mostrar_navbar():
    st.markdown("""
    <style>
    .navbar {
        overflow: hidden;
        background-color: #006699;
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        margin-bottom: 20px;
    }
    .dropdown {
        position: relative;
        display: inline-block;
    }
    .dropbtn {
        font-size: 16px;
        color: white;
        padding: 14px 20px;
        border: none;
        background: none;
        font-weight: 600;
        cursor: pointer;
    }
    .dropdown-content {
        display: none;
        position: absolute;
        background-color: #f9f9f9;
        min-width: 220px;
        box-shadow: 0px 8px 16px rgba(0,0,0,0.2);
        z-index: 1;
    }
    .dropdown-content a {
        color: black;
        padding: 12px 16px;
        text-decoration: none;
        display: block;
    }
    .dropdown-content a:hover {
        background-color: #ddd;
    }
    .dropdown:hover .dropdown-content {
        display: block;
    }
    </style>

    <div class="navbar">
      <div class="dropdown">
        <button class="dropbtn">Dispositivos ▼</button>
        <div class="dropdown-content">
          <a href="?mod=handheld">📦 Registro de Handhelds</a>
          <a href="?mod=temp">🌡️ Registro de Temperatura</a>
          <a href="?mod=prueba">🧪 Prueba de Ubicación</a>
          <a href="?mod=jornadas">📝 Gestión de Jornada</a>
          <a href="?mod=errores">🚨 Registro de Errores</a>
        </div>
      </div>

      <div class="dropdown">
        <button class="dropbtn">Panel Administrativo ▼</button>
        <div class="dropdown-content">
          <a href="?mod=admin">📋 Panel Administrativo</a>
          <a href="?mod=cert">📊 Panel de Certificaciones</a>
          <a href="?mod=prod">🕒 Productividad</a>
        </div>
      </div>

      <div class="dropdown">
        <button class="dropbtn">Almacenamiento ▼</button>
        <div class="dropdown-content">
          <a href="?mod=lpn">🏷️ Generación de LPNs</a>
          <a href="?mod=almacen">📥 Almacenamiento LPN</a>
          <a href="?mod=ocupacion">📦 Panel de Ocupación Nave</a>
          <a href="?mod=sku">🔍 Consulta de SKU</a>
          <a href="?mod=trecibo">📑 Reporte TRecibo</a>
        </div>
      </div>

      <div class="dropdown">
        <button class="dropbtn">Bloqueo ▼</button>
        <div class="dropdown-content">
          <a href="?mod=bloqueo">🚫 Bloqueo de Ubicaciones</a>
        </div>
      </div>

      <div class="dropdown">
        <button class="dropbtn">Mantenimiento ▼</button>
        <div class="dropdown-content">
          <a href="?mod=mantenimiento">🛠️ Estado de Mantenimiento</a>
        </div>
      </div>

      <div class="dropdown">
        <button class="dropbtn">Ayuda ▼</button>
        <div class="dropdown-content">
          <a href="?mod=ayuda">📖 Manual de Usuario</a>
        </div>
      </div>

      <div class="dropdown">
        <button class="dropbtn">Desarrollador ▼</button>
        <div class="dropdown-content">
          <a href="?mod=bitacora">📜 Bitácora</a>
        </div>
      </div>

      <div class="dropdown">
        <button class="dropbtn">Reportes ▼</button>
        <div class="dropdown-content">
          <a href="?mod=reportes">📑 Reportes Generales</a>
        </div>
      </div>

      <div class="dropdown">
        <button class="dropbtn">Misceláneos ▼</button>
        <div class="dropdown-content">
          <a href="?mod=inicio">🏠 Inicio</a>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

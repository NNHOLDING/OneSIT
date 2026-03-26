import streamlit as st

def script_inactividad(minutos=5):
    st.markdown(f"""
    <script>
    let timeout;
    function resetTimer() {{
        clearTimeout(timeout);
        timeout = setTimeout(() => {{
            localStorage.setItem("expired", "true");
            window.location.reload();
        }}, {minutos*60000});
    }}
    window.onload = resetTimer;
    document.onmousemove = resetTimer;
    document.onkeypress = resetTimer;
    </script>
    """, unsafe_allow_html=True)

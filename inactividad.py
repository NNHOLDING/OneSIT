def script_inactividad(minutos=5):
    st.markdown(f"""
    <script>
    let timeout;
    function resetTimer() {{
        clearTimeout(timeout);
        timeout = setTimeout(() => {{
            window.location.href = window.location.pathname + "?expired=true";
        }}, {minutos*60000});
    }}
    window.onload = resetTimer;
    document.onmousemove = resetTimer;
    document.onkeypress = resetTimer;
    </script>
    """, unsafe_allow_html=True)
"""
py server.py localhost 2025 2026 2027

py server.py localhost 2035 2036 2037

py server.py localhost 2045 2046 2047

py server.py localhost 2055 2056 2057

py server.py localhost 2065 2066 2067

py server.py localhost 2075 2076 2077

py server.py localhost 2085 2086 2087

py client.py localhost 2025 SET 123 456

"""

#si cierro uno y lo vuelvo a abrir se rompe (debe ser por no hacer close)
#Si haces un get y no te llega te bloqueas
#No se si estamos guardando los hexadecimales como quieren los profes
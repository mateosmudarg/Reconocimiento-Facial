import serial
try:
    arduino = serial.Serial('COM4', 9600, timeout=1)
except Exception as e:
    arduino = None
    print(f"No se pudo conectar con Arduino: {e}")
checkbox_vars = []
record_ids = []
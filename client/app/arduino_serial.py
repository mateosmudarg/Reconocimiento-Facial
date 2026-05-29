"""Control opcional de puerta vía Arduino por puerto serie."""


class ArduinoDoor:
    def __init__(self, port: str, baud: int = 9600) -> None:
        self._serial = None
        if not port:
            return
        try:
            import serial  # pyserial

            self._serial = serial.Serial(port, baud, timeout=1)
        except Exception as e:  # puerto inexistente / sin permisos
            print(f"[Arduino] No se pudo abrir {port}: {e}")
            self._serial = None

    @property
    def disponible(self) -> bool:
        return self._serial is not None

    def abrir_puerta(self) -> None:
        if self._serial:
            try:
                self._serial.write(b"A")
            except Exception as e:
                print(f"[Arduino] Error al enviar comando: {e}")

    def close(self) -> None:
        if self._serial:
            self._serial.close()
            self._serial = None

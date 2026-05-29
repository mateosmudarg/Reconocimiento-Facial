import httpx


class ApiError(Exception):
    pass


class ApiClient:
    """Cliente HTTP para la API central. Sincroniza el dispositivo con el servidor."""

    def __init__(self, base_url: str) -> None:
        self._base = base_url.rstrip("/")
        self._token: str | None = None
        self._client = httpx.Client(base_url=self._base, timeout=15.0)

    # ---------- Auth ----------
    def login(self, username: str, password: str) -> dict:
        r = self._client.post(
            "/api/auth/login", data={"username": username, "password": password}
        )
        if r.status_code != 200:
            raise ApiError("Usuario o contraseña incorrectos")
        data = r.json()
        self._token = data["access_token"]
        return data

    @property
    def autenticado(self) -> bool:
        return self._token is not None

    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self._token}"}

    # ---------- Reconocimiento ----------
    def identificar(
        self,
        embedding: list[float],
        tipo: str,
        dispositivo: str,
        imagen_b64: str | None = None,
    ) -> dict:
        r = self._client.post(
            "/api/reconocimiento/identificar",
            headers=self._headers(),
            json={
                "embedding": embedding,
                "tipo": tipo,
                "dispositivo": dispositivo,
                "imagen_b64": imagen_b64,
            },
        )
        if r.status_code != 200:
            raise ApiError(f"Error del servidor ({r.status_code})")
        return r.json()

    # ---------- Empleados ----------
    def crear_empleado(self, payload: dict) -> dict:
        r = self._client.post(
            "/api/empleados", headers=self._headers(), json=payload
        )
        if r.status_code not in (200, 201):
            detalle = r.json().get("detail", r.text) if r.content else r.text
            raise ApiError(str(detalle))
        return r.json()

    def close(self) -> None:
        self._client.close()

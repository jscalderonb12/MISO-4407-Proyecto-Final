class CShooter:
    """
    Componente que marca a una entidad como tirador y almacena
    parámetros para el sistema de disparo.

    Attributes:
        fire_rate (float): segundos entre cada disparo.
        bullet_speed (float): velocidad de las balas creadas.
        time_since_last (float): tiempo acumulado desde el último disparo.
    """

    def __init__(self, fire_rate: float, bullet_speed: float, time_since_last: float = 0.0) -> None:
        self.fire_rate = fire_rate
        self.bullet_speed = bullet_speed
        self.time_since_last = time_since_last

    def reset_timer(self) -> None:
        """Reinicia el contador de tiempo tras un disparo."""
        self.time_since_last = 0.0
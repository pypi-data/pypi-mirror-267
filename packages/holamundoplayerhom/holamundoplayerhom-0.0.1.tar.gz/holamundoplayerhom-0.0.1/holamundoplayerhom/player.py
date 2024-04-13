"""
    Este es el modulo que incluye la clase de reproductor de musica
"""


class Player:
    """
        Esta CLase crea un reporductor
        de Musica    
    """

    def play(self, song):
        """
        Reproduce la cancion que recibio
        en el constructor

        Parameters: 
        song(str): Este es un String con el path de la cancion

        Returns:
        int: Devuelve 1 si reproduce con exito si no un 0

        """
        print("Reproduciendo Canción")

    def stop(self):
        print("Sttoping")

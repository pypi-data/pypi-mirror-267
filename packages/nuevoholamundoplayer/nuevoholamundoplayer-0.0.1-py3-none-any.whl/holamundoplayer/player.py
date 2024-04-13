"""
Esta es el modulo que incluye el reproductor de musica
"""


class Player:
    """
    Esta clase crea un reproductor de musica
    """

    def play(self, song):
        # Documentamos el metodo
        """
        Este metodo reproduce la cancion que recibio como parametro

        Parameters:
        song (str): este es un string con el path de la cancion

        Returns:
        int: devuelve 1 si reproduce con exito, en caso de fracaso
        retorna 0
        """
        print("Reproduciendo cancion")

    def stop(self):
        print("stopping")

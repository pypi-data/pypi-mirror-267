class   TRAMAS:
    """
    Dicha Librería implementa diferentes funciones que permiten calcular el checksum
    de una trama y crear una nueva trama, que posteriormente se podrá enviar.
    """
    def __init__(self) -> None:
        pass
    def calcular_checksum(self,trama):
        """
        Esta función toma una trama en hexadecimal como entrada y calcula 
        el checksum para esa trama. Devuelve el valor del checksum.
        """
        # Suma todos los valores ASCII de los caracteres en la trama 
        check = sum(trama)
        # Devuelve el checksum módulo 256, comprobando que si check > 256 , el cheksum es 256 menos la diferencia que hay entre ambos
        if check >= 256:
            checksum = 256 - (abs(256-check))
        else:
            checksum = abs(256-check)
        return checksum # valor absoluto por si cheksum es mayor que 256
        
    def crear_trama(self,direccion_destino, numero_bits, direccion_origen, comando, datos):
        """
        Esta función construye una trama de acuerdo con la estructura proporcionada.Tiene 5 argumentos
        Hay que tener en cuenta que los datos que se introducen deben estar en formate hexadecimal 0XAB.
        También a la hora de introducir datos, estso deben estar en forma de lista datos=[0x00,0x00,..]
        Finalmente, se devuelve la trama creada.
        """
        # Convertir cadenas de texto a bytes en formato hexadecimal
        direccion_destino_bytes = bytes.fromhex(direccion_destino)
        numero_bits_bytes = bytes.fromhex(numero_bits)
        direccion_origen_bytes = bytes.fromhex(direccion_origen)
        comando_bytes = bytes.fromhex(comando)
        datos_bytes = [bytes.fromhex(dato) for dato in datos]
    
        # Construir la trama en forma de bytearray (valores en código ASCII)
        trama = bytearray()
        trama.append(int.from_bytes(direccion_destino_bytes, 'big'))
        trama.append(int.from_bytes(numero_bits_bytes, 'big'))
        trama.append(int.from_bytes(direccion_origen_bytes, 'big'))
        trama.append(int.from_bytes(comando_bytes, 'big'))
        
        # Agregar los datos a la trama
        for dato in datos_bytes:
            trama.append(int.from_bytes(dato, 'big'))
        
        # Calcular el checksum
        checksum = calcular_checksum(trama)
        
        # Añadir el checksum a la trama
        trama.append(checksum)
        
        return trama
class Instruccion:
    def __init__(self, mnemonico, destino='', computo='', salto=''):
        self.mnemonico = mnemonico
        self.destino = destino
        self.computo = computo
        self.salto = salto

    def traducir(self):
        if self.mnemonico.startswith('@'):
            return self.traducir_instruccion_A()
        else:
            return self.traducir_instruccion_C()

    def traducir_instruccion_A(self):
        direccion = self.mnemonico[1:]  
        direccion_binaria = format(int(direccion), '015b') 
        return '0' + direccion_binaria.zfill(15)  

    def traducir_instruccion_C(self):
        destino_binario = dest_table[self.destino].zfill(3)  
        computo_binario = comp_table[self.computo].zfill(7)  
        salto_binario = jump_table[self.salto].zfill(3) if self.salto else '000'  
        return '111' + computo_binario + destino_binario + salto_binario  

# Tablas de traducción
comp_table = {
    '0':   '0101010',
    '1':   '0111111',
    '-1':  '0111010',
    'D':   '0001100',
    'A':   '0110000',
    '!D':  '0001101',
    '!A':  '0110001',
    '-D':  '0001111',
    '-A':  '0110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'D+A': '0000010',
    'D-A': '0010011',
    'A-D': '0000111',
    'D&A': '0000000',
    'D|A': '0010101',
}

dest_table = {
    '':    '000',
    'M':   '001',
    'D':   '010',
    'MD':  '011',
    'A':   '100',
    'AM':  '101',
    'AD':  '110',
    'AMD': '111',
}

jump_table = {
    '':    '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111',
}

def ensamblar(codigo_fuente, archivo_salida):
    codigo_binario = []

    for linea in codigo_fuente:
        if not linea or linea.startswith('//'):
            continue

        instruccion = Instruccion(*tokenizar(linea))  
        codigo_binario.append(instruccion.traducir().zfill(16))  

    with open(archivo_salida, 'w') as f:
        for instruccion_binaria in codigo_binario:
            f.write(instruccion_binaria + '\n')  

def tokenizar(linea):
    linea = linea.strip()
    if linea.startswith('@'):
        return (linea,)
    elif '=' in linea:
        destino, resto = linea.split('=')
        if ';' in resto:
            computo, salto = resto.split(';')
            return ('', destino, computo, salto)
        else:
            return ('', destino, resto)
    else:
        computo, salto = linea.split(';')
        return ('', computo, salto)

# Código fuente de ejemplo
codigo_fuente = [
    '@2',    # Cargar el valor 2 en la dirección de memoria
    'D=A',   # Asignar el valor de A a D
    '@3',    # Cargar el valor 3 en la dirección de memoria
    'D=D+A', # Sumar el valor de D con el valor en la dirección de memoria 3 y almacenar en D
    '@0',    # Cargar el valor 0 en la dirección de memoria
    'M=D'    # Almacenar el valor de D en la dirección de memoria 0
]

# Ensamblar el código fuente y guardar el resultado
ensamblar(codigo_fuente, 'traducido.hack')

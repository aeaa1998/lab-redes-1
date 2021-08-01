def required_input(text="Ingrese un valor\n"):
    while(True):
        input_r = input(text)
        if input_r != "" and input_r is not None:
            return input_r
        print("Ingrese un valor \n")


def int_input(text="Ingrese un numero\n", error="Ingrese un numero valido\n"):
    while(True):
        try:
            int_input = int(input(text))
            return int_input
        except:
            print(error)


def int_input_range(text="Ingrese un numero\n", error="Ingrese un numero valido\n", min=1, max=100):
    while(True):
        int_input_value = int_input(text, error)
        if int_input_value < min:
            print("El numero no puede ser menor a " + str(min), "\n")
        elif int_input_value > max:
            print("El numero no puede ser mayor a " + str(max), "\n")
        else:
            return int_input_value


def get_index_from_list(list, text="Ingrese el numero de una de las opciones\n"):
    while True:
        size = len(list)
        for i, item in enumerate(list):
            print(str(i+1) + ") " + str(list[i]) + "\n")
        input = int_input(text, "Ingrese un numero de opcion valido\n")
        if input > 0 <= size:
            return input - 1
        print("Seleccione una opcion valida\n")

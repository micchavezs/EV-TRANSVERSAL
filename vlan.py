vlan = int(input("Ingrese el número de VLAN: "))

if vlan >= 1 and vlan <= 1005:
    print(f"La VLAN {vlan} pertenece al rango normal.")

elif vlan >= 1006 and vlan <= 4094:
    print(f"La VLAN {vlan} pertenece al rango extendido.")

else:
    print(f"La VLAN {vlan} no es válida.")

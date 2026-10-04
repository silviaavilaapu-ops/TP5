"""
UNJu - Facultad de Ingeniería
Teoría de Sistemas Operativos (TSO) - Ciclo Lectivo 2026
Cátedra: Ing. María Fernanda Vázquez - JTP: Ing. Fabio D. Argañaraz

Ejercicio Práctico N° 2: El Problema del Oso y las Abejas
Bibliografía de Referencia:
- Silberschatz: Cap. 6.6 (Problemas clásicos de sincronización)
- Stallings: Cap. 5.4 (Sincronización con semáforos)
"""

import sys
import threading
import time
import random

# Configuración UTF-8 para consola Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

M = 10                  # Capacidad del tarro de miel
NUM_ABEJAS = 5          # Número de abejas obreras
tarro_miel = 0          # Variable compartida
simulacion_activa = True

# TODO PARA EL ESTUDIANTE:
# 1. Define los mecanismos de sincronización necesarios:
# - Un cerrojo (Lock) o semáforo binario para exclusión mutua en el tarro.
# - Un semáforo para despertar al oso cuando el tarro esté lleno.
# - Un semáforo para que las abejas esperen si el tarro está lleno o el oso está comiendo.
mutex = threading.Lock()
sem_oso = threading.Semaphore(0)
sem_tarro_disponible = threading.Semaphore(1)

def abeja(id_abeja):
    global tarro_miel, simulacion_activa
    while simulacion_activa:
        time.sleep(random.uniform(0.05, 0.2))

        sem_tarro_disponible.acquire()
        mutex.acquire()
        tarro_miel += 1
        
        if tarro_miel == M:
            print("Despiertar al Oso")
            sem_oso.release()
        else:
            mutex.release()
            sem_tarro_disponible.release()
        

def oso(max_tarros=2):
    global tarro_miel, simulacion_activa
    tarros_comidos = 0
    while tarros_comidos < max_tarros:
        sem_oso.acquire()
        print("🐻 El oso se despierta y se come toda la miel!")
        tarro_miel = 0
        print("🐻 El oso vuelve a dormir.")
        tarros_comidos += 1
        time.sleep(0.1)
        mutex.release()
        sem_tarro_disponible.release()
        
    simulacion_activa = False
    sem_tarro_disponible.release()

if __name__ == "__main__":
    print("=" * 60)
    print(" Iniciando Simulación: El Oso y las Abejas (UNJu FI)")
    print("=" * 60)
    hilo_oso = threading.Thread(target=oso, arg=(2,))
    hilo_oso.start()

    hilos_abejas = []
    for i in range(NUM_ABEJAS):
        t = threading.Thread(target=abeja, arg=(i + 1,))
        hilos_abejas.append(t)
        t.start()
    
    hilo_oso.join()
    for t in hilos_abejas:
        t.join()
    
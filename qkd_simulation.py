from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import random

def simulate_BB84_key():
    backend = Aer.get_backend('qasm_simulator')
    alice_key = ""
    bob_key = ""

    print("Starting BB84 Quantum Key Distribution Simulation...")

    # Use a longer key length for better security
    key_length = 128  # 128-bit key length for AES

    while len(alice_key) < key_length:
        alice_bit = random.choice([0, 1])
        alice_basis = random.choice([0, 1])
        qc = QuantumCircuit(1, 1)

        if alice_bit == 1:
            qc.x(0)
        if alice_basis == 1:
            qc.h(0)

        bob_basis = random.choice([0, 1])
        if bob_basis == 1:
            qc.h(0)
        qc.measure(0, 0)

        # Transpile the circuit to ensure compatibility with the simulator
        transpiled_qc = transpile(qc, backend)
        
        # Execute the circuit and get the result
        result = backend.run(transpiled_qc, shots=1).result()
        bob_bit = int(result.get_counts().get('0', 0) < 1)

        if alice_basis == bob_basis:
            alice_key += str(alice_bit)
            bob_key += str(bob_bit)

    if alice_key == bob_key:
        print("Shared Quantum Key Generated:", alice_key)
        return alice_key
    else:
        print("Key Mismatch: Possible Eavesdropping Detected.")
        return None

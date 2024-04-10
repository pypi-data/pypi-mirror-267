# import for EnigmaMachine
from enigma_machine_german import EnigmaMachine

# Create an object of EnigmaMachine with 2,4,5 as the wheel/rotor configuration
obj = EnigmaMachine(2,4,5)
# Encrypt the message using encrypt_message method of EnigmaMachine
encrypted = obj.encrypt_message("hello world")
print("Encrypted message: ", encrypted)
# use decrypt_message method of EnigmaMachine to decrypt the encrypted message
obj2 = EnigmaMachine(2,4,5)
decrypted = obj2.encrypt_message(encrypted)
print("Decrypted message: ", decrypted)


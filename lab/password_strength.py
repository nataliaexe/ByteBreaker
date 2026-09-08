import hashlib
import time
import string
import itertools

def crack_time_estimate(password):
    """Estimar tempo para quebrar senha"""
    charset_sizes = {
        'lowercase': 26,
        'uppercase': 26,
        'digits': 10,
        'special': 32
    }
    
    # Determinar charset usado
    charset_size = 0
    if any(c.islower() for c in password):
        charset_size += charset_sizes['lowercase']
    if any(c.isupper() for c in password):
        charset_size += charset_sizes['uppercase']
    if any(c.isdigit() for c in password):
        charset_size += charset_sizes['digits']
    if any(c in string.punctuation for c in password):
        charset_size += charset_sizes['special']
    
    # Total de combinações
    combinations = charset_size ** len(password)
    
    # Assumindo 1 bilhão de tentativas por segundo (GPU)
    seconds = combinations / 1_000_000_000
    
    # Converter para tempo legível
    if seconds < 1:
        return "menos de 1 segundo"
    elif seconds < 60:
        return f"{seconds:.2f} segundos"
    elif seconds < 3600:
        return f"{seconds/60:.2f} minutos"
    elif seconds < 86400:
        return f"{seconds/3600:.2f} horas"
    elif seconds < 31536000:
        return f"{seconds/86400:.2f} dias"
    elif seconds < 31536000 * 100:
        return f"{seconds/31536000:.2f} anos"
    else:
        return f"{seconds/31536000:.2e} anos (idade do universo)"
    
passwords = [
    'password',
    'password123',
    'P@ssw0rd',
    'P@ssw0rd!2024',
    'correct horse battery staple',
    'Tr0ub4dor&3',
    'kX9#mP2$vL5@nQ8',
    'this is a very long passphrase with spaces and special chars !@#$%'
]

print("=== Estimativa de tempo para quebrar senhas ===")
print("(Assumindo 1 bilhão de tentativas/segundo com GPU)\n")

for pwd in passwords:
    time_to_crack = crack_time_estimate(pwd)
    print(f"Senha: {pwd}")
    print(f"  Tamanho: {len(pwd)} caracteres")
    print(f"  Tempo estimado: {time_to_crack}\n")

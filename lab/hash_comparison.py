import hashlib
import bcrypt
import time

def compare_hashing():
    """Comparar velocidade de diferentes algoritmos"""
    password = "P@ssw0rd!2024"
    
    print("=== Comparação de Algoritmos de Hash ===\n")
    
    # MD5 (inseguro)
    start = time.time()
    for _ in range(10000):
        hashlib.md5(password.encode()).hexdigest()
    md5_time = time.time() - start
    print(f"MD5: {md5_time:.4f} segundos para 10,000 hashes")
    print(f"  Velocidade: {10000/md5_time:.0f} hashes/segundo")
    
    # SHA256 (inseguro para senhas)
    start = time.time()
    for _ in range(10000):
        hashlib.sha256(password.encode()).hexdigest()
    sha256_time = time.time() - start
    print(f"\nSHA256: {sha256_time:.4f} segundos para 10,000 hashes")
    print(f"  Velocidade: {10000/sha256_time:.0f} hashes/segundo")
    
    # bcrypt (seguro)
    start = time.time()
    for _ in range(10):
        bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
    bcrypt_time = time.time() - start
    print(f"\nbcrypt (12 rounds): {bcrypt_time:.4f} segundos para 10 hashes")
    print(f"  Velocidade: {10/bcrypt_time:.2f} hashes/segundo")
    print(f"  ~{bcrypt_time/10:.2f} segundos por hash")
    
    print("\n=== Conclusão ===")
    print(f"MD5 é {int((10000/md5_time)/(10/bcrypt_time)):,}x mais rápido que bcrypt")
    print("Isso significa que um atacante pode testar mais de")
    print("1 milhão de senhas MD5 no tempo que leva para testar")
    print("uma única senha com bcrypt!")

if __name__ == "__main__":
    compare_hashing()

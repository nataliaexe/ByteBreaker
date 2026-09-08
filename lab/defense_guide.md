# Guia de Defesa Contra Ataques de Senha

## 1. Use Senhas Longas
- Mínimo de 12-16 caracteres
- Preferência por frases (passphrases)
- Exemplo: "correct horse battery staple" (28 caracteres)

## 2. Use Caracteres Diversos
- Maiúsculas e minúsculas
- Números
- Símbolos especiais
- Exemplo: "Tr0ub4dor&3"

## 3. Use Gerenciadores de Senha
- Bitwarden (open source)
- KeePass (local)
- 1Password (comercial)
- Gere senhas aleatórias únicas

## 4. Ative Autenticação de Dois Fatores (2FA)
- Google Authenticator (TOTP)
- Authy (multi-dispositivo)
- YubiKey (hardware)
- Evite SMS se possível

## 5. Use Hashing Seguro
- bcrypt (com custo 12+)
- Argon2id (recomendado)
- PBKDF2 (com 100k+ iterações)
- NUNCA use MD5 ou SHA1 para senhas

## 6. Implemente Rate Limiting
- Limite 5 tentativas por minuto
- Bloqueio após 10 falhas
- CAPTCHA após 3 tentativas

## 7. Monitore Atividades
- Logs de autenticação
- Alertas em tempo real
- Análise de comportamento

## 8. Eduque Usuários
- Treinamento regular
- Políticas claras
- Simulações de phishing

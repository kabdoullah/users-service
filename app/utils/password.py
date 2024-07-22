import re

def validate_password_complexity(password: str) -> bool:
    password_pattern = re.compile(
        r"""
        ^                # début de la chaîne
        (?=.*[A-Z])      # au moins une lettre majuscule
        (?=.*[a-z])      # au moins une lettre minuscule
        (?=.*\d)         # au moins un chiffre
        (?=.*[!@#$%^&*()\-_=+]) # au moins un caractère spécial
        .{8,}            # au moins 8 caractères de long
        $                # fin de la chaîne
        """, re.VERBOSE
    )

    return bool(password_pattern.match(password))

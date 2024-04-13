import math
import toml
import string
import secrets
import regex as re
from pyotp import TOTP
from pydantic import BaseModel
from pathlib import Path


def count_chars(arr: str | list[str]) -> dict[str, float]:
    frequency = dict()
    for c in arr:
        if c in frequency:
            frequency[c] += 1
        else:
            frequency[c] = 1
    return frequency


def shannon_entropy(text: str) -> float:
    if not text:
        return 0
    frequency = count_chars(text)
    entropy = -sum(
        (freq / len(text)) * math.log2(freq / len(text)) for freq in frequency.values()
    )
    maximum_entropy = math.log2(len(text))
    normalized_entropy = entropy / maximum_entropy if maximum_entropy > 0 else 1
    return abs(normalized_entropy)


def save_toml(data: dict, path: str | Path) -> None:
    with open(path, "w") as file:
        file.write(toml.dumps(data))
    file.close()


def load_toml(path: str | Path) -> dict:
    with open(path) as file:
        data = toml.loads(file.read())
    file.close()
    return data


def save_text(data: str, path: str | Path) -> None:
    with open(path, "w") as file:
        file.write(data)
    file.close()


def load_text(path: str | Path) -> str:
    with open(path) as file:
        data = file.read()
    file.close()
    return data


def compute_otp(secret: str) -> str:
    return TOTP(secret).now()


class PasswordValidation(BaseModel):
    text: str
    valid: bool
    errors: list[str] = list()


def secure_random_bounded(lower_bound: int, upper_bound: int) -> int:
    """Securely generate a random value between the inclusive upper and lower bounds."""
    return secrets.randbelow(upper_bound - lower_bound + 1) + lower_bound


def validate_password(
    password: str,
    character_count: int = 16,
    numeric_character_count: int = 1,
    special_character_count: int = 1,
    uppercase_character_count: int = 1,
    lowercase_character_count: int = 1,
    minimum_shannon_entropy: float = 0.64,
) -> PasswordValidation:
    """
    Validate a password based on a selection of various criteria.

    Default values are provided that form a baseline for a secure
    password.

    Args:
        password (str): password to validate
        character_count (int): Defaults to 16.
        numeric_character_count (int): Defaults to 1.
        special_character_count (int): Defaults to 1.
        uppercase_character_count (int): Defaults to 1.
        lowercase_character_count (int): Defaults to 1.
        minimum_shannon_entropy (float): "Randomness". Defaults to 0.64.

    Returns:
        Password: password object with text, validity, and failed rules (if any)
    """
    rule_checks = {
        "character_count": (
            len(password) >= character_count,
            character_count,
        ),
        "numeric_character_count": (
            len(re.findall(r"\d", password)) >= numeric_character_count,
            numeric_character_count,
        ),
        "special_character_count": (
            len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', password))
            >= special_character_count,
            special_character_count,
        ),
        "uppercase_character_count": (
            len(re.findall(r"[A-Z]", password)) >= uppercase_character_count,
            uppercase_character_count,
        ),
        "lowercase_character_count": (
            len(re.findall(r"[a-z]", password)) >= lowercase_character_count,
            lowercase_character_count,
        ),
        "shannon_entropy": (
            shannon_entropy(password) >= minimum_shannon_entropy,
            minimum_shannon_entropy,
        ),
    }
    password_is_valid: bool = all([val[0] for val in rule_checks.values()])
    rules_failed = list()
    for k, v in rule_checks.items():
        if not v[0]:
            rules_failed.append(f"Requires: {' '.join(k.split('_'))} >= {v[1]}")
    return PasswordValidation(
        text=password, valid=password_is_valid, errors=rules_failed
    )


def generate_secure_password(
    minimum_character_count: int = 16,
    minimum_numeric_character_count: int = 1,
    minimum_special_character_count: int = 1,
    minimum_uppercase_character_count: int = 1,
    minimum_lowercase_character_count: int = 1,
    minimum_shannon_entropy: float = 0.64,
) -> str:
    """
    Generate a cryptographically secure password.

    Args:
        character_count (int): Minimum total length of the password. Defaults to 16.
        numeric_character_count (int): Minimum number of numeric characters. Defaults to 1.
        special_character_count (int): Minimum number of special characters. Defaults to 1.
        uppercase_character_count (int): Minimum number of uppercase characters. Defaults to 1.
        lowercase_character_count (int): Minimum number of lowercase characters. Defaults to 1.
        minimum_shannon_entropy (float): Minimum "randomness" of password. Defaults to 0.64.

    Returns:
        str: A password.
    """
    characters = []
    characters.extend(
        secrets.choice(string.digits)
        for _ in range(
            secure_random_bounded(
                minimum_numeric_character_count, minimum_numeric_character_count * 4
            )
        )
    )
    special_chars = "!@#$%^&*(),.?:{}|<>"
    characters.extend(
        secrets.choice(special_chars)
        for _ in range(
            secure_random_bounded(
                minimum_special_character_count, minimum_special_character_count * 4
            )
        )
    )
    characters.extend(
        secrets.choice(string.ascii_uppercase)
        for _ in range(
            secure_random_bounded(
                minimum_uppercase_character_count, minimum_uppercase_character_count * 4
            )
        )
    )
    characters.extend(
        secrets.choice(string.ascii_lowercase)
        for _ in range(
            secure_random_bounded(
                minimum_lowercase_character_count, minimum_uppercase_character_count * 4
            )
        )
    )
    total_length = secure_random_bounded(
        minimum_character_count, minimum_character_count * 2
    )
    remaining_count = total_length - len(characters)
    if remaining_count <= 0:
        raise ValueError("Please increase your 'minimum_character_count'")
    characters.extend(
        secrets.choice(string.ascii_letters + string.digits + special_chars)
        for _ in range(remaining_count)
    )
    secrets.SystemRandom().shuffle(characters)
    output_password = "".join(characters)
    # ! rare edgecase: it hasn't happened yet, but theoretically could
    # ! if the password is too insecure, you might get an infinite recursion error
    if shannon_entropy(output_password) <= minimum_shannon_entropy:
        return generate_secure_password(
            minimum_character_count,
            minimum_numeric_character_count,
            minimum_special_character_count,
            minimum_uppercase_character_count,
            minimum_lowercase_character_count,
            minimum_shannon_entropy,
        )
    else:
        return output_password


def partial_hide_secret(secret: str, show_fraction: int = 4):
    fraction_size = int(len(secret) / show_fraction)
    hidden_part_length = len(secret) - fraction_size
    hidden_text = "*" * hidden_part_length
    return f"{secret[:fraction_size]}{hidden_text}"

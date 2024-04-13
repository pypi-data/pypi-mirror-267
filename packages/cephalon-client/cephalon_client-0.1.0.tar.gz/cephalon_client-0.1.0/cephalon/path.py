from pathlib import Path


home: Path = Path.home()
cephalon: Path = home / ".cephalon"
credentials: Path = cephalon / "credentials.toml"
config: Path = cephalon / "config.toml"
cache: Path = cephalon / "cache"

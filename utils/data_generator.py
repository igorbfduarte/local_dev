import hashlib


def make_name(user_id: int) -> str:
    """Returns a deterministic name based on the user_id."""
    names = ["john", "jane", "ash", "misty", "brock"]
    # Use a hash of the ID to determine the index
    index = int(hashlib.md5(str(user_id).encode()).hexdigest(), 16) % len(
        names
    )
    return names[index]

from django.core import signing

def encode_id(pk):
    """Convert an integer ID into a signed string."""
    return signing.dumps(pk)

def decode_id(encoded_pk):
    """Convert a signed string back into an integer ID."""
    try:
        return signing.loads(encoded_pk)
    except signing.BadSignature:
        return None  # invalid or tampered

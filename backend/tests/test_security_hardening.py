import pytest
from app.core.security import validate_secret_strength, INSECURE_SECRET_PLACEHOLDERS
from app.ai.ollama_provider import LocalOllamaProvider

def test_validate_secret_strength_empty():
    is_valid, msg = validate_secret_strength("")
    assert not is_valid
    assert "cannot be empty" in msg

    is_valid, msg = validate_secret_strength(None)
    assert not is_valid

def test_validate_secret_strength_known_placeholders():
    for placeholder in INSECURE_SECRET_PLACEHOLDERS:
        is_valid, msg = validate_secret_strength(placeholder)
        assert not is_valid, f"Expected placeholder {placeholder} to be rejected"
        assert "insecure" in msg.lower() or "placeholder" in msg.lower()

def test_validate_secret_strength_keywords():
    bad_keys = [
        "my-super-insecure-key-that-is-longer-than-32-characters-123",
        "change-this-production-key-which-is-super-long-hex-random-987",
        "dev-secret-key-that-is-long-enough-for-testing-purposes-1234",
    ]
    for key in bad_keys:
        is_valid, msg = validate_secret_strength(key)
        assert not is_valid, f"Expected key '{key}' to be rejected"

def test_validate_secret_strength_short():
    short_key = "a8f3b9c2d1e0f4a7b8c9d0e1"  # 24 chars
    is_valid, msg = validate_secret_strength(short_key)
    assert not is_valid
    assert "too short" in msg

def test_validate_secret_strength_valid_strong_key():
    valid_key = "7f8b9a1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f90"
    is_valid, msg = validate_secret_strength(valid_key)
    assert is_valid
    assert "satisfies" in msg

def test_ollama_provider_url_normalization():
    prov = LocalOllamaProvider(base_url="host.docker.internal:11434")
    assert prov.base_url == "http://host.docker.internal:11434"

    prov2 = LocalOllamaProvider(base_url="http://192.168.1.50:11434/")
    assert prov2.base_url == "http://192.168.1.50:11434"

@pytest.mark.asyncio
async def test_ollama_graceful_fallback_on_unreachable():
    prov = LocalOllamaProvider(base_url="http://127.0.0.1:54321")
    # Generating text to unreachable port must not throw unhandled exception
    res = await prov.generate_text("test prompt")
    assert "Ollama Connection Error" in res or "Error" in res

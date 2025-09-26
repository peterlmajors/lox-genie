import platform

def use_vllm() -> bool:
    """
    Determine if vLLM can be used provided operating system
    """
    platform_info = platform.platform()
    if platform_info.contains("macOS") or platform_info.contains("Windows"):
        return False
    elif platform_info.contains("Linux"):
        return True
    else:
        print(f"Unknown platform: {platform_info}")
        return False
# -*- coding: utf-8 -*-
import os
from typing import Dict, Any, Optional

def create_granite_client(timeout_seconds: int = 30, prefer_lite: bool = False):
    """
    Smart factory function that chooses the best Granite client based on availability.
    
    Args:
        timeout_seconds: How long to wait for model download/loading
        prefer_lite: If True, use lite version even if full model is available
    
    Returns:
        GraniteClient or GraniteClientLite instance
    """
    
    if prefer_lite:
        print("🔧 Using Granite Lite by preference")
        from .granite_client_lite import GraniteClientLite
        return GraniteClientLite()
    
    # Check if full model is likely to be available quickly
    try:
        from huggingface_hub import snapshot_download
        model_path = "ibm-granite/granite-3.3-2b-base"
        
        # Try to access cached model
        try:
            cache_dir = snapshot_download(model_path, local_files_only=True)
            print("🚀 Granite model found in cache - attempting full initialization")
            
            # Try to load the full client with a reasonable timeout
            from .granite_client import GraniteClient
            client = GraniteClient(timeout_seconds=timeout_seconds)
            
            if client.initialized:
                print("✅ Full Granite AI client initialized successfully!")
                return client
            else:
                print("⚠️  Full model initialization incomplete - falling back to Lite mode")
                
        except Exception as e:
            print(f"📥 Model not cached - would require download (~5GB)")
            print("🔧 Using Granite Lite for immediate functionality")
    
    except ImportError:
        print("📦 HuggingFace Hub not available - using Lite mode")
    
    # Fall back to lite version
    from .granite_client_lite import GraniteClientLite
    return GraniteClientLite()


class GraniteSmartClient:
    """
    Smart wrapper that automatically chooses the best available Granite client
    """
    
    def __init__(self, timeout_seconds: int = 30, prefer_lite: bool = False):
        self.client = create_granite_client(timeout_seconds, prefer_lite)
    
    def __getattr__(self, name):
        """Delegate all method calls to the underlying client"""
        return getattr(self.client, name)
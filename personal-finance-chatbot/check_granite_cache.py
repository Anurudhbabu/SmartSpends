#!/usr/bin/env python3
"""
Check if Granite model is cached and ready
"""

import os
from huggingface_hub import snapshot_download

def check_granite_cache():
    """Check if the Granite model is already cached"""
    model_name = "ibm-granite/granite-3.3-2b-base"
    
    print("🔍 Checking Granite model cache...")
    
    try:
        # Try to find cached model
        cache_dir = snapshot_download(model_name, local_files_only=True)
        print(f"✅ Model is cached at: {cache_dir}")
        
        # Check cache size
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(cache_dir):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if os.path.exists(filepath):
                    total_size += os.path.getsize(filepath)
        
        size_gb = total_size / (1024**3)
        print(f"📦 Cache size: {size_gb:.2f} GB")
        
        if size_gb > 3.0:  # Model should be around 4-5GB
            print("🎉 Full model appears to be cached!")
            return True
        else:
            print("⚠️ Cache exists but may be incomplete")
            return False
            
    except Exception as e:
        print(f"❌ Model not cached: {e}")
        return False

if __name__ == "__main__":
    check_granite_cache()
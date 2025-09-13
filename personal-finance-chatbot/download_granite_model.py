#!/usr/bin/env python3
"""
Pre-download the Granite 3.3 2B model to cache for faster loading
"""

import os
import sys
from huggingface_hub import snapshot_download
import time

def download_granite_model():
    """Download and cache the Granite model"""
    print("🚀 Starting Granite 3.3 2B Model Download...")
    print("📦 Model size: ~5GB - this may take 10-20 minutes depending on internet speed")
    print("🔄 Once downloaded, the model will be cached locally for instant future use")
    
    model_name = "ibm-granite/granite-3.3-2b-base"
    
    try:
        start_time = time.time()
        
        # Download with progress tracking
        print(f"\n📥 Downloading {model_name}...")
        cache_dir = snapshot_download(
            repo_id=model_name,
            resume_download=True,
            cache_dir=None,  # Use default cache
            local_files_only=False
        )
        
        download_time = time.time() - start_time
        print(f"\n✅ Download completed in {download_time/60:.1f} minutes!")
        print(f"📁 Model cached at: {cache_dir}")
        
        # Test loading the model
        print("\n🧪 Testing model loading...")
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            import torch
            
            print("📝 Loading tokenizer...")
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            print("🧠 Loading model...")
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16,
                device_map="auto",
                low_cpu_mem_usage=True
            )
            
            print("✅ Model loaded successfully!")
            print("🎉 Granite 3.3 2B is ready for use!")
            
            # Clean up to free memory
            del model
            del tokenizer
            
        except Exception as e:
            print(f"⚠️ Model download succeeded but loading failed: {e}")
            print("💡 This may be due to insufficient memory - the app will use Lite mode as fallback")
            
    except Exception as e:
        print(f"❌ Download failed: {e}")
        print("💡 The app will fall back to Lite mode")
        return False
    
    return True

if __name__ == "__main__":
    print("🤖 Granite Model Downloader")
    print("=" * 50)
    
    # Check available disk space
    import shutil
    free_space = shutil.disk_usage(".").free / (1024**3)  # GB
    print(f"💾 Available disk space: {free_space:.1f} GB")
    
    if free_space < 10:
        print("⚠️ Warning: Less than 10GB free space. Model download may fail.")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("❌ Download cancelled")
            sys.exit(1)
    
    success = download_granite_model()
    
    if success:
        print("\n🎯 Next steps:")
        print("1. Run: streamlit run src/app.py")
        print("2. The app will now use the full Granite AI model")
        print("3. Expect more accurate, contextual responses")
    else:
        print("\n💡 Fallback option:")
        print("The app will automatically use Granite Lite mode")
        print("This provides instant responses with rule-based logic")
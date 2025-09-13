#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check the status of Granite AI without triggering downloads
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def check_granite_status():
    """Check Granite AI status without loading the model"""
    print("🔍 Granite AI Status Check\n")
    
    try:
        # Check if dependencies are available
        print("📦 Checking dependencies...")
        import torch
        print(f"✅ PyTorch: {torch.__version__}")
        
        import transformers
        print(f"✅ Transformers: {transformers.__version__}")
        
        # Check device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🖥️  Device: {device}")
        if device == "cuda":
            print(f"   GPU: {torch.cuda.get_device_name()}")
            print(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
        
        # Check cache status
        print("\n📁 Checking model cache...")
        try:
            from huggingface_hub import snapshot_download
            model_path = "granite-3.3-2b-base"
            cache_dir = snapshot_download(model_path, local_files_only=True)
            print(f"✅ Model is cached at: {cache_dir}")
            model_cached = True
        except Exception as e:
            print(f"❌ Model not cached: {str(e)}")
            model_cached = False
        
        # Test import without initialization
        print("\n🧪 Testing client import...")
        from chatbot.granite_client import GraniteClient
        print("✅ GraniteClient import successful")
        
        # Create client without full initialization
        print("\n⚡ Creating lightweight client...")
        client = GraniteClient(timeout_seconds=5)  # Very short timeout
        
        info = client.get_model_info()
        print(f"\n📊 Client Status:")
        print(f"   Model: {info['model_name']}")
        print(f"   Initialized: {info['initialized']}")
        print(f"   Device: {info['device']}")
        
        # Test fallback response
        print("\n💬 Testing response generation...")
        response = client.get_response("What is an emergency fund?", "student")
        print(f"✅ Response generated ({len(response)} chars)")
        print(f"   Preview: {response[:100]}...")
        
        # Status summary
        print(f"\n🎯 Summary:")
        if info['initialized']:
            print("   🟢 Granite AI is fully operational!")
        elif model_cached:
            print("   🟡 Model is cached but needs more time to load")
            print("   💡 Use longer timeout for full functionality")
        else:
            print("   🔴 Model needs to be downloaded (~5GB)")
            print("   💡 Run with extended timeout to download:")
            print("      python -c \"from src.chatbot.granite_client import GraniteClient; GraniteClient(timeout_seconds=3600)\"")
        
        print(f"   📋 Capabilities: {', '.join(info['capabilities'])}")
        
        return info['initialized']
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("🔧 Install with: pip install torch transformers accelerate")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = check_granite_status()
    exit_code = 0 if success else 1
    sys.exit(exit_code)
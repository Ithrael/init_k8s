#!/usr/bin/env python3
"""
JWKS 快速生成工具
根据 issuer 快速生成 JWKS 配置
"""

import sys
import json
from generate_jwks import generate_jwks_for_issuer, save_jwks_files

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python3 quick_jwks.py <issuer> [key_id]")
        print("示例: python3 quick_jwks.py anyong")
        print("示例: python3 quick_jwks.py my-company custom-key-id")
        sys.exit(1)
    
    issuer = sys.argv[1]
    key_id = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"正在为 issuer '{issuer}' 生成 JWKS...")
    
    # 生成 JWKS
    result = generate_jwks_for_issuer(issuer, key_id)
    
    # 保存文件
    files = save_jwks_files(result, output_dir="/Users/w/code/github/ithrael/init_k8s/shentu/output")
    
    print(f"\n✅ JWKS 生成完成！")
    print(f"\n生成的 JWKS:")
    print(json.dumps(result["jwks"], indent=2))
    
    print(f"\n文件保存位置:")
    for file_type, file_path in files.items():
        print(f"- {file_type}: {file_path}")
    
    print(f"\nKey ID: {result['key_id']}")
    print(f"Issuer: {result['issuer']}")
    print(f"Algorithm: {result['algorithm']}")

if __name__ == "__main__":
    main()
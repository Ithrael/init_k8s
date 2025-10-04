#!/usr/bin/env python3
"""
JWKS (JSON Web Key Set) 生成器
根据 issuer 生成 RSA 密钥对和 JWKS 配置
用于 Istio RequestAuthentication 配置
"""

import json
import base64
import uuid
from datetime import datetime
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


def base64url_encode(data):
    """Base64URL 编码（JWT 标准）"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')


def base64url_decode(data):
    """Base64URL 解码"""
    padding = 4 - len(data) % 4
    if padding != 4:
        data += '=' * padding
    return base64.urlsafe_b64decode(data)


def generate_rsa_keypair(key_size=2048):
    """
    生成 RSA 密钥对
    
    Args:
        key_size: 密钥长度，默认为 2048
    
    Returns:
        tuple: (private_key, public_key)
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


def encode_rsa_public_key_jwk(public_key, kid=None, use="sig", alg="RS256"):
    """
    将 RSA 公钥编码为 JWK 格式
    
    Args:
        public_key: RSA 公钥对象
        kid: Key ID，如果为 None 则自动生成
        use: 密钥用途，默认为 "sig" (签名)
        alg: 算法，默认为 "RS256"
    
    Returns:
        dict: JWK 格式的公钥信息
    """
    # 获取公钥参数
    public_numbers = public_key.public_numbers()
    
    # 将大整数转换为 Base64URL 编码
    n = base64url_encode(public_numbers.n.to_bytes(
        (public_numbers.n.bit_length() + 7) // 8, 'big'
    ))
    e = base64url_encode(public_numbers.e.to_bytes(
        (public_numbers.e.bit_length() + 7) // 8, 'big'
    ))
    
    # 生成 Key ID
    if kid is None:
        kid = base64url_encode(str(uuid.uuid4()))[:16]
    
    # 构建 JWK
    jwk = {
        "kty": "RSA",
        "kid": kid,
        "use": use,
        "alg": alg,
        "n": n,
        "e": e
    }
    
    return jwk


def encode_rsa_private_key_pem(private_key, password=None):
    """
    将 RSA 私钥编码为 PEM 格式
    
    Args:
        private_key: RSA 私钥对象
        password: 加密密码，如果为 None 则不加密
    
    Returns:
        bytes: PEM 格式的私钥
    """
    if password:
        # 使用密码加密
        encryption_algorithm = serialization.BestAvailableEncryption(
            password.encode() if isinstance(password, str) else password
        )
    else:
        # 不加密
        encryption_algorithm = serialization.NoEncryption()
    
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption_algorithm
    )
    
    return pem


def generate_jwks_for_issuer(issuer, key_id=None, key_size=2048):
    """
    为指定的 issuer 生成 JWKS
    
    Args:
        issuer: JWT issuer
        key_id: 密钥 ID，如果为 None 则自动生成
        key_size: RSA 密钥长度
    
    Returns:
        dict: 包含 JWKS 和相关信息
    """
    print(f"正在为 issuer '{issuer}' 生成 JWKS...")
    
    # 生成 RSA 密钥对
    private_key, public_key = generate_rsa_keypair(key_size)
    print(f"✓ 生成 {key_size} 位 RSA 密钥对")
    
    # 生成 JWK
    jwk = encode_rsa_public_key_jwk(public_key, kid=key_id)
    print(f"✓ 生成 JWK，Key ID: {jwk['kid']}")
    
    # 生成 JWKS
    jwks = {
        "keys": [jwk]
    }
    
    # 生成私钥 PEM
    private_key_pem = encode_rsa_private_key_pem(private_key)
    print("✓ 生成私钥 PEM 文件")
    
    return {
        "issuer": issuer,
        "jwks": jwks,
        "private_key_pem": private_key_pem,
        "key_id": jwk['kid'],
        "algorithm": jwk['alg'],
        "key_type": jwk['kty']
    }


def save_jwks_files(result, output_dir="./"):
    """
    保存 JWKS 相关文件
    
    Args:
        result: generate_jwks_for_issuer 的结果
        output_dir: 输出目录
    """
    import os
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    issuer = result["issuer"]
    key_id = result["key_id"]
    
    # 保存 JWKS JSON 文件
    jwks_file = os.path.join(output_dir, f"jwks_{issuer}.json")
    with open(jwks_file, 'w', encoding='utf-8') as f:
        json.dump(result["jwks"], f, indent=2, ensure_ascii=False)
    print(f"✓ JWKS 已保存到: {jwks_file}")
    
    # 保存私钥 PEM 文件
    private_key_file = os.path.join(output_dir, f"private_key_{issuer}_{key_id}.pem")
    with open(private_key_file, 'wb') as f:
        f.write(result["private_key_pem"])
    print(f"✓ 私钥已保存到: {private_key_file}")
    
    # 生成 Istio RequestAuthentication 配置
    auth_config = generate_istio_auth_config(result)
    auth_file = os.path.join(output_dir, f"jwt-auth-{issuer}.yml")
    with open(auth_file, 'w', encoding='utf-8') as f:
        f.write(auth_config)
    print(f"✓ Istio 配置已保存到: {auth_file}")
    
    return {
        "jwks_file": jwks_file,
        "private_key_file": private_key_file,
        "auth_config_file": auth_file
    }


def generate_istio_auth_config(jwks_result):
    """
    生成 Istio RequestAuthentication 配置
    
    Args:
        jwks_result: generate_jwks_for_issuer 的结果
    
    Returns:
        str: YAML 格式的配置
    """
    issuer = jwks_result["issuer"]
    jwks_json = json.dumps(jwks_result["jwks"], separators=(',', ':'))
    
    config = f"""apiVersion: security.istio.io/v1beta1
kind: RequestAuthentication
metadata:
  name: "jwt-{issuer}"
  namespace: istio-system
spec:
  selector:
    matchLabels:
      tier: api
  jwtRules:
    - issuer: "{issuer}"
      jwks: '{jwks_json}'
      outputPayloadToHeader: x-jwt-payload
      fromHeaders:
        - name: Authorization
          prefix: "Bearer "
"""
    
    return config


def main():
    """主函数"""
    print("=== JWKS 生成器 ===")
    print("根据 issuer 生成 RSA 密钥对和 JWKS 配置")
    print()
    
    # 示例：为不同的 issuer 生成 JWKS
    issuers = [
        "anyong",  # 你的当前 issuer
        "my-company",
        "test-issuer"
    ]
    
    for issuer in issuers:
        print(f"\n--- 处理 issuer: {issuer} ---")
        
        # 生成 JWKS
        result = generate_jwks_for_issuer(issuer)
        
        # 保存文件
        files = save_jwks_files(result, output_dir="/Users/w/code/github/ithrael/init_k8s/shentu/output")
        
        # 显示 JWKS 内容
        print(f"\n生成的 JWKS:")
        print(json.dumps(result["jwks"], indent=2))
        
        # 显示 Key ID
        print(f"\nKey ID: {result['key_id']}")
        print(f"算法: {result['algorithm']}")
        print(f"密钥类型: {result['key_type']}")
        
        print("\n" + "="*60)
    
    print("\n✅ 所有 JWKS 生成完成！")
    print("\n文件说明:")
    print("- jwks_<issuer>.json: JWKS 公钥集合")
    print("- private_key_<issuer>_<kid>.pem: RSA 私钥（保密）")
    print("- jwt-auth-<issuer>.yml: Istio RequestAuthentication 配置")


if __name__ == "__main__":
    main()

# 工具函数
def load_existing_jwks(jwks_file):
    """加载现有的 JWKS 文件"""
    try:
        with open(jwks_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def validate_jwks(jwks):
    """验证 JWKS 格式"""
    if not isinstance(jwks, dict):
        return False, "JWKS 必须是字典格式"
    
    if "keys" not in jwks:
        return False, "JWKS 必须包含 'keys' 字段"
    
    if not isinstance(jwks["keys"], list):
        return False, "'keys' 必须是数组"
    
    for i, key in enumerate(jwks["keys"]):
        if key.get("kty") != "RSA":
            return False, f"第 {i+1} 个密钥必须是 RSA 类型"
        
        required_fields = ["n", "e", "kid", "alg"]
        for field in required_fields:
            if field not in key:
                return False, f"第 {i+1} 个密钥缺少 '{field}' 字段"
    
    return True, "JWKS 格式正确"

def generate_jwks_from_existing_key(n, e, kid, alg="RS256", use="sig"):
    """
    从现有的 RSA 参数生成 JWKS
    
    Args:
        n: RSA 模数 (Base64URL 编码)
        e: RSA 公钥指数 (Base64URL 编码)
        kid: Key ID
        alg: 算法
        use: 用途
    
    Returns:
        dict: JWKS 格式
    """
    return {
        "keys": [{
            "kty": "RSA",
            "kid": kid,
            "use": use,
            "alg": alg,
            "n": n,
            "e": e
        }]
    }
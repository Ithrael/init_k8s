#!/usr/bin/env python3
"""
JWT Token Generator for Istio RequestAuthentication
使用配置中的 issuer 和 JWKS 生成 JWT token
"""

import json
import base64
import time
import os
from datetime import datetime, timedelta
import jwt
from cryptography.hazmat.primitives import serialization

# 从配置中提取的 JWKS 数据
JWKS_DATA = {
    "keys":[{"kty":"RSA","kid":"OGU5MjA5ODYtZDAz","use":"sig","alg":"RS256","n":"oBL_hYFfZhraMXb-ZQcqafBWO32jz3p1Do8Ykkns7XdOowCiumSj4Nb8M2XVHEGS8L2TiYSGbAy3TSi4zd-JHv5vQPDM5JnuauvYwY7MWpbDAvQVCyo5tfR4NK4naHTkH4pfexoszY8w0Mj1CynmllBAR0CZIXNe9TcXtcyBh_UUVB0ObIjAWXrVEWkhxMPq58Nscg2B3cmMBtwwAgZFlAWqDbNpdUjv7uhyEwDovj3hFOGI_6hlW9pASjZI_5bxU5oGD6R3fkPoXGjSQFrtu0d1zTTne8MrZrIJDsMdK_i0BhJ6WTLqqBzkNDJfSS2aEuSlp9DM0d0M5-E1AYXLlw","e":"AQAB"}]
}

# 从配置中提取的 issuer
ISSUER = "anyong"

# JWT 声明配置
USER_ID = "user-123"
USER_ROLE = 1
NS = "test"

# 私钥文件路径
PRIVATE_KEY_PATH = os.path.join(os.path.dirname(__file__), "output", "private_key_anyong_OGU5MjA5ODYtZDAz.pem")

def create_jwt_token(user_id=None, user_role=None, user_ns=None,expiry_hours=24):
    """
    创建 JWT token
    
    Args:
        user_id: 用户ID，默认为 test-user-123
        user_role: 用户角色，默认为 admin
        user_ns: 用户命名空间，默认为 default

        expiry_hours: token 过期时间（小时），默认为 24 小时
    
    Returns:
        str: 生成的 JWT token
    """
    if user_id is None:
        user_id = USER_ID
    if user_role is None:
        user_role = USER_ROLE
    if user_ns is None:
        user_ns = NS
    
    # 获取当前时间和过期时间
    now = datetime.utcnow()
    expiry = now + timedelta(hours=expiry_hours)
    
    # 构建 JWT payload
    payload = {
        "iss": ISSUER,  # issuer
        "sub": user_id,  # subject (用户ID)
        "UserId": user_id,  # 自定义声明，用于 EnvoyFilter 解析
        "UserRole": user_role,  # 自定义声明，用于 EnvoyFilter 解析
        "NS": user_ns, # 自定义声明，用于 EnvoyFilter 解析
        "iat": int(now.timestamp()),  # issued at
        "exp": int(expiry.timestamp()),  # expiration time
        "nbf": int(now.timestamp()),  # not before
    }
    print(payload)
    
    # 从 JWKS 获取公钥信息
    key_data = JWKS_DATA["keys"][0]
    kid = key_data["kid"]
    
    # 从文件中加载实际的私钥
    if not os.path.exists(PRIVATE_KEY_PATH):
        raise FileNotFoundError(f"私钥文件不存在: {PRIVATE_KEY_PATH}\n请先运行 generate_jwks.py 生成私钥文件。")
    
    with open(PRIVATE_KEY_PATH, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
    
    # 生成 JWT token
    token = jwt.encode(
        payload,
        private_key,
        algorithm="RS256",
        headers={
            "kid": kid,
            "typ": "JWT",
            "alg": "RS256"
        }
    )
    
    return token

def decode_jwt_token(token):
    """
    解码 JWT token（仅用于测试）
    
    Args:
        token: JWT token
    
    Returns:
        dict: 解码后的 payload
    """
    try:
        # 注意：这里我们没有提供公钥，所以无法验证签名
        # 仅用于查看 token 内容
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload
    except jwt.InvalidTokenError as e:
        print(f"Token 解码失败: {e}")
        return None

def main():
    """主函数"""
    print("=== JWT Token Generator ===")
    print(f"Issuer: {ISSUER}")
    print(f"Default User ID: {USER_ID}")
    print(f"Default User Role: {USER_ROLE}")
    print()
    
    # 生成 token
    token = create_jwt_token()
    print(f"生成的 JWT Token:")
    print(f"{token}")
    print()
    
    # 解码查看内容
    decoded = decode_jwt_token(token)
    if decoded:
        print("Token 内容:")
        print(json.dumps(decoded, indent=2, ensure_ascii=False))
        print()
        
        # 显示过期时间
        exp_timestamp = decoded.get("exp", 0)
        exp_datetime = datetime.fromtimestamp(exp_timestamp)
        print(f"过期时间: {exp_datetime} (UTC)")
        
        # 显示剩余有效时间
        now = datetime.utcnow()
        remaining = exp_datetime - now
        print(f"剩余有效时间: {remaining}")

if __name__ == "__main__":
    main()

# 使用示例函数
def generate_custom_token(user_id, user_role, expiry_hours=24):
    """
    生成自定义 JWT token
    
    Args:
        user_id: 自定义用户ID
        user_role: 自定义用户角色
        expiry_hours: 过期时间（小时）
    
    Returns:
        str: JWT token
    """
    return create_jwt_token(user_id=user_id, user_role=user_role, expiry_hours=expiry_hours)

def test_with_different_users():
    """测试不同用户"""
    test_cases = [
        {"user_id": "admin-001", "user_role": "admin"},
        {"user_id": "user-123", "user_role": "user"},
        {"user_id": "guest-999", "user_role": "guest"},
    ]
    
    print("\n=== 测试不同用户 ===")
    for case in test_cases:
        token = generate_custom_token(case["user_id"], case["user_role"], expiry_hours=1)
        decoded = decode_jwt_token(token)
        print(f"用户: {case['user_id']} (角色: {case['user_role']})")
        print(f"Token: {token[:50]}...")
        print(f"过期时间: {datetime.fromtimestamp(decoded['exp'])} UTC")
        print()
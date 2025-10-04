-- 简化版 JWT Token 解析器
-- 用于直接解析和显示 JWT token 的 payload 内容

-- Base64 解码函数（简化版，修复了位模式处理问题）
function from_base64(s)
    local base64_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    local buffer = {}
    
    -- 处理填充字符
    s = string.gsub(s, '=', '')
    
    for i = 1, #s, 4 do
        if i+3 <= #s then
            local a_val = string.find(base64_chars, string.sub(s, i, i), 1, true) - 1
            local b_val = string.find(base64_chars, string.sub(s, i+1, i+1), 1, true) - 1
            local c_val = string.find(base64_chars, string.sub(s, i+2, i+2), 1, true) - 1
            local d_val = string.find(base64_chars, string.sub(s, i+3, i+3), 1, true) - 1
            
            if a_val and b_val then
                table.insert(buffer, string.char((a_val*4 + math.floor(b_val/16)) % 256))
                if c_val then
                    table.insert(buffer, string.char(((b_val*16) % 256) + math.floor(c_val/4)))
                    if d_val then
                        table.insert(buffer, string.char(((c_val*64) % 256) + d_val))
                    end
                end
            end
        end
    end
    
    return table.concat(buffer)
end

-- 提取用户信息
function extract_user_info(payload)
    local user_info = {}
    local decoded_payload = from_base64(payload)
    
    -- 提取 UserId
    local user_id = decoded_payload:match('"UserId":"([^"]+)"')
    if user_id then
        user_info.user_id = user_id
    end
    
    -- 提取 UserRole（兼容数字和字符串类型）
    local user_role = decoded_payload:match('"UserRole":([%d]+)') or decoded_payload:match('"UserRole":"([^"]+)"')
    if user_role then
        user_info.user_role = user_role
    end
    
    -- 提取 UserNs
    local user_ns = decoded_payload:match('"UserNs":"([^"]+)"')
    if user_ns then
        user_info.user_ns = user_ns
    end
    
    -- 提取 NS
    local ns = decoded_payload:match('"NS":"([^"]+)"')
    if ns then
        user_info.ns = ns
    end
    
    -- 提取其他主要字段
    local iss = decoded_payload:match('"iss":"([^"]+)"')
    if iss then
        user_info.issuer = iss
    end
    
    local sub = decoded_payload:match('"sub":"([^"]+)"')
    if sub then
        user_info.subject = sub
    end
    
    return user_info, decoded_payload
end

-- 解析 JWT token
function parse_jwt_token(jwt_token)
    -- 移除 Bearer 前缀（如果有）
    local token = jwt_token:gsub("Bearer ", "")
    
    -- 分割 JWT token 为三部分：header.payload.signature
    local parts = {}
    local part = ""
    for i = 1, #token do
        local char = token:sub(i, i)
        if char == '.' then
            if part ~= "" then
                table.insert(parts, part)
                part = ""
            end
        else
            part = part .. char
        end
    end
    if part ~= "" then
        table.insert(parts, part)
    end
    
    if #parts < 2 then
        error("无效的 JWT token 格式")
    end
    
    local header = parts[1]
    local payload = parts[2]
    local signature = parts[3] or ""
    
    -- 提取用户信息
    local user_info, decoded_payload = extract_user_info(payload)
    
    -- 返回完整信息
    return {
        token = token,
        header = header,
        payload = payload,
        signature = signature,
        user_info = user_info,
        raw_payload = decoded_payload
    }
end

-- 打印解析结果
function print_parsed_result(result)
    print("=== JWT Token 解析结果 ===")
    print("原始 token: " .. result.token)
    print("")
    print("Payload 内容:")
    print(result.raw_payload)
    print("")
    print("提取的用户信息:")
    for key, value in pairs(result.user_info) do
        print("  " .. key .. ": " .. value)
    end
end

-- 测试用的 JWT token
local test_token = "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Ik9HVTVNakE1T0RZdFpEQXoiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhbnlvbmciLCJzdWIiOiJ0ZXN0LXVzZXItMTIzIiwiVXNlcklkIjoidGVzdC11c2VyLTEyMyIsIlVzZXJSb2xlIjowLCJVc2VyTnMiOiJkZWZhdWx0IiwiaWF0IjoxNzU5NDcxMzY4LCJleHAiOjE3NTk1NTc3NjgsIm5iZiI6MTc1OTQ3MTM2OH0.IwnKfdgfNQCaYY0xtnkEnHGxTT1IHXostLG0PSSry1UJvtJ6MeG8K63asBQ1XI1opimTP7l2ghg2KezA6Q7FY4nFwYrXsyWisI7MzZ5XLndt3rBmwteJb1DnwJtuh0QYPc0xW-PmHx_SjDuMdXIDEmk214Qlwhk-xSH1BUMR4w1HKAOq45IqM_T7ButNxTSFA9zLupDYKhIRvccY4F7brxFTIERdZK09-CVjHnCevNPVh7JkwbH3LDojuscHmUKqSn_x0KGhVZ-kScGx5BO3zyp7J6ycUUi0rP-BXWyyGgYXvLBHz9ylg-OSwmSqgRnm0qJ_LdjxTixe9qb41_8hqw"

-- 解析 JWT token
local result = parse_jwt_token(test_token)

-- 打印结果
print_parsed_result(result)
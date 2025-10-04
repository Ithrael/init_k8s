-- JWT Parser Lua Module
-- 从 JWT payload 中解析用户信息

-- 二进制转换函数
function to_binary(integer)
    local remaining = tonumber(integer)
    local bin_bits = ''

    for i = 7, 0, -1 do
        local current_power = 2 ^ i

        if remaining >= current_power then
            bin_bits = bin_bits .. '1'
            remaining = remaining - current_power
        else
            bin_bits = bin_bits .. '0'
        end
    end

    return bin_bits
end

-- 从二进制转换为十进制
function from_binary(bin_bits)
    return tonumber(bin_bits, 2)
end

-- Base64 解码函数
function from_base64(to_decode)
    local index_table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

    local padded = to_decode:gsub("%s", "")
    local unpadded = padded:gsub("=", "")
    local bit_pattern = ''
    local decoded = ''

    for i = 1, string.len(unpadded) do
        local char = string.sub(to_decode, i, i)
        local offset, _ = string.find(index_table, char)
        if offset == nil then
            error("Invalid character '" .. char .. "' found.")
        end

        bit_pattern = bit_pattern .. string.sub(to_binary(offset-1), 3)
    end

    for i = 1, string.len(bit_pattern), 8 do
        local byte = string.sub(bit_pattern, i, i+7)
        decoded = decoded .. string.char(from_binary(byte))
    end

    local padding_length = padded:len()-unpadded:len()

    if (padding_length == 1 or padding_length == 2) then
        decoded = decoded:sub(1,-2)
    end
    return decoded
end

-- 提取 JWT payload 中的用户信息
-- @param payload Base64 编码的 JWT payload
-- @return table 包含用户信息的表
function extract_user_info(payload)
    local s = from_base64(payload)
    local user_info = {}
    
    -- 提取用户 ID
    for item in string.gmatch(s, 'UserId":"([%w|-]+)"') do
        user_info.user_id = item
    end

    -- 提取用户角色（同时兼容数字和字符串类型）
    for item in string.gmatch(s, 'UserRole":(%w+)') do
        user_info.user_role = item
    end
    for item in string.gmatch(s, 'UserRole":"([%w|-]+)"') do
        user_info.user_role = item
    end

    -- 提取用户命名空间
    for item in string.gmatch(s, 'UserNs":"([%w|-]+)"') do
        user_info.user_ns = item
    end
    
    -- 提取 NS 字段（旧版兼容）
    for item in string.gmatch(s, 'NS":"([%w|-]+)"') do
        user_info.ns = item
    end
    
    return user_info
end

-- Envoy 过滤器回调函数
function envoy_on_request(request_handle)
    local payload = request_handle:headers():get("X-Jwt-Payload");
    if payload then
        local user_info = extract_user_info(payload)
        
        -- 添加提取的用户信息到请求头
        if user_info.user_id then
            request_handle:headers():add("x-user-id", user_info.user_id)
        end
        
        if user_info.user_role then
            request_handle:headers():add("x-user-role", user_info.user_role)
        end
        
        if user_info.user_ns then
            request_handle:headers():add("x-user-ns", user_info.user_ns)
        end
        
        -- 旧版兼容
        if user_info.ns then
            request_handle:headers():add("x-ns", user_info.ns)
        end
    end
end

-- 模块导出（如果需要在其他地方使用）
return {
    from_base64 = from_base64,
    extract_user_info = extract_user_info,
    envoy_on_request = envoy_on_request
}
import requests
import base64

# 1. 在这里填入你想采集的公开订阅源URL (支持Base64或明文格式)
# 这里内置了几个常见的公开测试源作为演示
# 替换为你 main.py 中的 SOURCES 部分
SOURCES = [
    # 1. aiboboxx 每日更新的高质量 V2ray 源 (更新极快，存活率较高)
    "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2",
    
    # 2. ermaozi 自动抓取并测速的订阅源
    "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt",
    
    # 3. pawdroid 全网节点聚合池 (基数大，包含大量 VLESS/VMess/Trojan)
    "https://raw.githubusercontent.com/pawdroid/Free-servers/main/Sub",
    
    # 4. mahdibland 全球最大的 Shadowsocks/V2ray 聚合池之一 (Eternity 版本)
    "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity",
    
    # 5. Mfuu 自动抓取测速源
    "https://raw.githubusercontent.com/mfuu/v2ray/master/v2ray",
    
    # 6. tbbatbb 每日活跃节点聚合
    "https://raw.githubusercontent.com/tbbatbb/Proxy/master/main/v2ray.txt"
]

def decode_base64(data):
    """尝试解码 Base64，如果是明文则原样返回"""
    try:
        # 补齐 base64 的 '=' 后缀
        missing_padding = len(data) % 4
        if missing_padding:
            data += '=' * (4 - missing_padding)
        return base64.b64decode(data).decode('utf-8')
    except Exception:
        return data

def main():
    raw_nodes = []
    
    # 2. 遍历抓取每个源
    for url in SOURCES:
        print(f"正在获取源: {url}")
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                content = response.text.strip()
                decoded_content = decode_base64(content)
                
                # 逐行读取，提取有效节点链接
                for line in decoded_content.splitlines():
                    line = line.strip()
                    # 识别常见的代理协议
                    if line.startswith(('vmess://', 'vless://', 'ss://', 'ssr://', 'trojan://')):
                        raw_nodes.append(line)
        except Exception as e:
            print(f"获取 {url} 失败: {e}")

    # 3. 节点去重
    unique_nodes = list(set(raw_nodes))
    print(f"采集完成！共获取到 {len(unique_nodes)} 个去重节点。")

    # 4. 重新编码为 Base64 (代理软件通用的订阅格式)
    final_content = '\n'.join(unique_nodes)
    encoded_sub = base64.b64encode(final_content.encode('utf-8')).decode('utf-8')

    # 5. 保存为 sub.txt 文件
    with open('sub.txt', 'w') as f:
        f.write(encoded_sub)

if __name__ == '__main__':
    main()

import requests
import base64

# 1. 在这里填入你想采集的公开订阅源URL (支持Base64或明文格式)
# 这里内置了几个常见的公开测试源作为演示
# 替换为你 main.py 中的 SOURCES 部分
SOURCES = [
    # Mahdibland 的高频测速聚合源 (非常知名，几小时更新一次，去除了死节点)
    "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity",
    
    # 自动代理池 (经过可用性过滤)
    "https://raw.githubusercontent.com/w1770946466/Auto_Proxy/main/Subscription/V2ray.txt",
    
    # mfuu 的高频更新源
    "https://raw.githubusercontent.com/mfuu/v2ray/master/v2ray",
    
    # Pawdroid 提供的过滤后订阅
    "https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub",
    
    # 也可以加上一些专门收集 tg 频道的源
    "https://raw.githubusercontent.com/tbbatbb/Proxy/master/manual/v2ray.txt"
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

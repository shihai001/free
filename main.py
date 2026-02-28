import requests
import base64

# 1. 在这里填入你想采集的公开订阅源URL (支持Base64或明文格式)
# 这里内置了几个常见的公开测试源作为演示
# 替换为你 main.py 中的 SOURCES 部分
SOURCES = [
    # Barry-far 的高频更新聚合（目前全球最大的存活节点池之一，每隔几小时清洗一次）
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub1.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub2.txt",
    
    # NodeFree 每日实时更新源 (质量相对较高)
    "https://nodefree.org/dy/v2ray.txt",
    
    # 一个专门抓取 TG 频道新鲜节点的动态 API
    "https://sub.bonds.id/v2?pt=v2ray",
    
    # 纯 Base64 每日更新源
    "https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list.txt"
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

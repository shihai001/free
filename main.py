import requests
import base64

# 1. 在这里填入你想采集的公开订阅源URL (支持Base64或明文格式)
# 这里内置了几个常见的公开测试源作为演示
# 替换为你 main.py 中的 SOURCES 部分
SOURCES = [
    # 1. Epodonios (极冷门源，伊朗开发者维护，号称每 5 分钟执行一次 Actions 抓取)
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/All_Configs_base64_Sub.txt",

    # 2. MatinGhanbari (高质量中东冷门源，每 15 分钟更新，带节点去重机制)
    "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/v2ray/all_sub.txt",
    
    # 3. ebrasha (非常纯净的节点池，每 15 分钟清洗一次，自动剔除失效节点)
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/main/all_extracted_configs.txt",

    # 4. topvpnlist (通过 V2rayCollector 自动搜刮全网小众博客的源，每天多次更新)
    "https://raw.githubusercontent.com/topvpnlist/topvpnlist.github.io/main/subscriptions/all.txt",

    # 5. soroushmirzaei (专门抓取电报群的实时 VLESS 节点，国内用的人少，连通率不错)
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vless",
    
    # 6. soroushmirzaei (同上，VMess 专属节点池)
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vmess"
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

"""
创建模拟皮肤图片
生成赛博朋克风格的测试皮肤
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_cyberpunk_skin(filename, color_theme):
    """
    创建赛博朋克风格的皮肤

    Args:
        filename: 保存的文件名
        color_theme: 颜色主题 (primary, secondary, accent)
    """

    # 颜色配置
    color_schemes = {
        'purple': {
            'primary': (180, 0, 255),
            'secondary': (255, 0, 128),
            'accent': (0, 255, 255),
            'bg': (20, 10, 40)
        },
        'cyan': {
            'primary': (0, 255, 255),
            'secondary': (0, 128, 255),
            'accent': (128, 255, 0),
            'bg': (10, 20, 40)
        },
        'pink': {
            'primary': (255, 0, 128),
            'secondary': (255, 0, 255),
            'accent': (255, 128, 0),
            'bg': (40, 10, 20)
        }
    }

    colors = color_schemes[color_theme]

    # 创建图片
    img = Image.new('RGB', (512, 512), colors['bg'])
    draw = ImageDraw.Draw(img)

    # 绘制霓虹网格
    for i in range(0, 512, 32):
        draw.line([(0, i), (512, i)], fill=colors['primary'][:3], width=1)
        draw.line([(i, 0), (i, 512)], fill=colors['primary'][:3], width=1)

    # 绘制蛇形纹理（渐变矩形）
    for i in range(0, 512, 64):
        # 绘制多层渐变
        for offset in range(8, 0, -1):
            alpha = int(255 * (8 - offset) / 8)
            # 混合颜色
            r = int((colors['primary'][0] * offset + colors['secondary'][0] * (8 - offset)) / 8)
            g = int((colors['primary'][1] * offset + colors['secondary'][1] * (8 - offset)) / 8)
            b = int((colors['primary'][2] * offset + colors['secondary'][2] * (8 - offset)) / 8)
            draw.rectangle(
                [i + offset, offset, i + 64 - offset, 512 - offset],
                fill=(r, g, b)
            )

        # 添加发光边框
        draw.rectangle([i - 3, 0, i + 67, 512], outline=colors['accent'], width=3)

    # 添加文字
    try:
        # 尝试加载系统字体
        font_large = ImageFont.truetype("arial.ttf", 48)
        font_small = ImageFont.truetype("arial.ttf", 32)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # 文字阴影
    text1 = "CYBERPUNK"
    text2 = "SNAKE SKIN"

    # 计算文字位置
    bbox1 = draw.textbbox((0, 0), text1, font=font_large)
    text1_width = bbox1[2] - bbox1[0]
    text1_height = bbox1[3] - bbox1[1]

    bbox2 = draw.textbbox((0, 0), text2, font=font_small)
    text2_width = bbox2[2] - bbox2[0]
    text2_height = bbox2[3] - bbox2[1]

    # 绘制文字阴影
    shadow_offset = 5
    pos1_x = (512 - text1_width) // 2
    pos1_y = (512 - text1_height) // 2 - 60
    pos2_x = (512 - text2_width) // 2
    pos2_y = (512 - text2_height) // 2 + 60

    draw.text((pos1_x + shadow_offset, pos1_y + shadow_offset), text1,
             fill=(0, 0, 0), font=font_large)
    draw.text((pos2_x + shadow_offset, pos2_y + shadow_offset), text2,
             fill=(0, 0, 0), font=font_small)

    # 绘制发光文字
    draw.text((pos1_x, pos1_y), text1, fill=colors['accent'], font=font_large)
    draw.text((pos2_x, pos2_y), text2, fill=colors['secondary'], font=font_small)

    # 添加装饰性元素
    # 四角装饰
    corner_size = 40
    for x, y in [(10, 10), (502 - corner_size, 10),
                  (10, 502 - corner_size), (502 - corner_size, 502 - corner_size)]:
        draw.rectangle([x, y, x + corner_size, y + corner_size],
                     outline=colors['accent'], width=3)
        draw.rectangle([x + 5, y + 5, x + corner_size - 5, y + corner_size - 5],
                     outline=colors['primary'], width=2)

    return img

def main():
    """主函数"""
    print("=" * 60)
    print("创建模拟皮肤图片")
    print("=" * 60)

    # 确保存储目录存在
    os.makedirs("data/skins", exist_ok=True)

    # 创建三个不同颜色的皮肤
    skins = [
        ("mock_skin_1.png", "purple", "赛博朋克紫"),
        ("mock_skin_2.png", "cyan", "赛博朋克青"),
        ("mock_skin_3.png", "pink", "赛博朋克粉")
    ]

    for filename, theme, description in skins:
        print(f"\n创建 {description}...")
        img = create_cyberpunk_skin(filename, theme)

        # 保存图片
        filepath = os.path.join("data/skins", filename)
        img.save(filepath, 'PNG')
        print(f"[OK] 已保存: {filepath}")

    print("\n" + "=" * 60)
    print("完成！共创建 3 张皮肤图片")
    print("=" * 60)
    print("\n文件位置: data/skins/")
    print("访问地址: http://127.0.0.1:5000/api/skin/image/mock_skin_1.png")

if __name__ == "__main__":
    main()

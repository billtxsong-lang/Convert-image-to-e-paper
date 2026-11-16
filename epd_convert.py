from PIL import Image

def convert_image_to_epd_array(image_path, output_c_path):
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print(f"错误：找不到图片文件 -> {image_path}")
        return

    img = img.resize((400, 300)).convert("1")
    
    width, height = img.size
    hex_array = []
    
    for y in range(height):
        for x in range(0, width, 8):
            byte = 0
            for bit in range(8):
                if x + bit < width:
                    pixel_color = img.getpixel((x + bit, y))
                    if pixel_color == 0: 
                        byte |= (1 << (7 - bit))
            hex_array.append(byte)

    c_code = f"const unsigned char epd_image_data[{len(hex_array)}] = {{\n"
    hex_lines = [", ".join(hex(b) for b in hex_array[i:i+16]) for i in range(0, len(hex_array), 16)]
    c_code += ",\n".join(hex_lines)
    c_code += "\n};\n"

    with open(output_c_path, "w", encoding="utf-8") as f:
        f.write(c_code)
    
    print(f"转换成功！C 语言数组已保存至：{output_c_path}")
    print(f"总字节数：{len(hex_array)} Bytes")

if __name__ == "__main__":
    input_image = "your_image.png" 
    output_file = "epd_image.h"
    
    convert_image_to_epd_array(input_image, output_file)
from PIL import Image
from PIL import ImageOps
from screeninfo import get_monitors
import os


def set_wallpaper(path, mode="spanned"):
    cmd = f"""
dconf write /org/gnome/desktop/background/picture-uri-dark "'file://{path}'"
dconf write /org/gnome/desktop/background/picture-uri "'file://{path}'"
dconf write /org/gnome/desktop/background/picture-options "'{mode}'"
"""
    os.system(cmd)


class MultipleMonitorsWallpaperManager:
    def __init__(self, wallpapers):
        self.width = 0
        self.height = 0
        self.positions = []
        self.wallpapers = [os.path.abspath(wallpaper) for wallpaper in wallpapers]
        self.run()

    def resize_and_pad(self, img, size):
        """将 img 等比缩放到 size，空白填充为 color"""
        return ImageOps.pad(img, size, color=(0,0,0), method=Image.LANCZOS)

    def resize_and_crop(self, img, size):
        """将 img 等比缩放并裁剪到 size"""
        return ImageOps.fit(img, size, method=Image.LANCZOS)
    
    def run(self):
        for m in get_monitors():
            self.width += m.width
            self.height = max(self.height, m.height)
            self.positions.append({
                'x': m.x,
                'y': m.y,
                'width': m.width,
                'height': m.height
            })

        # 1. 创建指定大小的黑色图片
        black_img = Image.new('RGB', (self.width, self.height), color=(0, 0, 0))

        # 3. 设置图片到x,y位置
        for i, item in enumerate(self.positions):
            img_path = self.wallpapers[i]
            if not os.path.exists(img_path):
                print(f"图片 {img_path} 不存在，跳过。")
                continue  # 跳过
            img = Image.open(img_path)
            img = self.resize_and_crop(img, (item['width'], item['height']))
            x = item['x']
            y = item['y']
            black_img.paste(img, (x, y))

        # 4. 保存或显示结果
        black_img.save('result.png')
        set_wallpaper(os.path.join(os.getcwd(), 'result.png'), mode='spanned')


MultipleMonitorsWallpaperManager(wallpapers=['./images/0.jpg', './images/1.jpg', './images/2.jpg'])
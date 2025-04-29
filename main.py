from PIL import Image
from PIL import ImageOps
from screeninfo import get_monitors
import os
import random
import sys
import time

real_dir = os.path.dirname(os.path.abspath(sys.argv[0]))


def set_wallpaper(path, mode="spanned"):
    cmd = f"""
dconf write /org/gnome/desktop/background/picture-uri-dark "'file://{path}'"
dconf write /org/gnome/desktop/background/picture-uri "'file://{path}'"
dconf write /org/gnome/desktop/background/picture-options "'{mode}'"
"""
    os.system(cmd)


class MultipleMonitorsWallpaperManager:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.positions = []
        for m in get_monitors():
            self.width += m.width
            self.height = max(self.height, m.height)
            self.positions.append({
                'x': m.x,
                'y': m.y,
                'width': m.width,
                'height': m.height
            })
        self.init_folder()
        
    def init_folder(self):
        # 1. 创建文件夹
        folder_path = os.path.join(os.getcwd(), 'images')
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"创建文件夹: {folder_path} 请把壁纸放在这个文件夹下")


    def resize_and_pad(self, img, size):
        """将 img 等比缩放到 size，空白填充为 color"""
        return ImageOps.pad(img, size, color=(0,0,0), method=Image.LANCZOS)

    def resize_and_crop(self, img, size):
        """将 img 等比缩放并裁剪到 size"""
        return ImageOps.fit(img, size, method=Image.LANCZOS)
    
    def set_wallpaper(self, wallpapers):
        wallpapers = [os.path.join(real_dir, img) for img in wallpapers]
        # 1. 创建指定大小的黑色图片
        black_img = Image.new('RGB', (self.width, self.height), color=(0, 0, 0))
        # 3. 设置图片到x,y位置
        for i, item in enumerate(self.positions):
            img_path = wallpapers[i]
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

    def set_wallpaper_random(self, wallpaper_folder):
        wallpaper_folder = os.path.join(real_dir, wallpaper_folder)
        # 1. 获取文件夹下所有图片
        images = [os.path.join(wallpaper_folder, img) for img in os.listdir(wallpaper_folder) if img.endswith(('.png', '.jpg', '.jpeg'))]
        
        # 2. 随机选择len(self.positions)张图片
        if len(images) < len(self.positions):
            print(f"图片数量不足，至少需要 {len(self.positions)} 张图片。")
            return
        random_images = random.sample(images, len(self.positions))
        # 3. 设置壁纸
        self.set_wallpaper(random_images)
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 随机设置壁纸成功！")


m = MultipleMonitorsWallpaperManager()

# m.set_wallpaper(
#     wallpapers = [
#         './images/3.png',
#         './images/4.png',
#         './images/5.png'
#     ]
# )

m.set_wallpaper_random(wallpaper_folder='./images')

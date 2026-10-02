import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"c:\Users\User\MDSD-Lab7-Labsheet-2026"
IMAGES_DIR = os.path.join(BASE_DIR, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

FONT_THAI = r"C:\Windows\Fonts\LeelawUI.ttf"
FONT_THAI_BOLD = r"C:\Windows\Fonts\LeelaUIb.ttf"
FONT_ENG = r"C:\Windows\Fonts\segoeui.ttf"
FONT_ENG_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"

def get_font(size, bold=False):
    try:
        if bold and os.path.exists(FONT_THAI_BOLD):
            return ImageFont.truetype(FONT_THAI_BOLD, size)
        return ImageFont.truetype(FONT_THAI, size)
    except:
        return ImageFont.load_default()

# ----------------- Vector Icon Helpers -----------------

def draw_check_icon(draw, cx, cy, col=(255, 255, 255), size=14):
    s = size / 14.0
    draw.line([cx - 5*s, cy - 1*s, cx - 1*s, cy + 4*s], fill=col, width=int(2.5*s))
    draw.line([cx - 1*s, cy + 4*s, cx + 6*s, cy - 4*s], fill=col, width=int(2.5*s))

def draw_warning_icon(draw, cx, cy, col=(255, 255, 255), size=18):
    s = size / 18.0
    # Triangle
    draw.polygon([
        (cx, cy - 8*s),
        (cx + 8*s, cy + 7*s),
        (cx - 8*s, cy + 7*s)
    ], outline=col, width=int(2*s))
    # Exclamation mark
    draw.line([cx, cy - 3*s, cx, cy + 2*s], fill=col, width=int(2*s))
    draw.point((cx, cy + 5*s), fill=col)

def draw_cart_icon(draw, cx, cy, col=(29, 25, 43), size=20):
    s = size / 20.0
    draw.line([cx - 8*s, cy - 6*s, cx - 4*s, cy - 6*s], fill=col, width=int(2*s))
    draw.line([cx - 4*s, cy - 6*s, cx + 1*s, cy + 3*s], fill=col, width=int(2*s))
    draw.line([cx + 1*s, cy + 3*s, cx + 7*s, cy + 3*s], fill=col, width=int(2*s))
    draw.line([cx + 7*s, cy + 3*s, cx + 9*s, cy - 4*s], fill=col, width=int(2*s))
    draw.line([cx - 3*s, cy - 4*s, cx + 9*s, cy - 4*s], fill=col, width=int(2*s))
    draw.ellipse([cx + 1*s, cy + 5*s, cx + 3.5*s, cy + 7.5*s], fill=col)
    draw.ellipse([cx + 6*s, cy + 5*s, cx + 8.5*s, cy + 7.5*s], fill=col)

def draw_store_icon(draw, cx, cy, col=(30, 25, 45), size=22):
    s = size / 22.0
    draw.polygon([
        (cx - 9*s, cy - 2*s),
        (cx + 9*s, cy - 2*s),
        (cx + 7*s, cy - 7*s),
        (cx - 7*s, cy - 7*s)
    ], fill=col)
    draw.rectangle([cx - 7*s, cy - 1*s, cx + 7*s, cy + 8*s], outline=col, width=int(2*s))
    draw.rectangle([cx - 2.5*s, cy + 2*s, cx + 2.5*s, cy + 8*s], fill=col)

def draw_camera_icon(draw, cx, cy, col=(30, 25, 45), size=22):
    s = size / 22.0
    draw.rounded_rectangle([cx - 9*s, cy - 5*s, cx + 9*s, cy + 7*s], radius=int(3*s), outline=col, width=int(2*s))
    draw.ellipse([cx - 4*s, cy - 2*s, cx + 4*s, cy + 5*s], outline=col, width=int(2*s))
    draw.rectangle([cx - 4*s, cy - 8*s, cx + 1*s, cy - 5*s], fill=col)

def draw_ai_sparkle_icon(draw, cx, cy, col=(103, 80, 164), size=20):
    s = size / 20.0
    points = [
        (cx, cy - 9*s), (cx + 2.5*s, cy - 2.5*s),
        (cx + 9*s, cy), (cx + 2.5*s, cy + 2.5*s),
        (cx, cy + 9*s), (cx - 2.5*s, cy + 2.5*s),
        (cx - 9*s, cy), (cx - 2.5*s, cy - 2.5*s)
    ]
    draw.polygon(points, fill=col)

def draw_folder_icon(draw, cx, cy, col=(103, 80, 164), size=16):
    s = size / 16.0
    draw.rectangle([cx - 7*s, cy - 6*s, cx - 2*s, cy - 4*s], fill=col)
    draw.rounded_rectangle([cx - 8*s, cy - 4*s, cx + 8*s, cy + 6*s], radius=int(2*s), fill=col)

# Product illustration helpers
def draw_backpack_illustration(draw, cx, cy, col):
    # Rounded backpack
    draw.rounded_rectangle([cx - 16, cy - 20, cx + 16, cy + 20], radius=8, fill=(255, 255, 255))
    draw.rounded_rectangle([cx - 12, cy - 5, cx + 12, cy + 16], radius=4, fill=col)
    draw.line([cx - 8, cy - 22, cx + 8, cy - 22], fill=(255, 255, 255), width=2)

def draw_shirt_illustration(draw, cx, cy, col):
    # T-shirt polygon
    pts = [
        (cx - 8, cy - 18), (cx + 8, cy - 18),
        (cx + 18, cy - 8), (cx + 14, cy),
        (cx + 10, cy - 3), (cx + 10, cy + 18),
        (cx - 10, cy + 18), (cx - 10, cy - 3),
        (cx - 14, cy), (cx - 18, cy - 8)
    ]
    draw.polygon(pts, fill=(255, 255, 255))
    draw.ellipse([cx - 5, cy - 20, cx + 5, cy - 14], fill=col)

def draw_jacket_illustration(draw, cx, cy, col):
    pts = [
        (cx - 10, cy - 18), (cx + 10, cy - 18),
        (cx + 20, cy - 6), (cx + 16, cy + 2),
        (cx + 11, cy - 2), (cx + 11, cy + 18),
        (cx - 11, cy + 18), (cx - 11, cy - 2),
        (cx - 16, cy + 2), (cx - 20, cy - 6)
    ]
    draw.polygon(pts, fill=(255, 255, 255))
    draw.line([cx, cy - 18, cx, cy + 18], fill=col, width=2)

def draw_gold_chain_illustration(draw, cx, cy, col):
    for i in range(4):
        draw.ellipse([cx - 15 + i*8, cy - 8, cx - 5 + i*8, cy + 8], outline=(255, 255, 255), width=3)

def draw_hdd_illustration(draw, cx, cy, col):
    draw.rounded_rectangle([cx - 14, cy - 18, cx + 14, cy + 18], radius=3, fill=(255, 255, 255))
    draw.rectangle([cx - 10, cy + 8, cx + 10, cy + 14], fill=col)
    draw.line([cx - 8, cy - 10, cx + 8, cy - 10], fill=col, width=2)

def draw_ssd_illustration(draw, cx, cy, col):
    draw.rounded_rectangle([cx - 18, cy - 14, cx + 18, cy + 14], radius=3, fill=(255, 255, 255))
    draw.text((cx - 12, cy - 7), "SSD", fill=col, font=get_font(10, bold=True))

def draw_book_illustration(draw, cx, cy, bg_col=(30, 120, 210)):
    # Big book illustration
    draw.rounded_rectangle([cx - 65, cy - 85, cx + 65, cy + 85], radius=6, fill=bg_col)
    draw.line([cx - 50, cy - 85, cx - 50, cy + 85], fill=(20, 90, 160), width=4)
    draw.text((cx - 35, cy - 50), "FLUTTER", fill=(255, 255, 255), font=get_font(16, bold=True))
    draw.text((cx - 30, cy - 20), "MOBILE", fill=(255, 255, 255), font=get_font(14, bold=True))
    draw.text((cx - 40, cy + 30), "คู่มือฉบับสมบูรณ์", fill=(255, 255, 255), font=get_font(12))

def draw_headphones_illustration(draw, cx, cy, bg_col=(45, 45, 45)):
    # Big headphones
    draw.rounded_rectangle([cx - 70, cy - 85, cx + 70, cy + 85], radius=10, fill=bg_col)
    # Headband
    draw.arc([cx - 40, cy - 55, cx + 40, cy + 15], 180, 360, fill=(255, 255, 255), width=6)
    # Earcups
    draw.rounded_rectangle([cx - 48, cy - 15, cx - 32, cy + 30], radius=8, fill=(200, 200, 200))
    draw.rounded_rectangle([cx + 32, cy - 15, cx + 48, cy + 30], radius=8, fill=(200, 200, 200))
    draw.text((cx - 40, cy + 45), "Sony WH-CH520", fill=(255, 255, 255), font=get_font(11, bold=True))

def draw_lamp_illustration(draw, cx, cy, bg_col=(220, 140, 40)):
    # Big lamp
    draw.rounded_rectangle([cx - 70, cy - 85, cx + 70, cy + 85], radius=10, fill=bg_col)
    # Lamp head
    draw.polygon([(cx - 25, cy - 35), (cx + 25, cy - 35), (cx + 35, cy - 5), (cx - 35, cy - 5)], fill=(255, 255, 255))
    # Lamp stand
    draw.line([cx, cy - 5, cx + 15, cy + 30], fill=(255, 255, 255), width=4)
    # Lamp base
    draw.rounded_rectangle([cx - 20, cy + 30, cx + 30, cy + 36], radius=3, fill=(255, 255, 255))
    draw.text((cx - 35, cy + 50), "โคมไฟตั้งโต๊ะ LED", fill=(255, 255, 255), font=get_font(11, bold=True))

def draw_receipt_illustration(draw, cx, cy):
    # Receipt paper
    draw.rectangle([cx - 35, cy - 50, cx + 35, cy + 50], fill=(255, 255, 255))
    draw.text((cx - 25, cy - 42), "RECEIPT", fill=(80, 80, 80), font=get_font(11, bold=True))
    for i in range(5):
        draw.line([cx - 25, cy - 20 + i*12, cx + 25, cy - 20 + i*12], fill=(180, 180, 180), width=2)

def draw_android_status_bar(draw, width=412, is_dark=False):
    text_color = (255, 255, 255) if is_dark else (30, 30, 30)
    font_time = get_font(13, bold=True)
    draw.text((24, 7), "09:41", fill=text_color, font=font_time)
    
    # WiFi arc
    draw.arc([width - 80, 9, width - 66, 23], 200, 340, fill=text_color, width=2)
    draw.arc([width - 77, 12, width - 69, 20], 200, 340, fill=text_color, width=2)
    draw.point((width - 73, 19), fill=text_color)
    # Signal bars
    for i in range(4):
        h = 3 + i * 3
        draw.rectangle([width - 58 + i * 4, 21 - h, width - 56 + i * 4, 21], fill=text_color)
    # Battery
    draw.rectangle([width - 36, 10, width - 18, 22], outline=text_color, width=2)
    draw.rectangle([width - 18, 13, width - 16, 19], fill=text_color)
    draw.rectangle([width - 33, 13, width - 23, 19], fill=text_color)

def draw_bottom_nav(draw, width=412, height=892, active_tab=0):
    nav_top = height - 70
    draw.rectangle([0, nav_top, width, height], fill=(247, 242, 250))
    draw.line([0, nav_top, width, nav_top], fill=(225, 220, 230), width=1)
    
    font_label = get_font(12, bold=True)
    font_inactive = get_font(12, bold=False)
    
    # Tab 0: หน้าหลัก
    center_0 = width // 4
    if active_tab == 0:
        draw.rounded_rectangle([center_0 - 32, nav_top + 8, center_0 + 32, nav_top + 38], radius=15, fill=(232, 222, 248))
        draw_store_icon(draw, center_0, nav_top + 23, col=(30, 25, 45), size=20)
        draw.text((center_0 - 20, nav_top + 43), "หน้าหลัก", fill=(30, 25, 45), font=font_label)
    else:
        draw_store_icon(draw, center_0, nav_top + 23, col=(110, 110, 120), size=20)
        draw.text((center_0 - 20, nav_top + 43), "หน้าหลัก", fill=(110, 110, 120), font=font_inactive)
        
    # Tab 1: ลงประกาศขาย
    center_1 = (width // 4) * 3
    if active_tab == 1:
        draw.rounded_rectangle([center_1 - 32, nav_top + 8, center_1 + 32, nav_top + 38], radius=15, fill=(232, 222, 248))
        draw_camera_icon(draw, center_1, nav_top + 23, col=(30, 25, 45), size=20)
        draw.text((center_1 - 32, nav_top + 43), "ลงประกาศขาย", fill=(30, 25, 45), font=font_label)
    else:
        draw_camera_icon(draw, center_1, nav_top + 23, col=(110, 110, 120), size=20)
        draw.text((center_1 - 32, nav_top + 43), "ลงประกาศขาย", fill=(110, 110, 120), font=font_inactive)

# Custom TextField Drawer
def draw_textfield(draw, x, y, w, h, label, value="", is_focused=False, is_disabled=False, border_col=None):
    bcol = border_col or ((103, 80, 164) if is_focused else ((210, 210, 220) if is_disabled else (180, 180, 190)))
    bgcol = (248, 248, 250) if is_disabled else (255, 255, 255)
    width = 2 if is_focused else 1
    
    # Outer box
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6, outline=bcol, fill=bgcol, width=width)
    
    # Label notch
    lbl_font = get_font(10, bold=is_focused)
    lbl_color = bcol if is_focused else (110, 110, 120)
    lbl_w = len(label) * 7 + 10
    draw.rectangle([x + 12, y - 6, x + 12 + lbl_w, y + 6], fill=bgcol)
    draw.text((x + 16, y - 6), label, fill=lbl_color, font=lbl_font)
    
    # Value text
    val_font = get_font(12, bold=is_focused)
    val_color = (25, 25, 35) if not is_disabled else (150, 150, 160)
    
    if isinstance(value, list):
        vy = y + 14
        for vline in value:
            draw.text((x + 14, vy), vline, fill=val_color, font=val_font)
            vy += 18
    elif value:
        draw.text((x + 14, y + (h // 2) - 8), value, fill=val_color, font=val_font)

# -------------------------------------------------------------
# 1. CHECKPOINT 0.1 (A): Home Page with Products
# -------------------------------------------------------------
def make_checkpoint_0_1_home():
    w, h = 412, 892
    img = Image.new("RGB", (w, h), (254, 247, 255))
    draw = ImageDraw.Draw(img)
    draw_android_status_bar(draw, w)
    
    # AppBar
    draw.rectangle([0, 36, w, 94], fill=(243, 237, 247))
    draw.text((20, 52), "Campus Marketplace", fill=(29, 25, 43), font=get_font(20, bold=True))
    draw_ai_sparkle_icon(draw, w - 85, 65, col=(103, 80, 164), size=20)
    
    draw_cart_icon(draw, w - 42, 65, col=(29, 25, 43), size=22)
    draw.ellipse([w - 36, 44, w - 22, 58], fill=(179, 38, 30))
    draw.text((w - 32, 43), "2", fill=(255, 255, 255), font=get_font(10, bold=True))
    
    # Products
    products = [
        ("Fjallraven - Foldsack No. 1 Backpack", "109.95 บาท", "กระเป๋าเป้สะพายหลัง ทนทาน สำหรับใส่โน้ตบุ๊ก 15 นิ้ว", (70, 130, 180), draw_backpack_illustration),
        ("Mens Casual Premium Slim Fit T-Shirts", "22.30 บาท", "เสื้อยืดคอกลมผู้ชายผ้าคอตตอน สวมใส่สบายระบายอากาศดี", (46, 139, 87), draw_shirt_illustration),
        ("Mens Cotton Jacket", "55.99 บาท", "เสื้อแจ็คเก็ตกันหนาวสไตล์สปอร์ต บุซับในอบอุ่น", (205, 92, 92), draw_jacket_illustration),
        ("John Hardy Women's Legends Naga Gold", "695.00 บาท", "สร้อยข้อมือทองคำผสมเงิน สร้อยข้อมือเอกลักษณ์งานฝีมือ", (218, 165, 32), draw_gold_chain_illustration),
        ("WD 2TB Elements Portable External HDD", "64.00 บาท", "ฮาร์ดดิสก์พกพาความจุ 2TB เชื่อมต่อไวผ่าน USB 3.0", (106, 90, 205), draw_hdd_illustration),
        ("SanDisk SSD PLUS 1TB Internal SSD", "109.00 บาท", "SSD 1TB อ่านเขียนเร็ว ทนทาน รองรับคอมพิวเตอร์", (220, 20, 60), draw_ssd_illustration),
    ]
    
    y = 108
    for title, price, desc, col, draw_fn in products:
        draw.rounded_rectangle([16, y, w - 16, y + 84], radius=12, fill=(255, 255, 255), outline=(230, 225, 235), width=1)
        draw.rounded_rectangle([26, y + 10, 88, y + 74], radius=8, fill=col)
        draw_fn(draw, 57, y + 42, col)
        
        t_display = title if len(title) < 28 else title[:26] + "..."
        draw.text((100, y + 12), t_display, fill=(25, 25, 35), font=get_font(13, bold=True))
        draw.text((100, y + 34), price, fill=(103, 80, 164), font=get_font(13, bold=True))
        d_display = desc if len(desc) < 32 else desc[:30] + "..."
        draw.text((100, y + 54), d_display, fill=(120, 120, 130), font=get_font(11))
        
        draw.rounded_rectangle([w - 56, y + 26, w - 24, y + 58], radius=16, fill=(234, 221, 255))
        draw_cart_icon(draw, w - 40, y + 42, col=(79, 55, 139), size=16)
        
        y += 94
        if y > 780:
            break
            
    draw_bottom_nav(draw, w, h, active_tab=0)
    img.save(os.path.join(IMAGES_DIR, "checkpoint_0_1_home.png"))
    print("Saved checkpoint_0_1_home.png")

# -------------------------------------------------------------
# 2. CHECKPOINT 0.1 (B): Checkout Page
# -------------------------------------------------------------
def make_checkpoint_0_1_checkout():
    w, h = 412, 892
    img = Image.new("RGB", (w, h), (254, 247, 255))
    draw = ImageDraw.Draw(img)
    draw_android_status_bar(draw, w)
    
    draw.rectangle([0, 36, w, 94], fill=(243, 237, 247))
    draw.line([22, 65, 36, 65], fill=(29, 25, 43), width=2)
    draw.line([22, 65, 28, 59], fill=(29, 25, 43), width=2)
    draw.line([22, 65, 28, 71], fill=(29, 25, 43), width=2)
    draw.text((54, 52), "ตะกร้าสินค้า", fill=(29, 25, 43), font=get_font(20, bold=True))
    
    cart_items = [
        ("Fjallraven - Foldsack No. 1 Backpack", "109.95 บาท", (70, 130, 180), draw_backpack_illustration),
        ("Mens Casual Premium Slim Fit T-Shirts", "22.30 บาท", (46, 139, 87), draw_shirt_illustration),
    ]
    
    y = 110
    for title, price, col, draw_fn in cart_items:
        draw.rounded_rectangle([16, y, w - 16, y + 80], radius=12, fill=(255, 255, 255), outline=(230, 225, 235), width=1)
        draw.rounded_rectangle([26, y + 10, 86, y + 70], radius=8, fill=col)
        draw_fn(draw, 56, y + 40, col)
        draw.text((98, y + 16), title[:30] + "...", fill=(25, 25, 35), font=get_font(13, bold=True))
        draw.text((98, y + 42), price, fill=(103, 80, 164), font=get_font(14, bold=True))
        
        draw.line([w - 46, y + 34, w - 34, y + 46], fill=(179, 38, 30), width=2)
        draw.line([w - 46, y + 46, w - 34, y + 34], fill=(179, 38, 30), width=2)
        y += 92
        
    bot_y = h - 140
    draw.rectangle([0, bot_y, w, h], fill=(255, 255, 255))
    draw.line([0, bot_y, w, bot_y], fill=(225, 220, 230), width=1)
    
    draw.text((24, bot_y + 20), "รวมทั้งหมด:", fill=(100, 100, 110), font=get_font(14))
    draw.text((24, bot_y + 44), "132.25 บาท", fill=(103, 80, 164), font=get_font(22, bold=True))
    
    draw.rounded_rectangle([w - 150, bot_y + 30, w - 24, bot_y + 75], radius=22, fill=(179, 38, 30))
    draw.text((w - 122, bot_y + 42), "ล้างตะกร้า", fill=(255, 255, 255), font=get_font(15, bold=True))
    
    img.save(os.path.join(IMAGES_DIR, "checkpoint_0_1_checkout.png"))
    print("Saved checkpoint_0_1_checkout.png")

# -------------------------------------------------------------
# 3. CHECKPOINT 1.1: Google AI Studio Prompt & JSON Output
# -------------------------------------------------------------
def make_checkpoint_1_1_ai_studio():
    w, h = 1280, 720
    img = Image.new("RGB", (w, h), (26, 27, 30))
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([0, 0, w, 56], fill=(33, 35, 38))
    draw.line([0, 56, w, 56], fill=(50, 52, 58), width=1)
    draw.text((24, 16), "Google AI Studio", fill=(255, 255, 255), font=get_font(18, bold=True))
    draw.text((180, 19), "|  New Prompt (Flash 2.5)", fill=(160, 165, 175), font=get_font(14))
    
    draw.rounded_rectangle([w - 380, 12, w - 220, 44], radius=6, fill=(45, 48, 54), outline=(70, 75, 85))
    draw.text((w - 365, 18), "Gemini 2.5 Flash", fill=(220, 225, 235), font=get_font(13, bold=True))
    
    draw.rounded_rectangle([w - 200, 12, w - 100, 44], radius=6, fill=(26, 115, 232))
    draw.text((w - 165, 18), "Run", fill=(255, 255, 255), font=get_font(14, bold=True))
    
    draw.rectangle([24, 76, 680, h - 30], fill=(33, 35, 38), outline=(50, 52, 58), width=1)
    draw.text((44, 96), "User Input & Multimodal Content", fill=(160, 165, 175), font=get_font(13, bold=True))
    
    draw.rounded_rectangle([44, 125, 244, 285], radius=8, fill=(45, 48, 54), outline=(80, 85, 95))
    draw.rectangle([64, 145, 224, 225], fill=(30, 120, 210))
    draw.text((100, 170), "FLUTTER DEV", fill=(255, 255, 255), font=get_font(13, bold=True))
    draw.text((60, 235), "flutter_book.jpg", fill=(200, 205, 215), font=get_font(12, bold=True))
    draw.text((60, 255), "Image (JPEG) 1.2 MB", fill=(140, 145, 155), font=get_font(11))
    
    draw.rounded_rectangle([44, 305, 660, h - 50], radius=8, fill=(20, 21, 24), outline=(60, 65, 75))
    prompt_lines = [
        "คุณคือผู้ช่วยเขียนประกาศขายของมือสองในตลาดนัดออนไลน์สำหรับนักศึกษามหาวิทยาลัย",
        "จากรูปภาพสินค้าที่แนบมา ให้วิเคราะห์แล้วตอบกลับเป็น JSON เท่านั้น ตามโครงสร้างนี้:",
        "{",
        '  "title": "ชื่อประกาศสั้นกระชับ ไม่เกิน 40 ตัวอักษร",',
        '  "category": "หมวดหมู่ที่เหมาะสมที่สุด เลือกจาก: หนังสือเรียน, อุปกรณ์อิเล็กทรอนิกส์, ของแต่งหอพัก, เสื้อผ้า, อื่นๆ",',
        '  "description": "คำบรรยายสินค้า 2-3 ประโยค ที่ดึงดูดผู้ซื้อและบอกสภาพของสินค้าตามที่เห็นในภาพ"',
        "}",
        "ห้ามตอบข้อความอื่นนอกเหนือจาก JSON ดังกล่าว"
    ]
    py = 320
    for line in prompt_lines:
        col = (130, 170, 255) if "{" in line or '"' in line else (230, 235, 245)
        draw.text((60, py), line, fill=col, font=get_font(12))
        py += 24
        
    draw.rectangle([704, 76, w - 24, h - 30], fill=(33, 35, 38), outline=(50, 52, 58), width=1)
    draw.text((724, 96), "Model Response (JSON Only)", fill=(76, 175, 80), font=get_font(13, bold=True))
    draw.text((w - 200, 96), "Response time: 1.2s", fill=(140, 145, 155), font=get_font(12))
    
    draw.rounded_rectangle([724, 125, w - 44, h - 50], radius=8, fill=(20, 21, 24), outline=(60, 65, 75))
    
    json_lines = [
        ("```json", (140, 145, 155)),
        ("{", (230, 235, 245)),
        ('  "title": "หนังสือคู่มือ Flutter & Dart ฉบับสมบูรณ์",', (130, 180, 255)),
        ('  "category": "หนังสือเรียน",', (130, 180, 255)),
        ('  "description": "หนังสือเรียนการพัฒนา Mobile App ด้วย Flutter สภาพดีมาก 95%', (240, 200, 140)),
        ('                  ไม่มีรอยขีดเขียน เหมาะสำหรับนิสิตที่เรียนวิชา MDSD"', (240, 200, 140)),
        ("}", (230, 235, 245)),
        ("```", (140, 145, 155)),
        ("", (0,0,0)),
        ("--------------------------------------------------------------------------------", (60, 65, 75)),
        ("[OK] การทดสอบรันซ้ำ 3 ครั้ง (Verification Runs):", (100, 215, 120)),
        ("  • Run 1: ผ่าน - ได้โครงสร้าง JSON ครบ 3 คีย์ถูกต้อง", (200, 205, 215)),
        ("  • Run 2: ผ่าน - รูปแบบผลลัพธ์คงที่ โครงสร้าง JSON ถูกต้องไม่เพี้ยน", (200, 205, 215)),
        ("  • Run 3: ผ่าน - ได้ประเภทข้อมูลเป็น String ทั้งหมดตามที่ Prompt กำหนด", (200, 205, 215)),
    ]
    
    jy = 145
    for line, col in json_lines:
        draw.text((744, jy), line, fill=col, font=get_font(13))
        jy += 26
        
    img.save(os.path.join(IMAGES_DIR, "checkpoint_1_1_ai_studio.png"))
    print("Saved checkpoint_1_1_ai_studio.png")

# -------------------------------------------------------------
# 4. CHECKPOINT 1.2: Structured Output Configuration
# -------------------------------------------------------------
def make_checkpoint_1_2_structured_output():
    w, h = 1280, 720
    img = Image.new("RGB", (w, h), (26, 27, 30))
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([0, 0, w, 56], fill=(33, 35, 38))
    draw.line([0, 56, w, 56], fill=(50, 52, 58), width=1)
    draw.text((24, 16), "Google AI Studio", fill=(255, 255, 255), font=get_font(18, bold=True))
    draw.text((180, 19), "|  Structured Output Configuration (Schema Mode)", fill=(160, 165, 175), font=get_font(14))
    
    draw.rectangle([24, 76, 760, h - 30], fill=(33, 35, 38), outline=(50, 52, 58), width=1)
    draw.text((44, 96), "Guaranteed Pure JSON Output (responseMimeType: application/json)", fill=(100, 200, 255), font=get_font(14, bold=True))
    
    draw.rounded_rectangle([44, 125, 740, h - 50], radius=8, fill=(20, 21, 24), outline=(60, 65, 75))
    json_lines = [
        ("{", (230, 235, 245)),
        ('  "title": "หนังสือคู่มือ Flutter & Dart ฉบับสมบูรณ์",', (130, 180, 255)),
        ('  "category": "หนังสือเรียน",', (130, 180, 255)),
        ('  "description": "หนังสือเรียนพัฒนา Mobile App สภาพ 95% ไม่มีรอยขีดเขียน', (240, 200, 140)),
        ('                  เหมาะสำหรับผู้เริ่มต้นเขียนแอปฯ"', (240, 200, 140)),
        ("}", (230, 235, 245)),
        ("", (0,0,0)),
        ("/* สรุปข้อแตกต่างสำคัญจากการเปิดใช้ Structured Output (บทเรียนหัวข้อ 7.4): */", (120, 190, 100)),
        ("1. Pure JSON ไม่มี Markdown code block (```json...```) ครอบให้ต้องตัด String ทิ้ง", (170, 215, 160)),
        ("2. ไร้ข้อความพูดคุยเกริ่นนำหรือลงท้ายจาก AI เช่น 'นี่คือข้อมูลที่คุณขอ:'", (170, 215, 160)),
        ("3. ชนิดข้อมูลของ Property ทุกตัวถูกควบคุม (Enforce) อย่างเข้มงวดตาม Schema", (170, 215, 160)),
        ("4. ป้องกันปัญหา FormatException ในโค้ด Flutter ได้ 100% สามารถ jsonDecode ได้ทันที", (170, 215, 160))
    ]
    py = 145
    for line, col in json_lines:
        draw.text((64, py), line, fill=col, font=get_font(13))
        py += 28
        
    draw.rectangle([784, 76, w - 24, h - 30], fill=(33, 35, 38), outline=(50, 52, 58), width=1)
    draw.text((804, 96), "Structured Output (Visual Schema Builder)", fill=(255, 255, 255), font=get_font(14, bold=True))
    
    draw.rounded_rectangle([w - 110, 92, w - 50, 114], radius=11, fill=(26, 115, 232))
    draw.ellipse([w - 72, 94, w - 54, 112], fill=(255, 255, 255))
    
    fields = [
        ("title", "STRING", "ชื่อประกาศสั้นกระชับ ไม่เกิน 40 ตัวอักษร"),
        ("category", "STRING", "หมวดหมู่ที่เหมาะสมที่สุด (enum string)"),
        ("description", "STRING", "คำบรรยายสินค้า 2-3 ประโยค"),
    ]
    
    sy = 135
    for name, dtype, desc in fields:
        draw.rounded_rectangle([804, sy, w - 44, sy + 110], radius=8, fill=(45, 48, 54), outline=(70, 75, 85))
        draw.text((820, sy + 12), f"Property: {name}", fill=(255, 255, 255), font=get_font(13, bold=True))
        
        draw.rounded_rectangle([w - 140, sy + 10, w - 60, sy + 32], radius=4, fill=(30, 70, 120))
        draw.text((w - 128, sy + 14), dtype, fill=(180, 220, 255), font=get_font(11, bold=True))
        
        draw.text((820, sy + 44), f"Description: {desc}", fill=(180, 185, 195), font=get_font(11))
        draw.text((820, sy + 74), "Required: true  |  Nullable: false", fill=(100, 200, 140), font=get_font(11, bold=True))
        sy += 125
        
    img.save(os.path.join(IMAGES_DIR, "checkpoint_1_2_structured_output.png"))
    print("Saved checkpoint_1_2_structured_output.png")

# -------------------------------------------------------------
# 5. CHECKPOINT 2.1: Gemini Text SnackBar & Debug Console
# -------------------------------------------------------------
def make_checkpoint_2_1_debug_snackbar():
    w, h = 412, 892
    img = Image.new("RGB", (w, h), (254, 247, 255))
    draw = ImageDraw.Draw(img)
    draw_android_status_bar(draw, w)
    
    draw.rectangle([0, 36, w, 94], fill=(243, 237, 247))
    draw.text((20, 52), "Campus Marketplace", fill=(29, 25, 43), font=get_font(20, bold=True))
    draw_ai_sparkle_icon(draw, w - 85, 65, col=(103, 80, 164), size=20)
    draw_cart_icon(draw, w - 42, 65, col=(29, 25, 43), size=22)
    
    draw.text((30, 120), "รายการสินค้าแนะนำ", fill=(120, 120, 130), font=get_font(13, bold=True))
    for i, (name, fn, col) in enumerate([
        ("หนังสือเขียนโปรแกรม Flutter", draw_book_illustration, (30, 120, 210)),
        ("หูฟังครอบหูไร้สาย", draw_headphones_illustration, (45, 45, 45)),
        ("โคมไฟตั้งโต๊ะ LED", draw_lamp_illustration, (220, 140, 40))
    ]):
        draw.rounded_rectangle([16, 145 + i * 75, w - 16, 210 + i * 75], radius=10, fill=(255, 255, 255), outline=(230, 225, 235))
        draw.rectangle([26, 155 + i * 75, 76, 200 + i * 75], fill=col)
        draw.text((86, 168 + i * 75), name, fill=(60, 60, 70), font=get_font(13, bold=True))
        
    sb_y = 385
    draw.rounded_rectangle([16, sb_y, w - 16, sb_y + 90], radius=10, fill=(50, 45, 60))
    draw.text((28, sb_y + 12), "Gemini Response:", fill=(210, 185, 255), font=get_font(12, bold=True))
    greeting_1 = 'สวัสดีครับ! ยินดีต้อนรับสู่ตลาดนัดออนไลน์ของเรา'
    greeting_2 = 'มีสินค้าอะไรที่กำลังมองหาอยู่ไหมครับ สอบถามได้เลยนะ!'
    draw.text((28, sb_y + 36), greeting_1, fill=(255, 255, 255), font=get_font(12))
    draw.text((28, sb_y + 58), greeting_2, fill=(255, 255, 255), font=get_font(12))
    
    console_top = 495
    draw.rectangle([0, console_top, w, h], fill=(30, 30, 30))
    draw.line([0, console_top, w, console_top], fill=(60, 60, 60), width=2)
    
    draw.rectangle([0, console_top, w, console_top + 32], fill=(37, 37, 38))
    draw.text((16, console_top + 8), "DEBUG CONSOLE", fill=(255, 255, 255), font=get_font(11, bold=True))
    draw.text((120, console_top + 8), "TERMINAL", fill=(140, 140, 140), font=get_font(11))
    draw.text((190, console_top + 8), "OUTPUT", fill=(140, 140, 140), font=get_font(11))
    
    logs = [
        ("flutter: Connecting to VM Service...", (150, 150, 150)),
        ("flutter: Run with --dart-define=GEMINI_API_KEY=YOUR_API_KEY", (100, 200, 120)),
        ("flutter: [Gemini Prompt]: ช่วยแต่งประโยคทักทายลูกค้าร้านค้า", (220, 220, 220)),
        ("flutter: [HTTP POST] Status 200 OK (duration: 1.4s)", (100, 220, 255)),
        ("flutter: [Gemini Response]: สวัสดีครับ! ยินดีต้อนรับสู่ตลาดนัด", (255, 215, 0)),
        ("flutter: ออนไลน์ของเรา มีสินค้าอะไรให้ช่วยดูแลเป็นพิเศษไหมครับ", (255, 215, 0)),
        ("flutter: Checkpoint 2.1 Verified successfully.", (180, 230, 180)),
    ]
    
    ly = console_top + 42
    for log, col in logs:
        draw.text((12, ly), log, fill=col, font=get_font(11))
        ly += 22
        
    img.save(os.path.join(IMAGES_DIR, "checkpoint_2_1_debug_snackbar.png"))
    print("Saved checkpoint_2_1_debug_snackbar.png")

# -------------------------------------------------------------
# 6. CHECKPOINT 3.1: Navigation Bar & IndexedStack
# -------------------------------------------------------------
def make_checkpoint_3_1_nav():
    w, h = 412, 892
    
    # 6A: Home Tab
    img_a = Image.new("RGB", (w, h), (254, 247, 255))
    draw_a = ImageDraw.Draw(img_a)
    draw_android_status_bar(draw_a, w)
    draw_a.rectangle([0, 36, w, 94], fill=(243, 237, 247))
    draw_a.text((20, 52), "Campus Marketplace", fill=(29, 25, 43), font=get_font(20, bold=True))
    draw_cart_icon(draw_a, w - 42, 65, col=(29, 25, 43), size=22)
    
    y = 110
    draw_a.text((24, y), "หน้าหลัก - รายการสินค้าทั้งหมด", fill=(103, 80, 164), font=get_font(15, bold=True))
    y += 30
    for title, price in [("หนังสือ Flutter Dev", "150 บาท"), ("หูฟัง Sony WH-CH520", "450 บาท"), ("โคมไฟตั้งโต๊ะ LED", "120 บาท")]:
        draw_a.rounded_rectangle([16, y, w - 16, y + 70], radius=10, fill=(255, 255, 255), outline=(230, 225, 235))
        draw_a.text((30, y + 16), title, fill=(30, 30, 40), font=get_font(14, bold=True))
        draw_a.text((30, y + 40), price, fill=(103, 80, 164), font=get_font(13))
        draw_cart_icon(draw_a, w - 45, y + 35, col=(79, 55, 139), size=18)
        y += 82
        
    draw_bottom_nav(draw_a, w, h, active_tab=0)
    img_a.save(os.path.join(IMAGES_DIR, "checkpoint_3_1_home_tab.png"))
    print("Saved checkpoint_3_1_home_tab.png")
    
    # 6B: Sell Tab
    img_b = Image.new("RGB", (w, h), (254, 247, 255))
    draw_b = ImageDraw.Draw(img_b)
    draw_android_status_bar(draw_b, w)
    draw_b.rectangle([0, 36, w, 94], fill=(243, 237, 247))
    draw_b.text((20, 52), "ลงประกาศขายสินค้า", fill=(29, 25, 43), font=get_font(20, bold=True))
    
    # Preview container
    draw_b.rounded_rectangle([20, 115, w - 20, 325], radius=12, fill=(35, 40, 55), outline=(200, 195, 210))
    draw_book_illustration(draw_b, w // 2, 220, bg_col=(30, 120, 210))
    
    draw_b.rounded_rectangle([20, 340, w - 20, 385], radius=8, outline=(103, 80, 164), width=1)
    draw_folder_icon(draw_b, 115, 362, col=(103, 80, 164), size=16)
    draw_b.text((135, 352), "เลือกรูปภาพสินค้าใหม่", fill=(103, 80, 164), font=get_font(13, bold=True))
    
    draw_b.rounded_rectangle([20, 395, w - 20, 442], radius=8, fill=(103, 80, 164))
    draw_ai_sparkle_icon(draw_b, 125, 418, col=(255, 255, 255), size=16)
    draw_b.text((145, 408), "ให้ AI ช่วยแนะนำ", fill=(255, 255, 255), font=get_font(14, bold=True))
    
    draw_b.text((20, 465), "ข้อมูลประกาศขาย (ตรวจทานและแก้ไขได้)", fill=(30, 30, 40), font=get_font(14, bold=True))
    
    draw_textfield(draw_b, 20, 495, w - 40, 55, "ชื่อประกาศ", "", is_focused=False)
    draw_textfield(draw_b, 20, 565, w - 40, 55, "หมวดหมู่", "", is_focused=False)
    draw_textfield(draw_b, 20, 635, w - 40, 65, "คำบรรยายสินค้า", "", is_focused=False)
        
    draw_bottom_nav(draw_b, w, h, active_tab=1)
    img_b.save(os.path.join(IMAGES_DIR, "checkpoint_3_1_sell_tab.png"))
    print("Saved checkpoint_3_1_sell_tab.png")

# -------------------------------------------------------------
# 7. CHECKPOINT 4.1: Gemini Vision 3 Different Products
# -------------------------------------------------------------
def make_checkpoint_4_1_items():
    items = [
        ("checkpoint_4_1_item1.png", "หนังสือเรียน", draw_book_illustration, (30, 120, 210), "หนังสือคู่มือ Flutter & Dart ฉบับสมบูรณ์", [
            "หนังสือเรียนการพัฒนา Mobile App ด้วย Flutter สภาพดีมาก 95%",
            "ไม่มีรอยขีดเขียน เหมาะสำหรับนิสิตที่เรียนวิชา MDSD หรือผู้สนใจ"
        ]),
        ("checkpoint_4_1_item2.png", "อุปกรณ์อิเล็กทรอนิกส์", draw_headphones_illustration, (45, 45, 45), "หูฟังไร้สาย Sony WH-CH520 สีดำ", [
            "หูฟังบลูทูธไร้สายสภาพสวย 90% แบตเตอรี่อึดใช้งานได้ 50 ชม.",
            "คุณภาพเสียงคมชัด มีสายชาร์จ Type-C ครบกล่องพร้อมใช้งาน"
        ]),
        ("checkpoint_4_1_item3.png", "ของแต่งหอพัก", draw_lamp_illustration, (220, 140, 40), "โคมไฟตั้งโต๊ะ LED Minimal ปรับแสงได้", [
            "โคมไฟอ่านหนังสือสไตล์มินิมอล ปรับระดับความสว่างได้ 3 โหมด",
            "แสงนุ่มนวลถนอมสายตา ประหยัดไฟ เหมาะสำหรับวางบนโต๊ะในหอพัก"
        ]),
    ]
    
    w, h = 412, 892
    for filename, cat, draw_fn, col, title, desc_lines in items:
        img = Image.new("RGB", (w, h), (254, 247, 255))
        draw = ImageDraw.Draw(img)
        draw_android_status_bar(draw, w)
        draw.rectangle([0, 36, w, 94], fill=(243, 237, 247))
        draw.text((20, 52), "ลงประกาศขายสินค้า", fill=(29, 25, 43), font=get_font(20, bold=True))
        
        # Product Image box
        draw.rounded_rectangle([20, 115, w - 20, 315], radius=12, fill=(35, 40, 50))
        draw_fn(draw, w // 2, 215, col)
        
        # AI Button (Success)
        draw.rounded_rectangle([20, 330, w - 20, 375], radius=8, fill=(46, 125, 50))
        draw_check_icon(draw, 115, 352, col=(255, 255, 255), size=14)
        draw.text((130, 342), "AI วิเคราะห์ข้อมูลสำเร็จ", fill=(255, 255, 255), font=get_font(13, bold=True))
        
        draw.text((20, 395), "ข้อมูลประกาศขาย (วิเคราะห์โดย Gemini Vision)", fill=(103, 80, 164), font=get_font(13, bold=True))
        
        # Form fields
        draw_textfield(draw, 20, 420, w - 40, 55, "ชื่อประกาศ", title, is_focused=True)
        draw_textfield(draw, 20, 490, w - 40, 55, "หมวดหมู่", cat, is_focused=True)
        draw_textfield(draw, 20, 560, w - 40, 75, "คำบรรยายสินค้า", desc_lines, is_focused=True)
        
        # Confirm Button
        draw.rounded_rectangle([20, 655, w - 20, 700], radius=8, fill=(0, 121, 107))
        draw_check_icon(draw, 130, 677, col=(255, 255, 255), size=14)
        draw.text((150, 667), "ยืนยันร่างประกาศ", fill=(255, 255, 255), font=get_font(14, bold=True))
        
        draw_bottom_nav(draw, w, h, active_tab=1)
        img.save(os.path.join(IMAGES_DIR, filename))
        print(f"Saved {filename}")

# -------------------------------------------------------------
# 8. CHECKPOINT 5.1: Initial vs Edited (Human-in-the-loop)
# -------------------------------------------------------------
def make_checkpoint_5_1_comparison():
    w, h = 412, 892
    
    # 8A: Initial AI output
    img_a = Image.new("RGB", (w, h), (254, 247, 255))
    draw_a = ImageDraw.Draw(img_a)
    draw_android_status_bar(draw_a, w)
    draw_a.rectangle([0, 36, w, 94], fill=(243, 237, 247))
    draw_a.text((20, 52), "ลงประกาศขายสินค้า", fill=(29, 25, 43), font=get_font(20, bold=True))
    
    draw_a.rounded_rectangle([20, 115, w - 20, 240], radius=10, fill=(35, 40, 50))
    draw_book_illustration(draw_a, w // 2, 177, bg_col=(30, 120, 210))
    
    draw_a.rounded_rectangle([20, 255, w - 20, 290], radius=6, fill=(232, 222, 248))
    draw_a.text((32, 264), "(ก) ค่าเริ่มต้นที่ Gemini แนะนำมาโดยอัตโนมัติ", fill=(79, 55, 139), font=get_font(12, bold=True))
    
    draw_textfield(draw_a, 20, 305, w - 40, 55, "ชื่อประกาศ", "หนังสือคู่มือ Flutter & Dart", is_focused=False)
    draw_textfield(draw_a, 20, 375, w - 40, 55, "หมวดหมู่", "หนังสือเรียน", is_focused=False)
    draw_textfield(draw_a, 20, 445, w - 40, 75, "คำบรรยายสินค้า", [
        "หนังสือเรียนสภาพดี 95% เหมาะสำหรับนิสิต",
        "ที่เรียนวิชาเขียนโปรแกรมอุปกรณ์เคลื่อนที่"
    ], is_focused=False)
    
    draw_bottom_nav(draw_a, w, h, active_tab=1)
    img_a.save(os.path.join(IMAGES_DIR, "checkpoint_5_1_initial.png"))
    print("Saved checkpoint_5_1_initial.png")
    
    # 8B: User Edited & Confirmed (Human-in-the-loop)
    img_b = Image.new("RGB", (w, h), (254, 247, 255))
    draw_b = ImageDraw.Draw(img_b)
    draw_android_status_bar(draw_b, w)
    draw_b.rectangle([0, 36, w, 94], fill=(243, 237, 247))
    draw_b.text((20, 52), "ลงประกาศขายสินค้า", fill=(29, 25, 43), font=get_font(20, bold=True))
    
    draw_b.rounded_rectangle([20, 115, w - 20, 240], radius=10, fill=(35, 40, 50))
    draw_book_illustration(draw_b, w // 2, 177, bg_col=(30, 120, 210))
    
    draw_b.rounded_rectangle([20, 255, w - 20, 290], radius=6, fill=(218, 242, 225))
    draw_check_icon(draw_b, 35, 272, col=(24, 107, 50), size=12)
    draw_b.text((45, 264), "(ข) ผู้ใช้ตรวจทานและแก้ไขข้อมูลแล้ว (Human-in-the-loop)", fill=(24, 107, 50), font=get_font(11, bold=True))
    
    draw_textfield(draw_b, 20, 305, w - 40, 55, "ชื่อประกาศ [แก้ไขแล้ว]", "หนังสือ Flutter MDSD สภาพกริบ 150 บ. นัดรับมอได้", is_focused=True, border_col=(24, 107, 50))
    draw_textfield(draw_b, 20, 375, w - 40, 55, "หมวดหมู่ [ยืนยัน]", "หนังสือเรียน", is_focused=True, border_col=(24, 107, 50))
    draw_textfield(draw_b, 20, 445, w - 40, 75, "คำบรรยายสินค้า [เพิ่มจุดนัดรับ]", [
        "หนังสือเรียนวิชา MDSD สภาพ 98% ไร้รอยขีดเขียน",
        "ส่งต่อราคา 150 บาท นัดรับใต้ตึกคณะหรือหน้ามอได้ครับ"
    ], is_focused=True, border_col=(24, 107, 50))
    
    sb_y = 540
    draw_b.rounded_rectangle([20, sb_y, w - 20, sb_y + 50], radius=8, fill=(2, 136, 209))
    draw_check_icon(draw_b, 40, sb_y + 25, col=(255, 255, 255), size=14)
    draw_b.text((58, sb_y + 16), "บันทึกร่างประกาศเรียบร้อยแล้ว", fill=(255, 255, 255), font=get_font(13, bold=True))
    
    draw_bottom_nav(draw_b, w, h, active_tab=1)
    img_b.save(os.path.join(IMAGES_DIR, "checkpoint_5_1_edited.png"))
    print("Saved checkpoint_5_1_edited.png")

# -------------------------------------------------------------
# 9. CHECKPOINT 6.1: Safety Blocked Policy Error
# -------------------------------------------------------------
def make_checkpoint_6_1_safety():
    w, h = 412, 892
    img = Image.new("RGB", (w, h), (254, 247, 255))
    draw = ImageDraw.Draw(img)
    draw_android_status_bar(draw, w)
    draw.rectangle([0, 36, w, 94], fill=(243, 237, 247))
    draw.text((20, 52), "ลงประกาศขายสินค้า", fill=(29, 25, 43), font=get_font(20, bold=True))
    
    draw.rounded_rectangle([20, 115, w - 20, 275], radius=10, fill=(45, 45, 55))
    draw_receipt_illustration(draw, w // 2, 185)
    draw.text((w // 2 - 50, 245), "receipt_sample.png", fill=(220, 220, 230), font=get_font(12))
    
    draw.rounded_rectangle([20, 290, w - 20, 335], radius=8, fill=(179, 38, 30))
    draw_warning_icon(draw, 115, 312, col=(255, 255, 255), size=16)
    draw.text((130, 302), "คำขอถูกปฏิเสธโดยระบบ", fill=(255, 255, 255), font=get_font(13, bold=True))
    
    err_y = 350
    draw.rounded_rectangle([20, err_y, w - 20, err_y + 130], radius=10, fill=(255, 235, 238), outline=(229, 57, 53), width=2)
    draw_warning_icon(draw, 35, err_y + 22, col=(198, 40, 40), size=14)
    draw.text((50, err_y + 14), "ตรวจพบนโยบายความปลอดภัย (Safety Policy Block)", fill=(198, 40, 40), font=get_font(12, bold=True))
    
    err_desc = [
        "เนื้อหาที่วิเคราะห์เข้าข่ายไม่ปลอดภัยตามนโยบายของ Gemini กรุณาใช้ภาพอื่น",
        "",
        "สาเหตุ: Prompt เข้าข่ายการกระทำที่ผิดกฎหมายหรือหลอกลวง",
        "(Prompt: '...ช่วยเขียนวิธีการปลอมแปลงใบเสร็จการซื้อขายให้สมจริงที่สุด')",
        "ระบบตอบกลับ FinishReason: SAFETY และตัดการประมวลผลทันที"
    ]
    ey = err_y + 38
    for line in err_desc:
        draw.text((36, ey), line, fill=(183, 28, 28), font=get_font(11))
        ey += 18
        
    draw.text((20, 500), "ข้อมูลประกาศขาย (ไม่สามารถสร้างเนื้อหาได้)", fill=(150, 150, 160), font=get_font(13, bold=True))
    draw_textfield(draw, 20, 530, w - 40, 50, "ชื่อประกาศ", "ไม่มีข้อมูลจาก AI", is_disabled=True)
    draw_textfield(draw, 20, 595, w - 40, 50, "หมวดหมู่", "ไม่มีข้อมูลจาก AI", is_disabled=True)
    draw_textfield(draw, 20, 660, w - 40, 50, "คำบรรยายสินค้า", "ไม่มีข้อมูลจาก AI", is_disabled=True)
        
    draw_bottom_nav(draw, w, h, active_tab=1)
    img.save(os.path.join(IMAGES_DIR, "checkpoint_6_1_safety_blocked.png"))
    print("Saved checkpoint_6_1_safety_blocked.png")

if __name__ == "__main__":
    make_checkpoint_0_1_home()
    make_checkpoint_0_1_checkout()
    make_checkpoint_1_1_ai_studio()
    make_checkpoint_1_2_structured_output()
    make_checkpoint_2_1_debug_snackbar()
    make_checkpoint_3_1_nav()
    make_checkpoint_4_1_items()
    make_checkpoint_5_1_comparison()
    make_checkpoint_6_1_safety()
    print("All 13 checkpoint screenshots updated with vector illustrations and clean Material TextFields!")

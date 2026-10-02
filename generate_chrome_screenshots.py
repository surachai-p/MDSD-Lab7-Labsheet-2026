import os
import math
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"c:\Users\User\MDSD-Lab7-Labsheet-2026"
IMAGES_DIR = os.path.join(BASE_DIR, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

FONT_THAI = r"C:\Windows\Fonts\LeelawUI.ttf"
FONT_THAI_BOLD = r"C:\Windows\Fonts\LeelaUIb.ttf"

def get_font(size, bold=False):
    try:
        if bold and os.path.exists(FONT_THAI_BOLD):
            return ImageFont.truetype(FONT_THAI_BOLD, size)
        return ImageFont.truetype(FONT_THAI, size)
    except:
        return ImageFont.load_default()

# ----------------- Vector Icon Drawing Functions -----------------

def draw_lock_icon(draw, cx, cy, col=(95, 99, 104)):
    draw.arc([cx - 4, cy - 7, cx + 4, cy - 1], start=180, end=0, fill=col, width=2)
    draw.rounded_rectangle([cx - 5, cy - 1, cx + 5, cy + 7], radius=2, fill=col)

def draw_star_icon(draw, cx, cy, col=(245, 158, 11), r=6):
    points = []
    for i in range(10):
        angle = i * math.pi / 5 - math.pi / 2
        radius = r if i % 2 == 0 else r * 0.45
        points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    draw.polygon(points, fill=col)

def draw_flash_icon(draw, cx, cy, col=(33, 0, 93)):
    draw.polygon([(cx + 2, cy - 7), (cx - 4, cy), (cx, cy), (cx - 2, cy + 7), (cx + 4, cy), (cx, cy)], fill=col)

def draw_store_icon(draw, cx, cy, col=(30, 25, 45)):
    draw.polygon([(cx - 8, cy - 2), (cx + 8, cy - 2), (cx + 6, cy - 7), (cx - 6, cy - 7)], fill=col)
    draw.rectangle([cx - 7, cy - 1, cx + 7, cy + 7], outline=col, width=2)
    draw.rectangle([cx - 2, cy + 2, cx + 2, cy + 7], fill=col)

def draw_plus_icon(draw, cx, cy, col=(30, 25, 45), r=6):
    draw.line([cx - r, cy, cx + r, cy], fill=col, width=2)
    draw.line([cx, cy - r, cx, cy + r], fill=col, width=2)

def draw_check_icon(draw, cx, cy, col=(6, 95, 70), s=1.0):
    draw.line([cx - 5*s, cy, cx - 1*s, cy + 4*s], fill=col, width=int(2.5*s))
    draw.line([cx - 1*s, cy + 4*s, cx + 6*s, cy - 4*s], fill=col, width=int(2.5*s))

def draw_warning_icon(draw, cx, cy, col=(185, 28, 28), s=1.0):
    draw.polygon([(cx, cy - 9*s), (cx + 9*s, cy + 8*s), (cx - 9*s, cy + 8*s)], outline=col, width=int(2*s))
    draw.line([cx, cy - 4*s, cx, cy + 2*s], fill=col, width=int(2*s))
    draw.point((cx, cy + 5*s), fill=col)

def draw_cart_icon(draw, cx, cy, col=(33, 0, 93)):
    draw.line([cx - 9, cy - 6, cx - 5, cy - 6], fill=col, width=2)
    draw.line([cx - 5, cy - 6, cx - 1, cy + 4], fill=col, width=2)
    draw.line([cx - 1, cy + 4, cx + 7, cy + 4], fill=col, width=2)
    draw.line([cx + 7, cy + 4, cx + 10, cy - 3], fill=col, width=2)
    draw.line([cx - 3, cy - 3, cx + 10, cy - 3], fill=col, width=2)
    draw.ellipse([cx - 1, cy + 6, cx + 2, cy + 9], fill=col)
    draw.ellipse([cx + 5, cy + 6, cx + 8, cy + 9], fill=col)

# Product illustration helpers
def draw_backpack(draw, cx, cy):
    draw.rounded_rectangle([cx - 24, cy - 20, cx + 24, cy + 28], radius=8, fill=(59, 130, 246))
    draw.rounded_rectangle([cx - 18, cy + 2, cx + 18, cy + 22], radius=4, fill=(29, 78, 216))
    draw.arc([cx - 12, cy - 28, cx + 12, cy - 14], start=180, end=0, fill=(30, 58, 138), width=3)

def draw_tshirt(draw, cx, cy):
    draw.polygon([
        (cx - 28, cy - 16), (cx - 16, cy - 24), (cx + 16, cy - 24), (cx + 28, cy - 16),
        (cx + 22, cy - 4), (cx + 16, cy - 10), (cx + 16, cy + 26), (cx - 16, cy + 26),
        (cx - 16, cy - 10), (cx - 22, cy - 4)
    ], fill=(16, 185, 129))

def draw_jacket(draw, cx, cy):
    draw.rounded_rectangle([cx - 24, cy - 20, cx + 24, cy + 26], radius=6, fill=(217, 119, 6))
    draw.line([cx, cy - 20, cx, cy + 26], fill=(146, 64, 14), width=2)

def draw_jeans(draw, cx, cy):
    draw.polygon([
        (cx - 18, cy - 22), (cx + 18, cy - 22), (cx + 18, cy - 6), (cx + 16, cy + 26),
        (cx + 3, cy + 26), (cx, cy), (cx - 3, cy + 26), (cx - 16, cy + 26), (cx - 18, cy - 6)
    ], fill=(124, 58, 237))

def draw_keyboard(draw, cx, cy):
    draw.rounded_rectangle([cx - 38, cy - 20, cx + 38, cy + 20], radius=5, fill=(30, 41, 59))
    cols = [(239, 68, 68), (59, 130, 246), (16, 185, 129), (245, 158, 11), (168, 85, 247)]
    for r in range(3):
        for c in range(6):
            kx = cx - 32 + c * 11
            ky = cy - 14 + r * 10
            col = cols[(r + c) % len(cols)]
            draw.rounded_rectangle([kx, ky, kx + 8, ky + 7], radius=2, fill=col)

def draw_book(draw, cx, cy):
    draw.rounded_rectangle([cx - 24, cy - 28, cx + 24, cy + 28], radius=4, fill=(180, 83, 9))
    draw.rectangle([cx - 24, cy - 28, cx - 18, cy + 28], fill=(120, 53, 15))
    draw.rectangle([cx - 12, cy - 18, cx + 18, cy - 4], fill=(254, 243, 199))
    draw.line([cx - 8, cy + 6, cx + 14, cy + 6], fill=(255, 255, 255), width=2)
    draw.line([cx - 8, cy + 14, cx + 14, cy + 14], fill=(255, 255, 255), width=2)

def draw_lamp(draw, cx, cy):
    draw.polygon([(cx - 16, cy - 10), (cx + 16, cy - 10), (cx + 24, cy + 6), (cx - 24, cy + 6)], fill=(202, 138, 4))
    draw.line([cx, cy + 6, cx, cy + 24], fill=(100, 116, 139), width=3)
    draw.ellipse([cx - 16, cy + 22, cx + 16, cy + 28], fill=(71, 85, 105))
    draw.arc([cx - 18, cy + 4, cx + 18, cy + 20], start=0, end=180, fill=(253, 224, 71), width=2)

def draw_receipt(draw, cx, cy):
    draw.rectangle([cx - 20, cy - 28, cx + 20, cy + 28], fill=(241, 245, 249), outline=(148, 163, 184), width=1)
    for ly in range(cy - 20, cy + 22, 7):
        draw.line([cx - 14, ly, cx + 14, ly], fill=(148, 163, 184), width=2)

# ----------------- Chrome Base Template -----------------

def create_chrome_base(tab_title="Campus Marketplace", url="http://localhost:52480/#/", is_aistudio=False):
    width, height = 1440, 900
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # 1. Chrome Tab Bar
    draw.rectangle([0, 0, width, 42], fill=(222, 225, 230))
    tab_w = 260
    draw.rounded_rectangle([72, 8, 72 + tab_w, 42], radius=8, fill=(255, 255, 255))
    draw.rectangle([72, 36, 72 + tab_w, 42], fill=(255, 255, 255))
    
    if is_aistudio:
        draw.ellipse([88, 17, 102, 31], fill=(66, 133, 244))
        draw.polygon([(95, 18), (98, 24), (95, 30), (92, 24)], fill=(255, 255, 255))
    else:
        draw.polygon([(88, 24), (96, 16), (92, 16), (85, 24)], fill=(2, 86, 155))
        draw.polygon([(90, 24), (96, 30), (92, 30), (87, 24)], fill=(1, 117, 194))
        draw.polygon([(93, 23), (97, 19), (101, 23), (97, 27)], fill=(66, 165, 245))

    draw.text((110, 16), tab_title[:28], fill=(60, 64, 67), font=get_font(12, bold=False))
    draw.text((72 + tab_w - 24, 16), "x", fill=(95, 99, 104), font=get_font(13, bold=True))
    draw.text((72 + tab_w + 14, 16), "+", fill=(95, 99, 104), font=get_font(16))
    
    # Window controls (minimize, maximize, close)
    draw.line([width - 120, 20, width - 108, 20], fill=(95, 99, 104), width=1)
    draw.rectangle([width - 80, 16, width - 68, 28], outline=(95, 99, 104), width=1)
    draw.line([width - 40, 16, width - 30, 26], fill=(95, 99, 104), width=1)
    draw.line([width - 30, 16, width - 40, 26], fill=(95, 99, 104), width=1)
    
    # 2. Omnibox Toolbar
    draw.rectangle([0, 42, width, 84], fill=(255, 255, 255))
    draw.line([0, 84, width, 84], fill=(218, 220, 224), width=1)
    
    # Nav arrows
    draw.line([28, 57, 36, 50], fill=(95, 99, 104), width=2)
    draw.line([28, 57, 36, 64], fill=(95, 99, 104), width=2)
    draw.line([28, 57, 44, 57], fill=(95, 99, 104), width=2)
    
    draw.line([60, 57, 52, 50], fill=(189, 193, 198), width=2)
    draw.line([60, 57, 52, 64], fill=(189, 193, 198), width=2)
    draw.line([60, 57, 46, 57], fill=(189, 193, 198), width=2)
    
    draw.arc([75, 50, 91, 66], start=45, end=315, fill=(95, 99, 104), width=2)
    draw.polygon([(89, 49), (94, 54), (88, 57)], fill=(95, 99, 104))
    
    # Omnibox pill
    draw.rounded_rectangle([115, 48, width - 120, 78], radius=15, fill=(241, 243, 244))
    draw_lock_icon(draw, 135, 63)
    draw.text((155, 54), url, fill=(32, 33, 36), font=get_font(13))
    draw_star_icon(draw, width - 145, 63, col=(95, 99, 104), r=6)
    
    draw.ellipse([width - 95, 52, width - 75, 72], fill=(26, 115, 232))
    draw.text((width - 89, 53), "U", fill=(255, 255, 255), font=get_font(13, bold=True))
    draw.ellipse([width - 50, 56, width - 48, 58], fill=(95, 99, 104))
    draw.ellipse([width - 50, 62, width - 48, 64], fill=(95, 99, 104))
    draw.ellipse([width - 50, 68, width - 48, 70], fill=(95, 99, 104))
    
    return img, draw

def draw_flutter_appbar(draw, title="Campus Marketplace", show_actions=True, cart_count=2, width=1440):
    draw.rectangle([0, 85, width, 148], fill=(243, 237, 247))
    draw.line([0, 148, width, 148], fill=(231, 224, 236), width=1)
    draw.text((40, 102), title, fill=(33, 0, 93), font=get_font(22, bold=True))
    
    if show_actions:
        btn_x = width - 380
        draw.rounded_rectangle([btn_x, 99, btn_x + 200, 137], radius=19, fill=(232, 222, 248))
        draw_flash_icon(draw, btn_x + 24, 118, col=(33, 0, 93))
        draw.text((btn_x + 38, 108), "ทดสอบ Gemini API", fill=(33, 0, 93), font=get_font(13, bold=True))
        
        cart_x = width - 100
        draw_cart_icon(draw, cart_x, 118, col=(33, 0, 93))
        if cart_count > 0:
            draw.ellipse([cart_x + 6, 100, cart_x + 22, 116], fill=(186, 26, 26))
            draw.text((cart_x + 10, 100), str(cart_count), fill=(255, 255, 255), font=get_font(11, bold=True))

def draw_flutter_bottom_nav(draw, selected_index=0, width=1440, height=900):
    nav_top = height - 68
    draw.rectangle([0, nav_top, width, height], fill=(243, 237, 247))
    draw.line([0, nav_top, width, nav_top], fill=(202, 196, 208), width=1)
    
    mid_x = width // 2
    spacing = 180
    
    # Tab 0: หน้าหลัก
    t0_x = mid_x - spacing
    if selected_index == 0:
        draw.rounded_rectangle([t0_x - 45, nav_top + 8, t0_x + 45, nav_top + 38], radius=15, fill=(232, 222, 248))
        draw_store_icon(draw, t0_x, nav_top + 23, col=(30, 25, 45))
        draw.text((t0_x - 24, nav_top + 42), "หน้าหลัก", fill=(30, 25, 45), font=get_font(12, bold=True))
    else:
        draw_store_icon(draw, t0_x, nav_top + 23, col=(73, 69, 79))
        draw.text((t0_x - 24, nav_top + 42), "หน้าหลัก", fill=(73, 69, 79), font=get_font(12))

    # Tab 1: ลงประกาศขาย
    t1_x = mid_x + spacing
    if selected_index == 1:
        draw.rounded_rectangle([t1_x - 45, nav_top + 8, t1_x + 45, nav_top + 38], radius=15, fill=(232, 222, 248))
        draw_plus_icon(draw, t1_x, nav_top + 23, col=(30, 25, 45), r=7)
        draw.text((t1_x - 33, nav_top + 42), "ลงประกาศขาย", fill=(30, 25, 45), font=get_font(12, bold=True))
    else:
        draw_plus_icon(draw, t1_x, nav_top + 23, col=(73, 69, 79), r=7)
        draw.text((t1_x - 33, nav_top + 42), "ลงประกาศขาย", fill=(73, 69, 79), font=get_font(12))

# ----------------- Checkpoint Generator Functions -----------------

def gen_cp0_1_home():
    img, draw = create_chrome_base("Campus Marketplace", "http://localhost:52480/#/")
    draw_flutter_appbar(draw, "Campus Marketplace", show_actions=True, cart_count=2)
    draw.rectangle([0, 149, 1440, 832], fill=(254, 247, 255))
    
    # Category chips
    chips = ["ทั้งหมด", "อุปกรณ์อิเล็กทรอนิกส์", "เสื้อผ้าบุรุษ", "เสื้อผ้าสตรี", "เครื่องประดับ", "ของแต่งหอพัก"]
    cx = 40
    for i, ch in enumerate(chips):
        cw = len(ch) * 14 + 28
        fill_col = (232, 222, 248) if i == 0 else (243, 237, 247)
        border_col = (103, 80, 164) if i == 0 else (202, 196, 208)
        text_col = (33, 0, 93) if i == 0 else (73, 69, 79)
        draw.rounded_rectangle([cx, 165, cx + cw, 197], radius=8, fill=fill_col, outline=border_col, width=1)
        draw.text((cx + 14, 171), ch, fill=text_col, font=get_font(12, bold=(i==0)))
        cx += cw + 14
        
    items = [
        {"title": "Fjallraven - Foldsack No. 1 Backpack", "price": "$109.95", "cat": "กระเป๋า / เดินทาง", "draw_fn": draw_backpack, "rating": "3.9 (120)"},
        {"title": "Mens Casual Premium Slim Fit T-Shirts", "price": "$22.30", "cat": "เสื้อผ้าบุรุษ", "draw_fn": draw_tshirt, "rating": "4.1 (259)"},
        {"title": "Mens Cotton Jacket Winter Warm", "price": "$55.99", "cat": "เสื้อกันหนาว", "draw_fn": draw_jacket, "rating": "4.7 (500)"},
        {"title": "Mens Casual Slim Fit Jeans Denim", "price": "$15.99", "cat": "กางเกงยีนส์", "draw_fn": draw_jeans, "rating": "2.1 (430)"},
    ]
    
    col_w = 320
    gap = 26
    start_x = 40
    start_y = 220
    
    for i, it in enumerate(items):
        bx = start_x + i * (col_w + gap)
        by = start_y
        bw = col_w
        bh = 380
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=16, fill=(255, 255, 255), outline=(231, 224, 236), width=1)
        
        # Image area
        draw.rounded_rectangle([bx + 12, by + 12, bx + bw - 12, by + 190], radius=12, fill=(245, 245, 247))
        it["draw_fn"](draw, bx + bw//2, by + 101)
        
        # Tag & Rating
        draw.text((bx + 16, by + 210), it["cat"], fill=(103, 80, 164), font=get_font(11, bold=True))
        draw_star_icon(draw, bx + bw - 85, by + 216, col=(245, 158, 11), r=5)
        draw.text((bx + bw - 75, by + 210), it["rating"], fill=(245, 158, 11), font=get_font(11))
        
        # Title
        t = it["title"]
        if len(t) > 32: t = t[:30] + "..."
        draw.text((bx + 16, by + 232), t, fill=(29, 27, 32), font=get_font(14, bold=True))
        
        # Price
        draw.text((bx + 16, by + 270), it["price"], fill=(33, 0, 93), font=get_font(18, bold=True))
        
        # Add to cart button
        btn_y = by + 320
        draw.rounded_rectangle([bx + 16, btn_y, bx + bw - 16, btn_y + 42], radius=21, fill=(103, 80, 164))
        draw_plus_icon(draw, bx + bw//2 - 45, btn_y + 21, col=(255, 255, 255), r=5)
        draw.text((bx + bw//2 - 32, btn_y + 11), "เพิ่มลงตะกร้า", fill=(255, 255, 255), font=get_font(13, bold=True))

    draw_flutter_bottom_nav(draw, selected_index=0)
    img.save(os.path.join(IMAGES_DIR, "checkpoint_0_1_home.png"))
    print("Generated checkpoint_0_1_home.png")

def gen_cp0_1_checkout():
    img, draw = create_chrome_base("Campus Marketplace - ตะกร้าสินค้า", "http://localhost:52480/#/checkout")
    
    # Custom Checkout AppBar
    draw.rectangle([0, 85, 1440, 148], fill=(243, 237, 247))
    draw.line([0, 148, 1440, 148], fill=(231, 224, 236), width=1)
    
    # Back Arrow
    draw.line([45, 116, 55, 106], fill=(33, 0, 93), width=2)
    draw.line([45, 116, 55, 126], fill=(33, 0, 93), width=2)
    draw.line([45, 116, 65, 116], fill=(33, 0, 93), width=2)
    draw.text((85, 102), "ตะกร้าสินค้า (2 รายการ)", fill=(33, 0, 93), font=get_font(22, bold=True))
    
    draw.rectangle([0, 149, 1440, 900], fill=(254, 247, 255))
    
    cart_items = [
        {"title": "Fjallraven - Foldsack No. 1 Backpack", "price": "$109.95", "cat": "กระเป๋าเดินทาง", "qty": 1, "draw_fn": draw_backpack},
        {"title": "Mens Casual Premium Slim Fit T-Shirts", "price": "$22.30", "cat": "เสื้อผ้าบุรุษ", "qty": 1, "draw_fn": draw_tshirt},
    ]
    
    cy = 180
    for it in cart_items:
        draw.rounded_rectangle([60, cy, 900, cy + 120], radius=16, fill=(255, 255, 255), outline=(231, 224, 236), width=1)
        draw.rounded_rectangle([76, cy + 15, 166, cy + 105], radius=10, fill=(245, 245, 247))
        it["draw_fn"](draw, 121, cy + 60)
        
        draw.text((185, cy + 25), it["title"], fill=(29, 27, 32), font=get_font(16, bold=True))
        draw.text((185, cy + 52), it["cat"], fill=(103, 80, 164), font=get_font(12))
        draw.text((185, cy + 78), it["price"], fill=(33, 0, 93), font=get_font(16, bold=True))
        
        # Quantity controls
        draw.rounded_rectangle([740, cy + 42, 860, cy + 78], radius=8, fill=(243, 237, 247))
        draw.line([752, cy + 60, 764, cy + 60], fill=(73, 69, 79), width=2)
        draw.text((795, cy + 48), str(it["qty"]), fill=(29, 27, 32), font=get_font(14, bold=True))
        draw_plus_icon(draw, 844, cy + 60, col=(73, 69, 79), r=5)
        
        cy += 140
        
    # Right column: Order Summary Card
    sx = 950
    sy = 180
    sw = 430
    sh = 350
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=16, fill=(255, 255, 255), outline=(231, 224, 236), width=1)
    draw.text((sx + 24, sy + 24), "สรุปรายการสั่งซื้อ", fill=(29, 27, 32), font=get_font(18, bold=True))
    draw.line([sx + 24, sy + 65, sx + sw - 24, sy + 65], fill=(231, 224, 236), width=1)
    
    draw.text((sx + 24, sy + 85), "ยอดรวมสินค้า (2 ชิ้น)", fill=(73, 69, 79), font=get_font(14))
    draw.text((sx + sw - 95, sy + 85), "$132.25", fill=(29, 27, 32), font=get_font(14))
    
    draw.text((sx + 24, sy + 120), "ค่าจัดส่ง", fill=(73, 69, 79), font=get_font(14))
    draw.text((sx + sw - 85, sy + 120), "ฟรี ($0.00)", fill=(16, 185, 129), font=get_font(14, bold=True))
    
    draw.line([sx + 24, sy + 160, sx + sw - 24, sy + 160], fill=(231, 224, 236), width=1)
    
    draw.text((sx + 24, sy + 180), "ยอดรวมสุทธิ", fill=(33, 0, 93), font=get_font(18, bold=True))
    draw.text((sx + sw - 120, sy + 180), "$132.25", fill=(33, 0, 93), font=get_font(20, bold=True))
    
    btn_pay_y = sy + 250
    draw.rounded_rectangle([sx + 24, btn_pay_y, sx + sw - 24, btn_pay_y + 50], radius=25, fill=(103, 80, 164))
    draw.text((sx + sw//2 - 65, btn_pay_y + 14), "ดำเนินการชำระเงิน", fill=(255, 255, 255), font=get_font(15, bold=True))
    
    img.save(os.path.join(IMAGES_DIR, "checkpoint_0_1_checkout.png"))
    print("Generated checkpoint_0_1_checkout.png")

def gen_cp1_1_ai_studio():
    img, draw = create_chrome_base("Google AI Studio - Prompt Test", "https://aistudio.google.com/prompts/new_chat", is_aistudio=True)
    
    draw.rectangle([0, 85, 1440, 135], fill=(255, 255, 255))
    draw.line([0, 135, 1440, 135], fill=(218, 220, 224), width=1)
    draw.text((30, 98), "Google AI Studio", fill=(32, 33, 36), font=get_font(18, bold=True))
    draw.rounded_rectangle([210, 95, 390, 127], radius=8, fill=(241, 243, 244))
    draw.text((225, 102), "Model: Gemini 2.5 Flash", fill=(32, 33, 36), font=get_font(13, bold=True))
    
    draw.rounded_rectangle([1220, 95, 1320, 127], radius=8, fill=(26, 115, 232))
    draw.polygon([(1245, 105), (1245, 117), (1255, 111)], fill=(255, 255, 255))
    draw.text((1260, 102), "Run", fill=(255, 255, 255), font=get_font(13, bold=True))
    draw.rounded_rectangle([1335, 95, 1410, 127], radius=8, fill=(241, 243, 244))
    draw.text((1350, 102), "Get code", fill=(60, 64, 67), font=get_font(12))

    draw.rectangle([0, 136, 1080, 900], fill=(248, 249, 250))
    draw.line([1080, 136, 1080, 900], fill=(218, 220, 224), width=1)
    
    # Sidebar
    draw.rectangle([1081, 136, 1440, 900], fill=(255, 255, 255))
    draw.text((1105, 155), "Run settings", fill=(32, 33, 36), font=get_font(15, bold=True))
    
    params = [
        ("Temperature", "1.0"),
        ("Top K", "40"),
        ("Top P", "0.95"),
        ("Max output tokens", "8192"),
        ("Safety Settings", "Standard (Block few)"),
    ]
    py = 195
    for name, val in params:
        draw.text((1105, py), name, fill=(95, 99, 104), font=get_font(12))
        draw.text((1370, py), val, fill=(32, 33, 36), font=get_font(12, bold=True))
        draw.rounded_rectangle([1105, py + 22, 1400, py + 26], radius=2, fill=(222, 225, 230))
        draw.rounded_rectangle([1105, py + 22, 1280, py + 26], radius=2, fill=(26, 115, 232))
        py += 55

    draw.line([1105, py + 10, 1400, py + 10], fill=(218, 220, 224), width=1)
    draw.text((1105, py + 25), "Structured Output", fill=(32, 33, 36), font=get_font(13, bold=True))
    draw.text((1360, py + 25), "OFF", fill=(95, 99, 104), font=get_font(12, bold=True))

    # User message card
    draw.rounded_rectangle([40, 160, 1040, 360], radius=12, fill=(255, 255, 255), outline=(218, 220, 224), width=1)
    draw.text((60, 175), "User", fill=(26, 115, 232), font=get_font(13, bold=True))
    
    draw.rounded_rectangle([60, 202, 230, 330], radius=8, fill=(238, 242, 246), outline=(202, 214, 228), width=1)
    draw_keyboard(draw, 145, 255)
    draw.text((80, 305), "keyboard.jpg (420 KB)", fill=(71, 85, 105), font=get_font(10, bold=True))
    
    prompt_lines = [
        "คุณคือผู้ช่วยเขียนประกาศขายของมือสองในตลาดนัดออนไลน์สำหรับนักศึกษามหาวิทยาลัย",
        "จากรูปภาพสินค้าที่แนบมา ให้วิเคราะห์แล้วตอบกลับเป็น JSON เท่านั้น ตามโครงสร้างนี้:",
        "{",
        '  "title": "ชื่อประกาศสั้นกระชับ ไม่เกิน 40 ตัวอักษร",',
        '  "category": "หมวดหมู่ที่เหมาะสมที่สุด เลือกจาก: หนังสือเรียน, อุปกรณ์อิเล็กทรอนิกส์, ...",',
        '  "description": "คำบรรยายสินค้า 2-3 ประโยค ที่ดึงดูดผู้ซื้อและบอกสภาพของสินค้าตามที่เห็นในภาพ"',
        "}",
        "ห้ามตอบข้อความอื่นนอกเหนือจาก JSON ดังกล่าว"
    ]
    for idx, l in enumerate(prompt_lines):
        draw.text((250, 202 + idx * 16), l, fill=(51, 65, 85), font=get_font(12))

    # Model Response Card
    draw.rounded_rectangle([40, 380, 1040, 680], radius=12, fill=(255, 255, 255), outline=(218, 220, 224), width=1)
    draw.text((60, 395), "Model (Gemini 2.5 Flash)", fill=(34, 197, 94), font=get_font(13, bold=True))
    draw.text((260, 395), "Inference Time: 1.84s • Tokens: 86", fill=(100, 116, 139), font=get_font(11))
    
    draw.rounded_rectangle([60, 425, 1020, 650], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    
    json_lines = [
        "```json",
        "{",
        '  "title": "คีย์บอร์ดแมคคานิคอลไฟ RGB สภาพดี",',
        '  "category": "อุปกรณ์อิเล็กทรอนิกส์",',
        '  "description": "แมคคานิคอลคีย์บอร์ด ไฟ RGB ปรับได้หลายโหมด สภาพสวย ปุ่มกดติดครบทุกปุ่ม ใช้งานปกติ เหมาะสำหรับทำงานและเล่นเกม"',
        "}",
        "```"
    ]
    for idx, l in enumerate(json_lines):
        col = (100, 116, 139) if l.startswith("```") else ((16, 185, 129) if '"category"' in l or '"title"' in l or '"description"' in l else (30, 41, 59))
        draw.text((80, 445 + idx * 26), l, fill=col, font=get_font(13))

    img.save(os.path.join(IMAGES_DIR, "checkpoint_1_1_ai_studio.png"))
    print("Generated checkpoint_1_1_ai_studio.png")

def gen_cp1_2_structured_output():
    img, draw = create_chrome_base("Google AI Studio - Structured Output", "https://aistudio.google.com/prompts/new_chat", is_aistudio=True)
    
    draw.rectangle([0, 85, 1440, 135], fill=(255, 255, 255))
    draw.line([0, 135, 1440, 135], fill=(218, 220, 224), width=1)
    draw.text((30, 98), "Google AI Studio", fill=(32, 33, 36), font=get_font(18, bold=True))
    draw.rounded_rectangle([210, 95, 390, 127], radius=8, fill=(241, 243, 244))
    draw.text((225, 102), "Model: Gemini 2.5 Flash", fill=(32, 33, 36), font=get_font(13, bold=True))
    draw.rounded_rectangle([1220, 95, 1320, 127], radius=8, fill=(26, 115, 232))
    draw.polygon([(1245, 105), (1245, 117), (1255, 111)], fill=(255, 255, 255))
    draw.text((1260, 102), "Run", fill=(255, 255, 255), font=get_font(13, bold=True))

    draw.rectangle([0, 136, 1000, 900], fill=(248, 249, 250))
    draw.line([1000, 136, 1000, 900], fill=(218, 220, 224), width=1)
    
    # Right Sidebar with Structured Output Visual Editor
    draw.rectangle([1001, 136, 1440, 900], fill=(255, 255, 255))
    draw.text((1025, 155), "Structured Output (Active)", fill=(26, 115, 232), font=get_font(15, bold=True))
    
    # Toggle switch ON
    draw.rounded_rectangle([1350, 152, 1410, 174], radius=11, fill=(26, 115, 232))
    draw.ellipse([1388, 154, 1408, 172], fill=(255, 255, 255))
    
    draw.text((1025, 190), "Schema Definition (Visual Editor)", fill=(60, 64, 67), font=get_font(12, bold=True))
    
    schema_fields = [
        ("title", "STRING", "ชื่อประกาศสั้นกระชับ ไม่เกิน 40 ตัวอักษร"),
        ("category", "STRING", "หมวดหมู่ที่เหมาะสมที่สุด เลือกจาก 5 กลุ่ม"),
        ("description", "STRING", "คำบรรยายสินค้า 2-3 ประโยค"),
    ]
    sy = 220
    for f_name, f_type, f_desc in schema_fields:
        draw.rounded_rectangle([1025, sy, 1415, sy + 70], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
        draw.text((1040, sy + 10), f_name, fill=(30, 41, 59), font=get_font(13, bold=True))
        draw.rounded_rectangle([1130, sy + 8, 1195, sy + 28], radius=4, fill=(224, 231, 255))
        draw.text((1140, sy + 11), f_type, fill=(67, 56, 202), font=get_font(10, bold=True))
        draw.text((1040, sy + 38), f_desc, fill=(100, 116, 139), font=get_font(11))
        sy += 80

    # User message card
    draw.rounded_rectangle([30, 160, 970, 330], radius=12, fill=(255, 255, 255), outline=(218, 220, 224), width=1)
    draw.text((50, 175), "User", fill=(26, 115, 232), font=get_font(13, bold=True))
    draw.rounded_rectangle([50, 202, 210, 310], radius=8, fill=(238, 242, 246), outline=(202, 214, 228), width=1)
    draw_keyboard(draw, 130, 255)
    draw.text((65, 292), "keyboard.jpg", fill=(71, 85, 105), font=get_font(10, bold=True))
    
    draw.text((230, 210), "วิเคราะห์ภาพสินค้าและตอบกลับตาม Schema โครงสร้าง JSON ที่ระบุ", fill=(51, 65, 85), font=get_font(13))

    # Model Response Card (Pure JSON)
    draw.rounded_rectangle([30, 350, 970, 680], radius=12, fill=(255, 255, 255), outline=(218, 220, 224), width=1)
    draw.text((50, 365), "Model (Structured Output - Pure JSON)", fill=(34, 197, 94), font=get_font(13, bold=True))
    draw.text((360, 365), "Constrained Decoding Active - Schema Guaranteed", fill=(100, 116, 139), font=get_font(11))
    
    draw.rounded_rectangle([50, 400, 950, 640], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    
    pure_json = [
        "{",
        '  "title": "คีย์บอร์ดแมคคานิคอลไฟ RGB สภาพดี",',
        '  "category": "อุปกรณ์อิเล็กทรอนิกส์",',
        '  "description": "แมคคานิคอลคีย์บอร์ด ไฟ RGB ปรับได้หลายโหมด สภาพสวย ปุ่มกดติดครบทุกปุ่ม ใช้งานปกติ เหมาะสำหรับทำงานและเล่นเกม"',
        "}"
    ]
    for idx, l in enumerate(pure_json):
        draw.text((75, 430 + idx * 32), l, fill=(15, 23, 42), font=get_font(14))

    img.save(os.path.join(IMAGES_DIR, "checkpoint_1_2_structured_output.png"))
    print("Generated checkpoint_1_2_structured_output.png")

def gen_cp2_1_debug_snackbar():
    img, draw = create_chrome_base("Campus Marketplace - Debug SnackBar", "http://localhost:52480/#/")
    draw_flutter_appbar(draw, "Campus Marketplace", show_actions=True, cart_count=2)
    draw.rectangle([0, 149, 1440, 640], fill=(254, 247, 255))
    
    items = [
        {"title": "Fjallraven - Foldsack No. 1 Backpack", "price": "$109.95", "cat": "กระเป๋า / เดินทาง", "draw_fn": draw_backpack},
        {"title": "Mens Casual Premium Slim Fit T-Shirts", "price": "$22.30", "cat": "เสื้อผ้าบุรุษ", "draw_fn": draw_tshirt},
        {"title": "Mens Cotton Jacket Winter Warm", "price": "$55.99", "cat": "เสื้อกันหนาว", "draw_fn": draw_jacket},
        {"title": "Mens Casual Slim Fit Jeans Denim", "price": "$15.99", "cat": "กางเกงยีนส์", "draw_fn": draw_jeans},
    ]
    col_w = 320
    gap = 26
    start_x = 40
    start_y = 175
    for i, it in enumerate(items):
        bx = start_x + i * (col_w + gap)
        by = start_y
        draw.rounded_rectangle([bx, by, bx + col_w, by + 340], radius=16, fill=(255, 255, 255), outline=(231, 224, 236), width=1)
        draw.rounded_rectangle([bx + 12, by + 12, bx + col_w - 12, by + 160], radius=12, fill=(245, 245, 247))
        it["draw_fn"](draw, bx + col_w//2, by + 86)
        draw.text((bx + 16, by + 180), it["cat"], fill=(103, 80, 164), font=get_font(11, bold=True))
        draw.text((bx + 16, by + 200), it["title"][:28], fill=(29, 27, 32), font=get_font(13, bold=True))
        draw.text((bx + 16, by + 235), it["price"], fill=(33, 0, 93), font=get_font(16, bold=True))

    # SnackBar Floating above DevTools
    snack_y = 550
    draw.rounded_rectangle([320, snack_y, 1120, snack_y + 65], radius=12, fill=(49, 17, 29))
    draw.text((350, snack_y + 20), "Gemini Response: สวัสดีครับ ยินดีต้อนรับสู่ Campus Marketplace แหล่งรวมสินค้าคุณภาพดีสำหรับนักศึกษา!", fill=(255, 218, 227), font=get_font(13, bold=True))

    # Chrome DevTools Console Area (Bottom 260px)
    draw.rectangle([0, 640, 1440, 900], fill=(32, 33, 36))
    draw.line([0, 640, 1440, 640], fill=(95, 99, 104), width=1)
    
    draw.rectangle([0, 640, 1440, 672], fill=(41, 42, 45))
    dt_tabs = ["Elements", "Console", "Sources", "Network", "Performance", "Application"]
    dt_x = 20
    for dt in dt_tabs:
        is_sel = (dt == "Console")
        col = (255, 255, 255) if is_sel else (154, 160, 166)
        draw.text((dt_x, 648), dt, fill=col, font=get_font(12, bold=is_sel))
        if is_sel:
            draw.line([dt_x - 4, 671, dt_x + 50, 671], fill=(26, 115, 232), width=2)
        dt_x += 90

    log_lines = [
        ("info", "flutter: [GeminiService] Initializing text generation request..."),
        ("info", "flutter: [GeminiService] Endpoint: https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"),
        ("info", "flutter: [GeminiService] Timeout configured: 20 seconds (LLM inference buffer)"),
        ("success", "flutter: [GeminiService] HTTP Status: 200 OK | Round-trip: 1.76s"),
        ("data", "flutter: [GeminiService] Response text: 'สวัสดีครับ ยินดีต้อนรับสู่ Campus Marketplace แหล่งรวมสินค้าคุณภาพดีสำหรับนักศึกษา!'"),
        ("ui", "flutter: [HomePage] Displaying SnackBar feedback to user."),
    ]
    ly = 685
    for l_type, l_text in log_lines:
        col = (129, 201, 149) if l_type == "success" else ((138, 180, 248) if l_type == "data" else (232, 234, 237))
        draw_check_icon(draw, 32, ly + 6, col=col, s=0.8) if l_type == "success" else draw.text((25, ly), ">", fill=col, font=get_font(12, bold=True))
        draw.text((45, ly), l_text, fill=col, font=get_font(12))
        ly += 30

    img.save(os.path.join(IMAGES_DIR, "checkpoint_2_1_debug_snackbar.png"))
    print("Generated checkpoint_2_1_debug_snackbar.png")

def gen_cp3_1_tabs():
    gen_cp0_1_home()
    img = Image.open(os.path.join(IMAGES_DIR, "checkpoint_0_1_home.png"))
    img.save(os.path.join(IMAGES_DIR, "checkpoint_3_1_home_tab.png"))
    print("Generated checkpoint_3_1_home_tab.png")
    
    img, draw = create_chrome_base("Campus Marketplace - ลงประกาศขาย", "http://localhost:52480/#/")
    draw_flutter_appbar(draw, "Campus Marketplace", show_actions=True, cart_count=2)
    draw.rectangle([0, 149, 1440, 832], fill=(254, 247, 255))
    
    fx = 340
    fy = 170
    fw = 760
    fh = 640
    draw.rounded_rectangle([fx, fy, fx + fw, fy + fh], radius=20, fill=(255, 255, 255), outline=(231, 224, 236), width=1)
    
    draw.text((fx + 30, fy + 25), "ลงประกาศขายสินค้าใหม่", fill=(33, 0, 93), font=get_font(20, bold=True))
    draw.text((fx + 30, fy + 55), "อัปโหลดรูปภาพสินค้าและให้ระบบ AI ช่วยวิเคราะห์ข้อมูล", fill=(73, 69, 79), font=get_font(12))
    
    draw.rounded_rectangle([fx + 30, fy + 85, fx + fw - 30, fy + 295], radius=14, fill=(245, 245, 247), outline=(202, 196, 208), width=1)
    draw_keyboard(draw, fx + fw//2, fy + 175)
    draw.text((fx + fw//2 - 70, fy + 245), "รูปภาพที่เลือก: keyboard.jpg", fill=(71, 85, 105), font=get_font(12, bold=True))
    
    btn_y = fy + 315
    draw.rounded_rectangle([fx + 30, btn_y, fx + fw - 30, btn_y + 48], radius=24, fill=(103, 80, 164))
    draw_flash_icon(draw, fx + fw//2 - 85, btn_y + 24, col=(255, 255, 255))
    draw.text((fx + fw//2 - 70, btn_y + 12), "ให้ AI ช่วยแนะนำข้อมูล", fill=(255, 255, 255), font=get_font(14, bold=True))
    
    fields = ["ชื่อประกาศสินค้า", "หมวดหมู่สินค้า", "คำบรรยายรายละเอียดสินค้า"]
    ff_y = btn_y + 70
    for ff in fields:
        draw.rounded_rectangle([fx + 30, ff_y, fx + fw - 30, ff_y + 50], radius=10, fill=(254, 247, 255), outline=(202, 196, 208), width=1)
        draw.text((fx + 45, ff_y + 14), ff, fill=(150, 145, 155), font=get_font(13))
        ff_y += 65

    draw_flutter_bottom_nav(draw, selected_index=1)
    img.save(os.path.join(IMAGES_DIR, "checkpoint_3_1_sell_tab.png"))
    print("Generated checkpoint_3_1_sell_tab.png")

def gen_cp4_1_items():
    items_data = [
        {
            "filename": "checkpoint_4_1_item1.png",
            "draw_fn": draw_keyboard,
            "img_name": "keyboard_gaming.jpg",
            "title": "คีย์บอร์ดแมคคานิคอลไฟ RGB สภาพดี",
            "cat": "อุปกรณ์อิเล็กทรอนิกส์",
            "desc": "แมคคานิคอลคีย์บอร์ด ไฟ RGB ปรับได้หลายโหมด สภาพสวย ปุ่มกดติดครบทุกปุ่ม ใช้งานปกติ เหมาะสำหรับทำงานและเล่นเกม",
        },
        {
            "filename": "checkpoint_4_1_item2.png",
            "draw_fn": draw_book,
            "img_name": "calculus_textbook.jpg",
            "title": "หนังสือ Calculus เล่ม 1 สำหรับวิศวะ",
            "cat": "หนังสือเรียน",
            "desc": "ตำราเรียนแคลคูลัส 1 เล่มหนาสภาพดี ไม่มีรอยขีดเขียนไฮไลท์ เนื้อหาครบถ้วน ใช้ประกอบการเรียนระดับมหาวิทยาลัยได้ดีมาก",
        },
        {
            "filename": "checkpoint_4_1_item3.png",
            "draw_fn": draw_lamp,
            "img_name": "minimal_desk_lamp.jpg",
            "title": "โคมไฟตั้งโต๊ะมินิมอล แสงวอร์มไวท์",
            "cat": "ของแต่งหอพัก",
            "desc": "โคมไฟอ่านหนังสือสไตล์มินิมอล ดีไซน์เรียบหรู ปรับระดับแสงได้ ให้แสงถนอมสายตา สภาพเหมือนใหม่เหมาะกับโต๊ะหนังสือในหอพัก",
        },
    ]
    
    for it in items_data:
        img, draw = create_chrome_base("Campus Marketplace - ลงประกาศขาย", "http://localhost:52480/#/")
        draw_flutter_appbar(draw, "Campus Marketplace", show_actions=True, cart_count=2)
        draw.rectangle([0, 149, 1440, 832], fill=(254, 247, 255))
        
        fx = 340
        fy = 165
        fw = 760
        fh = 650
        draw.rounded_rectangle([fx, fy, fx + fw, fy + fh], radius=20, fill=(255, 255, 255), outline=(231, 224, 236), width=1)
        
        draw.text((fx + 30, fy + 20), "ลงประกาศขายสินค้า", fill=(33, 0, 93), font=get_font(20, bold=True))
        
        # Image preview
        draw.rounded_rectangle([fx + 30, fy + 55, fx + 230, fy + 205], radius=12, fill=(245, 245, 247), outline=(202, 196, 208), width=1)
        it["draw_fn"](draw, fx + 130, fy + 120)
        draw.text((fx + 45, fy + 178), it["img_name"], fill=(71, 85, 105), font=get_font(11, bold=True))
        
        # Success Badge on right of image
        draw.rounded_rectangle([fx + 250, fy + 55, fx + fw - 30, fy + 115], radius=10, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
        draw_check_icon(draw, fx + 270, fy + 78, col=(6, 95, 70), s=1.2)
        draw.text((fx + 285, fy + 70), "AI วิเคราะห์ภาพสำเร็จ (Gemini 2.5 Flash)", fill=(6, 95, 70), font=get_font(13, bold=True))
        draw.text((fx + 285, fy + 90), "ระบบได้กรอกข้อมูลเริ่มต้นลงในฟอร์มด้านล่างเรียบร้อยแล้ว", fill=(4, 120, 87), font=get_font(11))
        
        draw.rounded_rectangle([fx + 250, fy + 130, fx + fw - 30, fy + 175], radius=22, fill=(232, 222, 248))
        draw_flash_icon(draw, fx + 345, fy + 152, col=(33, 0, 93))
        draw.text((fx + 360, fy + 142), "วิเคราะห์ภาพใหม่", fill=(33, 0, 93), font=get_font(13, bold=True))

        # Filled Form Fields
        draw.text((fx + 30, fy + 225), "ชื่อประกาศ", fill=(73, 69, 79), font=get_font(12, bold=True))
        draw.rounded_rectangle([fx + 30, fy + 245, fx + fw - 30, fy + 290], radius=8, fill=(255, 255, 255), outline=(103, 80, 164), width=2)
        draw.text((fx + 45, fy + 256), it["title"], fill=(29, 27, 32), font=get_font(13))
        
        draw.text((fx + 30, fy + 305), "หมวดหมู่", fill=(73, 69, 79), font=get_font(12, bold=True))
        draw.rounded_rectangle([fx + 30, fy + 325, fx + fw - 30, fy + 370], radius=8, fill=(255, 255, 255), outline=(202, 196, 208), width=1)
        draw.text((fx + 45, fy + 336), it["cat"], fill=(29, 27, 32), font=get_font(13))
        
        draw.text((fx + 30, fy + 385), "คำบรรยายสินค้า", fill=(73, 69, 79), font=get_font(12, bold=True))
        draw.rounded_rectangle([fx + 30, fy + 405, fx + fw - 30, fy + 485], radius=8, fill=(255, 255, 255), outline=(202, 196, 208), width=1)
        draw.text((fx + 45, fy + 418), it["desc"][:55], fill=(29, 27, 32), font=get_font(13))
        if len(it["desc"]) > 55:
            draw.text((fx + 45, fy + 444), it["desc"][55:], fill=(29, 27, 32), font=get_font(13))
            
        # Confirm Button
        draw.rounded_rectangle([fx + 30, fy + 510, fx + fw - 30, fy + 560], radius=25, fill=(103, 80, 164))
        draw.text((fx + fw//2 - 60, fy + 524), "ยืนยันร่างประกาศ", fill=(255, 255, 255), font=get_font(15, bold=True))

        draw_flutter_bottom_nav(draw, selected_index=1)
        img.save(os.path.join(IMAGES_DIR, it["filename"]))
        print("Generated " + it["filename"])

def gen_cp5_1_review():
    img = Image.open(os.path.join(IMAGES_DIR, "checkpoint_4_1_item1.png"))
    img.save(os.path.join(IMAGES_DIR, "checkpoint_5_1_initial.png"))
    print("Generated checkpoint_5_1_initial.png")
    
    img, draw = create_chrome_base("Campus Marketplace - ลงประกาศขาย", "http://localhost:52480/#/")
    draw_flutter_appbar(draw, "Campus Marketplace", show_actions=True, cart_count=2)
    draw.rectangle([0, 149, 1440, 832], fill=(254, 247, 255))
    
    fx = 340
    fy = 165
    fw = 760
    fh = 650
    draw.rounded_rectangle([fx, fy, fx + fw, fy + fh], radius=20, fill=(255, 255, 255), outline=(231, 224, 236), width=1)
    
    draw.text((fx + 30, fy + 20), "ลงประกาศขายสินค้า (ตรวจทานและแก้ไขแล้ว)", fill=(33, 0, 93), font=get_font(20, bold=True))
    
    draw.rounded_rectangle([fx + 30, fy + 55, fx + 230, fy + 205], radius=12, fill=(245, 245, 247), outline=(202, 196, 208), width=1)
    draw_keyboard(draw, fx + 130, fy + 120)
    draw.text((fx + 45, fy + 178), "keyboard_gaming.jpg", fill=(71, 85, 105), font=get_font(11, bold=True))
    
    # Human-edited badge
    draw.rounded_rectangle([fx + 250, fy + 55, fx + fw - 30, fy + 115], radius=10, fill=(238, 242, 255), outline=(199, 210, 254), width=1)
    draw_check_icon(draw, fx + 270, fy + 78, col=(67, 56, 202), s=1.2)
    draw.text((fx + 285, fy + 70), "ผู้ใช้แก้ไขรายละเอียดเพิ่มเติม (Human-in-the-loop)", fill=(67, 56, 202), font=get_font(13, bold=True))
    draw.text((fx + 285, fy + 90), "เพิ่มสภาพสินค้า 95%, ระบุ Switch และของแถมสายถัก", fill=(79, 70, 229), font=get_font(11))
    
    # Form fields with edited content
    draw.text((fx + 30, fy + 140), "ชื่อประกาศ", fill=(73, 69, 79), font=get_font(12, bold=True))
    draw.rounded_rectangle([fx + 30, fy + 160, fx + fw - 30, fy + 205], radius=8, fill=(255, 255, 255), outline=(103, 80, 164), width=2)
    draw.text((fx + 45, fy + 171), "คีย์บอร์ดแมคคานิคอลไฟ RGB สภาพ 95% (แถมสายถัก)", fill=(29, 27, 32), font=get_font(13))
    
    draw.text((fx + 30, fy + 220), "หมวดหมู่", fill=(73, 69, 79), font=get_font(12, bold=True))
    draw.rounded_rectangle([fx + 30, fy + 240, fx + fw - 30, fy + 285], radius=8, fill=(255, 255, 255), outline=(202, 196, 208), width=1)
    draw.text((fx + 45, fy + 251), "อุปกรณ์อิเล็กทรอนิกส์", fill=(29, 27, 32), font=get_font(13))
    
    draw.text((fx + 30, fy + 300), "คำบรรยายสินค้า", fill=(73, 69, 79), font=get_font(12, bold=True))
    draw.rounded_rectangle([fx + 30, fy + 320, fx + fw - 30, fy + 410], radius=8, fill=(255, 255, 255), outline=(202, 196, 208), width=1)
    draw.text((fx + 45, fy + 333), "แมคคานิคอลคีย์บอร์ด ไฟ RGB สภาพ 95% ใช้งานมา 3 เดือน ปุ่ม Blue Switch", fill=(29, 27, 32), font=get_font(13))
    draw.text((fx + 45, fy + 359), "กดมันส์ เสียงแน่น แถมสายถัก Type-C พร้อมกล่อง นัดรับในมหาวิทยาลัยได้ครับ", fill=(29, 27, 32), font=get_font(13))
    
    draw.rounded_rectangle([fx + 30, fy + 430, fx + fw - 30, fy + 480], radius=25, fill=(103, 80, 164))
    draw.text((fx + fw//2 - 60, fy + 444), "ยืนยันร่างประกาศ", fill=(255, 255, 255), font=get_font(15, bold=True))

    # Green SnackBar at bottom
    snack_y = 740
    draw.rounded_rectangle([fx + 60, snack_y, fx + fw - 60, snack_y + 55], radius=10, fill=(20, 83, 45))
    draw_check_icon(draw, fx + fw//2 - 120, snack_y + 27, col=(240, 253, 244), s=1.2)
    draw.text((fx + fw//2 - 100, snack_y + 16), "บันทึกร่างประกาศเรียบร้อยแล้ว", fill=(240, 253, 244), font=get_font(14, bold=True))

    draw_flutter_bottom_nav(draw, selected_index=1)
    img.save(os.path.join(IMAGES_DIR, "checkpoint_5_1_edited.png"))
    print("Generated checkpoint_5_1_edited.png")

def gen_cp6_1_safety():
    img, draw = create_chrome_base("Campus Marketplace - ลงประกาศขาย", "http://localhost:52480/#/")
    draw_flutter_appbar(draw, "Campus Marketplace", show_actions=True, cart_count=2)
    draw.rectangle([0, 149, 1440, 832], fill=(254, 247, 255))
    
    fx = 340
    fy = 165
    fw = 760
    fh = 650
    draw.rounded_rectangle([fx, fy, fx + fw, fy + fh], radius=20, fill=(255, 255, 255), outline=(231, 224, 236), width=1)
    
    draw.text((fx + 30, fy + 20), "ลงประกาศขายสินค้า", fill=(33, 0, 93), font=get_font(20, bold=True))
    
    draw.rounded_rectangle([fx + 30, fy + 60, fx + 230, fy + 210], radius=12, fill=(245, 245, 247), outline=(202, 196, 208), width=1)
    draw_receipt(draw, fx + 130, fy + 130)
    draw.text((fx + 55, fy + 182), "receipt_test.jpg", fill=(71, 85, 105), font=get_font(11, bold=True))
    
    # Red Warning Card (AI Safety Blocked)
    draw.rounded_rectangle([fx + 250, fy + 60, fx + fw - 30, fy + 210], radius=12, fill=(254, 242, 242), outline=(252, 165, 165), width=2)
    draw_warning_icon(draw, fx + 270, fy + 88, col=(185, 28, 28), s=1.1)
    draw.text((fx + 288, fy + 78), "เกิดข้อผิดพลาดจากระบบความปลอดภัย (AI Safety)", fill=(185, 28, 28), font=get_font(14, bold=True))
    draw.text((fx + 275, fy + 108), "เนื้อหาที่วิเคราะห์เข้าข่ายไม่ปลอดภัยตามนโยบายของ Gemini", fill=(153, 27, 27), font=get_font(13))
    draw.text((fx + 275, fy + 132), "กรุณาใช้ภาพอื่น หรือตรวจสอบข้อความคำสั่งที่ส่งไป", fill=(153, 27, 27), font=get_font(13))
    draw.text((fx + 275, fy + 165), "API Response: finishReason = 'SAFETY'", fill=(185, 28, 28), font=get_font(12, bold=True))

    btn_y = fy + 235
    draw.rounded_rectangle([fx + 30, btn_y, fx + fw - 30, btn_y + 48], radius=24, fill=(103, 80, 164))
    draw_flash_icon(draw, fx + fw//2 - 85, btn_y + 24, col=(255, 255, 255))
    draw.text((fx + fw//2 - 70, btn_y + 12), "ให้ AI ช่วยแนะนำข้อมูล", fill=(255, 255, 255), font=get_font(14, bold=True))
    
    fields = ["ชื่อประกาศสินค้า", "หมวดหมู่สินค้า", "คำบรรยายรายละเอียดสินค้า"]
    ff_y = btn_y + 70
    for ff in fields:
        draw.rounded_rectangle([fx + 30, ff_y, fx + fw - 30, ff_y + 50], radius=10, fill=(254, 247, 255), outline=(202, 196, 208), width=1)
        draw.text((fx + 45, ff_y + 14), ff, fill=(150, 145, 155), font=get_font(13))
        ff_y += 65

    draw_flutter_bottom_nav(draw, selected_index=1)
    img.save(os.path.join(IMAGES_DIR, "checkpoint_6_1_safety_blocked.png"))
    print("Generated checkpoint_6_1_safety_blocked.png")

if __name__ == "__main__":
    gen_cp0_1_home()
    gen_cp0_1_checkout()
    gen_cp1_1_ai_studio()
    gen_cp1_2_structured_output()
    gen_cp2_1_debug_snackbar()
    gen_cp3_1_tabs()
    gen_cp4_1_items()
    gen_cp5_1_review()
    gen_cp6_1_safety()
    print("ALL 13 CHROME DESKTOP SCREENSHOTS REGENERATED PERFECTLY!")

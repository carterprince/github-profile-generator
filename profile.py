import random
from PIL import Image

def bits(hash_value, bits=15):
    for i in range(bits):
        yield (hash_value >> i) & 1

def hash_username(data):
    str_data = str(data)
    
    hash_value = 3049
    
    for char in str_data:
        hash_value ^= ord(char)
        hash_value = ((hash_value << 5) | (hash_value >> 10)) & 0x7FFF
        hash_value = (hash_value * 31) & 0x7FFF
        hash_value = ((hash_value << 3) ^ (hash_value >> 2)) & 0x7FFF
    
    return hash_value

def generate_color(hash_value, min_range=25):
    random.seed(hash_value)
    r = random.randint(130, 240)
    g = random.randint(130, 240)
    b = random.randint(130, 240)
    
    if max(r, g, b) - min(r, g, b) <= min_range:
        return generate_color(hash_value+1, min_range)

    pastel = (r, g, b)
    return pastel

def generate_profile(username):
    hash_value = hash_username(username)
    hashed_bits = bits(hash_value)
    
    # Generate pastel color
    pastel = generate_color(hash_value)

    im = Image.new("RGB", (7, 7), (255, 255, 255))

    for x in range(1, 4):
        for y in range(1, 6):
            colored = next(hashed_bits)
            if colored:
                im.putpixel((x, y), pastel)
                if x < 3:
                    im.putpixel((6-x, y), pastel)

    return im.resize((896, 896), resample=0)

if __name__ == "__main__":
    username = input("Username: ")
    im = generate_profile(username)
    im.save(f"profile.png")
    print(f"Saved to profile.png")

import random

class PIL_Package:
    
    clues = [
        
        "elephant", "banana", "sunshine", "computer", "giraffe", "ocean", "mountain", "butterfly", "umbrella", "chocolate",
    "happiness", "laughter", "rainbow", "puzzle", "fireworks", "bicycle", "sunset", "library", "adventure", "treasure",
    "whisper", "orchard", "sparkle", "dragon", "moonlight", "carousel", "jungle", "harmony", "magic", "serendipity",
    "enchanted", "wonder", "carousel", "friendship", "galaxy", "journey", "dream", "volcano", "inspiration", "novel",
    "laughter", "infinity", "paradise", "radiance", "discovery", "reflection", "passion", "imagination", "silhouette",
    "serenity", "crescent", "celestial", "blossom", "tranquility", "mystical", "fantasy", "wanderlust", "azure",
    "melody", "glisten", "tropical", "solstice", "legend", "luminous", "embrace", "wisdom", "secret", "glow",
    "eternity", "spark", "whimsical", "twilight", "cascade", "cosmos", "spellbound", "radiant", "bliss", "glimmer",
    "hope", "fairy", "infinity", "garden", "serene", "stardust", "whisper", "charming", "treasure", "silence", "miracle",
    "enchanted", "laughter", "dream", "harmony", "butterfly", "fantasy", "serendipity", "ocean", "wonder", "lullaby",
    "adventure", "moonlight", "breeze", "sunshine", "novel", "rainbow", "carousel", "blossom", "peace", "sunset",
    "imagination", "whimsical", "sparkle", "eternity", "silhouette", "magic", "dream", "reflection", "serenity", "joy",
    "glow", "radiance", "celestial", "paradise", "glisten", "mystical", "solstice", "journey", "azure", "laughter",
    "luminous", "secret", "cascade", "passion", "glimmer", "melody", "embrace", "whisper", "wisdom", "tranquility",
    "cosmos", "wanderlust", "fairy", "legend", "radiant", "hope", "garden", "whisper", "twilight", "lullaby", "silence",
    "glisten", "magic", "butterfly", "harmony", "miracle", "sparkle", "sunshine", "serenity", "reflection", "wonder",
    "adventure", "fantasy", "eternity", "joy", "moonlight", "peace", "ocean", "dream", "serendipity", "imagination",
    "celestial", "bliss", "novel", "cosmos", "solstice", "laughter", "whimsical", "paradise", "garden", "luminous",
    "embrace", "passion", "wanderlust", "twilight", "radiant", "breeze", "azure", "silhouette", "harmony", "hope",
    "carousel", "whisper", "stardust", "secret", "tranquility", "legend", "glimmer", "enchanted", "melody", "wisdom"
        ]

    def __init__(self) -> None:
        self.clue_index = random.randint(0, len(self.clues) - 1)
        self.clues = self.clues
        self.secret_code = random.randint(1000, 9999)
        self.attempts = 3
        print("Hello Participants! Good luck finding the clue!!")

    def get_real_final_code(self):
        print(
            r"""
 ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ 
||e |||a |||r |||t |||h |||s |||h |||a |||k |||e |||r |||s ||
||__|||__|||__|||__|||__|||__|||__|||__|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|
"""
        )

    def get_random_number(self):
        return random.randint(1, 100)

    def get_final_code(self, length=10):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        return ''.join(random.choice(letters) for _ in range(length))

    def shuffle_clues(self, input_list):
        shuffled_list = input_list[:]
        random.shuffle(shuffled_list)
        return shuffled_list

    def is_prime(self, num):
        if num <= 1:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    def reverse_string(self, text):
        return text[::-1]


    def get_code(self, length=8):
        characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*'
        return ''.join(random.choice(characters) for _ in range(length))

    def get_random_element(self, elements):
        return random.choice(elements)

    def get_clue(self):
        return random.choice(self.clues)

    def get_file_contents(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return "File not found!"
        

    def encrypt_message(self, message):
        key = random.randint(1, 25)
        encrypted_message = ''
        for char in message:
            if char.isalpha():
                shifted = ord(char) + key
                if char.islower():
                    if shifted > ord('z'):
                        shifted -= 26
                    elif shifted < ord('a'):
                        shifted += 26
                elif char.isupper():
                    if shifted > ord('Z'):
                        shifted -= 26
                    elif shifted < ord('A'):
                        shifted += 26
                encrypted_message += chr(shifted)
            else:
                encrypted_message += char
        return encrypted_message

    def get_random_prime(self, start, end):
        primes = [num for num in range(start, end + 1) if self.is_prime(num)]
        return random.choice(primes)

if __name__=="__main__":
    a=PIL_Package()
    print(dir(a))
    a.get_Code()
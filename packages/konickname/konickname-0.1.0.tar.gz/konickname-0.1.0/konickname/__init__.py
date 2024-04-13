import random

ADJECTIVES = [
    "영롱한",
    "빛나는",
    "반짝이는",
    "빛나는",
    "귀여운",
    "멋진",
    "아름다운",
    "화려한",
    "행복한",
    "행운의",
    "고운",
    "예쁜",
    "화난",
    "정열적인",
    "무서운",
    "무시무시한",
    "감동적인",
    "감격적인",
]

NOUNS = [
    "호랑이",
    "사자",
    "코끼리",
    "기린",
    "코알라",
    "팬더",
    "늑대",
    "여우",
    "오소리",
    "청솔모",
    "다람쥐",
    "토끼",
    "사슴",
    "햄스터",
    "고양이",
    "강아지",
    "송아지",
    "족제비",
]


def generate_nickname(digits: int = 4):
    adjective = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    number = random.randint(0, 10**digits - 1)
    return f"{adjective}{noun}{number:0{digits}d}"

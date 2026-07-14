from model import detect_hair_texture

test_cases = [
    ("data/straight/01-10-2019-latest-haircut-for-girls_Equal_Length_4PNG.jpg", "straight"),
    ("data/textured/0b7aa42d28a71654681bfd13b569ce32.jpg", "textured"),
    
]

correct = 0

for path, expected in test_cases:
    result = detect_hair_texture(path)

    predicted = result.get("hair_texture", "error")

    match = "✓" if predicted == expected else "✗"

    print(
        f"{match} Expected: {expected:10} "
        f"Got: {predicted:10} "
        f"Confidence: {result.get('confidence')}"
    )

    if predicted == expected:
        correct += 1

print(f"\nAccuracy: {correct}/{len(test_cases)}")
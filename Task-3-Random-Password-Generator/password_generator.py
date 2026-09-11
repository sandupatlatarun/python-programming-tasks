import string
import secrets


def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password


print("🔐 RANDOM PASSWORD GENERATOR 🔐")

while True:
    try:
        length = int(input("Enter password length: "))

        if length < 4:
            print("❌ Password length must be at least 4.")
            continue

        password = generate_password(length)

        print("\n✅ Your password is:")
        print(password)

        again = input("\nGenerate another password? (yes/no): ").strip().lower()

        if again != "yes":
            print("👋 Goodbye!")
            break

    except ValueError:
        print("❌ Please enter a valid number.")
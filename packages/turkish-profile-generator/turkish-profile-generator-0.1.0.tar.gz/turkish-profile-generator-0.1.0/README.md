# Turkish Profile Generator

Turkish Profile Generator is a Python package for generating random Turkish user profiles.

## Installation

You can install Turkish Profile Generator using pip:

```bash
pip install turkish_profile_generator


from turkish_profile_generator import UserProfileGenerator

# Create a UserProfileGenerator instance
generator = UserProfileGenerator(min_age=18, max_age=65)

# Generate a random user profile
profile = generator.generate_profile()

print(profile)
from setuptools import setup, find_packages

setup(
    name='turkish-profile-generator',
    version='0.1.6',
    packages=find_packages(),
    package_data={'turkish_profile_generator': ['data/*.txt']},
    include_package_data=True,
    install_requires=[],
    author='Mustafa Buyruk',
    author_email='bossturk@hotmail.com',
    description='Generate random Turkish user profiles',
    license='MIT',
    keywords='turkish profile generator',
    url='https://github.com/bossturk/turkish-profile-generator/'
)
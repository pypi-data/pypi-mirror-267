from setuptools import setup, find_packages

# Membaca isi dari requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='haku',
    version='1.0',
    packages=find_packages(),
    description='Seratus Persen Clone Pyrofork',
    author='hakutaka',
    author_email='hakutaka@gmail.com',
    url='https://t.me/pyrogram',  # Ganti dengan URL proyek Anda
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=requirements,
)


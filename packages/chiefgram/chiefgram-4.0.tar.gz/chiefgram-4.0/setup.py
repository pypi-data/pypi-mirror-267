from setuptools import setup, find_packages

# Membaca isi dari requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='chiefgram',
    version='4.0',
    packages=find_packages(),
    description='Hanya Buat Senang',
    author='GatauTeh',
    author_email='rizaldaitona@gmail.com',
    url='https://example.com',  # Ganti dengan URL proyek Anda
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=requirements,  # Menggunakan requirements dari file requirements.txt
)


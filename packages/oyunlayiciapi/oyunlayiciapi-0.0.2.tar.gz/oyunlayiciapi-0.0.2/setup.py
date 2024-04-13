from setuptools import setup, find_packages

setup(
    name="oyunlayiciapi",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0"
    ],
    author="mavi_v",
    description="Minecraft sunucularından bilgi almaya yarayan Oyunlayıcı API kütüphanesi",
)
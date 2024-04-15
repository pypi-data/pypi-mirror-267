from setuptools import setup, find_packages

setup(
    name="facecam",
    version="0.0.1a",
    author="emhang",
    author_email="emhang@126.com",
    description="A simple AI face detection library that can perform real-time face detection and includes preset sticker images, specifically for Huanma coding courses.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        "opencv-python>=4.5.5.64",
        "numpy>=1.21.2",
        "imageio>=2.21.0",
        "pillow>=8.3.2"
    ]
)

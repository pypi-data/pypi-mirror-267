from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = 'An image caption generator for advertisements.'
LONG_DESCRIPTION = ('A package that generates captions, collects text, and saves it to a .csv file after being given '
                    'an image of an advertisement.')

# Setting up
setup(
    name='ogicg',
    version=VERSION,
    author='Ian King, Mason Myles, Omar Elsegeiny, Emily Anderson, & Bohdan Ivanyshyn',
    author_email="kingian404@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pillow', 'torch', 'requests', 'validators', 'transformers', 'cohere',
                      'numpy', 'opencv-python-headless', 'gradio', 'easyocr'],
    keywords=['python', 'image', 'caption', 'generator', 'image caption generator', 'OCR',
              'optical character recognition', 'ad', 'ads', 'advertisement', 'advertisements',
              'ogicg', 'Ovative', 'Ovative Group', 'Ovative Group Image Caption Generator'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

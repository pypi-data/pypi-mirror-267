import io
from setuptools import setup, find_packages
import os

dir_path = os.path.dirname(os.path.abspath(__file__))

rd_file = os.path.join(dir_path, 'README.md')

with io.open(rd_file, encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='PyMLRS',
    version='0.0.1',
    description='A library for processing and interpreting DNA high-resolution melt and amplification curves for the meningoencephalitis panel.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/PyPCR/PyPCR',
    authors=["ChandruGaneshan", "VikramSekar"],
    authors_email=['chandruganeshan24@gmail.com', 'vikramsekar2305@gmail.com'],
    license='MIT',
    keywords=['High Resolution Melt', 'Amplification Curve', "Cycle threshold",
              'PCR', 'rt-PCR', 'Meningoencephalitis', "MEP", 'Pathogens', "Bharathiar University"],
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    package_data={"PyMLRS": ["*.py", "*.pkl", "*.md", "*.xlsx"]},
    include_package_data=True,
    install_requires=[
        'fpdf==1.7.2',
        'matplotlib==3.6.3',
        'numpy==1.23.5',
        'pandas==1.5.3',
        'Pillow==9.4.0',
        'plotly==5.13.1',
        'scikit_learn==1.4.1.post1',
        'scipy==1.13.0',
        'openpyxl==3.1.2'
    ]
)

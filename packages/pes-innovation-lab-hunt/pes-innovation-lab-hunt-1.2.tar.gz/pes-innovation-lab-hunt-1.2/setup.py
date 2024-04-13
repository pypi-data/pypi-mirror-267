from setuptools import setup, find_packages

setup(
    name='pes-innovation-lab-hunt',
    version='1.2',
    packages=find_packages(),
    install_requires=[],  # Add dependencies if any
    entry_points={},
    # Metadata
    author='PES Innovation Lab',
    author_email='innovationlab@pes.edu',
    description='Hunt package',
    long_description="""
# pes_innovation_lab_hunt

```python
import pes_innovation_lab_hunt
# poke around and find out!

""",
    long_description_content_type='text/markdown',
)

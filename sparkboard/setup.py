from setuptools import setup 

setup(
    name="ecook",
    version="1.0",
    author="Eric Behling, Rodney Perez, Ahana Mukherjee, Sarah Yasuda",  # Replace with author's name
    author_email="ericbehl@uw.edu",  # Replace with author's email
    description="Dashboard for energy benchmarking",  # Replace with project description
    url="https://github.com/CSE583-Electric-Cooking/e-cook",
    packages=find_packages(),
    install_requires=[
        "ansi2html==1.8.0",
        "astroid==3.0.1",
        "certifi==2023.11.17",
        "charset-normalizer==3.3.2",
        "dash==2.14.2",
        "dash-leaflet==1.0.11",
        "dash-table==5.0.0",
        "idna==3.6",
        "importlib-metadata==7.0.0",
        "kaleido==0.2.1",
        "nest-asyncio==1.5.8",
        "pylint==3.0.3",
        "requests==2.31.0",
        "retrying==1.3.4",
        "typing-extensions==4.8.0",
        "urllib3==2.1.0",
        "zipp==3.17.0"
    ],

    python_requires='>=3.6',
)


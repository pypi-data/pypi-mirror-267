from setuptools import setup

file = open('README.md', 'r',encoding='utf-8')
readme = file.read()


setup(
    name='selenium-network-intercept',
    version='1.0.1',
    license='MIT License',
    author='Alexandre Mariano',
    long_description=readme,
    long_description_content_type='text/markdown',
    author_email='alexandre_mariano@hotmail.com.br',
    keywords=['selenium', 'network', 'intercept','http','requests','selenium network intercept','selenium intercept','search download selenium'],
    description='Interceptador de requisições http não oficial do selenium 4',
    packages=['selenium_network_intercept','selenium_search_file'],
    install_requires=[]
)

file.close()
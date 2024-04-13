from setuptools import setup,find_packages
setup(
    name='Mensajes-Truqueli',
    version='5.0',
    description='Un paquete para enviar mensajes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Diego Altamirano',
    author_email='diego@hola.com',
    license_files=['LICENSE'],
    packages=find_packages(),
    scripts=[],
    test_suite='tests',
install_requires=[paquete.strip()
                      for paquete in open("requirements.txt").readlines()],    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python'
    ]
    
)
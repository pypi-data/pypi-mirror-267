from setuptools import setup, find_packages

setup(
    name='CropwiseWorker',
    version='0.1',
    packages=find_packages(),
    author='Molev Arkhip',
    author_email='jobarkhip@gmail.com',
    description='Модуль реализует функции для работы с API цифровой платформы управления агропредприятием Cropwise Operations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Указываем формат описания
    install_requires=[
        'requests',
        'pandas'
    ],
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: Russian',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
)


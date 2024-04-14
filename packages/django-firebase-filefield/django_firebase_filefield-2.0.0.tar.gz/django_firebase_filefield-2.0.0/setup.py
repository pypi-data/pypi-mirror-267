from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='django_firebase_filefield',
    version='2.0.0',
    license='MIT License',
    author='Issei Momonge',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='mggyggf@gmail.com',
    keywords=['django','firebase','filefield','django firebase','django firebase filefield','firebase filefield'],
    description=u'An Unofficial Django and Firebase Library',
    packages=['firebasefilefield'],
    install_requires=['firebase_admin','django','filetype'],)
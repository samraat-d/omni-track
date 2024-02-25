from setuptools import setup

setup(
    name='dailytrackerapp',
    packages=['dailytrackerapp'],
    include_package_data=True,
    install_requires=[
        'flask','flask_sqlalchemy', 'sqlalchemy', 'flask_socketio',
    ],
)
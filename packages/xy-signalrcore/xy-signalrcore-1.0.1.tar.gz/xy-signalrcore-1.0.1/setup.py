import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xy-signalrcore",
    version="1.0.1",
    author="Colin Chang",
    author_email="zhangcheng5468@gmail.com",
    description="A Python SignalR Core client(json and messagepack), with invocation auth and two way streaming. Compatible with azure / serverless functions. Also with automatic reconnect and manually reconnect.",
    keywords="signalr core client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license_file="LICENSE",
    url="https://github.com/colin-chang/signalrcore",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.10"
    ],
    install_requires=[
        "requests>=2.22.0",
        "websocket-client==1.0.0",
        "msgpack==1.0.2"
    ]
)

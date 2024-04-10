import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-cdk.aws-kinesisfirehose-alpha",
    "version": "2.136.1.a0",
    "description": "The CDK Construct Library for AWS::KinesisFirehose",
    "license": "Apache-2.0",
    "url": "https://github.com/aws/aws-cdk",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/aws/aws-cdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_cdk.aws_kinesisfirehose_alpha",
        "aws_cdk.aws_kinesisfirehose_alpha._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_kinesisfirehose_alpha._jsii": [
            "aws-kinesisfirehose-alpha@2.136.1-alpha.0.jsii.tgz"
        ],
        "aws_cdk.aws_kinesisfirehose_alpha": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.136.1, <3.0.0",
        "constructs>=10.0.0, <11.0.0",
        "jsii>=1.96.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved",
        "Framework :: AWS CDK",
        "Framework :: AWS CDK :: 2"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)

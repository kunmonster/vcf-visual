from setuptools import setup, find_packages

setup(
    name="statvcf",  # 替换为你的程序名称
    version="1.0.0",
    author="fengkunjiang",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # 添加依赖包，例如 'numpy', 'pandas' 等
        'matplotlib',
        'rich',
        'scikit-allel',
        'natsort',
        'pandas',
        'scikit-learn',
        'numpy',
    ],
    py_modules=["main"], 
    entry_points={
        "console_scripts": [
            "statvcf=main:main",  # "命令名称=模块:函数"
        ],
    },
)

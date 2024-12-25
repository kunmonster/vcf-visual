from setuptools import setup, find_packages

setup(
    name="vcf_visual",  # 替换为你的程序名称
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # 添加依赖包，例如 'numpy', 'pandas' 等
        'matplotlib',
        'rich',
        'natsort',
        'pandas',
        'scikit-learn',
        'numpy',
        'cyvcf2'
    ],
    entry_points={
        "console_scripts": [
            "vcf_visual=vcf_visual.main:main",  # "命令名称=模块:函数"
        ],
    },
)

from setuptools import setup

package_name = 'my_inference_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools', 'stable-baselines3', 'numpy'],
    zip_safe=True,
    maintainer='your_name',
    entry_points={
        'console_scripts': [
            'inference_node = my_inference_pkg.inference_node:main',
        ],
    },
)

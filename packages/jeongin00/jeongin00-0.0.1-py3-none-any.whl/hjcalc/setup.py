import setuptools

setuptools.setup(
  include_package_data = True,
   name = 'jeongin00',
   version='0.0.1',
   description = 'first package',
   author = 'jeongin',
   autho_email = 'ghkdwjddls12@gmail.com',
   url = 'https://github.com/jeongin22/Jeongin_sw',
  download_url = 'https://github.com/jeongin22/Jeongin_sw',
  install_requires=['pytest'],
  long_description = 'oss-dev calculator and tengudan python module',
  long_description_content_type = 'text/markdown',
   packages = ['hjcalc'],
  classifiers = [
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.10',
    # 기타 등등...
]
)

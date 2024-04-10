from setuptools import setup
setup(name='sodata',
      version='0.0.1',
      description='processing web text data for NLP LLM',
      author='ZH',
      author_email='zhanghongsz@yunic.ai',
      packages=['sodata'],
      python_requires=">=3.10",
      install_requires=["numpy", "scipy"],#需要安装的依赖
      zip_safe=False)

from setuptools import setup
setup(name='sodata',
      version='0.0.3',
      description='processing web text data for NLP LLM',
      author='ZH',
      author_email='zhanghongsz@yunic.ai',
      packages=['sodata'],
      python_requires=">=3.6",
      install_requires=["numpy", "scipy","pandas"],#需要安装的依赖
      )

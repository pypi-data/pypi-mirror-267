from setuptools import setup
import os

def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()

setup(
  name = 'multi-agent-decision',         
  packages = ['multi_agent_decision'],   
  version = '0.3',      
  license='MIT',        
  description = 'Simulates the actions which agents take under multi-agent systems and social networks',  
  long_description=read_file('README.md'),
  long_description_content_type='text/markdown',  
  author = 'ankurtutlani',                   
  author_email = 'ankur.tutlani@gmail.com',      
  url = 'https://github.com/ankur-tutlani/multi-agent-decision',   
  download_url = 'https://github.com/ankur-tutlani/multi_agent_decision/archive/refs/tags/v_03.tar.gz',    
  keywords = ['game theory', 'evolutionary game', 'social norms','multi-agent systems','evolution','social network','computational economics','simulation','agent-based modeling','computation'],   
  install_requires=[            
          'numpy>=1.24.3',
		  'pandas>=2.0.3',
		  'networkx>=3.1',
		  'matplotlib>=3.7.2',
		  'setuptools>=68.0.0'
		  
		  
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
												
	'Programming Language :: Python :: 3.11',
  ],
)
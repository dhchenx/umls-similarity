# UMLS-Similarity

Estimate the similarity of medical concepts based on Unified Medical Language System (UMLS) and WordNet

## Installation

First of all, please install Perl environment ([Strawberry](https://strawberryperl.com/)).

### For UMLS use:
1. Install MySQL and MySQL Workbench and the MySQL Home folder should not have space in its path;
2. Download the UMLS and extract the subset;
3. Goto UMLS's META and NET folders and Load UMLS data into MySQL database with [scripts](https://www.nlm.nih.gov/research/umls/implementation_resources/scripts/README_RRF_MySQL_Output_Stream.html);
4. Install necessary libs with 'cpanm' command with the flag `--force` like below:
   ```
   cpanm UMLS::Interface --force
   
   cpanm UMLS::Similarity --force
   ```
   Errors may occur in the above process, just ignore them. 
5. Please check if you have installed ```DBI```, ```DBD::mysql```; install them if not;

    - Issue: mysql.xs.dll not found problem, please found more details in [link](https://github.com/perl5-dbi/DBD-mysql/issues/318).

    - Solution: Copying C:\strawberry\c\bin\libmysql.dll_ to c:\strawberry\perl\vendor\lib\auto\mysql 

6. Finished!

### For WordNet use (skip it if not)
1. Download the [WordNet-2.1](https://wordnet.princeton.edu/download/old-versions) if you want to use WordNet Similarity (if not, please skip)
2. Set WNHome environment variables (if you need to use WordNet Similarity)
3. Install ```WordNet::QueryData``` via `cpanm` command in perl
4. Install ```WordNet::Similarity``` via `cpanm` command in perl
5. Finished!

### Finally, install our Python package `umls-similrity` via pip

```pip
pip install umls-similarity
```

### Available similarity measures

- Leacock and Chodorow (1998) referred to as lch
- Wu and Palmer (1994) referred to as  wup
- Zhong, et al. (2002) referred to as zhong
- The basic path measure referred to as path
- The undirected path measure referred to as upath
- Rada, et. al. (1989) referred to as cdist
- Nguyan and Al-Mubaid (2006) referred to as nam
- Resnik (1996) referred to as res
- Lin (1988) referred to as lin
- Jiang and Conrath (1997) referred to as jcn
- The vector measure referred to as vector
- Pekar and Staab (2002) referred to as pks
- Pirro and Euzenat (2010) referred to as faith
- Maedche and Staab (2001) referred to as cmatch
- Batet, et al (2011) referred to as batet
- Sanchez, et al. (2012) referred to as sanchez

## Let Codes Speak

Example Code 1: Estimate similarity between two medical concepts using UMLS

```python
from umls_similarity.umls import UMLSSimilarity
import os

if __name__ == "__main__":
    # define MySQL information that stores UMLS data in your computer
    mysql_info = {}
    mysql_info["database"] = "umls"
    mysql_info["username"] = "root"
    mysql_info["password"] = "{I am not gonna tell you}"
    mysql_info["hostname"] = "localhost"

    # Perl bin's path which will be automatically detected by the lib, but you can also manually specify in its constructor
    # perl_bin_path = r"C:\Strawberry\perl\bin\perl"

    # create an instance
    umls_sim = UMLSSimilarity(mysql_info=mysql_info,
                              # perl_bin_path=''
                              )
    
    # show the names of all available measures so you can pass them into the following `measure` parameter
    measures=umls_sim.get_all_measures()
    print(measures)

    # Directly pass two CUIs into the function below:
    sims = umls_sim.similarity(cui1="C0017601", cui2="C0232197", measure="lch")
    print(sims[0])  # only one pair with two concepts
    
    # Or batch process many CUI pairs from a text file where each line is formatted like 'C0006949<>C0031507'
    current_path = os.path.dirname(os.path.realpath(__file__))
    sims = umls_sim.similarity_from_file(current_path + r"\cuis_umls_sim.txt", measure="lch")
    for sim in sims:
        print(sim)
```
Example Code 2: Estimate similarity between concept using WordNet 2.1

```python
from umls_similarity.wordnet import WNSimilarity

if __name__ == "__main__":

    wn_root_path = r"C:\Program Files (x86)\WordNet\2.1"
    # perl_bin_path=r"C:\Strawberry\perl\bin\perl"

    var1 = "dog#n#1"
    var2 = "orange#n#1"

    wn_sim = WNSimilarity(wn_root_path=wn_root_path)

    sims = wn_sim.similarity(var1, var2)
    print(sims)

    for k, v in enumerate(sims):
        print(k, '\t', v, '\t', sims[v])
```

## Credits

This project is a wrapper of the Perl library of [UMLS::Similarity](https://www.d.umn.edu/~tpederse/umls-similarity.html) and [UMLS::Interface](http://www.people.vcu.edu/~btmcinnes/software/umls-interface.html). 

Note: There are plenty of unexpected errors to occur during the installation of the perl library of `UMLS::Similarity`, possibly because I am not an expert about Perl and its library use.

## License
The `umls-similarity` Python package is provided by [Donghua Chen](https://github.com/dhchenx). 


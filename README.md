# UMLS-Similarity

Estimate similarity of medical concepts based on Unified Medical Language System (UMLS)

## Installation

First of all, please install Perl environment ([Strawberry](https://strawberryperl.com/)).
   
### For WordNet use:
1. Download the [WordNet-2.1](https://wordnet.princeton.edu/download/old-versions) if you want to use WordNet Similarity (if not, please skip)
2. Set WNHome environment variables (if you need WordNet Similarity)
3. Install WordNet::QueryData via `cpanm` command in perl
4. Install WordNet::Similarity via `cpanm` command in perl

### For UMLS use:
1. Install MySQL and WorkBench, the MySQL Home folder should not have space in its path;
2. Download UMLS and extract the subset;
3. Goto UMLS's META and NET folders and Load UMLS data into MySQL database with scripts: Ref: https://www.nlm.nih.gov/research/umls/implementation_resources/scripts/README_RRF_MySQL_Output_Stream.html;
4. Install Perl (Strawberry) environment;
5. Install necessary libs with 'cpanm' command like below:
6. `cpanm UMLS::Interface --force`

Issue: need to fix the problem of UMLS::Interface that is unable to install due to mysql connecting issue

Solution: adding fixed username and password in Line 721 in CuiFinder.pm from the distribution files and try again.

7. `cpanm UMLS::Similarity`

8. `cpanm UMLS::Similarity::lch --force` if error occurs

9. Please check if you have installed DBI, DBD::mysql; install them if not;

Issue: mysql.xs.dll not found problem: https://github.com/perl5-dbi/DBD-mysql/issues/318

Solution: Copying C:\strawberry\c\bin\libmysql.dll_ to c:\strawberry\perl\vendor\lib\auto\mysql 

### Finally, install the umls-similrity package via pip

```pip
pip install umls-similarity
```

## Measures

Available measures are: 
1. Leacock and Chodorow (1998) referred to as lch
2. Wu and Palmer (1994) referred to as  wup
3. Zhong, et al. (2002) referred to as zhong
4. The basic path measure referred to as path
5. The undirected path measure referred to as upath
6. Rada, et. al. (1989) referred to as cdist
7. Nguyan and Al-Mubaid (2006) referred to as nam
8. Resnik (1996) referred to as res
9. Lin (1988) referred to as lin
10 Jiang and Conrath (1997) referred to as jcn
11. The vector measure referred to as vector
12. Pekar and Staab (2002) referred to as pks
13. Pirro and Euzenat (2010) referred to as faith
14. Maedche and Staab (2001) referred to as cmatch
15. Batet, et al (2011) referred to as batet
16. Sanchez, et al. (2012) referred to as sanchez


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
    umls_sim = UMLSSimilarity(mysql_info=mysql_info)

    # processing many CUI pairs from a text file where each line is formatted like 'C0006949<>C0031507'
    current_path = os.path.dirname(os.path.realpath(__file__))
    sims = umls_sim.similarity_from_file(current_path + r"\cuis_umls_sim.txt", measure="lch")
    for sim in sims:
        print(sim)

    # Or directly pass two CUIs into the function below:
    sims = umls_sim.similarity(cui1="C0017601", cui2="C0232197", measure="lch")
    print(sims[0])  # only one pair with two concepts

```
Example Code 2: Estimate similarity between concept using WordNet (version 2.1)

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

## Credit

This project is a wrapper of the Perl library of [UMLS::Similarity](https://www.d.umn.edu/~tpederse/umls-similarity.html) and [UMLS::Interface](http://www.people.vcu.edu/~btmcinnes/software/umls-interface.html). 

Note: There are plenty of issues to fix during the installation of the UMLS::Similarity libraries because I am not familiar with Perl and its library use.

## License
The `umls-similarity` project is provided by [Donghua Chen](https://github.com/dhchenx). 


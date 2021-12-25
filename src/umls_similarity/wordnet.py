import subprocess
import os
# Install:
# https://sourceforge.net/projects/wn-similarity/files/WordNet-Similarity/WordNet-Similarity-2.07/WordNet-Similarity-2.07.tar.gz/download
# https://wordnet.princeton.edu/download/old-versions
# https://strawberryperl.com/
# Set WNHome environment
# cpanm WordNet::QueryData
# cpanm UMLS::Interface
# cpanm WordNet::Similarity

class WNSimilarity:
    def __init__(self,wn_root_path,perl_bin_path=""):
        self.wn_root_path=wn_root_path
        self.perl_bin_path = perl_bin_path
        if self.perl_bin_path == "":
            self.perl_bin_path = self.get_perl_bin()
        if self.perl_bin_path == "":
            self.perl_bin_path = r"C:\Strawberry\perl\bin\perl"

    def get_perl_bin(self):
        new_env = os.environ.copy()
        PATH = new_env["PATH"]
        perl_bin_path = r"C:\Strawberry\perl\bin\perl"
        for path in PATH.split(";"):
            if ('perl' in path) and ('site' not in path):
                # print(path)
                perl_bin_path = path + r"\perl"
                break
        return perl_bin_path

    def similarity(self,syn1,syn2):
        new_env = os.environ.copy()
        current_path = os.path.dirname(os.path.realpath(__file__))
        cwd = current_path+"/scripts/wordnet"
        new_env["WNHome"] = self.wn_root_path

        p = subprocess.Popen([self.perl_bin_path, current_path+"/scripts/wordnet/sample.pl", syn1, syn2], cwd=cwd, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, env=new_env)
        stdout, stderr = p.communicate()
        # print(stdout)
        ls = stdout.decode('utf-8').split('\n')
        dict = {}
        for l in ls:
            if '=' in l:
                pp = l.strip().split('=')
                key = pp[0].strip().replace('Similarity', '').strip()
                value = pp[1].strip()
                dict[key] = value
        return dict


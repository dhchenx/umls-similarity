import subprocess
import os
import tempfile

'''
available measure are: 
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
    16. S{\'a}nchez, et al. (2012) referred to as sanchez
'''

class UMLSSimilarity:
    def __init__(self,mysql_info,perl_bin_path="",work_directory=""):
        self.perl_bin_path=perl_bin_path
        if self.perl_bin_path=="":
            self.perl_bin_path=self.get_perl_bin()
        if self.perl_bin_path == "":
            self.perl_bin_path= r"C:\Strawberry\perl\bin\perl"
        self.mysql_info=mysql_info
        self.work_directory=work_directory

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

    def similarity(self,cui1,cui2,measure='lch',precision=4,forcerun=True):
        # in_file_obj = tempfile.mkstemp(suffix = '.txt')
        in_file_path=tempfile.gettempdir()+"/umls-similarity-temp.txt"
        # print(in_file_path)
        f_out=open(in_file_path,'w',encoding='utf-8')
        f_out.write(f"{cui1}<>{cui2}")
        f_out.close()
        result= self.similarity_from_file(in_file_path,measure,precision,forcerun)

        return result

    def similarity_from_file(self,in_file,measure='lch',precision=4,forcerun=True):

        kv = {}
        kv["--database"] = self.mysql_info["database"]
        kv["--username"] =self.mysql_info["username"]
        kv["--password"] = self.mysql_info["password"]
        kv["--hostname"] =self.mysql_info["hostname"]
        kv["--measure"] = measure
        # kv["--realtime"] = ""
        kv["--precision"] = str(precision)
        # kv["--debug"]=""
        # kv["--matrix"]=""
        if forcerun:
            kv["--forcerun"] = ""
        kv["--infile"]=in_file

        current_path = os.path.dirname(os.path.realpath(__file__))
        cwd = current_path+ r'\scripts\umls\utils'

        if self.work_directory!="":
            cwd=self.work_directory

        umls_similarity_pl_path=cwd+ r"\umls-similarity.pl"

        # new_env["WNHome"] = r'C:\Program Files (x86)\WordNet\2.1'
        ps = []
        ps.append(self.perl_bin_path)
        ps.append(umls_similarity_pl_path)
        for k, v in enumerate(kv):
            ps.append(v)
            ps.append(kv[v])
        # print(ps)
        kv_str = " ".join(ps)
        # print(kv_str)
        # print("Working Directory: ", cwd)
        p = subprocess.Popen(ps, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        # print(stdout)
        r_stdout = stdout.decode('utf-8', 'ignore')
        # print(r_stdout)
        ls = r_stdout.strip().split('\r\n')
        r = []
        for l in ls:
            ls=l.strip().split('<>')
            if len(ls)>=3:
                r.append([measure,ls[1],ls[2],ls[0]])
        return r

    def get_all_measures(self):
        measures = ['lch', 'wup', 'zhong', 'path', 'cdist', 'nam', 'res', 'lin', 'jcn', 'vector', 'pks', 'faith',
                    'batet', 'sanchez']
        return measures

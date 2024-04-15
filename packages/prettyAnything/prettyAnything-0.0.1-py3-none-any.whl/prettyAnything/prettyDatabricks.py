# PRETTY DATABRICKS
from datetime import datetime
from databricks.sdk.runtime import *

class prettyDatabricks:
    def __init__(self):
        self.__old_path=None
        self.__list_ls=[]
        self.__number_of_layers_constant=0
    
    def _size_formatter(self, size_in_bytes:int)->str:
        if round(size_in_bytes/(1024**1), 3)<=1024:
            return str(round(size_in_bytes/(1024**1), 3))+' kb'
        elif round(size_in_bytes/(1024**2), 3)<=1024:
            return str(round(size_in_bytes/(1024**2), 3))+' mb'
        elif round(size_in_bytes/(1024**3), 3)<=1024:
            return str(round(size_in_bytes/(1024**3), 3))+' gb'
        elif round(size_in_bytes/(1024**4), 4)<=1024:
            return str(round(size_in_bytes/(1024**4), 3))+' tb'
        else:
            return str(round(size_in_bytes/(1024**5), 3))+' pb'
    def _directory_size_finder(self, path:str, size=0)->int:
        for i in dbutils.fs.ls(path):
            if i[0].endswith('/'):
                size=self._directory_size_finder(path=i[0], size=size)
            else:
                size+=i[2]
        return size
    def _directory_time_finder(self, path:str, times=[])->int:
        for i in dbutils.fs.ls(path):
            if i[0].endswith('/'):
                self._directory_time_finder(path=i[0], times=times)
            else:
                times.append(i[-1])
        try:
            return max(times)
        except:
            return datetime(1970, 1, 1, 0, 0, 0).timestamp()
    
    def __ami_main_pretty_ls(self, path, hierarchy='\x1b[1;48;5;255;38;5;0m|___', flag=0, theme="light", size=True, time=True):
        if theme.lower()=="light":
            background_color=255
            hierarchy=hierarchy.replace(";0;", ";255;")
        else:
            background_color=0
            hierarchy=hierarchy.replace(";255;", ";0;")
        
        if flag==0:
            print(f"\033[1;38;5;{background_color};48;5;0m "+path.strip('/').split('/')[-1]+" \033[0m")
        for i in dbutils.fs.ls(path):
            if i[0].endswith('/'):
                if self.__old_path!=i[0]:
                    if size==True and time==True:
                        print(hierarchy+i[1]+"\033[0m" +" \033[1;31m"+self._size_formatter(self._directory_size_finder(i[0], size=0))+"\033[0m " +f"{datetime.fromtimestamp((self._directory_time_finder(i[0], times=[]))//1000).strftime('%Y-%m-%d %H:%M:%S')}")
                    elif size==True and time==False:
                        print(hierarchy+i[1]+"\033[0m" +" \033[1;31m"+self._size_formatter(self._directory_size_finder(i[0], size=0))+"\033[0m")
                    elif size==False and time==True:
                        print(hierarchy+i[1]+"\033[0m" +f" {datetime.fromtimestamp((self._directory_time_finder(i[0], times=[]))//1000).strftime('%Y-%m-%d %H:%M:%S')}")
                    else:
                        print(hierarchy+i[1]+"\033[0m")
                    self.__old_path=i[0]
                    prettyDatabricks().__ami_main_pretty_ls(path=i[0], hierarchy='    '+hierarchy, flag=1, theme=theme, size=size, time=time)
                else:
                    print(hierarchy+i[1]+"\033[0m")
            else:
                if size==True and time==True:
                    print("\033[1m\033[38;5;30m"+hierarchy[:-5]+'\|___ '+i[1]+"\033[0m" +" < \033[1;31m"+self._size_formatter(i[2])+"\033[0m > " +f"\x1b[1;48;5;{background_color};38;5;0m {datetime.fromtimestamp(i[-1]//1000).strftime('%Y-%m-%d %H:%M:%S')} \033[0m")
                elif size==True and time==False:
                    print("\033[1m\033[38;5;30m"+hierarchy[:-5]+'\|___ '+i[1]+"\033[0m" +" < \033[1;31m"+self._size_formatter(i[2])+"\033[0m > ")
                elif size==False and time==True:
                    print("\033[1m\033[38;5;30m"+hierarchy[:-5]+'\|___ '+i[1]+"\033[0m" +f" \x1b[1;48;5;{background_color};38;5;0m {datetime.fromtimestamp(i[-1]//1000).strftime('%Y-%m-%d %H:%M:%S')} \033[0m")
                else:
                    print("\033[1m\033[38;5;30m"+hierarchy[:-5]+'\|___ '+i[1]+"\033[0m")
    @staticmethod
    def pretty_ls(path, theme="light", sizeChecker=True, timeChecker=True):
        prettyDatabricks().__ami_main_pretty_ls(path=path, theme=theme, size=sizeChecker, time=timeChecker)
    
    def __ami_main_df_ls(self, path, layer):
        layer-=1
        for i in dbutils.fs.ls(path):
            if i[0].endswith('/'):
                self.__list_ls.append((i[0], i[1], self._directory_size_finder(i[0], size=0), datetime.fromtimestamp((self._directory_time_finder(i[0], times=[]))//1000).strftime('%Y-%m-%d %H:%M:%S'), self.number_of_layers_constant-layer))
                if layer==0:
                    continue
                else:
                    self.__ami_main_df_ls(path=i[0], layer=layer)
            else:
                self.__list_ls.append((i[0], i[1], i[2], datetime.fromtimestamp((self._directory_time_finder(i[0], times=[]))//1000).strftime('%Y-%m-%d %H:%M:%S'), self.number_of_layers_constant-layer))
    def __df_ls_private(self, path, number_of_layers, spark_session_object):
        self.__list_ls=[]
        self.number_of_layers_constant=number_of_layers
        self.__ami_main_df_ls(path=path, layer=number_of_layers)
        return spark_session_object.createDataFrame(self.__list_ls, ["path", "name", "size", "time", "layer"])
    @staticmethod
    def df_ls(path, number_of_layers=30, spark_session_object=spark):
        return prettyDatabricks().__df_ls_private(path=path, number_of_layers=number_of_layers, spark_session_object=spark_session_object)


def pretty_ls(path, theme="light", sizeChecker=True, timeChecker=True):
        prettyDatabricks.pretty_ls(path=path, theme=theme, sizeChecker=sizeChecker, timeChecker=timeChecker)
def df_ls(path, number_of_layers=1, spark_session_object=spark):
        return prettyDatabricks.df_ls(path=path, number_of_layers=number_of_layers, spark_session_object=spark_session_object)
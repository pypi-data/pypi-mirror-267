import logging
import threading
#import sys
#import sys
#class Unbuffered(object):
#   def __init__(self, stream):
#       self.stream = stream
#   def write(self, data):
#       self.stream.write(data)
#       self.stream.flush()
#   def writelines(self, datas):
#       self.stream.writelines(datas)
#       self.stream.flush()
#   def __getattr__(self, attr):
#       return getattr(self.stream, attr)


#sys.stdout = Unbuffered(sys.stdout)
#print 'Hello'
class deploy_logger:
    def __init__(self,level):
        self._error_list = []

    def log_error(self,msg:str, thread:str, traceback_text:str):
        err = {}
        err['message'] = msg
        err['thread'] = thread
        err['traceback'] = traceback_text
        self._error_list.append(err)
    
    def get_error_count(self)->int:
        return len(self._error_list)
    
    def get_error_log(self)->list:
        return self._error_list
    
    def log(self, object_name:str, msg:str):
        if object_name is None or object_name == '':
            log_msg = msg
        else:
            log_msg = object_name + ': ' + msg
        #print(log_msg, flush=True)
        #print(log_msg)
        #sys.stdout.write(log_msg)
        #sys.stdout.flush()
        # acquire the lock
        lock = threading.Lock()
        lock.acquire()
        # report message
        print(log_msg, flush=True)
        # release the lock
        lock.release()

    def highlight(self, msg:str):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(msg)
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', flush=True)

    def show_all_errors(self):
        error_count = self.get_error_count()
        if error_count > 0:
            self.log('','!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            self.log('','!!!               Processing Errors                   !!!')
            self.log('','!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            err_list = self.get_error_log()
            for err in err_list:
                self.log('','####################')
                if err['thread'] is not None and err['thread'] != '':
                    self.log('','### Error Object ###')
                    self.log('',err['thread'])
                self.log('',err['message'])
                self.log('',err['traceback'])
                self.log('','####################')
            self.log('','!!!!!!!!!!!!!!!!!!!!!!!!! end !!!!!!!!!!!!!!!!!!!!!!!!!!!')
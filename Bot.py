import openai
import pickle
import os
from time import time
import re

class Bot:
    _current = None
    _cdir = None
    _hist = None
    _seetings = {
        'model': 'gpt-3.5-turbo',
        'temperature': 0.7,
        'tokens': 50,
        'number': 1
    }

###############################################################################    
    def __init__(self):
        openai.api_key = os.environ['OPENAI_KEY']
        self._cdir = os.path.join(os.environ['MYTOOLS_PATH'], 'helper', 'context')
        self._currentfile = os.path.join(self._cdir, 'current.pickle')
        if not os.path.isdir(self._cdir):
            os.mkdir(self._cdir)
            
###############################################################################
    @property
    def current(self):
        if not self._current:
            if os.path.exists(self._currentfile):
                with open(self._currentfile, 'rb') as f:
                    self.current = pickle.load(f)
        
        if not self._current:
            self.new()
        
        return self._current          

###############################################################################
    @current.setter
    def current(self, fpath):
        with open(self._currentfile, 'wb') as f:
            pickle.dump(fpath, f)
            self._current = fpath
            self._hist = [{"role": "system", "content": "You are a helpful assistant that gives short answers."},]

###############################################################################
    @property
    def hist(self):
        if not self._hist:
            with open(self.current, 'rb') as f:
                self._hist = pickle.load(f)
                
        return self._hist
            
###############################################################################
    def new(self, name=None):
        if name == 'current':
            raise PermissionError
        
        fname = f'{name if name else int(time())}.pickle'
        fpath = os.path.join(self._cdir, fname)
        self.current = fpath
        
        with open(fpath, 'wb') as f:
            f = pickle.dump(self._hist,f)

       
        
        return fpath
###############################################################################
    def open(self, name):
        if name == 'current':
            raise PermissionError
        
        fname = f'{name}.pickle'
        fpath = os.path.join = os.path.join(self._cdir, fname)
        
        if os.path.exists(fpath):
            self.current = fpath
        else:
            self.new(name)
    
###############################################################################
    def save(self):
        with open(self.current, 'wb') as f:
            pickle.dump(self._hist, f)
        
###############################################################################
    def chat(self, msg):
        
        prompt = msg
        max_tokens = 1024
        for m in msg:
            match = re.match('-t(\d+)', m)
            if match:
                max_tokens = int(match.group(1))
                prompt.remove(m)    
        
        prompt = " ".join(prompt)
        
        self.hist.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model=self._seetings['model'],
            messages=self.hist,
            temperature=self._seetings['temperature'],
            max_tokens=max_tokens,
            n=self._seetings['number'],
        )

        answer = response.choices[0]["message"]["content"].strip()
        
        print(answer)
        
        answer = {"role": "assistant", "content": answer}
        self.hist.append(answer)
        
        self.save()
        
###############################################################################
    def list(self):
        l = [f.removesuffix('.pickle') for f in os.listdir(self._cdir) if f.endswith('.pickle')]
        if 'current' in l:
            l.remove('current')
        
        for i in range(len(l)):
            if l[i] == os.path.basename(self.current).removesuffix('.pickle'):
                l[i] = f'{l[i]}  <-- current'
                
        return [i for i in l if i != 'current']
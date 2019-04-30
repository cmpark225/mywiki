# 모듈

모듈은 파이썬 코드의 기본적인 조직화 단위이고, import 문(import 를 참고)이나, importlib.import_module() 과 내장 __import__() 함수를 호출해서 구동할 수 있는 임포트 시스템 에 의해 만들어진다. . 모듈 객체는 딕셔너리 객체로 구현되는 이름 공간을 갖는다(이 딕셔너리 객체는 모듈에서 정의되는 함수들의 __globals__ 어트리뷰트로 참조된다). 어트리뷰트 참조는 이 딕셔너리에 대한 조회로 변환된다. 예를 들어, m.x 는 m.__dict__["x"] 와 같다. 모듈 객체는 모듈을 초기화하는데 사용된 코드 객체를 갖고 있지 않다 (일단 초기화가 끝나면 필요 없으므로).

어트리뷰트 대입은 모듈의 이름 공간 딕셔너리를 갱신한다. 예를 들어, m.x = 1 은 m.__dict__["x"] = 1 과 같다.

```
import test
import inspect

for x in test.__dict__.values():
    if inspect.ismodule(x):
        print x
        print type(x)
        print x.__name__


# 결과
<module 'test' from '........................./test.pyc'>
<type 'module'>
test
```


## dir() 함수
내장 함수 dir() 은 모듈이 정의하는 이름들을 찾는 데 사용됩니다. 문자열들의 정렬된 리스트를 돌려줍니다:

```
>>>
>>> import fibo, sys
>>> dir(fibo)
['__name__', 'fib', 'fib2']
>>> dir(sys)  
['__displayhook__', '__doc__', '__excepthook__', '__loader__', '__name__',
 '__package__', '__stderr__', '__stdin__', '__stdout__',
 '_clear_type_cache', '_current_frames', '_debugmallocstats', '_getframe',
 '_home', '_mercurial', '_xoptions', 'abiflags', 'api_version', 'argv',
 'base_exec_prefix', 'base_prefix', 'builtin_module_names', 'byteorder',
 'call_tracing', 'callstats', 'copyright', 'displayhook',
 'dont_write_bytecode', 'exc_info', 'excepthook', 'exec_prefix',
 'executable', 'exit', 'flags', 'float_info', 'float_repr_style',
 'getcheckinterval', 'getdefaultencoding', 'getdlopenflags',
 'getfilesystemencoding', 'getobjects', 'getprofile', 'getrecursionlimit',
 'getrefcount', 'getsizeof', 'getswitchinterval', 'gettotalrefcount',
 'gettrace', 'hash_info', 'hexversion', 'implementation', 'int_info',
 'intern', 'maxsize', 'maxunicode', 'meta_path', 'modules', 'path',
 'path_hooks', 'path_importer_cache', 'platform', 'prefix', 'ps1',
 'setcheckinterval', 'setdlopenflags', 'setprofile', 'setrecursionlimit',
 'setswitchinterval', 'settrace', 'stderr', 'stdin', 'stdout',
 'thread_info', 'version', 'version_info', 'warnoptions']
```

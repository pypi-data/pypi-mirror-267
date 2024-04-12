import os, sys, json, pytest, io
#currentdir = os.path.dirname(os.path.realpath(__file__))
#parentdir = os.path.dirname(currentdir)
sys.path.append("..")
from src import RubyxClient

with open(os.path.expanduser('~/.rubyx/config-test.json')) as f:
    conf = json.load(f)

def rubyx(cmd):
    return RubyxClient(cmd, conf).run()

def list_equals(a, b):
    diff = set(a) ^ set(b)
    return not diff and len(a) == len(b)

'''
rubyx ( new | use | disable | enable ) <program> [ -t key:value ]...
rubyx programs [ --show-disabled --show-empty-scope ]
'''
def test_program():
    rubyx('new test')
    # program without scope is not going to show up
    assert 'test' not in rubyx('programs')
    assert 'test' in rubyx('programs --show-empty-scope')  
    
    rubyx('disable test')
    assert [] == rubyx('programs')
    assert 'test' not in rubyx('programs --show-empty-scope')
    assert 'test' in rubyx('programs --show-empty-scope --show-disabled')
    
    rubyx('enable test')
    assert 'test' not in rubyx('programs')
    assert 'test' in rubyx('programs --show-empty-scope')
    
    rubyx('new testtag -t test:tag -t test2:tag2')
    assert rubyx('program active') == 'testtag'
    assert json.loads(rubyx('show testtag'))['tags']['test'] == 'tag'
    assert json.loads(rubyx('show testtag'))['tags']['test2'] == 'tag2'

def test_program_special_chars(monkeypatch):
    rubyx('new test/weird&char?')
    # program without scope is not going to show up
    assert 'test/weird&char?' not in rubyx('programs')
    assert 'test/weird&char?' in rubyx('programs --show-empty-scope')
    rubyx('use test/weird&char?')
    rubyx('program update test/weird&char? -t test:tagupdated -t test2:tagupdated2')
    rubyx('inscope add *.weird.com')
    rubyx('domain add sub.weird.com')
    assert 'sub.weird.com' in rubyx('domains')
    # answer 'yes' to 'are you sure you want to remove'
    rubyx('domain remove sub.weird.com')
    rubyx('inscope remove *.weird.com')
    
    
def test_program_use():
    rubyx('use test')
    assert rubyx('program active') == 'test'
    rubyx('use testtag')
    assert rubyx('program active') == 'testtag'
    with pytest.raises(Exception):
        rubyx('use notexist')
    
'''
rubyx programs where <tag_name> is [ before | after ] <value>
'''
def test_programs_where():
    assert 'testtag' in rubyx('programs where test is tag --show-empty-scope')
    assert 'testtag' in rubyx('programs where test2 is tag2 --show-empty-scope')
    assert 'testtag' in rubyx('programs where test is before tagzzz --show-empty-scope')
    assert 'testtag' not in rubyx('programs where test is after tagZZZ --show-empty-scope')
    assert 'testtag' not in rubyx('programs where test is before aaatag --show-empty-scope')
    assert 'testtag' in rubyx('programs where test is after aaatag --show-empty-scope')
    
'''
rubyx program ( active | update ( <program>... | - ) -t key:value... [--append-tags])
'''
def test_program_update_tags():
    rubyx('program update testtag -t test:tagupdated -t test2:tagupdated2')
    assert json.loads(rubyx('show testtag'))['tags']['test'] == 'tagupdated'
    rubyx('program update testtag -t test:tagupdated -t test:testarray')
    assert list_equals(json.loads(rubyx('show testtag'))['tags']['test'], ['tagupdated','testarray'])
    rubyx('program update testtag -t test:tagone')
    rubyx('program update testtag -t test:tagtwo --append-tags')
    assert list_equals(json.loads(rubyx('show testtag'))['tags']['test'], ['tagone','tagtwo'])
    rubyx('program update testtag -t test:tagone -t test:tagtwo')
    rubyx('program update testtag -t test:tagthree --append-tags')
    assert list_equals(json.loads(rubyx('show testtag'))['tags']['test'], ['tagone','tagtwo','tagthree'])

'''
rubyx ( inscope | outscope ) ( add | remove ) ( - | <element>... ) [ -p <program> ]
rubyx scope filter ( in | out ) [ (--wildcard [--top] ) ] [ ( -p <program> ) | ( --all [--show-disabled] ) ]
'''
def test_scope():
    rubyx('use test')
    rubyx('inscope add *.example.com')  
    rubyx('inscope add *.sub.example.com *.dev.example.com')
    assert list_equals(rubyx('scope in'), ['*.example.com', '*.sub.example.com', '*.dev.example.com'])

    
    rubyx('inscope remove *.dev.example.com')
    assert list_equals(rubyx('scope in'), ['*.example.com', '*.sub.example.com'])
    assert list_equals(rubyx('scope in --wildcard'), ['example.com', 'sub.example.com'])
    assert list_equals(rubyx('scope in --wildcard --top'), ['example.com'])
    
    rubyx('inscope add *.example.co.uk -p testtag')  
    rubyx('inscope add *.sub.example.co.uk *.dev.example.co.uk -p testtag')
    assert list_equals(rubyx('scope in -p testtag'), ['*.example.co.uk', '*.sub.example.co.uk', '*.dev.example.co.uk'])
    rubyx('inscope remove *.dev.example.co.uk -p testtag')
    assert list_equals(rubyx('scope in -p testtag'), ['*.example.co.uk', '*.sub.example.co.uk'])
    
    rubyx('outscope add *.dev.example.com')
    assert rubyx('scope out') == ['*.dev.example.com']
    assert rubyx('scope out --wildcard') == ['dev.example.com']
    assert rubyx('scope out --wildcard --top') == ['dev.example.com']
    rubyx('outscope add sub.dev.example.com')
    assert rubyx('scope out --wildcard --top') == ['dev.example.com']
    
    assert list_equals(rubyx('scope in --all'), [
        '*.example.com',
        '*.sub.example.com',
        '*.example.co.uk',
        '*.sub.example.co.uk',
    ])
    
    rubyx('disable testtag')
    assert list_equals(rubyx('scope in --all'), [
        '*.example.com',
        '*.sub.example.com',
    ])
    # TODO: this is inconsistent behaviour, and returns ONLY
    # disabled programs. See https://github.com/honoki/rubyx-client/issues/47
    assert list_equals(rubyx('scope in --all --show-disabled'), [
        '*.example.com',
        '*.sub.example.com',
        '*.example.co.uk',
        '*.sub.example.co.uk',
    ])
    rubyx('enable testtag')

    # test URL scopes
    rubyx('inscope add http://url.example.com/ https://url2.example.com')
    assert 'url.example.com' in rubyx('scope in')
    assert 'url2.example.com' in rubyx('scope in')
    rubyx('outscope add http://URL3.EXaMPLe.cOM/')
    assert 'url3.example.com' in rubyx('scope out')
    
def test_scope_filter(monkeypatch):
    rubyx('use test')
    monkeypatch.setattr('sys.stdin', io.StringIO('one.example.com\ntwo.example.com\nsub.dev.example.com'))
    assert list_equals(rubyx('scope filter in'), ['one.example.com', 'two.example.com'])
    monkeypatch.setattr('sys.stdin', io.StringIO('one.example.com\ntwo.example.com\nsub.dev.example.com'))
    assert list_equals(rubyx('scope filter out'), ['sub.dev.example.com'])
    
    monkeypatch.setattr('sys.stdin', io.StringIO('''
one.example.com
two.example.com
sub.dev.example.com
one.example.co.uk
two.example.co.uk
sub.dev.example.co.uk
'''))
    assert list_equals(rubyx('scope filter in --all'), ['one.example.com', 'two.example.com','one.example.co.uk', 'two.example.co.uk', 'sub.dev.example.co.uk'])
    monkeypatch.setattr('sys.stdin', io.StringIO('''
one.example.com
two.example.com
sub.dev.example.com
one.example.co.uk
two.example.co.uk
sub.dev.example.co.uk
'''))
    assert list_equals(rubyx('scope filter out --all'), ['sub.dev.example.com'])
    
'''
rubyx domain ( add | remove | update ) ( - | <domain>... ) [ -p <program> -s <source> --show-new ( -t key:value... [--append-tags] ) ]
rubyx domains [ --view <view> ( -p <program> | ( --all [--show-disabled] ) ) ]
'''
def test_domains(monkeypatch):
    assert rubyx('domains') == []
    
    # test adding and tagging
    rubyx('domain add one.example.com two.example.com three.example.com')
    assert list_equals(rubyx('domains'), ['one.example.com','two.example.com','three.example.com'])
    rubyx('domain add four.example.com:4.4.4.4')
    assert list_equals(rubyx('domains'), ['one.example.com','two.example.com','three.example.com', 'four.example.com'])
    rubyx('domain update one.example.com -t tagging:test_domains')
    assert json.loads(rubyx('show one.example.com'))['tags']['tagging'] == 'test_domains'
    rubyx('domain update one.example.com -t tagging:test_domains -t tagging:array')
    assert list_equals(json.loads(rubyx('show one.example.com'))['tags']['tagging'], ['test_domains', 'array'])
    rubyx('domain update one.example.com -t tagging:append --append-tags')
    assert list_equals(json.loads(rubyx('show one.example.com'))['tags']['tagging'], ['test_domains', 'array', 'append'])
    rubyx('domain update one.example.com -t tagging:overwrite')
    assert json.loads(rubyx('show one.example.com'))['tags']['tagging'] == 'overwrite'
    
    # test domains through input pipe
    monkeypatch.setattr('sys.stdin', io.StringIO('''
pipe1.example.com
pipe2.example.com
pipe3.dev.example.com
'''))
    rubyx('domain add -')
    assert list_equals(rubyx('domains'), ['one.example.com','two.example.com','three.example.com', 'four.example.com', 'pipe1.example.com', 'pipe2.example.com'])
    monkeypatch.setattr('sys.stdin', io.StringIO('''
pipe1.example.com
pipe2.example.com
pipe3.dev.example.com
'''))
    rubyx('domain remove -')
    assert list_equals(rubyx('domains'), ['one.example.com','two.example.com','three.example.com', 'four.example.com'])

    # test adding out-of-scope domains
    rubyx('domain add not-in-scope.example.be')
    assert 'not-in-scope.example.be' not in rubyx('domains')
    rubyx('domain add not-in-scope.example.be --ignore-scope')
    assert 'not-in-scope.example.be' in rubyx('domains')
    rubyx('domain remove not-in-scope.example.be')
    
    # test ips
    assert list_equals(json.loads(rubyx('show four.example.com'))['ips'], ['4.4.4.4'])
    rubyx('domain update four.example.com:4.4.4.4,4.4.4.5,4.4.4.6')
    assert list_equals(json.loads(rubyx('show four.example.com'))['ips'], ['4.4.4.4', '4.4.4.5','4.4.4.6'])
    rubyx('domain update four.example.com:4.4.4.4,4.4.4.5,4.4.4.6 four.example.com:4.4.4.4,4.4.4.7 -s pytest')
    assert list_equals(json.loads(rubyx('show four.example.com'))['ips'], ['4.4.4.4', '4.4.4.5','4.4.4.6','4.4.4.7'])
    
    # test source
    assert json.loads(rubyx('show four.example.com'))['source'] == 'pytest'
    
    # test --show-new for new and updated domains
    assert rubyx('domain add five.example.com --show-new -s pytest') == ['[NEW] five.example.com']
    assert json.loads(rubyx('show five.example.com'))['source'] == 'pytest'
    assert rubyx('domain update five.example.com -n') == None
    assert rubyx('domain update five.example.com:5.5.5.5 -n') == ['[UPDATED] five.example.com']
    assert rubyx('domain update five.example.com:5.5.5.5 -n') == None
    assert rubyx('domain update five.example.com:5.5.5.5 -n -s updated') == ['[UPDATED] five.example.com']
    
    # test remove
    rubyx('domain remove four.example.com five.example.com')
    assert list_equals(rubyx('domains'), ['one.example.com','two.example.com','three.example.com'])
    
    

'''
rubyx domains where <tag_name> is [ before | after ] <value> [ -p <program> | ( --all [--show-disabled] ) ]
'''
def test_domains_where():
    assert list_equals(rubyx('domains'), ['one.example.com','two.example.com','three.example.com'])
    rubyx('domain add four.example.com:4.4.4.4')
    
    assert list_equals(rubyx('domains where ip is 4.4.4.4'), ['four.example.com'])
    assert 'four.example.com' in rubyx('domains where ip is before 4.4.4.4ZZZ')
    assert 'four.example.com' not in rubyx('domains where ip is before 1.1.1.1')
    assert 'four.example.com' in rubyx('domains where ip is after 4.4.4.0')
    assert 'four.example.com' not in rubyx('domains where ip is after 4.4.4.9')
    
    
    assert list_equals(rubyx('domains where tagging is overwrite'), ['one.example.com'])
    assert 'one.example.com' in rubyx('domains where tagging is before overwriteZZZ')
    assert 'one.example.com' not in rubyx('domains where tagging is before overwritA')
    assert 'one.example.com' in rubyx('domains where tagging is after overwrita')
    assert 'one.example.com' not in rubyx('domains where tagging is after overwritZ')

def test_domains_underscore():
    rubyx('domain add _one.example.com _two.example.com')
    assert '_one.example.com' in rubyx('domains')
    assert '_two.example.com' in rubyx('domains')
    assert rubyx('domain add _three.example.com:3.0.3.0 -n') == ['[NEW] _three.example.com']
    assert rubyx('domains where ip is 3.0.3.0') == ['_three.example.com']
    assert rubyx('domain update _three.example.com:4.0.4.0 -n') == ['[UPDATED] _three.example.com']
    assert rubyx('domain remove _three.example.com -n') == ['[DELETED] _three.example.com']
    rubyx('domain remove _one.example.com _two.example.com')
    assert '_one.example.com' not in rubyx('domains')
    assert '_two.example.com' not in rubyx('domains')

def test_domains_resolved():
    rubyx('domain add one.example.com:1.1.1.1 two.example.com:2.2.2.2 three.example.com:127.0.0.1 four.example.com:10.0.0.1 five.example.com:192.168.0.1 six.example.com:172.16.0.0 seven.example.com:172.10.1.1')
    rubyx('domain update one.example.com:1.1.1.1 four.example.com:10.0.0.1')
    assert 'one.example.com' in rubyx('domains --resolved')
    assert 'one.example.com' in rubyx('domains --resolved --no-private')
    assert 'three.example.com' not in rubyx('domains --resolved --no-private')
    assert 'four.example.com' not in rubyx('domains --resolved --no-private')
    assert 'five.example.com' not in rubyx('domains --resolved --no-private')
    assert 'six.example.com' not in rubyx('domains --resolved --no-private')
    assert 'seven.example.com' in rubyx('domains --resolved --no-private')
    rubyx('domain add eight.example.com')
    assert 'eight.example.com' in rubyx('domains --unresolved')
    rubyx('domain remove two.example.com three.example.com four.example.com five.example.com six.example.com seven.example.com eight.example.com')

'''
rubyx ips [ --filter-cdns ( -p <program> | ( --all [--show-disabled] ) ) ]
'''
def test_ips(monkeypatch):
    assert rubyx('ips') == []
    # test adding and tagging
    rubyx('ip add 1.1.1.1 2.2.2.2 3.3.3.3')
    assert list_equals(rubyx('ips'), ['1.1.1.1','2.2.2.2','3.3.3.3'])
    rubyx('ip add 4.4.4.4:four.example.com')
    assert list_equals(rubyx('ips'), ['1.1.1.1','2.2.2.2','3.3.3.3', '4.4.4.4'])
    rubyx('ip update 1.1.1.1 -t tagging:test_domains')
    assert json.loads(rubyx('show 1.1.1.1'))['tags']['tagging'] == 'test_domains'
    rubyx('ip update 1.1.1.1 -t tagging:test_domains -t tagging:array')
    assert list_equals(json.loads(rubyx('show 1.1.1.1'))['tags']['tagging'], ['test_domains', 'array'])
    rubyx('ip update 1.1.1.1 -t tagging:append --append-tags')
    assert list_equals(json.loads(rubyx('show 1.1.1.1'))['tags']['tagging'], ['test_domains', 'array', 'append'])
    rubyx('ip update 1.1.1.1 -t tagging:overwrite')
    assert json.loads(rubyx('show 1.1.1.1'))['tags']['tagging'] == 'overwrite'
    
    # test ips through input pipe
    monkeypatch.setattr('sys.stdin', io.StringIO('''
11.11.11.11
22.22.22.22
33.33.33.33
'''))
    rubyx('ip add -')
    assert list_equals(rubyx('ips'), ['1.1.1.1','2.2.2.2','3.3.3.3', '4.4.4.4', '11.11.11.11', '22.22.22.22', '33.33.33.33'])
    monkeypatch.setattr('sys.stdin', io.StringIO('''
11.11.11.11
22.22.22.22
33.33.33.33
'''))
    rubyx('ip remove -')
    assert list_equals(rubyx('ips'), ['1.1.1.1','2.2.2.2','3.3.3.3','4.4.4.4'])
    
    # test domains
    assert list_equals(json.loads(rubyx('show 4.4.4.4'))['domains'], ['four.example.com'])
    rubyx('ip update 4.4.4.4:four.example.com,four2.example.com,four3.example.com')
    assert list_equals(json.loads(rubyx('show 4.4.4.4'))['domains'], ['four.example.com', 'four2.example.com','four3.example.com'])
    rubyx('ip update 4.4.4.4:four4.example.com,four5.example.com 4.4.4.4:four6.example.com,four7.example.com -s pytest')
    assert list_equals(json.loads(rubyx('show 4.4.4.4'))['domains'], ['four.example.com', 'four2.example.com','four3.example.com','four4.example.com', 'four5.example.com','four6.example.com','four7.example.com'])
    
    # test source
    assert json.loads(rubyx('show 4.4.4.4'))['source'] == 'pytest'
    
    # test --show-new for new and updated domains
    assert rubyx('ip add 5.5.5.5 --show-new -s pytest') == ['[NEW] 5.5.5.5']
    assert json.loads(rubyx('show 5.5.5.5'))['source'] == 'pytest'
    assert rubyx('ip update 5.5.5.5 -n') == None
    assert rubyx('ip update 5.5.5.5:five.example.com -n') == ['[UPDATED] 5.5.5.5']
    assert rubyx('ip update 5.5.5.5:five.example.com -n') == None
    assert rubyx('ip update 5.5.5.5:five.example.com -n -s updated') == ['[UPDATED] 5.5.5.5']
    
    # test remove
    rubyx('ip remove 4.4.4.4 5.5.5.5')
    assert list_equals(rubyx('ips'), ['1.1.1.1','2.2.2.2','3.3.3.3'])

def test_cidr_scope(monkeypatch):
    rubyx('inscope add 3.2.1.0/23')
    assert '3.2.1.0/23' in rubyx('scope in')
    rubyx('outscope add 3.2.1.254')
    assert '3.2.1.254' in rubyx('scope out')
    # at the moment this only impacts URLs
    rubyx('url add http://1.2.3.4:80 http://3.2.1.1:80')
    assert 'http://3.2.1.1:80' in rubyx('urls')
    assert 'http://1.2.3.4:80' not in rubyx('urls')
    rubyx('url remove http://3.2.1.1:80')
    # ensure the URL is added if --ignore-scope is used
    rubyx('url add http://1.2.3.4:80 http://3.2.1.1:80 --ignore-scope')
    assert 'http://3.2.1.1:80' in rubyx('urls')
    assert 'http://1.2.3.4:80' in rubyx('urls')
    rubyx('url remove http://3.2.1.1:80 http://1.2.3.4:80')
    

'''
rubyx ips where <tag_name> is [ before | after ] <value> [ -p <program> | ( --all [--show-disabled] ) ]
'''
def test_ips_where():
    assert list_equals(rubyx('ips'), ['1.1.1.1','2.2.2.2','3.3.3.3'])
    rubyx('ip add 4.4.4.4:four.example.com')
    
    assert list_equals(rubyx('ips where domain is four.example.com'), ['4.4.4.4'])
    assert '4.4.4.4' in rubyx('ips where domain is before four.example.coZ')
    assert '4.4.4.4' not in rubyx('ips where domain is before AAAA.example.com')
    assert '4.4.4.4' in rubyx('ips where domain is after four.example.aaa')
    assert '4.4.4.4' not in rubyx('ips where domain is after four.example.ZZZ')
    
    
    assert list_equals(rubyx('ips where tagging is overwrite'), ['1.1.1.1'])
    assert '1.1.1.1' in rubyx('ips where tagging is before overwriteZZZ')
    assert '1.1.1.1' not in rubyx('ips where tagging is before overwritA')
    assert '1.1.1.1' in rubyx('ips where tagging is after overwrita')
    assert '1.1.1.1' not in rubyx('ips where tagging is after overwritZ')

'''
rubyx urls [ -d <hostname> | ( -p <program> | ( --all [--show-disabled] ) ) ] [--with-query]
'''
def test_urls():
    assert list_equals(rubyx('urls'), [])
    
    # plain http
    rubyx('url add http://one.example.com/one')
    rubyx('url add http://two.example.com/two http://three.example.com/three')
    assert list_equals(rubyx('urls'), [
        'http://one.example.com/one',
        'http://two.example.com/two',
        'http://three.example.com/three'
    ])
    
    # https
    rubyx('url add http://three.example.com/1 http://three.example.com/2 http://three.example.com/3 -t protocol:http')
    rubyx('url add https://three.example.com/1 https://three.example.com/2 https://three.example.com/3 -t protocol:https')
    # with query strings
    rubyx('url add http://three.example.com/query?one=two&three=four')
    rubyx('url add http://three.example.com/query?five=six')
    rubyx('url add https://three.example.com:8080/url?some=what')
    # relative path with specified domain
    rubyx('url add /relative -d three.example.com')
    
    # when port :80 or :443 are explicitly set in the URL, they need to be removed
    # so we don't duplicate value where port is not set!
    rubyx('url add http://three.example.com:80/1 https://port.example.com:443/port https://port.example.com/port')
    
    assert list_equals(rubyx('urls'), [
        'http://one.example.com/one',
        'http://two.example.com/two',
        'http://three.example.com/three',
        'http://three.example.com/1',
        'http://three.example.com/2',
        'http://three.example.com/3',
        #https
        'https://three.example.com/1',
        'https://three.example.com/2',
        'https://three.example.com/3',
        #querystrings
        'http://three.example.com/query',
        'https://three.example.com:8080/url',
        #relative
        'http://three.example.com/relative',
        
        # explicit ports:
        # https://port.example.com:443/port should not be listed
        # http://three.example.com:80/1 should not be listed
        'https://port.example.com/port'
    ])
    
    # including query strings
    assert list_equals(rubyx('urls -q'), [
        'http://one.example.com/one',
        'http://two.example.com/two',
        'http://three.example.com/three',
        'http://three.example.com/1',
        'http://three.example.com/2',
        'http://three.example.com/3',
        #https
        'https://three.example.com/1',
        'https://three.example.com/2',
        'https://three.example.com/3',
        #querystrings
        'http://three.example.com/query?one=two&three=four',
        'http://three.example.com/query?five=six',
        'https://three.example.com:8080/url?some=what',
        #relative
        'http://three.example.com/relative',
        # explicit ports:
        'https://port.example.com/port'
    ])
    
    # including status codes and content lengths
    rubyx('url add http://three.example.com/c 200 1234')
    assert 'http://three.example.com/c' in rubyx('urls')
    
'''
rubyx urls where <tag_name> is [ before | after ] <value> [ -p <program> | ( --all [--show-disabled] ) ]
'''
def test_urls_where():
    assert 'http://one.example.com/one' in rubyx('urls where hostname is one.example.com')
    assert 'https://three.example.com:8080/url' in rubyx('urls where port is 8080')
    
    assert 'http://three.example.com/1' in rubyx('urls where protocol is http')
    assert 'http://three.example.com/1' in rubyx('urls where protocol is after httA')
    assert 'http://three.example.com/1' not in rubyx('urls where protocol is after httpZZZ')
    assert 'http://three.example.com/1' in rubyx('urls where protocol is before httZ')
    assert 'http://three.example.com/1' not in rubyx('urls where protocol is before httA')

'''
rubyx url remove ( - | <url>... )
'''
def test_urls_remove(monkeypatch):
    rubyx('url remove https://three.example.com:8080/url')
    assert 'https://three.example.com:8080/url' not in rubyx('urls')
    monkeypatch.setattr('sys.stdin', io.StringIO('''
http://one.example.com/one
http://two.example.com/two
http://three.example.com/three
http://three.example.com/1
http://three.example.com/2
http://three.example.com/3
http://three.example.com/c
'''))
    rubyx('url remove -')
    assert list_equals(rubyx('urls'), [
        #https
        'https://three.example.com/1',
        'https://three.example.com/2',
        'https://three.example.com/3',
        #querystrings
        'http://three.example.com/query',
        #relative
        'http://three.example.com/relative',
        # explicit ports:
        'https://port.example.com/port'
    ])

'''
rubyx services [ -p <program> | ( --all [--show-disabled] ) ]
rubyx service add ( - | <service>... ) [ -s <source> -p <program> --show-new ( -t key:value... [ --append-tags ] ) ]
'''
def test_services():
    assert rubyx('services') == []
    rubyx('service add 1.1.1.1:11 2.2.2.2:22:ssh 3.3.3.3:33')
    assert rubyx('service add 3.3.3.3:33 -n') == None
    assert rubyx('service add 3.3.3.3:33:some -n') == ['[UPDATED] 3.3.3.3:33']
    assert rubyx('service add 3.3.3.3:33:some -n') == None
    assert rubyx('service add 3.3.3.3:33:some -n -s updated') == ['[UPDATED] 3.3.3.3:33']
    
    assert list_equals(rubyx('services'), [
        '1.1.1.1:11',
        '2.2.2.2:22',
        '3.3.3.3:33'
    ])
    
    rubyx('service add 1.1.1.1:11 -t tagging:test_services')
    assert json.loads(rubyx('show 1.1.1.1:11'))['tags']['tagging'] == 'test_services'
    rubyx('service add 1.1.1.1:11 -t tagging:test_services -t tagging:array')
    assert list_equals(json.loads(rubyx('show 1.1.1.1:11'))['tags']['tagging'], ['test_services', 'array'])
    rubyx('service add 1.1.1.1:11 -t tagging:append --append-tags')
    assert list_equals(json.loads(rubyx('show 1.1.1.1:11'))['tags']['tagging'], ['test_services', 'array', 'append'])
    rubyx('service add 1.1.1.1:11 -t tagging:overwrite')
    assert json.loads(rubyx('show 1.1.1.1:11'))['tags']['tagging'] == 'overwrite'

'''
rubyx services where <tag_name> is [ before | after ] <value> [ -p <program> | ( --all [--show-disabled] ) ]
'''
def test_services_where():
    assert '1.1.1.1:11' in rubyx('services where ip is 1.1.1.1')
    assert '1.1.1.1:11' in rubyx('services where port is 11')
    assert '2.2.2.2:22' in rubyx('services where service is ssh')
    assert '3.3.3.3:33' in rubyx('services where service is some')
    
    assert '1.1.1.1:11' in rubyx('services where tagging is overwrite')
    assert '1.1.1.1:11' in rubyx('services where tagging is after overwritA')
    assert '1.1.1.1:11' not in rubyx('services where tagging is after overwriteZZZ')
    assert '1.1.1.1:11' in rubyx('services where tagging is before overwritZ')
    assert '1.1.1.1:11' not in rubyx('services where tagging is before overwritA')

'''
rubyx service remove ( - | <service>... )
'''
def test_service_remove(monkeypatch):
    rubyx('service remove 1.1.1.1:11')
    assert '1.1.1.1:11' not in rubyx('services')
    monkeypatch.setattr('sys.stdin', io.StringIO('''
1.1.1.1:11
1.1.1.1:11
2.2.2.2:22
3.3.3.3:33
'''))
    rubyx('service remove -')
    assert list_equals(rubyx('services'), [])

'''
rubyx blacklist ( add | remove ) ( - | <element>... ) [ -p <program> ]
'''
def test_blacklist():
    rubyx('use test')
    rubyx('blacklist add blacklist.example.com')
    rubyx('domain add blacklist.example.com')
    assert 'blacklist.example.com' not in rubyx('domains')
    
    rubyx('blacklist remove blacklist.example.com')
    rubyx('domain add blacklist.example.com')
    assert 'blacklist.example.com' in rubyx('domains')
    
    rubyx('blacklist add 9.9.9.9')
    rubyx('domain add blacklistip.example.com:9.9.9.9')
    assert 'blacklistip.example.com' not in rubyx('domains')

'''
rubyx agent ( list | ( register | remove ) <agent>... | gateway [ <url> ] )
'''
def test_agent():
    assert rubyx('agent list') == []
    rubyx('agent register testagent')
    assert rubyx('agent list') == ['testagent']
    rubyx('agent register testagent2')
    rubyx('agent remove testagent')
    assert rubyx('agent list') == ['testagent2']
    rubyx('agent gateway http://localhost/gateway-test')
    assert rubyx('agent gateway') == 'http://localhost/gateway-test'
    
'''
rubyx agents
'''
def test_agents():
    assert rubyx('agents') == ['testagent2']

'''
rubyx run <agent> [ -p <program> ]
'''
pass

'''
rubyx listen
'''
pass

'''
rubyx alert ( - | <message> ) [ -s <source> ]
'''
pass

'''
rubyx tags [<name>] [ -p <program> | --all ]
'''
def test_tags():
    assert list_equals(rubyx('tags'), [
        'tagging',
        'protocol'
    ])
    
    assert list_equals(rubyx('tags --all'), [
        'test', # tag on program test
        'test2', # tag on proram test
        'tagging',
        'protocol'
    ])
    
    assert list_equals(rubyx('tags protocol'), [
        'https://three.example.com/1 https',
        'https://three.example.com/2 https',
        'https://three.example.com/3 https',
    ])
    assert list_equals(rubyx('tags tagging'), [
        '1.1.1.1 overwrite',
        'one.example.com overwrite',
    ])

'''
rubyx server upgrade
'''
def test_upgrade():
    # not yet sure how to test this here
    pass
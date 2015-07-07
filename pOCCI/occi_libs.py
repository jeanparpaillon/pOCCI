import ConfigParser
import json
import os
import sys

occi_config = {}

def occi_format(results):
    count_f = 0
    count_o = 0
    for r in results:
        if 'status' in r:
            if r['status']:
                count_o += 1
            else:
                count_f += 1

            r['status'] = result2str(r['status'])
        
        if 'running_time' in r:
            r['running_time'] = round(r['running_time'], 3)

    out = {}
    out['tests'] = results
    out['passed'] = count_o
    out['failed'] = count_f
    return out

def occi_print(results, outputformat):
    if outputformat == 'plain':
        for r in results['tests']:
            print '%s  %s' % (r['name'], r['status'])
            if 'reason' in r:
                print >> sys.stderr, r['reason']
    elif outputformat == 'json':
        print json.dumps(results, indent=4, sort_keys=True)
    else:
        print 'Only "plain", "json" output types are possible'


def occi_test(name, status, err_msg, running_time = None):
    test = {}
    test['name'] = name
    test['status'] = status
    if running_time is not None:
        test['running_time'] = running_time
    if err_msg:
        test['reason'] = err_msg

    return test


def result2str(result):
    return 'OK' if result else 'FAIL'


def occi_init():
    global occi_config

    config = ConfigParser.ConfigParser()
    config.read(['/etc/pOCCI.cfg', os.path.expanduser('~/.pOCCI.cfg')])
    if not config.has_section('main'):
        return False
    for key, value in config.items('main'):
        #print 'config: %s = %s (%s)' % (key, value, type(eval(value)))
        occi_config[key] = eval(value)
    return True
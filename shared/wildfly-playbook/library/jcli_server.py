#!/usr/bin/python

from ansible.module_utils.basic import *
import subprocess
import json
import time

def isServerGroupAlreadyCreated(data):
    cmd = data['jboss_home'] + '/bin/jboss-cli.sh'
    cli = "/server-group=%s:query" % (data['server_group_name'])
    controller = "--controller=%s:%s" % (data['controller_host'],data['controller_port'])
    user = "-u=%s" % (data['user'])
    password = "-p=%s" % (data['password'])
    p = subprocess.Popen(["sh", cmd, "-c", cli, controller, user, password], stdout=subprocess.PIPE)
    result , err = p.communicate()

    print(err)

    if "WFLYCTL0216" in result:
        return False
    else:
        return True

def isServerAlreadyCreated(data):
    cmd = data['jboss_home'] + '/bin/jboss-cli.sh'
    cli = "/host=%s/server=%s:query" % (data['host'], data['server_config_name'])
    controller = "--controller=%s:%s" % (data['controller_host'],data['controller_port'])
    user = "-u=%s" % (data['user'])
    password = "-p=%s" % (data['password'])
    p = subprocess.Popen(["sh", cmd, "-c", cli, controller, user, password], stdout=subprocess.PIPE)
    output = p.communicate()[0]

    if "WFLYCTL0216" in output:
        return False
    else:
        return True

def server_present(data):
    cmd = data['jboss_home'] + '/bin/jboss-cli.sh'
    controller = "--controller=%s:%s" % (data['controller_host'],data['controller_port'])
    user = "-u=%s" % (data['user'])
    password = "-p=%s" % (data['password'])
    exists = isServerAlreadyCreated(data)
    isError = False
    hasChanged = True
    meta = {}
    res = []

    if not exists:
        cli = "/host=%s/server-config=%s:add(group=%s,socket-binding-port-offset=%s,socket-binding-group=%s)" % (data['host'],data['server_config_name'],data['server_group_name'],data['server_socket_binding_port_offset'],data['server_group_socket'])
        p = subprocess.Popen(["sh", cmd, "-c", cli, controller, user, password], stdout=subprocess.PIPE)
        result,err = p.communicate()
        res.append(result)

        cli = "/host=%s/server-config=%s:start" % (data['host'],data['server_config_name'])
        p = subprocess.Popen(["sh", cmd, "-c", cli, controller, user, password], stdout=subprocess.PIPE)
        result,err = p.communicate()
        res.append(result)

        meta = {"status": "OK", "response": res}
    else:
        hasChanged = False
        resp = "Server %s already created" % (data['server_config_name'])
        meta = {"status" : "OK", "response" : resp}

    return isError, hasChanged, meta

def server_absent(data):
    cmd = data['jboss_home'] + '/bin/jboss-cli.sh'
    controller = "--controller=%s:%s" % (data['controller_host'],data['controller_port'])
    user = "-u=%s" % (data['user'])
    password = "-p=%s" % (data['password'])

    exists = isServerAlreadyCreated(data)
    isError = False
    hasChanged = True
    meta = {}
    res = []

    if not exists:
        hasChanged = False
        resp = "Server %s does not exist" % (data['server_config_name'])
        meta = {"status" : "OK", "response" : resp}
    else:
        cli = "/host=%s/server-config=%s:stop" % (data['host'],data['server_config_name'])
        p = subprocess.Popen(["sh", cmd, "-c", cli, controller, user, password], stdout=subprocess.PIPE)
        result,err = p.communicate()
        res.append(result)

        while not "STOPPED" in result:
            time.sleep(0.5)
            cli = "/host=%s/server-config=%s:stop" % (data['host'],data['server_config_name'])
            p = subprocess.Popen(["sh", cmd, "-c", cli, controller, user, password], stdout=subprocess.PIPE)
            result = p.communicate()[0]

        cli = "/host=%s/server-config=%s:remove" % (data['host'],data['server_config_name'])
        p = subprocess.Popen(["sh", cmd, "-c", cli, controller, user, password], stdout=subprocess.PIPE)
        result,err = p.communicate()
        res.append(result)
        meta = {"status": "OK", "response": res}

    return isError, hasChanged, meta

def server_start(data):
    cmd = data['jboss_home'] + '/bin/jboss-cli.sh'
    controller = "--controller=%s:%s" % (data['controller_host'],data['controller_port'])
    user = "-u=%s" % (data['user'])
    password = "-p=%s" % (data['password'])
    exists = isServerAlreadyCreated(data)
    isError = False
    hasChanged = True
    meta = {}

    if exists:
        cli = "/host=%s/server-config=%s:start" % (data['host'],data['server_config_name'])
        p = subprocess.Popen(["sh", cmd, "-c", cli, controller, user, password], stdout=subprocess.PIPE)
        result,err = p.communicate()
        meta = {"status": "OK", "response": result}
    else:
        hasChanged = False
        resp = "Server %s does not exist" % (data['server_config_name'])
        meta = {"status" : "OK", "response" : resp}

    return isError, hasChanged, meta

def server_stop(data):
    cmd = data['jboss_home'] + '/bin/jboss-cli.sh'
    controller = "--controller=%s:%s" % (data['controller_host'],data['controller_port'])
    user = "-u=%s" % (data['user'])
    password = "-p=%s" % (data['password'])
    exists = isServerAlreadyCreated(data)
    isError = False
    hasChanged = True
    meta = {}

    if exists:
        cli = "/host=%s/server-config=%s:stop" % (data['host'],data['server_config_name'])
        p = subprocess.Popen(["sh", cmd, "-c", cli, controller, user, password], stdout=subprocess.PIPE)
        result,err = p.communicate()
        meta = {"status": "OK", "response": result}
    else:
        hasChanged = False
        resp = "Server %s does not exist" % (data['server_config_name'])
        meta = {"status" : "OK", "response" : resp}

    return isError, hasChanged, meta

def main():

    fields = {
        "jboss_home" : {"required": True, "type": "str"},
        "host": {
            "required": False,
            "default": "master",
            "type": "str"
        },
        "server_group_name": {
            "required": True,
            "type": "str"
        },
        "server_config_name": {
            "required": True,
            "type": "str"
        },
        "server_socket_binding_port_offset": {
            "required": False,
            "default": 0,
            "type": "int"
        },
        "server_group_socket": {
            "required": False,
            "default": "standard-sockets",
            "type": "str"
        },
        "controller_host": {
            "required": False,
            "default": "localhost",
            "type": "str"
        },
        "controller_port": {
            "required": False,
            "default": 9990,
            "type": "int"
        },
        "user" : {
            "required": True,
            "type": "str"
        },
        "password" : {
            "required": True,
            "type": "str"
        },
        "state": {
            "default": "present",
            "choices": ['present', 'absent', 'start', 'stop'],
            "type": 'str'
        },
    }

    choice_map = {
        "present": server_present,
        "absent": server_absent,
        "start": server_start,
        "stop": server_stop,
    }

    module = AnsibleModule(argument_spec=fields)
    is_error, has_changed, result = choice_map.get(
        module.params['state'])(module.params)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error creating server", meta=result)

if __name__ == '__main__':
    main()

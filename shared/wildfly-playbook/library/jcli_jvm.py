#!/usr/bin/python

from ansible.module_utils.basic import *
import subprocess
import json

def isJvmAlreadyCreated(data):
    cmd = data['jboss_home'] + '/bin/jboss-cli.sh'
    cli = "/host=%s/server-config=%s/jvm=%s:query" % (data['host'], data['server_config_name'], data['jvn_name'])
    controller = "--controller=%s:%s" % (data['controller_host'],data['controller_port'])
    user = "-u=%s" % (data['user'])
    password = "-p=%s" % (data['password'])
    p = subprocess.Popen(["sh", cmd, "-c", cli, controller, user, password], stdout=subprocess.PIPE)
    result = p.communicate()[0]

    created = False
    remoteExists = False

    if "WFLYCTL0216" in result:
        created = False
    else:
        created = True

    if "WFLYPRT0053" in result:
        remoteExists = False
    else:
        remoteExists = True

    return remoteExists, created

def jvm_present(data):
    cmd = data['jboss_home'] + '/bin/jboss-cli.sh'
    controller = "--controller=%s:%s" % (data['controller_host'],data['controller_port'])
    user = "-u=%s" % (data['user'])
    password = "-p=%s" % (data['password'])
    exists, created  = isJvmAlreadyCreated(data)
    isError = False
    hasChanged = True
    meta = {}
    res =[]

    if not exists:
        mesg = "Could not connect http-remoting://%s:%s" % (data['controller_host'],data['controller_port'])
        meta = {"status": "Error", "response": mesg}
        isError = True
        hasChanged = False
    else:
        if not created:
            cli = "/host=%s/server-config=%s/jvm=%s:add" % (data['host'],data['server_config_name'],data['jvn_name'])
            p = subprocess.Popen(["sh", cmd, "-c", cli, controller, user, password], stdout=subprocess.PIPE)
            result,err = p.communicate()
            res.append(result)

            cli = "/host=%s/server-config=%s/jvm=%s:write-attribute(name=heap-size,value=%s)" % (data['host'],data['server_config_name'],data['jvn_name'],data['heap_size'])
            p = subprocess.Popen(["sh", cmd, "-c", cli, controller, user, password], stdout=subprocess.PIPE)
            result,err = p.communicate()
            res.append(result)

            cli = "/host=%s/server-config=%s/jvm=%s:write-attribute(name=max-heap-size,value=%s)" % (data['host'],data['server_config_name'],data['jvn_name'],data['max_heap_size'])
            p = subprocess.Popen(["sh", cmd, "-c", cli, controller, user, password], stdout=subprocess.PIPE)
            result,err = p.communicate()
            res.append(result)

            cli = "/host=%s/server-config=%s/jvm=%s:write-attribute(name=permgen-size,value=%s)" % (data['host'],data['server_config_name'],data['jvn_name'],data['permgen_size'])
            p = subprocess.Popen(["sh", cmd, "-c", cli, controller, user, password], stdout=subprocess.PIPE)
            result,err = p.communicate()
            res.append(result)

            cli = "/host=%s/server-config=%s/jvm=%s:write-attribute(name=max-permgen-size,value=%s)" % (data['host'],data['server_config_name'],data['jvn_name'],data['max_permgen_size'])
            p = subprocess.Popen(["sh", cmd, "-c", cli, controller, user, password], stdout=subprocess.PIPE)
            result,err = p.communicate()
            res.append(result)

            if data['jvm_options'] is not None:
                cli = "/host=%s/server-config=%s/jvm=%s:add-jvm-option(jvm-option=%s)" % (data['host'],data['server_config_name'],data['jvn_name'],data['jvm_options'])
                p = subprocess.Popen(["sh", cmd, "-c", cli, controller, user, password], stdout=subprocess.PIPE)
                result,err = p.communicate()
                res.append(result)

            cli = "reload --host=%s" % (data['host'])
            p = subprocess.Popen(["sh", cmd, "-c", cli, controller, user, password], stdout=subprocess.PIPE)
            result,err = p.communicate()
            res.append(result)

            meta = {"status": "OK", "response": res}
        else:
            hasChanged = False
            resp = "JVM %s already created" % (data['jvn_name'])
            meta = {"status" : "OK", "response" : resp}

    return isError, hasChanged, meta

def jvm_absent(data):
    cmd = data['jboss_home'] + '/bin/jboss-cli.sh'
    controller = "--controller=%s:%s" % (data['controller_host'],data['controller_port'])
    user = "-u=%s" % (data['user'])
    password = "-p=%s" % (data['password'])
    exists, created  = isJvmAlreadyCreated(data)
    isError = False
    hasChanged = True
    meta = {}

    if not exists:
        mesg = "Could not connect http-remoting://%s:%s" % (data['controller_host'],data['controller_port'])
        meta = {"status": "Error", "response": mesg}
        isError = True
        hasChanged = False
    else:
        if not created:
            hasChanged = False
            resp = "JVM %s does not exist" % (data['jvn_name'])
            meta = {"status" : "OK", "response" : resp}
        else:
            cli = "/host=%s/server-config=%s/jvm=%s:remove" % (data['host'],data['server_config_name'],data['jvn_name'])
            p = subprocess.Popen(["sh", cmd, "-c", cli, controller, user, password], stdout=subprocess.PIPE)
            result,err = p.communicate()
            meta = {"status": "OK", "response": result}

    return isError, hasChanged, meta

def main():

    fields = {
        "jboss_home" : {"required": True, "type": "str"},
        "host": {
            "required": False,
            "default": "master",
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
        "server_config_name": {
            "required": True,
            "type": "str"
        },
        "jvn_name": {
            "required": True,
            "type": "str"
        },
        "heap_size": {
            "required": True,
            "type": "str"
        },
        "max_heap_size": {
            "required": True,
            "type": "str"
        },
        "permgen_size": {
            "required": True,
            "type": "str"
        },
        "max_permgen_size": {
            "required": True,
            "type": "str"
        },
        "jvm_options": {
            "required": False,
            "type": "str"
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
            "choices": ['present', 'absent'],
            "type": 'str'
        },
    }

    choice_map = {
        "present": jvm_present,
        "absent": jvm_absent,
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

#!/usr/bin/python

from ansible.module_utils.basic import *
import subprocess
import json

def isArtifactAlreadyDeployed(data):
    cmd = data['jboss_home'] + '/bin/jboss-cli.sh'
    cli = "deployment-info --name=%s" % (data['artifact'])
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

def deployment_present(data):
    cmd = data['jboss_home'] + '/bin/jboss-cli.sh'
    controller = "--controller=%s:%s" % (data['controller_host'],data['controller_port'])
    user = "-u=%s" % (data['user'])
    password = "-p=%s" % (data['password'])
    mode = data['server_mode']
    exists, created = isArtifactAlreadyDeployed(data)
    isError = False
    hasChanged = True
    meta = {}
    result = ""

    if not exists:
        mesg = "Could not connect http-remoting://%s:%s" % (data['controller_host'],data['controller_port'])
        meta = {"status": "Error", "response": mesg}
        isError = True
        hasChanged = False
    else:
        if not created:
            if mode == 'standalone':
                cli = "deploy %s/%s" % (data['artifact_dir'],data['artifact'])
            else:
                cli = "deploy %s/%s --server-groups=%s" % (data['artifact_dir'],data['artifact'],data['server_group_name'])
            p = subprocess.Popen(["sh", cmd, "-c", cli, controller, user, password], stdout=subprocess.PIPE)
            result,err = p.communicate()
        else:
            cli = "deploy %s/%s --force" % (data['artifact_dir'],data['artifact']) #same behaviour between standalone and domain
            p = subprocess.Popen(["sh", cmd, "-c", cli, controller, user, password], stdout=subprocess.PIPE)
            result,err = p.communicate()

        if "WFLYDC0074" in result:
            meta = {"status" : "Failed to deploy", "response" : result}
            isError = True
        else:
            meta = {"status" : "OK", "response" : result}

    return isError, hasChanged, meta

def deployment_absent(data):
    cmd = data['jboss_home'] + '/bin/jboss-cli.sh'
    controller = "--controller=%s:%s" % (data['controller_host'],data['controller_port'])
    user = "-u=%s" % (data['user'])
    password = "-p=%s" % (data['password'])

    mode = data['server_mode']
    exists, created = isArtifactAlreadyDeployed(data)
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
            resp = "Deployment %s does not exist" % (data['artifact'])
            meta = {"status" : "OK", "response" : resp}
        else:
            if mode == 'standalone':
                cli = "undeploy %s" % (data['artifact'])
            else:
                cli = "undeploy %s --server-groups=%s" % (data['artifact'],data['server_group_name'])

            p = subprocess.Popen(["sh", cmd, "-c", cli, controller, user, password], stdout=subprocess.PIPE)
            result,err = p.communicate()

            if "WFLYDC0074" in result:
                meta = {"status" : "Failed to undeploy", "response" : result}
                isError = True
            else:
                meta = {"status": "OK", "response": result}

    return isError, hasChanged, meta

def main():

    fields = {
        "jboss_home" : {"required": True, "type": "str"},
        "server_group_name": {
            "required": True,
            "type": "str"
        },
        "artifact": {
            "required": True,
            "type": "str"
        },
        "artifact_dir": {
            "required": True,
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
        "server_mode" : {
            "required": True,
            "choices": ['standalone', 'domain'],
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
        "present": deployment_present,
        "absent": deployment_absent,
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

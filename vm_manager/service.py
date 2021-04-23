import virtualbox
from virtualbox.library import MachineState

vbox = virtualbox.VirtualBox()


class VmManager:
    @staticmethod
    def status(data, allowed_vms):
        vm_name = data.get('vmName', '')
        if vm_name:
            return {
                'command': 'status',
                'vmName': vm_name,
                'staus': VmManager._get_status(vm_name),
            }
        else:
            return {
                'command': 'status',
                'details': [
                    {
                        'vmName': allowed_vm,
                        'status': VmManager._get_status(allowed_vm)
                    }
                    for allowed_vm in allowed_vms
                ]
            }

    @staticmethod
    def _get_status(vm_name):
        machin = vbox.find_machine(vm_name)
        state = machin.state
        if state == MachineState.powered_off:
            status = 'off'
        elif state == MachineState.starting:
            status = 'powering on'
        elif state == MachineState.running:
            status = 'on'
        elif state == MachineState.stopping:
            status = 'powering off'
        else:
            status = 'unkown'
        return status

    @staticmethod
    def on(data, allowed_vms):
        vm_name = data.get('vmName', '')
        if vm_name and vm_name in allowed_vms:
            machine = vbox.find_machine(vm_name)
            session = virtualbox.Session()
            progress = machine.launch_vm_process(session, "gui", [])
            # progress.wait_for_completion()
        return {
            'command': 'on',
            'vmName': vm_name,
            'status': 'pwering on'
        }

    @staticmethod
    def off(data, allowed_vms):
        vm_name = data.get('vmName', '')
        if vm_name and vm_name in allowed_vms:
            machine = vbox.find_machine(vm_name)
            session = machine.create_session()
            session.console.power_down()

        return {
            'command': 'off',
            'vmName': vm_name,
            'status': 'pwering off'
        }

    @staticmethod
    def setting(data, allowed_vms):
        return {'command': 'setting'}

    @staticmethod
    def clone(data, allowed_vms):
        return {'command': 'clone'}

    @staticmethod
    def delete(data, allowed_vms):
        return {'command': 'delete'}

    @staticmethod
    def execute(data, allowed_vms):
        return {'command': 'execute'}

    @staticmethod
    def transfer(data, allowed_vms):
        return {'command': 'transfer'}


REGISTERED_COMMANDS = {
    'status': VmManager.status,
    'on': VmManager.on,
    'off': VmManager.off,
    'setting': VmManager.setting,
    'clone': VmManager.clone,
    'delete': VmManager.delete,
    'execute': VmManager.execute,
    'transfer': VmManager.transfer,
}


def run(command, data, allowed_vms):
    return REGISTERED_COMMANDS[command](data, allowed_vms)

import virtualbox
from virtualbox.library import MachineState, LockType, CloneMode, IGuestSession

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
        else:
            return {
                'detail': 'not allowed'
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
        else:
            return {
                'detail': 'not allowed'
            }

    @staticmethod
    def setting(data, allowed_vms):
        vm_name = data.get('vmName', '')
        if vm_name and vm_name in allowed_vms:
            cpu = int(data.get('cpu'))
            ram = int(data.get('ram'))
            machine = vbox.find_machine(vm_name)
            session = machine.create_session(LockType.write)
            session.machine.cpu_count = cpu
            session.machine.memory_size = ram
            session.machine.save_settings()
            session.unlock_machine()

            return {
                'command': 'setting',
                'vmName': vm_name,
                'cpu': cpu,
                'ram': ram,
                'status': 'ok'
            }

        else:
            return {
                'detail': 'not allowed'
            }

    @staticmethod
    def clone(data, allowed_vms):
        src_vm_name = data.get('sourceVmName', '')
        dst_vm_name = data.get('destVmName', '')
        if src_vm_name in allowed_vms:
            dst_machine = vbox.create_machine('', dst_vm_name, [], '', '')
            src_machine = vbox.find_machine(src_vm_name)
            src_machine.clone_to(dst_machine, CloneMode.machine_state, [])
            return {
                'command': 'clone',
                'sourceVmName': src_vm_name,
                'destVmName': dst_vm_name,
                'status': 'ok'
            }
        else:
            return {
                'detail': 'not allowed'
            }

    @staticmethod
    def delete(data, allowed_vms):
        vm_name = data.get('vmName', '')
        if vm_name and vm_name in allowed_vms:
            machine = vbox.find_machine(vm_name)
            machine.remove(delete=True)
            return {
                'command': 'delete',
                'vmName': vm_name,
            }
        else:
            return {
                'detail': 'not allowed'
            }

    @staticmethod
    def execute(data, allowed_vms):
        vm_name = data.get('vmName', '')
        if vm_name and vm_name in allowed_vms:
            machine = vbox.find_machine(vm_name)
            session = machine.create_session()
            gs = session.console.guest.create_session(vm_name.lower(), vm_name.lower())
            input = data.get('input', '')
            process, stdout, stderr = gs.execute(input, [])
        return {'command': 'execute'}

    @staticmethod
    def transfer(data, allowed_vms):
        session = IGuestSession()
        session.fs_obj_move('VM1/home/vm1/x.txt', 'VM2/home/vm2/', [])
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

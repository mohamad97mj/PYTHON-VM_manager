import virtualbox


class VmManager:
    @staticmethod
    def status(data):
        return {'command': 'status'}

    @staticmethod
    def on_off(data):
        return {'command': 'on/off'}

    @staticmethod
    def setting(data):
        return {'command': 'setting'}

    @staticmethod
    def clone(data):
        return {'command': 'clone'}

    @staticmethod
    def delete(data):
        return {'command': 'delete'}

    @staticmethod
    def execute(data):
        return {'command': 'execute'}

    @staticmethod
    def transfer(data):
        return {'command': 'transfer'}


REGISTERED_COMMANDS = {
    'status': VmManager.status,
    'on/off': VmManager.on_off,
    'setting': VmManager.setting,
    'clone': VmManager.clone,
    'delete': VmManager.delete,
    'execute': VmManager.execute,
    'transfer': VmManager.transfer,
}


def run(command, data):
    return REGISTERED_COMMANDS[command](data)

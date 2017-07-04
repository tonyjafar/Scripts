import atexit
import argparse
from pyVmomi import vim
from pyvim.connect import SmartConnect, Disconnect
import ssl

default_context = ssl._create_default_https_context
ssl._create_default_https_context = ssl._create_unverified_context


def getargs():
    parser = argparse.ArgumentParser(description='Monitoring ESXs Datastores')

    parser.add_argument('-u', '--username', required=True, action='store',
                        help='Vcenter username.')
    parser.add_argument('-p', '--password', required=True, action='store',
                        help='Vcenter password.')
    parser.add_argument('-H', '--host', required=True, action='store',
                        help='Vcenter IP.')
    parser.add_argument('-w', '--warning', required=True, action='store',
                        help='Warning Value.', type=int)
    parser.add_argument('-c', '--critical', required=True, action='store',
                        help='Critical Value.', type=int)
    args = parser.parse_args()

    return args


def get_obj(content):
    datastores = []
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.Datastore], True)
    for c in container.view:
        obj = c
        datastores.append(obj)
    return datastores


def print_datastore_info(ds_obj):
    summary = ds_obj.summary
    ds_capacity = summary.capacity
    ds_freespace = summary.freeSpace
    ds_uncommitted = summary.uncommitted if summary.uncommitted else 0
    ds_provisioned = ds_capacity - ds_freespace + ds_uncommitted
    ds_overp = ds_provisioned - ds_capacity
    ds_overp_pct = (ds_overp * 100) / ds_capacity \
        if ds_capacity else 0
    datastore_name = summary.name
    capacity = float(ds_capacity)
    freespace = float(ds_freespace)
    percentage = int((freespace * 100) / capacity)

    return datastore_name, percentage


def main():
    args = getargs()
    criticals = {}
    warnings = {}
    normals = {}
    perf = []
    si = SmartConnect(
        host=args.host,
        user=args.username,
        pwd=args.password,
        port=443)
    atexit.register(Disconnect, si)
    content = si.RetrieveContent()
    ds_obj_list = get_obj(content)
    for datastore in ds_obj_list:
        name, perc = print_datastore_info(datastore)
        if args.warning > perc > args.critical:
            warnings[name] = str(perc)
        elif perc <= args.critical:
            criticals[name] = str(perc)
        else:
            normals[name] = str(perc)
    if len(criticals) > 0:
        print('Critical: Some Datastores have low space')
        for name in criticals:
            print('Critical: ' + name + ' has ' + criticals[name] + '%')
            perf.append(name + '_' + 'Free_space=%s' % criticals[name])
        if len(warnings) > 0:
            for name in warnings:
                print('Warning: ' + name + ' has ' + warnings[name] + '%')
                perf.append(name + '_' + 'Free_space=%s' % warnings[name])
        for name in normals:
            print('Normal: ' + name + ' has ' + normals[name] + '%')
            perf.append(name + '_' + 'Free_space=%s' % normals[name])
        print('|' + ' '.join(perf))
        exit(2)
    elif len(warnings) > 0:
        print('Warning: Some Datastores have warning space')
        for name in warnings:
            print('Warning: ' + name + ' has ' + warnings[name] + '%')
            perf.append(name + '_' + 'Free_space=%s' % warnings[name])
        for name in normals:
            print('Normal: ' + name + ' has ' + normals[name] + '%')
            perf.append(name + '_' + 'Free_space=%s' % normals[name])
        print('|' + ' '.join(perf))
        exit(1)
    else:
        print('Normal: All Datastores have Normal space')
        for name in normals:
            print('Normal: ' + name + ' has ' + normals[name] + '%')
            perf.append(name + '_' + 'Free_space=%s' % normals[name])
        print('|' + ' '.join(perf))
        exit(0)
# start
if __name__ == "__main__":
    main()
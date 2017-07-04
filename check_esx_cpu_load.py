import atexit
from pyVim.connect import SmartConnect, Disconnect
import argparse


def getargs():
    parser = argparse.ArgumentParser(description='Monitoring ESXs CPU load')

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


def metricvalue(item, depth):
    maxdepth = 10
    if hasattr(item, 'childEntity'):
        if depth > maxdepth:
            return 0
        else:
            item = item.childEntity
            item = metricvalue(item,depth+1)
    return item


def main():
    import ssl
    default_context = ssl._create_default_https_context
    ssl._create_default_https_context = ssl._create_unverified_context
    port = 443
    try:
        si = SmartConnect(
                host=app_args.host,
                user=app_args.username,
                pwd=app_args.password,
                port=port)
    except:
        print("Failed to connect")
    atexit.register(Disconnect, si)
    content = si.RetrieveContent()
    warnings = {}
    criticals = {}
    normals = {}
    perf = []
    for child in content.rootFolder.childEntity:
        datacenter = child
        hostfolder = datacenter.hostFolder
        hostlist = metricvalue(hostfolder, 0)
        for hosts in hostlist:
            esxhosts = hosts.host
            for esx in esxhosts:
                summary = esx.summary
                cpuMhz = summary.hardware.cpuMhz
                cores = summary.hardware.numCpuCores
                totalMhz = cpuMhz * cores
                name = summary.config.name
                cpuloadpercentage = int((summary.quickStats.overallCpuUsage * 100) / totalMhz)
                if app_args.warning < cpuloadpercentage < app_args.critical:
                    warnings[name] = str(cpuloadpercentage)
                elif cpuloadpercentage > app_args.critical:
                    criticals[name] = str(cpuloadpercentage)
                else:
                    normals[name] = str(cpuloadpercentage)
    if len(criticals) > 0:
        print 'Critical: Some ESX have high cpu load'
        for name in criticals:
            print 'Critical: ' + name + ' has ' + criticals[name] + '%'
            perf.append(name.split('.')[0] + '_' + 'cpu_load=%s' % criticals[name])
        if len(warnings) > 0:
            for name in warnings:
                print 'Warning: ' + name + ' has ' + warnings[name] + '%'
                perf.append(name.split('.')[0] + '_' + 'cpu_load=%s' % warnings[name])
        for name in normals:
            print 'Normal: ' + name + ' has ' + normals[name] + '%'
            perf.append(name.split('.')[0] + '_' + 'cpu_load=%s' % normals[name])
        print '|' + ' '.join(perf)
        exit(2)
    elif len(warnings) > 0:
        print 'Warning: Some ESX have warning cpu load'
        for name in warnings:
            print 'Warning: ' + name + ' has ' + warnings[name] + '%'
            perf.append(name.split('.')[0] + '_' + 'cpu_load=%s' % warnings[name])
        for name in normals:
            print 'Normal: ' + name + ' has ' + normals[name] + '%'
            perf.append(name.split('.')[0] + '_' + 'cpu_load=%s' % normals[name])
        print '|' + ' '.join(perf)
        exit(1)
    else:
        print 'Normal: All ESX have normal cpu load'
        for name in normals:
            print 'Normal: ' + name + ' has ' + normals[name] + '%'
            perf.append(name.split('.')[0] + '_' + 'cpu_load=%s' % normals[name])
        print '|' + ' '.join(perf)
# start
if __name__ == "__main__":
    app_args = getargs()
    main()

from boto import ec2
import argparse


def my_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--region', help='AWS Region', required=True)
    parser.add_argument('-i', '--instance', help='Instance.id', required=True)
    parser.add_argument('-k', '--key', help='aws access id', required=True)
    parser.add_argument('-s', '--secret', help='aws secret key', required=True)
    parser.add_argument('-n', '--image_name', help='Image Name', required=True)
    args = parser.parse_args()

    return args

app_args = my_args()
region_connect = ec2.connect_to_region(app_args.region,
                                       aws_access_key_id=app_args.key,
                                       aws_secret_access_key=app_args.secret)
instance = ec2.EC2Connection.get_all_instances(region_connect, instance_ids=app_args.instance)

stats = region_connect.get_all_instance_status(instance_ids=app_args.instance)

snapshots = ec2.EC2Connection.get_all_snapshots(region_connect, owner='self')


for stat in stats:
    server_status = str(stat.system_status.status + '/' + stat.instance_status.status)

if server_status == 'ok/ok':
    images = region_connect.get_all_images(owners='self')
    for image in images:
        if image.name == app_args.image_name:
            try:
                image_id = image.id
                name = image.name
            except:
                exit()
            image.deregister()

    try:
        for snapshot in snapshots:
            if str(name) == str(snapshot.description):
                response = snapshot.delete(
                    DryRun=False,
                )
    except:
        pass

    NEW_image = instance[0].create_image(
        DryRun=False,
        Name=app_args.image_name,
        Description=app_args.image_name,
        NoReboot=True,
    )


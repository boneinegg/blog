import openstack.config
import sys, os, errno
from openstack import utils

openstack .enable_logging()
utils.enable_logging(debug=True, path='openstack.log', stream=sys.stdout)
"""
cloud_regions = openstack.config.OpenStackConfig().get_all()
for cloud_region in cloud_regions:
    print(cloud_region.name, cloud_region.region, cloud_region.config)
"""

def create_connection_from_config():
    return openstack.connect(cloud='openstack')

def list_servers(conn):
    print('List servers:')
    for server in conn.compute.servers():
        print(server)

def list_flavors(conn):
    print('List flavors:')
    for flavor in conn.compute.flavors():
        print(flavor)

def list_images(conn):
    print('List Images:')

    for image in conn.compute.images():
        print(image)

def list_networks(conn):
    print('List Networks:')
    for network in conn.network.networks():
        print(network)

def create_keypair(conn):
    keypair = conn.compute.find_keypair('openstack')
    if not keypair:
        print('Create Key Pair:')
        keypair = conn.compute.create_keypair(name='openstack')
        print(keypair)

        try:
            os.mkdir('./mykeypair')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e

        with open('./mykeypair/openstack', 'w') as f:
            f.write('%s' % keypair.private_key)

        os.chmod('./mykeypair', 0o400)
    return keypair

def create_server(conn):
    print('Create Server:')

    image = conn.compute.find_image('cirros-0.3.5-x86_64-disk')
    flavor = conn.compute.find_flavor('cirros256')
    network = conn.network.find_network('private')
    keypair = create_keypair(conn)

    server = conn.compute.create_server(
        name='cirros', image_id=image.id, flavor_id=flavor.id,
        network=[{'uuid': network.id}], key_name=keypair.name
    )

    server = conn.compute.wait_for_server(server)

    print("ssh -l {key} root@{ip}".format(
        key='./mykeypair/openstack',
        ip=server.access_ipv4,
    ))


conn = create_connection_from_config()
list_servers(conn)
list_flavors(conn)
list_images(conn)
list_networks(conn)
create_keypair(conn)


if __name__ == '__main__':
    create_server(conn)






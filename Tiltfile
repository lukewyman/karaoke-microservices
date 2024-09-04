version_settings(constraint='>=0.22.2')

docker_build('song-library', './microservices/song_library/src')


load('ext://helm_resource', 'helm_resource', 'helm_repo')
helm_repo('bitnami', 'https://charts.bitnami.com/bitnami')
helm_resource('mongo', 'bitnami/mongodb',
                resource_deps=['bitnami'],
                flags=[
                    '--version=14.4.9',
                    '--set=architecture=standalone',
                    '--set=useStatefulSet=true',
                    '--set=auth.rootUser=admin',
                    '--set=auth.rootPassword=p@ssw0RD123'
                ])

k8s_yaml('./deploy/k8s/song-library.yaml')

k8s_resource(
    'song-library',
    port_forwards='5001:5000',
    labels=['song-library']
)
k8s_resource(
    'mongo',
    labels=['song-library']
)



tiltfile_path = config.main_path
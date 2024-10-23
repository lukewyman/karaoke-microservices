version_settings(constraint='>=0.22.2')

load('ext://helm_resource', 'helm_resource', 'helm_repo')
helm_repo('bitnami', 'https://charts.bitnami.com/bitnami')


############ SONG LIBRARY (port 32101) ############
# Microservice
docker_build('song-library', './microservices/song_library/src')
k8s_yaml('./deploy/k8s/song-library.yaml')
k8s_resource(
    'song-library',
    port_forwards='8081:8080',
    labels=['song-library']
)
k8s_resource(
    'mongo',
    labels=['song-library']
)

# Database
helm_resource('mongo', 'bitnami/mongodb',
                resource_deps=['bitnami'],
                labels='song-library',
                flags=[
                    '--version=14.4.9',
                    '--set=architecture=standalone',
                    '--set=useStatefulSet=true',
                    '--set=auth.rootUser=admin',
                    '--set=auth.rootPassword=p@ssw0RD123'
                ])

#Tests
k8s_yaml('./deploy/k8s/song-library-tests.yaml')
k8s_resource(
    'song-library-tests',
    labels=['song-library'],
    trigger_mode=TRIGGER_MODE_MANUAL
)


############ SINGERS ##############################
# Database
helm_resource('postgres', 'bitnami/postgresql',
                resource_deps=['bitnami'],
                labels='singers',
                flags=[
                    '--version=13.2.5',
                    '--set=architecture=standalone',
                    '--set=auth.postgresPassword=postgres'
                ])

# Migrations
docker_build('singers-migrations', './migrations/singers/src')
k8s_yaml('./deploy/k8s/singers-migrations.yaml')
k8s_resource(
    'singers-migrations',
    labels=['singers']
)


############ ROTATIONS (port 32103) ###############
# Microservice
docker_build('rotations', './microservices/rotations/src')
k8s_yaml('./deploy/k8s/rotations.yaml')
k8s_resource(
    'rotations',
    labels=['rotations']
)

# Tests
k8s_yaml('./deploy/k8s/rotations-tests.yaml')
k8s_resource(
    'rotations-tests',
    labels=['rotations'],
    trigger_mode=TRIGGER_MODE_MANUAL
)


############ SONG CHOICES (port 32104) ############
# Microservice 
docker_build('song-choices', './microservices/song_choices/src')
k8s_yaml('./deploy/k8s/song-choices.yaml')
k8s_resource(
    'song-choices',
    labels=['song-choices']
)

# Tests
k8s_yaml('./deploy/k8s/song-choices-tests.yaml')
k8s_resource(
    'song-choices-tests',
    labels=['song-choices'],
    trigger_mode=TRIGGER_MODE_MANUAL
)


tiltfile_path = config.main_path
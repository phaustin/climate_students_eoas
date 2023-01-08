from oauthenticator.github import GitHubOAuthenticator
from pathlib import Path
import os
from oauthenticator.github import GitHubOAuthenticator

c.JupyterHub.authenticator_class = GitHubOAuthenticator
# launch with docker
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

# we need the hub to listen on all ips when it is in a container
c.JupyterHub.hub_ip = '0.0.0.0'
# the hostname/ip that should be used to connect to the hub
# this is usually the hub services's name
c.JupyterHub.hub_connect_ip = 'climatehub'

# pick a docker image. This should have the same version of jupyterhub
# in it as our Hub.
c.DockerSpawner.image ='phaustin/climate_image:solo'
notebook_dir = "/home/jovyan"
c.DockerSpawner.notebook_dir = notebook_dir

# tell the user containers to connect to our docker network
c.DockerSpawner.network_name = 'traefik_net'
c.DockerSpawner.volumes = {"jupyterhub-user-{username}": notebook_dir,
                            "/home/jovyan/repos/climate_modeling_eoas/shared_files": 
                            {"bind": '/home/jovyan/shared_files', "mode": "rw"},
                            "/home/jovyan/repos/climate_students_eoas/content/courseware":
                            {"bind": '/home/jovyan/course_notebooks', "mode": "ro"}
                           }


# delete containers when the stop
c.DockerSpawner.remove = True

c.GitHubOAuthenticator.oauth_callback_url = os.environ['JHUB_OAUTH_CALLBACK_URL']
c.GitHubOAuthenticator.client_id = os.environ['JHUB_OAUTH_CLIENT_ID']
c.GitHubOAuthenticator.client_secret = os.environ['JHUB_OAUTH_CLIENT_SECRET']
c.Authenticator.allowed_users = allowed = set()
c.Authenticator.admin_users = admin = set()

curr_dir = Path()
user_list = curr_dir / 'user_list.txt'

with open(user_list,'r') as f:
   all_lines=f.readlines()
   for the_line in all_lines:
      the_line=the_line.strip()
      if len(the_line) < 1:
         continue
      parts=the_line.split(';')
      username=parts[0].strip()
      allowed.add(username)
      if len(parts) > 1:
         part2 = parts[1].strip()
         if part2 == 'admin':
            admin.add(username)
            
with open(curr_dir / 'dump.txt','w') as out:
   out.write("hello\n\n")
   out.write(f"{all_lines}\n\n")
   out.write(f"admin: {admin}\n\n")
   out.write(f"allowed: {allowed}\n\n")


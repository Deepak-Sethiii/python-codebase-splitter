from git import Repo
repo_url = "https://github.com/Deepak-Sethiii/MedBot_25"
local_folder = "requests"
Repo.clone_from(repo_url, local_folder)
print("done")

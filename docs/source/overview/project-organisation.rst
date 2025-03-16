======================================
|:card_file_box:| Project Organisation
======================================

|:file_folder:| Some key project directories (all found at ``/app`` within the project's Docker container):

- ``build``: Files used to build the project Docker image go here
- ``src``: ``header-hook`` source code lives here
- ``tests``: Contains Python-based test cases to validate ``header-hook``
- ``data``: Contains lightweight files for use in ``header-hook`` testing

|:scroll:| Some key project files (root of GitHub, or ``/app/`` within the project's Docker image):

- ``.github/workflows``: Contains GitHub Actions used for code testing and publishing.
- ``build/Dockerfile``: Configures the Docker build process
- ``.dockerignore``: A list of project files/directories Docker should not incorporate into the build process
- ``.gitignore``: A list of files/directories that Git should not track
- ``.devcontainer/devcontainer.json``: Contains the configuration for the development container for VSCode, including the Docker image to use, any additional VSCode extensions to install, and whether or not to mount the project directory into the container.
- ``./pyproject.toml``: This file stores high-level project configuration options.

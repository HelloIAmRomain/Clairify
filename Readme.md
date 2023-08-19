# Docker instructions

Building docker image :
`docker build -t deeplearningcuda:latest .`

Run the Docker container with a volume:
`docker run --gpus all -it --name deeplearning_container -v ./docker_folder:$HOME deeplearningcuda:latest /bin/bash`


Setup Your Development Environment in the Container:

Since you're using VSCode, it would be beneficial to use the Remote - Containers extension to connect directly to this container and develop from within VSCode.
Inside VSCode, open the command palette (Ctrl+Shift+P or Cmd+Shift+P) and choose "Remote-Containers: Attach to Running Container...". From the list, select deeplearning_container.
Start Developing:

With your setup, any Python script you run inside this container will have access to the GPU and the installed libraries like TensorFlow and PyTorch.
All the development and execution should happen within the container to leverage the specific CUDA version and libraries you've set up.
Managing the Container:

When you're done for the day, you can exit the bash shell using the exit command. This will stop the container.
To start the container again, use:

`docker start deeplearning_container`

And to get back into an interactive shell:
`docker exec -it deeplearning_container /bin/bash`


Cleanup:

If you ever need to delete the container (to maybe create a new one), you can do so with:

docker rm deeplearning_container
And to remove the image:

docker rmi deeplearningcuda:latest